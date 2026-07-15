#version2
from __future__ import annotations
import math
import pandas as pd
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple

# =====================================================================
# VOCABULARY NORMALIZATION TABLES
# =====================================================================

PAIN_GEN_ALIASES: dict[str, str] = {
    "stenosis: canal": "stenosis: canal",
    "stenosis: central canal": "stenosis: canal",
    "central canal stenosis": "stenosis: canal",
    "central stenosis": "stenosis: canal",
    "spinal stenosis": "stenosis: canal",
    "lumbar spinal stenosis": "stenosis: canal",
    "lumbar stenosis": "stenosis: canal",
    "stenosis: subarticular": "stenosis: subarticular",
    "stenosis: subarticular zone": "stenosis: subarticular",
    "subarticular stenosis": "stenosis: subarticular",
    "lateral recess stenosis": "stenosis: subarticular",
    "stenosis: foraminal": "stenosis: foraminal",
    "stenosis: foramen": "stenosis: foraminal",
    "foraminal stenosis": "stenosis: foraminal",
    "foraminal narrowing": "stenosis: foraminal",
    "disc hrn/annular tear+no stenosis": "disc hrn/annular tear",
    "disc hrn/annular tear": "disc hrn/annular tear",
    "disk herniation, annular tear no stenosis": "disc hrn/annular tear",
    "disc herniation, annular tear no stenosis": "disc hrn/annular tear",
    "disc herniation": "disc hrn/annular tear",
    "disk herniation": "disc hrn/annular tear",
    "herniated disc": "disc hrn/annular tear",
    "herniated disk": "disc hrn/annular tear",
    "disc herniation or stenosis": "disc hrn/annular tear",
    "annular tear": "disc hrn/annular tear",
    "ddd w/ bone marrow edema": "ddd w/ bone marrow edema",
    "degenerative disc disease with bone marrow edema": "ddd w/ bone marrow edema",
    "ddd with bone marrow edema": "ddd w/ bone marrow edema",
    "facet arthropathy": "facet arthropathy",
    "facet arthropathy & instability": "facet arthropathy",
    "facet joint arthropathy": "facet arthropathy",
    "facet joint degeneration": "facet arthropathy",
    "facet joint disease": "facet arthropathy",
    "facet joint pain": "facet arthropathy",
    "facet joint": "facet arthropathy",
    "z-joint": "facet arthropathy",
    "zygapophyseal joint": "facet arthropathy",
    "z-joint disease": "facet arthropathy",
    "degenerative facet arthropathy": "facet arthropathy",
    "degenerative facet disease": "facet arthropathy",
    "spondylolysis": "spondylolysis",
    "pars defect": "spondylolysis",
    "pars interarticularis defect": "spondylolysis",
}

PAIN_GEN_FAMILIES: dict[str, str] = {
    "stenosis: canal": "stenosis",
    "stenosis: subarticular": "stenosis",
    "stenosis: foraminal": "stenosis",
    "disc hrn/annular tear": "disc",
    "ddd w/ bone marrow edema": "disc",
    "facet arthropathy": "bone_joint",
    "spondylolysis": "bone_joint",
}

SIDE_ALIASES: dict[str, str] = {
    "right": "right",
    "left": "left",
    "bilateral": "midline/bilateral",
    "midline": "midline/bilateral",
    "midline/bilateral": "midline/bilateral",
    "midline or left": "midline/bilateral",
    "midline or right": "midline/bilateral",
    "both": "midline/bilateral",
    "b/l": "midline/bilateral",
    "rigth": "right", 
}

LEVEL_ORDER = ["l1-2", "l2-3", "l3-4", "l4-5", "l5-s1"]
LEVEL_ALIASES: dict[str, str] = {
    "l1-2": "l1-2", "l1-l2": "l1-2", "l1/l2": "l1-2",
    "l2-3": "l2-3", "l2-l3": "l2-3", "l2/l3": "l2-3",
    "l3-4": "l3-4", "l3-l4": "l3-4", "l3/l4": "l3-4",
    "l4-5": "l4-5", "l4-l5": "l4-5", "l4/l5": "l4-5",
    "l5-s1": "l5-s1", "l5-s2": "l5-s1", "l5/s1": "l5-s1",
    "l5 (if pars defect)": "l5-s1",
    "ns": "ns",
    "not specified": "ns",
}

LEVEL_MULTI: dict[str, str] = {
    "l4-5 or l5-s1": "l4-5",
    "l4-l5 or l5-s1": "l4-5",
    "l3-4 or l4-5": "l3-4",
    "l3-l4 or l4-l5": "l3-4",
    "l2-3 or l3-4": "l2-3",
}

