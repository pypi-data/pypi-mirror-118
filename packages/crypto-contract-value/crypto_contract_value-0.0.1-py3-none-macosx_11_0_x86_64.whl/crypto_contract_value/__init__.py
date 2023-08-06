from enum import IntEnum

from crypto_contract_value._lowlevel import ffi, lib


class MarketType(IntEnum):
    '''Market type.'''
    spot = lib.Spot
    linear_future = lib.LinearFuture
    inverse_future = lib.InverseFuture
    linear_swap = lib.LinearSwap
    inverse_swap = lib.InverseSwap

    american_option = lib.AmericanOption
    european_option = lib.EuropeanOption

    quanto_future = lib.QuantoFuture
    quanto_swap = lib.QuantoSwap

    move = lib.Move
    bvol = lib.BVOL


def get_contract_value(
    exchange: str,
    market_type: MarketType,
    pair: str
) -> float:
    return lib.get_contract_value(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char[]", pair.encode("utf-8")),
    )
