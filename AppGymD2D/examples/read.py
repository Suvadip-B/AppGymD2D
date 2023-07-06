import json

from pathlib import Path
from typing import Optional


def load_position_config(position_config_file) -> dict:
    with open(position_config_file, mode='r') as fid:
        return json.load(fid)


pos_file: Optional[Path]="C:\\Users\\Suvadip\\Documents\\New D2D\\gym-d2d-master\\examples\\position_config.json"
position=load_position_config(pos_file)
print(position)

lst=['1','2','3','4','5']
print(lst[-5:])