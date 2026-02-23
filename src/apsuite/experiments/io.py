from __future__ import annotations

import json
import os
import shutil
import sys
import platform
from datetime import datetime
import pandas as pd
import yaml


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def save_results(rows: list[dict], out_dir: str):
    ensure_dir(out_dir)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(out_dir, "results.csv"), index=False)


def save_metadata(out_dir: str):
    meta = {
        "timestamp": datetime.now().isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
    }
    with open(os.path.join(out_dir, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)


def copy_config(config_path: str, out_dir: str):
    shutil.copy(config_path, os.path.join(out_dir, "config_used.yaml"))