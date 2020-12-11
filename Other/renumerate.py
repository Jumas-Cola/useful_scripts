#!/bin/python3

from pathlib import Path

p = Path('.')
numeric_names = [f for f in p.iterdir() if f.name.split('.')[0].isdigit()]
file_types = {ft.suffix for ft in numeric_names}
file_types.add('')

for ft in file_types:
    files_of_type = []
    for f in numeric_names:
        if f.suffix == ft:
            files_of_type.append(f)
    files_of_type.sort(key=lambda x: int(x.name.split('.')[0]))
    for n, sf in enumerate(files_of_type, 1):
        sf.rename(Path(str(n) + sf.suffix))
