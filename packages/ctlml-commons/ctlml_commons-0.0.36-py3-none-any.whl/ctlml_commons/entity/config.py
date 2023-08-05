from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, Tuple

from ctlml_commons.util.entity_utils import separate_fields
from ctlml_commons.util.num_utils import convert_floats


@dataclass(frozen=True)
class Config:
    email: str
    users_key: str
    delimiter: str
    testing: bool
    debug: bool
    f_it_mode: bool
    profile_info: bool
    buy_one_sell_one_mode: bool
    window_length: int
    window_secs: int
    random_investors: int
    error_sleep_time_sec: int
    storage_bucket: str
    total_loss_threshold: float = -2000
    update_candidate_tickers_in_sec: int = 60 * 3  # 3 minutes
    max_order_wait_attempts: int = 50
    wash_sale_protection_enabled: bool = True
    dirs: Dict[str, str] = field(default_factory=dict)
    queues: Dict[str, str] = field(default_factory=dict)
    urls: Dict[str, str] = field(default_factory=dict)
    other: Dict[str, str] = field(default_factory=dict)

    def serialize(self) -> Dict[str, Any]:
        return deepcopy(self.__dict__)

    @classmethod
    def deserialize(cls, input_data: Dict[str, Any]) -> Config:
        known, other = cls.separate(input_data=input_data)

        return cls(**Config.clean(input_data=known), other=other)

    @classmethod
    def clean(cls, input_data: Dict[str, Any]) -> Dict[str, Any]:
        data: Dict[str, Any] = convert_floats(input_data, ["total_loss_threshold"])

        for field in [
            "window_length",
            "window_secs",
            "random_investors",
            "error_sleep_time_sec",
            "update_candidate_tickers_in_sec",
            "max_order_wait_attempts",
        ]:
            data[field] = int(data[field])

        return data

    @classmethod
    def separate(cls, input_data: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        return separate_fields(known_fields=cls.__dataclass_fields__.keys(), input_data=input_data)