NERVE_ORDER = ["l1", "l2", "l3", "l4", "l5", "s1", "s2"]
NERVE_ALIASES: dict[str, str] = {
    "l1": "l1", "l2": "l2", "l3": "l3",
    "l4": "l4", "l5": "l5",
    "s1": "s1", "s2": "s2",
    "ns": "ns", "n/a": "ns", "none": "ns",
    "not applicable": "ns", "not specified": "ns",
    "unknown": "ns", "no": "ns", "na": "ns",
}

NERVE_MULTI: dict[str, str] = {
    "l5 and s1": "l5",
    "l4 or l5": "l4",
    "l5 or s1": "l5",
    "l3 or l4": "l3",
    "l4 or l5 or s1": "l4",
    "l5 or s1 or s2": "l5",
}

DISC_BONE_ALIASES: dict[str, str] = {
    "disc": "disc",
    "bone": "bone",
    "disc or bone": "disc or bone",
    "disc/bone": "disc or bone",
    "disc disease": "disc",
    "disc herniation": "disc",
    "degenerative disc disease": "disc",
    "bone disease": "bone",
    "facet arthropathy": "bone",
    "facet joint disease": "bone",
    "z-joint disease": "bone",
    "degenerative joint disease": "bone",
    "ns": "ns",
    "not specified": "ns",
}

# =====================================================================
# NORMALIZATION HELPERS
# =====================================================================

def _clean(val) -> Optional[str]:
    """Return lowercase-stripped string, or None for missing/NaN."""
    if val is None:
        return None
    if isinstance(val, float):
        if math.isnan(val):
            return None
    s = str(val).strip().lower()
    return s if s else None

def normalize_pg(val) -> Optional[str]:
    s = _clean(val)
    return PAIN_GEN_ALIASES.get(s) if s else None

def normalize_side(val) -> Optional[str]:
    s = _clean(val)
    return SIDE_ALIASES.get(s) if s else None

def normalize_level(val) -> Optional[str]:
    s = _clean(val)
    if s is None:
        return None
    if s in LEVEL_MULTI:
        return LEVEL_MULTI[s]
    return LEVEL_ALIASES.get(s)

def normalize_nerve(val) -> str:
    s = _clean(val)
    if s is None:
        return "ns"
    if s in NERVE_MULTI:
        return NERVE_MULTI[s]
    return NERVE_ALIASES.get(s, "ns")

def normalize_db(val) -> Optional[str]:
    s = _clean(val)
    if s is None:
        return None
    if s in DISC_BONE_ALIASES:
        return DISC_BONE_ALIASES[s]
    if "bone" in s and "disc" not in s:
        return "bone"
    if "disc" in s and "bone" not in s:
        return "disc"
    return None

# =====================================================================
# GROUND TRUTH STRUCTURE
# =====================================================================

@dataclass
class GroundTruth:
    yc_pg: Optional[str] = None
    fran_pg: Optional[str] = None
    yc_level: Optional[str] = None
    fran_level: Optional[str] = None
    yc_side: Optional[str] = None
    fran_side: Optional[str] = None
    yc_nerve: str = "ns"
    fran_nerve: str = "ns"
    yc_db: Optional[str] = None
    fran_db: Optional[str] = None
    yc_pg2: Optional[str] = None
    fran_pg2: Optional[str] = None
    yc_level2: Optional[str] = None
    fran_level2: Optional[str] = None
    yc_nerve2: str = "ns"
    fran_nerve2: str = "ns"
    pooled_pg: Optional[str] = None
    pooled_level: Optional[str] = None
    pooled_side: Optional[str] = None
    pooled_nerve: str = "ns"
    pooled_db: Optional[str] = None
    consensus: dict = field(default_factory=dict)

    def __post_init__(self):
        self.consensus = {
            "pg": self.yc_pg == self.fran_pg and self.yc_pg is not None,
            "level": self.yc_level == self.fran_level and self.yc_level is not None,
            "side": self.yc_side == self.fran_side and self.yc_side is not None,
            "nerve": self.yc_nerve == self.fran_nerve,
            "db": self.yc_db == self.fran_db and self.yc_db is not None,
        }

    def pg_labels(self) -> list[str]:
        return [v for v in [self.yc_pg, self.fran_pg, self.yc_pg2, self.fran_pg2, self.pooled_pg] if v]

    def level_labels(self) -> list[str]:
        return [v for v in [self.yc_level, self.fran_level, self.yc_level2, self.fran_level2, self.pooled_level] if v and v != "ns"]

    def side_labels(self) -> list[str]:
        return [v for v in [self.yc_side, self.fran_side, self.pooled_side] if v]

    def nerve_labels(self) -> list[str]:
        return [v for v in [self.yc_nerve, self.fran_nerve, self.yc_nerve2, self.fran_nerve2, self.pooled_nerve] if v and v != "ns"]

    def db_labels(self) -> list[str]:
        return [v for v in [self.yc_db, self.fran_db, self.pooled_db] if v]

    @property
    def nerve_is_ns(self) -> bool:
        return len(self.nerve_labels()) == 0

