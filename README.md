# Approximation Algorithms Benchmark Suite

Research-oriented implementation and benchmarking framework for approximation and heuristic algorithms for:

- 1D Bin Packing
- (Scheduling modules coming soon)

## Implemented Algorithms

### 1D Bin Packing
- First Fit (FF)
- Best Fit (BF)
- First Fit Decreasing (FFD)
- Best Fit Decreasing (BFD)

## Lower Bounds
- Volume bound
- Combined bound (volume + large-item bound)

## Reproducibility

Create environment:

    conda env create -f environment.yml
    conda activate apsuite
    pip install -e .

Run baseline benchmark:

    python scripts/bench_packing1d.py

Generate plots:

    python scripts/plot_packing1d.py

## Project Structure
- src/apsuite/packing1d: algorithms + bounds
- scripts/: experiment runners
- tests/: pytest suite
- report/: research report (in progress)

## Status
v0.1 – 1D packing benchmark framework completed.