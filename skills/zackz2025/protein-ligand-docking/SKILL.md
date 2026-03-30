---
name: protein-ligand-docking
description: |
  Protein-Ligand In Silico Docking Workflow. A complete pipeline from sequence retrieval and structure modeling to molecular docking and quantitative analysis.

  **Use Cases**:
  (1) Evaluate whether a small molecule / drug can bind to a target protein
  (2) Study selectivity of inhibitors between bacterial and host proteins
  (3) Explore drug target conservation (host vs pathogen)
  (4) Research direction: antibacterial drug mechanism, drug-host-microbiome interactions

  **When to Use This Skill**:
  - User mentions "molecular docking", "protein docking", "drug prediction"
  - Evaluating "Can X target Y protein?"
  - Studying "inhibitor selectivity" or "cross-species target conservation"
  - Needs a complete in silico drug discovery pipeline
---

# Protein-Ligand In Silico Docking Workflow

## Applicable Problem Types

```
"Can Drug X bind to Protein Y?"
"How selective is this inhibitor between bacterial and human proteins?"
"Does this inhibitor act through direct bactericidal or indirect mechanisms?"
```

## Workflow Overview (7 Steps)

```
Step 1: Sequence Retrieval (UniProt API)
         ↓
Step 2: PDB Structure Search (RCSB PDB API)
         ↓
Step 3: Sequence Alignment (Biopython)
         ↓
Step 4: Protein Complex Modeling (AlphaFold-Multimer, Colab)
         ↓
Step 5: Model Quality Assessment (pLDDT + PAE)
         ↓
Step 6: Molecular Docking (AutoDock Vina, WSL)
         ↓
Step 7: Quantitative Analysis & Conclusions
```

---

## Step 1 — Sequence Retrieval

**Input**: Protein name or UniProt ID
**Output**: FASTA sequence file

```bash
# User needs to provide:
# - Target protein UniProt ID (or name)
# - Species (human, E. coli, etc.)
```

**Tool**: UniProt REST API (automatic, no manual download needed)

---

## Step 2 — PDB Structure Search

**Purpose**: Obtain reference crystal structure (for binding site reference)
**Tool**: RCSB PDB API

**Key PDB Structure Types**:
- Target protein has structure → Use directly as reference
- No structure → Proceed to Step 4 AlphaFold modeling

---

## Step 3 — Sequence Alignment (Critical!)

**Purpose**: Assess sequence conservation between targets → Determine if ligand binding pocket is conserved

**Tools**: Biopython `PairwiseAligner` (local) + Clustal Omega (EBI API)

**Output Interpretation**:
| Similarity | Inference |
|------------|-----------|
| > 40% | Binding pocket likely conserved, proceed with docking |
| 20-40% | Uncertain, structural analysis needed |
| < 20% | Likely not conserved, conclusion can be drawn directly |

**Operation**: Run `scripts/step3_alignment.py`

---

## Step 4 — AlphaFold-Multimer Protein Complex Modeling

**Required only when target protein lacks PDB structure**

**Platform**: Google Colab (free GPU)
**Input**: Multi-chain FASTA file (`>chainA\nseq\n>chainB\nseq`)
**Output**: Predicted protein complex PDB structure

**Colab Code Template**: `notebooks/alphafold_multimer_colab.ipynb`

**Key Parameters**:
```python
from colabfold.batch import run
run(
    queries=['complex.fasta'],
    result_dir='./AF_output',
    model_type='alphafold2_multimer_v3',  # For heteromeric complexes
    num_models=5,
    num_recycles=6,
    is_complex=True,
)
```

**Note**: Only include the functional subunits of the complex. Exclude non-structural or accessory chains.

---

## Step 5 — Model Quality Assessment (Mandatory!)

**Both metrics are essential:**

### pLDDT (Per-Residue Fold Quality)
- > 90: Very high confidence
- 70-90: Confident
- < 50: Likely disordered region

### PAE (Predicted Alignment Error) — Most Critical!
- PAE < 5 Å: High confidence at interface
- PAE 5-10 Å: Medium confidence, can proceed
- PAE > 15 Å: Interface unreliable, docking results meaningless

**Operation**: Run `scripts/step5_pae_analysis.py`

---

## Step 6 — AutoDock Vina Molecular Docking

