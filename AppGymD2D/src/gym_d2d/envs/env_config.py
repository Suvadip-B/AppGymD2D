from dataclasses import dataclass
import json
from pathlib import Path
from typing import Optional, Type

from gym_d2d.path_loss import PathLoss, LogDistancePathLoss
from gym_d2d.traffic_model import TrafficModel, DownlinkTrafficModel


@dataclass
class EnvConfig:
    num_rbs: int = 100
    num_cues: int = 40
    num_due_pairs: int = 70
    num_grps:int = 1
    cell_radius_m: float = 1500.0
    d2d_radius_m: float = 20.0
    due_min_tx_power_dBm: int = 0
    due_max_tx_power_dBm: int = 20
    cue_max_tx_power_dBm: int = 24
    mbs_max_tx_power_dBm: int = 43
    path_loss_model: Type[PathLoss] = LogDistancePathLoss
    traffic_model: Type[TrafficModel] = DownlinkTrafficModel
    carrier_freq_GHz: float = 2.1
    num_subcarriers: int = 12
    subcarrier_spacing_kHz: int = 15
    channel_bandwidth_MHz: float = 20.0
    device_config_file: Optional[Path] = None
    position_config_file: Optional[Path] = 'drive\\position_config.json' #Put proper file location here.

    
    def __post_init__(self):
        #self.positions = self.load_position_config()
        self.devices=self.load_device_config()

    def load_position_config(self) -> dict:
        if isinstance(self.position_config_file, Path):
            with self.position_config_file.open(mode='r') as fid:
                return json.load(fid)
        else:
            return {}

    def load_device_config(self) -> dict:
        if isinstance(self.device_config_file, Path):
            with self.device_config_file.open(mode='r') as fid:
                return json.load(fid)
        else:
            return {}
