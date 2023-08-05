from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from ctlml_commons.entity.execution_type import ExecutionType
from ctlml_commons.entity.order import OrderType
from ctlml_commons.util.date_utils import convert_dates, datetime_to_str
from ctlml_commons.util.num_utils import convert_floats


@dataclass
class Execution:
    id: str
    brokerage_id: str
    investor: str
    symbol: str
    execution_type: ExecutionType
    order_type: OrderType
    shares: float
    bid_price: float
    purchase_price: float
    sell_price: float
    profit_loss: float
    notes: str
    strategy: str
    time: datetime

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = deepcopy(self.__dict__)

        data["execution_type"] = self.execution_type.value()
        data["order_type"] = self.order_type.value()
        data["time"] = datetime_to_str(self.time)

        return data

    @classmethod
    def deserialize(cls, input_data: Dict[str, Any]) -> Execution:
        return Execution(**cls.clean(input_data=input_data))

    @classmethod
    def clean(cls, input_data: Dict[str, Any]) -> Dict[str, Any]:
        data = deepcopy(input_data)

        data["execution_type"] = ExecutionType.to_enum(data["execution_type"])
        data["order_type"] = OrderType.to_enum(data["order_type"])

        data = convert_floats(data, ["bid_price", "profit_loss", "purchase_price", "sell_price", "shares"])
        data = convert_dates(data, "time")

        return data