**Platform**: WSL (Linux) or Colab
**Software**: AutoDock Vina v1.2.7

### 6.1 Receptor Preparation (PDB → PDBQT)
```bash
obabel -ipdb receptor.pdb -opdbqt -O receptor.pdbqt -xr
```

### 6.2 Ligand Preparation (SDF/MOL → PDBQT)
```bash
obabel -isdf ligand.sdf -opdbqt -O ligand.pdbqt
```

### 6.3 Run Docking
```bash
./vina --receptor receptor.pdbqt \
        --ligand ligand.pdbqt \
        --center_x -1.5 --center_y 3.3 --center_z -5.0 \
        --size_x 25 --size_y 25 --size_z 25 \
        --exhaustiveness 16 \
        --num_modes 20 \
        --write_maps vina_maps \
        --force_even_voxels
```

### 6.4 Grid Box Coordinates Source
Grid Box center = Calculated from AlphaFold interface analysis (see Step 5 output)

---

## Step 7 — Quantitative Analysis

**All three dimensions must be reported:**

### Dimension 1: Binding Affinity
| Binding Energy | Strength |
|----------------|----------|
| < -9 kcal/mol | Strong binding |
| -7 ~ -9 kcal/mol | Moderate |
| > -7 kcal/mol | Weak / not meaningful |

### Dimension 2: Spatial Position (Binding Pose)
- Is the ligand on the functional interface?
- Nearest distance to both chains?
- Number of contact residues within 4 Å?

### Dimension 3: Structural Reasonableness
- Can the ligand physically fit into the binding pocket?
- Conformational consistency (RMSD across poses)?

---

## Complete Analysis Report Template

After completing all steps, run:
```bash
python scripts/step7_summary_report.py \
    --workspace /path/to/output \
    --protein_name "ProteinName" \
    --ligand_name "LigandName"
```

Generates:
- `Summary.md`
- `Summary.docx`
- `docking_summary_fig.png`

---

## Tool Dependencies

| Tool | Installation | Purpose |
|------|-------------|---------|
| Python 3 | System-provided | All pipeline scripts |
| Biopython | `pip install biopython` | Sequence alignment |
| RDKit | `pip install rdkit` | Ligand processing |
| OpenBabel | `pip install openbabel-wheel` | PDBQT conversion |
| AutoDock Vina | See below | Molecular docking |
| py3Dmol | `pip install py3Dmol` | HTML 3D visualization |

### AutoDock Vina Installation (WSL/Linux)
```bash
# x86_64 Linux
wget https://github.com/ccsb-scripps/AutoDock-Vina/releases/download/v1.2.7/vina_1.2.7_linux_x86_64 -O vina
chmod +x vina
```

### AlphaFold-Multimer (Colab)
Colab notebook template: `notebooks/alphafold_multimer_colab.ipynb`

---

## Typical Workflow Time Estimate

| Step | Time | Who |
|------|------|-----|
| Step 1 Sequence Retrieval | 5 min | AI |
| Step 2 PDB Search | 5 min | AI |
| Step 3 Sequence Alignment | 10 min | AI |
| Step 4 AlphaFold | 5-15 min | User (Colab) |
| Step 5 PAE Analysis | 5 min | AI |
| Step 6 Vina Docking | 5-10 min | AI |
| Step 7 Report Generation | 5 min | AI |

---

## Quality Control Checklist

Before drawing conclusions, confirm all of the following:

- [ ] pLDDT > 70 (model single-chain fold is confident)
- [ ] PAE < 15 Å (interface position is confident)
- [ ] Docking exhaustiveness ≥ 8
- [ ] Best pose RMSD vs second-best < 3 Å across 9 modes (convergence)
- [ ] Ligand position is on the functional interface (not floating on surface)
- [ ] Contact residues within 4 Å from receptor

---

## Limitations (Must Inform User)

1. **Static Docking**: Does not account for ligand-induced fit and conformational changes
2. **AlphaFold Limitations**: N/C-terminal disordered regions may be missing; complex interface PAE has errors
3. **Force Field**: Vina scoring function may be inaccurate for certain compound classes
4. **Gold Standard for Experimental Validation**: SPR, ITC, enzyme inhibition assays are the final arbiters

---

*Skill: protein-ligand-docking | For in silico drug discovery research*
