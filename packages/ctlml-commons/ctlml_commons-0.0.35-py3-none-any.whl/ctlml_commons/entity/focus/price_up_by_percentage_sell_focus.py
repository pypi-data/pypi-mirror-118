from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from logging import Logger
from typing import Any, Dict, List, Tuple

from ctlml_commons.entity.candle import Candle
from ctlml_commons.entity.focus.focus import Focus
from ctlml_commons.entity.focus.focus_plugins import FocusPlugins
from ctlml_commons.entity.lot import Lot
from ctlml_commons.entity.news import News
from ctlml_commons.entity.range_window import RangeWindow


@dataclass(frozen=True)
class PriceUpBuyPercentageSellFocus(Focus):
    """Price up buy and percentage change sell based investment strategy."""

    """Number of up periods to consider for buy decisions"""
    num_periods: int

    """Percentage up per share total to decide to sell"""
    percentage_window: RangeWindow

    """If should sell at the end of day"""
    sell_at_end_of_day: bool

    def evaluate_buy(
        self, symbol: str, news: List[News], current_price: float, candles: Dict[str, Candle], logger: Logger
    ) -> Tuple[bool, str]:
        return FocusPlugins.should_buy_price_wise(
            current_price=current_price,
            candles=candles,
            num_periods=self.num_periods,
            logger=logger,
        )

    def evaluate_sell(
        self, lot: Lot, news: List[News], current_price: float, candles: Dict[str, Candle], logger: Logger
    ) -> Tuple[bool, str]:
        return FocusPlugins.should_sell_percentage_wise(
            lot=lot,
            current_price=current_price,
            percentage_window=self.percentage_window,
            logger=logger,
        )

    def serialize(self) -> Dict[str, Any]:
        data = deepcopy(self.__dict__)
        data["percentage_window"] = self.percentage_window.serialize()
        data["focus_type"] = self.__class__.__name__
        return data

    @classmethod
    def deserialize(cls, input_data: Dict[str, Any]) -> PriceUpBuyPercentageSellFocus:
        data = deepcopy(input_data)

        del data["focus_type"]
        data["num_periods"] = int(data["num_periods"])
        data["percentage_window"] = RangeWindow.deserialize(data["percentage_window"])

        return cls(**data)
