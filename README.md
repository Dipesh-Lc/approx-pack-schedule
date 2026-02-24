# Approx-Pack-Schedule

**Approximation & benchmarking framework for discrete optimization: (1D,2D) packing, scheduling,**

---

## 📌 Overview

**Approx-Pack-Schedule** is a research-oriented implementation and empirical evaluation of classical approximation algorithms for:

- 📦 1D Bin Packing  
- 📦 2D Bin Packing  
- ⏱ Identical Machine Scheduling  
- 🧮 Unrelated Machine Scheduling (LP Relaxation + Rounding)

The project emphasizes:

- Clean and modular algorithm implementations  
- Theoretical lower bounds  
- Empirical approximation ratios  
- Runtime scaling analysis  
- Config-driven reproducible experiments  

This repository is designed as an algorithm engineering project combining theory and experimentation.

---

# Implemented Phases

---

## Phase 1 — 1D Bin Packing

### Algorithms

- First Fit (FF)  
- Best Fit (BF)  
- First Fit Decreasing (FFD)  
- Best Fit Decreasing (BFD)  
- Hybrid heuristics  

### Lower Bound

Volume lower bound:

$$
LB = \left\lceil \sum_i s_i \right\rceil
$$

### Metrics

- Number of bins  
- Gap vs lower bound  
- Approximation ratio  
- Runtime  

---

## Phase 2 — 2D Bin Packing

### Heuristics

- Shelf (height-decreasing)  
- Guillotine greedy  
- Hybrid (best-of Shelf & Guillotine)  

### Lower Bound

Area lower bound:

$$
LB = \left\lceil \frac{\sum_i w_i h_i}{W \cdot H} \right\rceil
$$

Rotation is currently not considered.

---

## Phase 3 — Identical Machine Scheduling

### Algorithms

- List Scheduling  
- LPT (Longest Processing Time first)  

### Lower Bound

$$
LB = \max \left( \frac{\sum_j p_j}{m}, \max_j p_j \right)
$$

### Empirical Observation

| Algorithm | Typical Ratio |
|-----------|--------------|
| LIST      | ~1.03–1.15   |
| LPT       | ~1.00–1.02   |

---

## Phase 4 — Unrelated Machine Scheduling

### LP Relaxation

Minimize makespan \( T \)

Subject to:

$$
\sum_i x_{ij} = 1
$$

$$
\sum_j p_{ij} x_{ij} \le T
$$

$$
0 \le x_{ij} \le 1
$$

### Solver

- SciPy `linprog` (HiGHS backend)

### Rounding

- Assign each job to machine with largest fractional value  
- Optional local search improvement  
- Greedy baseline comparison  

### Theoretical Guarantee

- 2-approximation  

### Empirical Behavior

Typically:

- `LP_ROUND ≈ 1.10–1.20` vs LP bound  
- `LP_ROUND + LS` improves further  

---

## Phase 5 — Config-Driven Experiment Harness

Experiments are fully configurable via YAML:

```bash
python scripts/run_experiments.py --config configs/packing1d_small.yaml
```

### Logged Metadata per Run

Each experiment execution records:

- `task`
- `distribution`
- `instance_size`
- `num_machines` (if applicable)
- `seed`
- `algorithm`
- `objective_value`
- `lower_bound`
- `lp_optimum` (if applicable)
- `approximation_ratio`
- `runtime`

### Output Directory

Results are saved under:

```text
results/experiments/<experiment_name>/
```

## Phase 6 — Experimental Study

### Synthetic Distributions

#### Packing

- Uniform(0,1)
- Bimodal
- Heavy-tail

#### Scheduling

- Uniform processing times
- Exponential
- Correlated machine speeds (unrelated machines)

---

### Generated Plots

- Approximation ratio histograms  
- Runtime vs. \( n \) scaling curves  
- LP rounding quality plots  
- Comparative scaling curves  

All plots use **Matplotlib**.

---

# 📂 Project Structure

```text
src/apsuite/
    packing1d/
    packing2d/
    scheduling/
        identical/
        unrelated/
    experiments/

scripts/
    run_experiments.py
    plot_experiments.py
    run_sched_unrelated.py
    ...

configs/
    *.yaml

results/
    tables/
    figures/
    experiments/

tests/
environment.yml
```

---

# ⚙️ Installation

## 1️⃣ Clone repository

```bash
git clone https://github.com/Dipesh-Lc/approx-pack-schedule.git
cd approx-pack-schedule
```

## 2️⃣ Create environment

```bash
conda env create -f environment.yml
conda activate approx-pack-schedule
```

## 3️⃣ Install package (editable mode)

```bash
pip install -e .
```

---

# 🧪 Run Tests

```bash
pytest -q
```

All phases are covered by unit tests:

- Packing heuristics  
- Lower bounds  
- Scheduling algorithms  
- LP solver integration  
- Rounding validity  
- Local search improvement  

---

# 📊 Running Experiments

## Example

```bash
python scripts/run_experiments.py --config configs/packing1d_scale.yaml
```

## Generate plots

```bash
python scripts/plot_experiments.py --exp_dir results/experiments/packing1d_scale
```

---

# 🔬 Reproducibility

- Explicit random seeds  
- Config-driven instance generation  
- CSV result logging  
- Deterministic rounding  
- No hidden randomness  

Designed to mirror research-grade experimental pipelines.

---

# 📈 Sample Observations

## 1D Packing

- FFD consistently near best practical heuristic  
- Hybrid strategies sometimes improve robustness  

## 2D Packing

- Shelf performs well on uniform   
- Guillotine struggles on heavy-tail   
- Hybrid improves consistency  

## Identical Scheduling

- LPT nearly optimal empirically  

## Unrelated Scheduling

- LP rounding significantly improves greedy baseline  
- Local search provides additional gains  
- Empirical ratios far below worst-case 2-approximation bound  

---

# 🧠 Design Philosophy

- Classical approximation algorithms  
- Clear separation of:
  - Algorithm logic  
  - Lower bounds  
  - Experiment harness  
- Runtime measured in harness, not algorithms  
- Clean and extensible architecture  
- Focus on clarity and reproducibility  

---

# 🛠 Future Extensions

Potential future work:

- 2D packing with rotation  
- Karmarkar–Karp heuristic  
- Exact ILP solver comparisons  
- Statistical confidence intervals  
- Log-scale runtime plots  
- Advanced correlated speed models  
- Larger LP experiments  

---

# 📚 References

- Coffman, Garey, Johnson -- Bin Packing  
- Graham (1966) -- List Scheduling  
- Shmoys & Tardos -- LP Rounding for Scheduling  
- Williamson & Shmoys -- *The Design of Approximation Algorithms*  

---

# 🏁 Project Status

- ✅ Phase 1 — 1D Packing  
- ✅ Phase 2 — 2D Packing  
- ✅ Phase 3 — Identical Scheduling  
- ✅ Phase 4 — Unrelated Scheduling  
- ✅ Phase 5 — Experiment Harness  
- ✅ Phase 6 — Experimental Evaluation  

---

# 📜 License

MIT License

---

## 👤 Author

**Dipesh**

Independent Research Project  
Discrete Optimization & Approximation Algorithms  
2026
