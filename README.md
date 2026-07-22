# PrIME Rubric

**Pain-Relevant Imaging Evaluation (PrIME)** is a clinically weighted benchmark for evaluating AI-generated lumbar spine pain classifications against expert spine specialist reference standards.

The rubric was developed to assess how accurately large language models (LLMs) identify clinically relevant pain generators and their associated imaging characteristics from lumbar spine MRI reports. It was designed for benchmarking AI systems against specialist interpretation rather than replacing clinical judgment.

---

## How to Cite

If you use this rubric in your research, please cite:

```bibtex
@article{chen2026prime,
  title={Benchmarking Large Language Models for Classification of Lumbar Spine Pain Generators Using the PrIME Rubric},
  author={Chen, Yung Hsin and colleagues},
  institution={Massachusetts General Hospital},
  year={2026}
}
```

*Please update the citation once the final AJR publication is available.*

---

## What is PrIME?

PrIME evaluates whether an AI system correctly identifies:

1. **Pain Generator**
2. **Anatomic Level**
3. **Laterality**
4. **Affected Nerve Root**
5. **Tissue Origin**

Unlike simple accuracy metrics, PrIME evaluates multiple clinically important dimensions of a diagnosis. 


## PrIME Components

| Dimension | Clinical Question | Example Labels | Weight |
|------------|------------------|---------------|---------|
| Pain Generator | What pathology is causing the patient's pain? | Canal stenosis, foraminal stenosis, disc herniation, facet arthropathy | 35% |
| Laterality | Which side is affected? | Right, Left, Midline/Bilateral | 25% |
| Spinal Level | Where is the pathology located? | L1-2, L2-3, L3-4, L4-5, L5-S1 | 20% |
| Nerve Root | Which nerve root is involved? | L1, L2, L3, L4, L5, S1, S2 | 10% |
| Tissue Origin | Is the pathology primarily disc or bone/joint related? | Disc, Bone | 10% |

Each component receives a weighted score reflecting its clinical importance.

The rubric explicitly incorporates partial credit for anatomically plausible but imperfect responses, enabling more nuanced benchmarking of AI performance than binary correct/incorrect scoring.

---

## Table of Contents

