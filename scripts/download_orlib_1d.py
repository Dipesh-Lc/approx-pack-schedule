from __future__ import annotations

from pathlib import Path
from urllib.request import urlretrieve

BASE = "https://people.brunel.ac.uk/~mastjjb/jeb/orlib/files"
FILES = [f"binpack{i}.txt" for i in range(1, 9)]

def main() -> None:
    outdir = Path("data/raw/orlib_1d")
    outdir.mkdir(parents=True, exist_ok=True)

    for fn in FILES:
        url = f"{BASE}/{fn}"
        outpath = outdir / fn
        print(f"Downloading {url} -> {outpath}")
        urlretrieve(url, outpath)

    print("Done.")

if __name__ == "__main__":
    main()