def build_gt(
    yc_pg=None, fran_pg=None, yc_level=None, fran_level=None, yc_side=None, fran_side=None,
    yc_nerve=None, fran_nerve=None, yc_db=None, fran_db=None, yc_pg2=None, fran_pg2=None,
    yc_level2=None, fran_level2=None, yc_nerve2=None, fran_nerve2=None, pooled_pg=None,
    pooled_level=None, pooled_side=None, pooled_nerve=None, pooled_db=None,
) -> GroundTruth:
    return GroundTruth(
        yc_pg=normalize_pg(yc_pg), fran_pg=normalize_pg(fran_pg),
        yc_level=normalize_level(yc_level), fran_level=normalize_level(fran_level),
        yc_side=normalize_side(yc_side), fran_side=normalize_side(fran_side),
        yc_nerve=normalize_nerve(yc_nerve), fran_nerve=normalize_nerve(fran_nerve),
        yc_db=normalize_db(yc_db), fran_db=normalize_db(fran_db),
        yc_pg2=normalize_pg(yc_pg2), fran_pg2=normalize_pg(fran_pg2),
        yc_level2=normalize_level(yc_level2), fran_level2=normalize_level(fran_level2),
        yc_nerve2=normalize_nerve(yc_nerve2), fran_nerve2=normalize_nerve(fran_nerve2),
        pooled_pg=normalize_pg(pooled_pg), pooled_level=normalize_level(pooled_level),
        pooled_side=normalize_side(pooled_side), pooled_nerve=normalize_nerve(pooled_nerve),
        pooled_db=normalize_db(pooled_db),
    )

# =====================================================================
# INDIVIDUAL FIELD SCORERS
# =====================================================================

def _level_dist(a: str, b: str) -> Optional[int]:
    if a not in LEVEL_ORDER or b not in LEVEL_ORDER:
        return None
    return abs(LEVEL_ORDER.index(a) - LEVEL_ORDER.index(b))

def _nerve_dist(a: str, b: str) -> Optional[int]:
    if a not in NERVE_ORDER or b not in NERVE_ORDER:
        return None
    return abs(NERVE_ORDER.index(a) - NERVE_ORDER.index(b))

def score_pain_gen(llm_val, gt: GroundTruth) -> tuple[int, str]:
    llm = normalize_pg(llm_val)
    if llm is None:
        return 0, f"unparseable PG: {repr(llm_val)!r}"
    all_labels = gt.pg_labels()
    if not all_labels:
        return 0, "no expert PG labels available"
    if gt.consensus["pg"] and llm == gt.yc_pg:
        return 4, f"consensus exact match: {llm}"
    if llm in all_labels:
        return 3, f"matches one expert/pooled: {llm}"
    
    llm_fam = PAIN_GEN_FAMILIES.get(llm)
    gt_fams = {PAIN_GEN_FAMILIES.get(lbl) for lbl in all_labels if lbl in PAIN_GEN_FAMILIES}
    gt_fams.discard(None)
    
    if llm_fam and llm_fam in gt_fams:
        return 2, f"same disease family ({llm_fam}) but wrong subtype: {llm}"
    if llm in PAIN_GEN_FAMILIES:
        return 1, f"different disease family ({llm_fam} vs {gt_fams}): {llm}"
    return 0, f"vocabulary-violating PG: {llm}"

def score_side(llm_val, gt: GroundTruth) -> tuple[int, str]:
    llm = normalize_side(llm_val)
    if llm is None:
        return 0, f"unparseable side: {repr(llm_val)!r}"
    all_labels = gt.side_labels()
    if not all_labels:
        return 0, "no expert side labels available"
    if gt.consensus["side"] and llm == gt.yc_side:
        return 4, f"consensus exact match: {llm}"
    if llm in all_labels:
        return 3, f"matches one expert/pooled: {llm}"
    if llm == "midline/bilateral" and any(l in ("right", "left") for l in all_labels):
        return 2, "LLM hedged bilateral; expert specified unilateral"
    unilateral_map = {"right": "left", "left": "right"}
    if llm in unilateral_map and unilateral_map[llm] in all_labels:
        return 1, f"opposite laterality: LLM {llm}, expert {unilateral_map[llm]}"
    return 0, f"anatomically invalid side: {llm}"

