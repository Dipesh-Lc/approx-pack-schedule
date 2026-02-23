import argparse

from apsuite.experiments.registry import REGISTRY
from apsuite.experiments.io import (
    load_config,
    ensure_dir,
    save_results,
    save_metadata,
    copy_config,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    cfg = load_config(args.config)
    task = cfg["task"]

    if task not in REGISTRY:
        raise ValueError(f"Unknown task: {task}")

    runner = REGISTRY[task]
    rows = runner(cfg)

    out_dir = cfg["out_dir"]
    ensure_dir(out_dir)

    save_results(rows, out_dir)
    save_metadata(out_dir)
    copy_config(args.config, out_dir)

    print(f"Experiment complete. Results saved to {out_dir}")


if __name__ == "__main__":
    main()