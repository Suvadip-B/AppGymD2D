from math import log2
from typing import Dict, Tuple
import json

from .actions import Actions
from .conversion import dB_to_linear, linear_to_dB
from .device import BaseStation, UserEquipment
from .devices import Devices
from .envs.env_config import EnvConfig
from .id import Id
from .path_loss import PathLoss
from .position import get_random_position_nearby, get_random_position, Position
from .traffic_model import TrafficModel
from .device_types import randomize, write_to_json, Device_to_json


BASE_STATION_ID = Id('mbs')


def create_devices(num_grps:int, d_lst: list, c_lst: list, config: EnvConfig) -> Devices:
    """Initialise devices: BSs, CUEs & DUE pairs as per the env config.

    :param config: The environment's configuration.
    :returns: A dataclass containing BSs, CUEs, and DUE pairs.
    """

    base_cfg = {
        'num_subcarriers': config.num_subcarriers,
        'subcarrier_spacing_kHz': config.subcarrier_spacing_kHz,
    }
    default_cue_cfg = {**base_cfg, **{'max_tx_power_dBm': config.cue_max_tx_power_dBm}}
    default_due_cfg = {**base_cfg, **{'max_tx_power_dBm': config.due_max_tx_power_dBm}}
    get_config = lambda id_, default_cfg: config.devices.get(id_, {}).get('config', default_cfg)

    # create macro base station
    bs = BaseStation(Id(BASE_STATION_ID), get_config(BASE_STATION_ID, base_cfg))

    # create cellular UEs
    cues = {}
    #val=config.load_device_config()
    #num_cues=int(val['num_cues'])
    #print("Cell users: ", c_lst)
    for j in range(num_grps):
        for i in c_lst[j]:
            #print("Yes")
            cue_id = Id(f'cue{i:03d}')
            cues[cue_id] = UserEquipment(cue_id, get_config(cue_id, default_cue_cfg))


    # create D2D UE pairs
    dues = {}
    #val=config.load_device_config()
    #num_due_pairs=int(val['num_due_pairs'])
    #print("Due pairs: ",d_lst)
    for j in range(num_grps):
        for i in range(0, int(len(d_lst[j])), 2):
            due_tx_id, due_rx_id = "due"+f'{d_lst[j][i]:03d}', "due"+f'{d_lst[j][i+1]:03d}'
            #print("In create devices: ", due_tx_id, due_rx_id)
        #due_tx_id, due_rx_id = Id(f'due{i:02d}'), Id(f'due{i + 1:02d}')
            due_tx = UserEquipment(due_tx_id, get_config(due_tx_id, default_due_cfg))
            due_rx = UserEquipment(due_rx_id, get_config(due_rx_id, default_due_cfg))
            dues[(due_tx.id, due_rx.id)] = due_tx, due_rx

    return Devices(bs, cues, dues)

def load_position_config(position_config_file) -> dict:
    with open(position_config_file, mode='r') as fid:
        return json.load(fid)