def score_level(llm_val, gt: GroundTruth) -> tuple[int, str]:
    llm = normalize_level(llm_val)
    if llm is None:
        return 0, f"unparseable level: {repr(llm_val)!r}"
    if llm == "ns":
        return 0, "model returned NS; expert specified a level"
    
    all_levels = gt.level_labels()
    if not all_levels:
        return 4, "both model and experts: no specific level"
    if llm not in LEVEL_ORDER:
        return 0, f"non-lumbar or invalid level: {llm}"
        
    if gt.consensus["level"] and llm == gt.yc_level:
        return 4, f"consensus exact match: {llm}"
    if llm in all_levels:
        return 3, f"matches one expert: {llm}"
        
    if gt.consensus["level"]:
        d = _level_dist(llm, gt.yc_level)
        if d == 1:
            return 3, f"adjacent (±1) to consensus {gt.yc_level}: {llm}"
        if d == 2:
            return 2, f"±2 levels from consensus {gt.yc_level}: {llm}"
        if d is not None:
            return 1, f"±{d} levels from consensus {gt.yc_level}: {llm}"
    else:
        dists = [_level_dist(llm, lbl) for lbl in all_levels if lbl in LEVEL_ORDER]
        dists = [d for d in dists if d is not None]
        if not dists:
            return 0, "no valid level distances computable"
        best = min(dists)
        if best == 1:
            return 2, f"±1 level from one expert (non-consensus): {llm}"
        if best == 2:
            return 1, f"±2 levels from one expert (non-consensus): {llm}"
        return 0, f"≥3 levels from any expert: {llm}"
    return 0, f"no match: {llm}"

def score_nerve(llm_val, gt: GroundTruth) -> tuple[int, str]:
    llm = normalize_nerve(llm_val)
    if gt.nerve_is_ns and llm == "ns":
        return 4, "both model and experts: no nerve root specified (NS)"
    if gt.nerve_is_ns and llm != "ns":
        return 2, f"model named nerve {llm} but experts said NS"
    if not gt.nerve_is_ns and llm == "ns":
        return 0, "model returned NS; expert specified a nerve root"
    if llm not in NERVE_ORDER:
        return 0, f"non-lumbar/invalid nerve: {llm}"
        
    all_nerves = gt.nerve_labels()
    if gt.consensus["nerve"] and llm == gt.yc_nerve:
        return 4, f"consensus exact match: {llm}"
    if llm in all_nerves:
        return 3, f"matches one expert: {llm}"
        
    if gt.consensus["nerve"]:
        d = _nerve_dist(llm, gt.yc_nerve)
        if d == 1:
            return 3, f"adjacent (±1) to consensus {gt.yc_nerve}: {llm}"
        if d == 2:
            return 2, f"±2 from consensus {gt.yc_nerve}: {llm}"
        if d is not None:
            return 1, f"±{d} from consensus {gt.yc_nerve}: {llm}"
    else:
        dists = [_nerve_dist(llm, n) for n in all_nerves if n in NERVE_ORDER]
        dists = [d for d in dists if d is not None]
        if not dists:
            return 0, "no valid nerve distances"
        best = min(dists)
        if best == 1:
            return 2, f"±1 nerve from one expert (non-consensus): {llm}"
        if best == 2:
            return 1, f"±2 nerves from one expert (non-consensus): {llm}"
        return 0, f"≥3 nerves from any expert: {llm}"
    return 0, f"no match: {llm}"

def score_disc_bone(llm_val, gt: GroundTruth) -> tuple[int, str]:
    llm = normalize_db(llm_val)
    if llm is None:
        return 0, f"unparseable disc/bone: {repr(llm_val)!r}"
    all_labels = gt.db_labels()
    if not all_labels:
        return 0, "no expert disc/bone labels available"
        
    if gt.consensus["db"] and llm == gt.yc_db:
        return 4, f"consensus exact match: {llm}"
    if gt.consensus["db"] and gt.yc_db == "disc or bone" and llm in ("disc", "bone"):
        return 4, f"expert hedged 'disc or bone'; specific {llm} accepted"
    if llm in all_labels:
        return 3, f"matches one expert/pooled: {llm}"
    if "disc or bone" in all_labels and llm in ("disc", "bone"):
        return 3, f"one expert hedged; specific {llm} matches partial"
    if llm == "disc or bone" and all(l in ("disc", "bone") for l in all_labels):
        return 2, "LLM hedged 'disc or bone'; expert gave specific answer"
    if llm in ("disc", "bone") and any(l in ("disc", "bone") for l in all_labels):
        return 1, f"wrong designation: LLM {llm}, expert {all_labels}"
    return 0, f"vocabulary-violating disc/bone: {llm}"

