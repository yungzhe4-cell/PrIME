# PrIME Rubric

**Pain-Relevant Imaging Evaluation (PrIME)** is a clinically weighted benchmark for evaluating AI-generated lumbar spine pain classifications against expert musculoskeletal radiologist reference standards.

The rubric was developed to assess how accurately large language models (LLMs) identify clinically relevant pain generators and associated imaging findings from lumbar spine MRI reports. PrIME provides a reproducible framework for comparing AI outputs with subspecialty radiologist interpretations and consensus labels.

---

## How to Cite

If you use this rubric in your research, please cite:

```bibtex
@article{chen2026prime,
  title={Benchmarking Large Language Models for Classification of Lumbar Spine Pain Generators Using the PrIME Rubric},
  author={Chen, Yung Hsin and colleagues},
  journal={American Journal of Roentgenology},
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

Rather than using simple binary correctness, PrIME awards partial credit for anatomically plausible responses and weights diagnostic components according to clinical importance.

---

## Table of Contents

1. [PrIME Components](#prime-components)
2. [Pain Generator Categories](#pain-generator-categories)
3. [Normalization Rules](#normalization-rules)
4. [Scoring Framework](#scoring-framework)
5. [Composite Score Calculation](#composite-score-calculation)
6. [Ground Truth Construction](#ground-truth-construction)
7. [Repository Contents](#repository-contents)
8. [Intended Use](#intended-use)
9. [Limitations](#limitations)
10. [License](#license)

---

## PrIME Components

| Dimension | Clinical Question | Weight |
|------------|------------------|---------|
| Pain Generator | What pathology is causing the patient's pain? | 35% |
| Laterality | Which side is affected? | 25% |
| Anatomic Level | Where is the pathology located? | 20% |
| Nerve Root | Which nerve root is involved? | 10% |
| Tissue Origin | Is the pathology disc-related or bone/joint-related? | 10% |

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

The overall PrIME score is calculated using weighted component scores:

| Component | Weight |
|------------|---------|
| Pain Generator | 35% |
| Laterality | 25% |
| Anatomic Level | 20% |
| Nerve Root | 10% |
| Tissue Origin | 10% |

Composite scores are reported on a 0-100% scale.

---

## Ground Truth Construction

Reference labels are derived from independent review by fellowship-trained musculoskeletal radiologists.

The framework supports:

- Individual expert labels
- Consensus labels
- Pooled expert labels
- Secondary pain generators when applicable

This structure allows evaluation against both strict consensus standards and broader expert agreement.

---

## Repository Contents

| File | Description |
|--------|-------------|
| `PrIME_Rubric.py` | Core implementation of the scoring framework |
| `README.md` | Documentation and methodology overview |

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

PrIME measures concordance with expert-derived reference labels rather than clinical outcomes.

A high score indicates agreement with subspecialty radiologist assessment but does not demonstrate:

- Diagnostic correctness
- Treatment appropriateness
- Clinical utility
- Improved patient outcomes

The framework was developed specifically for lumbar spine pain classification and may require modification before use in other musculoskeletal or neuroradiology domains.

---

## License

Please cite the associated publication when using this repository or adapting the rubric for future studies.