class Simulator:
    def __init__(self, env_config: dict) -> None:
        super().__init__()
        self.config = EnvConfig(**env_config)
        #val=
        num_cues=self.config.num_cues
        num_due_pairs=self.config.num_due_pairs
        num_grps=self.config.num_grps
        self.total_devices=num_cues+num_due_pairs*2
        num_cues_grp, num_due_pairs_grp = randomize(self.total_devices, num_grps)      #in each group
        #print("cues: ", num_cues_grp, "dues: ", num_due_pairs_grp)
        self.due_list, self.cue_list=write_to_json(num_cues_grp, num_due_pairs_grp, self.total_devices)
        print(self.due_list, self.cue_list)
        self.devices: Devices = create_devices(num_grps, self.due_list, self.cue_list, self.config)
        self.traffic_model: TrafficModel = self.config.traffic_model(self.config.num_rbs)
        self.path_loss: PathLoss = self.config.path_loss_model(self.config.carrier_freq_GHz)
        #print("position file", self.config.position_config_file)
        self.types = Device_to_json('./sorted_rpgm_180.tr', self.config.position_config_file, self.cue_list, self.due_list)
        

    def reset(self) -> None:
        self.types._truncate()
        self.types.append_to_json()
        self.positions=self.config.load_position_config()
        #print(self.positions)
        
        for device in self.devices.values():
            if device.id == BASE_STATION_ID:
                pos = Position(100, 100)  # assume MBS fixed at (0,0) and everything else builds around it
            elif device.id in self.config.devices:
                pos = Position(*self.positions[device.id]['position'])
                print("not here")
                self.types._truncate()
            elif any(device.id in d for d in [self.devices.cues, self.devices.due_pairs]):
                val=int(device.id[-3:])
                #print("Device ID: ",device.id, "val: ", val)
                pos = Position(*self.positions[val][device.id]['position'])
                pos.x, pos.y = float(pos.x), float(pos.y)
                #print("here")
            elif device.id in self.devices.due_pairs_inv:
                due_tx_id = self.devices.due_pairs_inv[device.id]
                due_tx = self.devices[due_tx_id]
                #print("DUE Tx: ", due_tx_id)
                val=int(due_tx_id[-3:])
                pos = Position(*self.positions[val][due_tx_id]['position'])
                pos.x, pos.y = float(pos.x), float(pos.y)
                #get_random_position_nearby(self.config.cell_radius_m, due_tx.position, self.config.d2d_radius_m)
            else:
                raise ValueError(f'Invalid configuration for device "{device.id}".')
            device.set_position(pos)

    def step(self, actions: Actions) -> dict:
        # self.channels = self.traffic_model.get_traffic(self.devices)
        sinrs_db = self._calculate_sinrs(actions)
        capacities = self._calculate_network_capacity(sinrs_db)

        return {
            'sinrs_db': sinrs_db,
            'snrs_db': self._calculate_snrs(actions),
            'rate_bps': self._calculate_rates(sinrs_db),
            'capacity_mbps': capacities,
        }

    def _calculate_sinrs(self, actions: Actions) -> Dict[Tuple[Id, Id], float]:
        sinrs_db = {}
        for (tx_id, rx_id), action in actions.items():
            tx, rx = action.tx, action.rx
            rx_pwr_dBm = rx.rx_signal_level_dBm(tx.eirp_dBm(action.tx_pwr_dBm), self.path_loss(tx, rx))

            ix_actions = actions.get_actions_by_rb(action.rb).difference({action})
            sum_ix_pwr_mW = 0.0
            for ix_action in ix_actions:
                ix_tx = ix_action.tx
                ix_eirp_dBm = ix_tx.eirp_dBm(ix_action.tx_pwr_dBm)
                ix_path_loss_dB = self.path_loss(ix_tx, rx)
                sum_ix_pwr_mW += dB_to_linear(ix_eirp_dBm - ix_path_loss_dB)

            # noise_mW = dB_to_linear(rx.thermal_noise_dBm)  # @todo this can be memoized
            # ix_and_noise_mW = sum_ix_pwr_mW + noise_mW
            # sinrs_db[(tx_id, rx_id)] = rx_pwr_dBm - linear_to_dB(ix_and_noise_mW)
            sinrs_db[(tx_id, rx_id)] = \
                float(rx_pwr_dBm - linear_to_dB(sum_ix_pwr_mW + dB_to_linear(rx.thermal_noise_dBm)))
        return sinrs_db

    def _calculate_snrs(self, actions: Actions) -> Dict[Tuple[Id, Id], float]:
        SNRs_dB = {}
        for ids, action in actions.items():
            tx, rx = action.tx, action.rx
            rx_pwr_dBm = rx.rx_signal_level_dBm(tx.eirp_dBm(action.tx_pwr_dBm), self.path_loss(tx, rx))
            SNRs_dB[ids] = float(rx_pwr_dBm - rx.thermal_noise_dBm)
        return SNRs_dB

    def _calculate_rates(self, sinrs_db: Dict[Tuple[Id, Id], float]) -> Dict[Tuple[Id, Id], float]:
        rates_bps = {}
        for (tx_id, rx_id), sinr_db in sinrs_db.items():
            _, rx = self.devices[tx_id], self.devices[rx_id]
            # max_path_loss_dB = rx.max_path_loss_dB(tx.eirp_dBm())
            if sinr_db > rx.rx_sensitivity_dBm:
                rates_bps[(tx_id, rx_id)] = float(log2(1 + dB_to_linear(sinr_db)))
            else:
                rates_bps[(tx_id, rx_id)] = 0.0
        return rates_bps

    def _calculate_throughput_lte(self, sinrs_db: Dict[Tuple[Id, Id], float]) -> Dict[Tuple[Id, Id], float]:
        capacities = {}
        num_rbs = 100  # 100RBs @ 20MHz channel bandwidth
        num_re = 12 * 7 * 2  # num_subcarriers * num_symbols (short CP) * num_slots/subframe
        for (tx_id, rx_id), sinr_dB in sinrs_db.items():
            _, rx = self.devices[tx_id], self.devices[rx_id]
            if sinr_dB > rx.rx_sensitivity_dBm:
                num_bits = 6  # 64QAM
                capacity_b_per_ms = num_rbs * num_re * num_bits
                capacity_mbps = capacity_b_per_ms / 1000
                capacities[(tx_id, rx_id)] = capacity_mbps
            else:
                capacities[(tx_id, rx_id)] = 0
        return capacities

    def _calculate_network_capacity(self, sinrs_db: Dict[Tuple[Id, Id], float]) -> Dict[Tuple[Id, Id], float]:
        capacities_mbps = {}
        for (tx_id, rx_id), sinr_db in sinrs_db.items():
            tx, rx = self.devices[tx_id], self.devices[rx_id]
            # max_path_loss_dB = rx.max_path_loss_dB(tx.eirp_dBm())
            if sinr_db > rx.rx_sensitivity_dBm:
                b = tx.rb_bandwidth_kHz * 1000
                capacities_mbps[(tx_id, rx_id)] = float(1e-6 * b * log2(1 + dB_to_linear(sinr_db)))
            else:
                capacities_mbps[(tx_id, rx_id)] = 0.0
        return capacities_mbps