# =====================================================================
# COMPOSITE SCORER
# =====================================================================

FIELD_WEIGHTS = {
    "pg": 0.35,
    "side": 0.25,
    "level": 0.20,
    "nerve": 0.10,
    "db": 0.10,
}

@dataclass
class PrIMEResult:
    pg: int
    side: int
    level: int
    nerve: int
    db: int
    pg_rationale: str = ""
    side_rationale: str = ""
    level_rationale: str = ""
    nerve_rationale: str = ""
    db_rationale: str = ""
    composite_raw: float = 0.0
    composite_pct: float = 0.0
    consensus: dict = field(default_factory=dict)

    def __post_init__(self):
        self.composite_raw = round(
            self.pg * FIELD_WEIGHTS["pg"] +
            self.side * FIELD_WEIGHTS["side"] +
            self.level * FIELD_WEIGHTS["level"] +
            self.nerve * FIELD_WEIGHTS["nerve"] +
            self.db * FIELD_WEIGHTS["db"],
            4,
        )
        self.composite_pct = round(self.composite_raw / 4 * 100, 2)

    def to_dict(self) -> dict:
        return {
            "PrIME_PG": self.pg,
            "PrIME_Side": self.side,
            "PrIME_Level": self.level,
            "PrIME_Nerve": self.nerve,
            "PrIME_DB": self.db,
            "PrIME_Composite_raw": self.composite_raw,
            "PrIME_Composite_pct": self.composite_pct,
            "PG_rationale": self.pg_rationale,
            "Side_rationale": self.side_rationale,
            "Level_rationale": self.level_rationale,
            "Nerve_rationale": self.nerve_rationale,
            "DB_rationale": self.db_rationale,
            "consensus_pg": self.consensus.get("pg"),
            "consensus_side": self.consensus.get("side"),
            "consensus_level": self.consensus.get("level"),
            "consensus_nerve": self.consensus.get("nerve"),
            "consensus_db": self.consensus.get("db"),
        }

class PrIMEScorer:
    """
    Main entry point for evaluating AI outputs against the PrIME benchmark.
    Instantiate once; call score_case() per LLM output row.
    """
    def score_case(
        self, llm_pg, llm_level, llm_side, llm_nerve, llm_db, gt: GroundTruth
    ) -> PrIMEResult:
        pg, pg_r = score_pain_gen(llm_pg, gt)
        side, side_r = score_side(llm_side, gt)
        level, level_r = score_level(llm_level, gt)
        nerve, nerve_r = score_nerve(llm_nerve, gt)
        db, db_r = score_disc_bone(llm_db, gt)
        
        return PrIMEResult(
            pg=pg, side=side, level=level, nerve=nerve, db=db,
            pg_rationale=pg_r, side_rationale=side_r,
            level_rationale=level_r, nerve_rationale=nerve_r,
            db_rationale=db_r, consensus=gt.consensus,
        )

    def score_dataframe(
        self,
        df: pd.DataFrame,
        gt_lookup: dict, 
        accession_col: str = "ACCESSION_NUM",
        pg_col: str = "PAIN_GENERATOR",
        level_col: str = "LEVEL",
        side_col: str = "SIDE",
        nerve_col: str = "NERVE",
        db_col: str = "DISC_OR_BONE_DISEASE",
    ) -> pd.DataFrame:
        """
        Score an entire DataFrame of LLM outputs.
        Returns the same DataFrame with PrIME score columns appended.
        """
        records = []
        for _, row in df.iterrows():
            acc = row[accession_col]
            gt = gt_lookup.get(acc)
            if gt is None:
                records.append({
                    "PrIME_PG": None, "PrIME_Side": None, "PrIME_Level": None,
                    "PrIME_Nerve": None, "PrIME_DB": None,
                    "PrIME_Composite_raw": None, "PrIME_Composite_pct": None,
                })
                continue
            
            result = self.score_case(
                llm_pg=row.get(pg_col),
                llm_level=row.get(level_col),
                llm_side=row.get(side_col),
                llm_nerve=row.get(nerve_col),
                llm_db=row.get(db_col),
                gt=gt,
            )
            records.append(result.to_dict())
            
        scored_cols = pd.DataFrame(records, index=df.index)
        return pd.concat([df, scored_cols], axis=1)
