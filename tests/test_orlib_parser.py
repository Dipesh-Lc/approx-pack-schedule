from pathlib import Path
from apsuite.packing1d.orlib_parser import load_orlib_file

def test_orlib_parser_reads_first_file_if_present():
    p = Path("data/raw/orlib_1d/binpack1.txt")
    if not p.exists():
        return  # allow tests to pass even before download
    instances = load_orlib_file(p, normalize_capacity=True)
    assert len(instances) > 0
    inst0 = instances[0]
    assert inst0.capacity == 1.0
    assert len(inst0.items) > 0
    assert all(0 < x <= 1.0 for x in inst0.items)