1. [Pain Generator Categories](#pain-generator-categories)
2. [Normalization Rules](#normalization-rules)
3. [Scoring Framework](#scoring-framework)
4. [Composite Score Calculation](#composite-score-calculation)
5. [Ground Truth Construction](#ground-truth-construction)
6. [Repository Contents](#repository-contents)
7. [Intended Use](#intended-use)
8. [Limitations](#limitations)
9. [License](#license)

---



## Pain Generator Categories

PrIME standardizes synonymous clinical terminology into the following primary categories.

| Category | Representative Terms |
|-----------|---------------------|
| Canal Stenosis | Central canal stenosis, lumbar spinal stenosis |
| Subarticular Stenosis | Lateral recess stenosis, subarticular stenosis |
| Foraminal Stenosis | Foraminal narrowing, foraminal stenosis |
| Disc Herniation / Annular Tear | Disc herniation, annular tear |
| Degenerative Disc Disease with Bone Marrow Edema | Modic-associated pain patterns |
| Facet Arthropathy | Facet degeneration, zygapophyseal joint disease |
| Spondylolysis | Pars interarticularis defect |

---

## Normalization Rules

To ensure consistent scoring across raters and AI outputs, synonymous clinical terminology is normalized before scoring.

### Anatomic Level

| Input Label | Standardized Label |
|-------------|-------------------|
| L1-L2 | L1-2 |
| L1/L2 | L1-2 |
| L2-L3 | L2-3 |
| L2/L3 | L2-3 |
| L3-L4 | L3-4 |
| L3/L4 | L3-4 |
| L4-L5 | L4-5 |
| L4/L5 | L4-5 |
| L5/S1 | L5-S1 |
| L5-S2 | L5-S1 |
| Not Specified | NS |

#### Ambiguous Level Mapping

| Input Label | Standardized Label |
|-------------|-------------------|
| L4-5 or L5-S1 | L4-5 |
| L3-4 or L4-5 | L3-4 |
| L2-3 or L3-4 | L2-3 |

---

### Laterality

| Input Label | Standardized Label |
|-------------|-------------------|
| Right | Right |
| Left | Left |
| Bilateral | Midline/Bilateral |
| Midline | Midline/Bilateral |
| Both | Midline/Bilateral |
| B/L | Midline/Bilateral |
| Midline or Right | Midline/Bilateral |
| Midline or Left | Midline/Bilateral |

---

### Nerve Root

| Input Label | Standardized Label |
|-------------|-------------------|
| L1 | L1 |
| L2 | L2 |
| L3 | L3 |
| L4 | L4 |
| L5 | L5 |
| S1 | S1 |
| S2 | S2 |
| Not Specified | NS |
| N/A | NS |
| None | NS |

#### Multiple Nerve Root Mapping

| Input Label | Standardized Label |
|-------------|-------------------|
| L5 and S1 | L5, S1 |
| L4 or L5 | L4, L5 |
| L5 or S1 | L5, S1 |
| L3 or L4 | L3, L4 |
| L4 or L5 or S1 | L4, L5, S1 |
| L5 or S1 or S2 | L5, S1, S2 |

---

### Tissue Origin

| Input Label | Standardized Label |
|-------------|-------------------|
| Disc Herniation | Disc |
| Degenerative Disc Disease | Disc |
| Annular Tear | Disc |
| Facet Arthropathy | Bone |
| Degenerative Facet Disease | Bone |
| Degenerative Joint Disease | Bone |
| Bone Disease | Bone |
| Disc or Bone | Disc or Bone |
| Not Specified | NS |

---

## Scoring Framework

Each diagnostic dimension is scored independently.

### Pain Generator

Assesses agreement regarding the primary pain-producing pathology.

### Laterality

Evaluates whether the affected side is correctly identified.

### Anatomic Level

Measures agreement regarding the lumbar level responsible for symptoms.

### Nerve Root

Measures agreement regarding the implicated nerve root.

### Tissue Origin

Evaluates whether pathology is correctly classified as primarily disc-related or bone/joint-related.

The rubric supports partial credit when outputs are anatomically plausible but not exact matches.

---

## Composite Score Calculation

| Field | Abbreviation | Weight |
|---------|-------------|---------|
| Pain Generator | PG | 35% |
| Side / Laterality | Side | 25% |
| Spinal Level | Level | 20% |
| Nerve Root | NR | 10% |
| Disc/Bone Designation | DB | 10% |

### Composite Formula

PrIME = 0.35·PG + 0.25·Side + 0.20·Level + 0.10·NR + 0.10·DB

Maximum possible score = 4.0

Higher scores indicate greater concordance with expert spine specialist reference labels.

---

## Field-Level Scoring Rules


| Field | Weight | Score 4 | Score 3 | Score 2 | Score 1 | Score 0 |
|---------|---------|---------|---------|---------|---------|---------|
| Pain Generator | 35% | Expert consensus match | Match to one expert | Same disease family, wrong subtype | Unrelated structural finding | Invalid or hallucinated answer |
| Side | 25% | Expert consensus match | Match to one expert | Bilateral hedge when expert specifies unilateral side | Opposite laterality | Invalid side |
| Level | 20% | Exact consensus level | Adjacent level or match to one expert | Two-level proximity | Three-level proximity | Impossible level |
| Nerve Root | 10% | Exact consensus nerve | Adjacent root or match to one expert | Two-root proximity | Three-root proximity | Impossible nerve |
| Disc/Bone | 10% | Consensus match | Match to one expert | "Disc or bone" hedge | Wrong category | Invalid designation |

---

## Clinical Weighting Rationale


Weights were assigned according to expected downstream clinical consequences.


| Field | Clinical Importance | Weight |
|---------|--------------------|---------|
| Pain Generator | Determines presumed symptomatic pathology and treatment pathway | 35% |
| Side / Laterality | Influences procedural targeting and patient safety | 25% |
| Spinal Level | Guides anatomic localization and intervention planning | 20% |
| Nerve Root | Supports radiculopathy mapping and communication | 10% |
| Disc/Bone Designation | Provides disease-category context | 10% |

---

## Ground Truth Construction

Reference labels are derived from independent review by fellowship-trained musculoskeletal radiologist and anesthesia spine pain specialist.

The framework supports:

- Individual expert labels
- Consensus labels
- Pooled expert labels
- Secondary pain generators and nerve distribution when applicable

This structure allows evaluation against both strict consensus standards and broader expert agreement.

---

## Repository Contents

| File | Description |
|--------|-------------|
| `PrIME_Rubric.py` | Core implementation of the PrIME scoring framework |
| `README.md` | Repository documentation and methodology overview |
| `examples/` | Example inputs and scoring outputs (if provided) |
| `sample_data/` | Demonstration dataset for testing the rubric (if provided) |

Key features include:

- Clinical vocabulary normalization
- Ground truth construction utilities
- Component-specific scoring functions
- Weighted composite scoring
- Reproducible benchmarking workflow

---

## Intended Use

PrIME is intended for:

- LLM benchmarking studies
- Clinical NLP research
- Radiology AI validation
- Diagnostic reasoning assessment
- Reproducible comparison of AI systems

---

## Limitations

PrIME measures agreement with expert-derived labels rather than clinical outcomes. 

A high score indicates agreement with subspecialty radiologist assessment but does not demonstrate:

- Diagnostic correctness
- Treatment appropriateness
- Clinical utility
- Improved patient outcomes

The framework was developed specifically for lumbar spine pain classification and may require modification before use in other musculoskeletal or neuroradiology domains.

---

## License

Please cite the associated publication when using this repository or adapting the rubric for future studies.
