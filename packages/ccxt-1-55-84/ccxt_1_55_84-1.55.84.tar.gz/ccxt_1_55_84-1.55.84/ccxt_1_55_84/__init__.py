# -*- coding: utf-8 -*-

"""CCXT: CryptoCurrency eXchange Trading Library"""

# MIT License
# Copyright (c) 2017 Igor Kroitor
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ----------------------------------------------------------------------------

__version__ = '1.55.84'

# ----------------------------------------------------------------------------

from ccxt_1_55_84.base.exchange import Exchange                     # noqa: F401
from ccxt_1_55_84.base.precise import Precise                       # noqa: F401

from ccxt_1_55_84.base.decimal_to_precision import decimal_to_precision  # noqa: F401
from ccxt_1_55_84.base.decimal_to_precision import TRUNCATE              # noqa: F401
from ccxt_1_55_84.base.decimal_to_precision import ROUND                 # noqa: F401
from ccxt_1_55_84.base.decimal_to_precision import DECIMAL_PLACES        # noqa: F401
from ccxt_1_55_84.base.decimal_to_precision import SIGNIFICANT_DIGITS    # noqa: F401
from ccxt_1_55_84.base.decimal_to_precision import TICK_SIZE             # noqa: F401
from ccxt_1_55_84.base.decimal_to_precision import NO_PADDING            # noqa: F401
from ccxt_1_55_84.base.decimal_to_precision import PAD_WITH_ZERO         # noqa: F401

from ccxt_1_55_84.base import errors
from ccxt_1_55_84.base.errors import BaseError                      # noqa: F401
from ccxt_1_55_84.base.errors import ExchangeError                  # noqa: F401
from ccxt_1_55_84.base.errors import AuthenticationError            # noqa: F401
from ccxt_1_55_84.base.errors import PermissionDenied               # noqa: F401
from ccxt_1_55_84.base.errors import AccountSuspended               # noqa: F401
from ccxt_1_55_84.base.errors import ArgumentsRequired              # noqa: F401
from ccxt_1_55_84.base.errors import BadRequest                     # noqa: F401
from ccxt_1_55_84.base.errors import BadSymbol                      # noqa: F401
from ccxt_1_55_84.base.errors import BadResponse                    # noqa: F401
from ccxt_1_55_84.base.errors import NullResponse                   # noqa: F401
from ccxt_1_55_84.base.errors import InsufficientFunds              # noqa: F401
from ccxt_1_55_84.base.errors import InvalidAddress                 # noqa: F401
from ccxt_1_55_84.base.errors import AddressPending                 # noqa: F401
from ccxt_1_55_84.base.errors import InvalidOrder                   # noqa: F401
from ccxt_1_55_84.base.errors import OrderNotFound                  # noqa: F401
from ccxt_1_55_84.base.errors import OrderNotCached                 # noqa: F401
from ccxt_1_55_84.base.errors import CancelPending                  # noqa: F401
from ccxt_1_55_84.base.errors import OrderImmediatelyFillable       # noqa: F401
from ccxt_1_55_84.base.errors import OrderNotFillable               # noqa: F401
from ccxt_1_55_84.base.errors import DuplicateOrderId               # noqa: F401
from ccxt_1_55_84.base.errors import NotSupported                   # noqa: F401
from ccxt_1_55_84.base.errors import NetworkError                   # noqa: F401
from ccxt_1_55_84.base.errors import DDoSProtection                 # noqa: F401
from ccxt_1_55_84.base.errors import RateLimitExceeded              # noqa: F401
from ccxt_1_55_84.base.errors import ExchangeNotAvailable           # noqa: F401
from ccxt_1_55_84.base.errors import OnMaintenance                  # noqa: F401
from ccxt_1_55_84.base.errors import InvalidNonce                   # noqa: F401
from ccxt_1_55_84.base.errors import RequestTimeout                 # noqa: F401
from ccxt_1_55_84.base.errors import error_hierarchy                # noqa: F401

from ccxt_1_55_84.aax import aax                                    # noqa: F401
from ccxt_1_55_84.aofex import aofex                                # noqa: F401
from ccxt_1_55_84.ascendex import ascendex                          # noqa: F401
from ccxt_1_55_84.bequant import bequant                            # noqa: F401
from ccxt_1_55_84.bibox import bibox                                # noqa: F401
from ccxt_1_55_84.bigone import bigone                              # noqa: F401
from ccxt_1_55_84.binance import binance                            # noqa: F401
from ccxt_1_55_84.binancecoinm import binancecoinm                  # noqa: F401
from ccxt_1_55_84.binanceus import binanceus                        # noqa: F401
from ccxt_1_55_84.binanceusdm import binanceusdm                    # noqa: F401
from ccxt_1_55_84.bit2c import bit2c                                # noqa: F401
from ccxt_1_55_84.bitbank import bitbank                            # noqa: F401
from ccxt_1_55_84.bitbay import bitbay                              # noqa: F401
from ccxt_1_55_84.bitbns import bitbns                              # noqa: F401
from ccxt_1_55_84.bitcoincom import bitcoincom                      # noqa: F401
from ccxt_1_55_84.bitfinex import bitfinex                          # noqa: F401
from ccxt_1_55_84.bitfinex2 import bitfinex2                        # noqa: F401
from ccxt_1_55_84.bitflyer import bitflyer                          # noqa: F401
from ccxt_1_55_84.bitforex import bitforex                          # noqa: F401
from ccxt_1_55_84.bitget import bitget                              # noqa: F401
from ccxt_1_55_84.bithumb import bithumb                            # noqa: F401
from ccxt_1_55_84.bitmart import bitmart                            # noqa: F401
from ccxt_1_55_84.bitmex import bitmex                              # noqa: F401
from ccxt_1_55_84.bitpanda import bitpanda                          # noqa: F401
from ccxt_1_55_84.bitso import bitso                                # noqa: F401
from ccxt_1_55_84.bitstamp import bitstamp                          # noqa: F401
from ccxt_1_55_84.bitstamp1 import bitstamp1                        # noqa: F401
from ccxt_1_55_84.bittrex import bittrex                            # noqa: F401
from ccxt_1_55_84.bitvavo import bitvavo                            # noqa: F401
from ccxt_1_55_84.bitz import bitz                                  # noqa: F401
from ccxt_1_55_84.bl3p import bl3p                                  # noqa: F401
from ccxt_1_55_84.braziliex import braziliex                        # noqa: F401
from ccxt_1_55_84.btcalpha import btcalpha                          # noqa: F401
from ccxt_1_55_84.btcbox import btcbox                              # noqa: F401
from ccxt_1_55_84.btcmarkets import btcmarkets                      # noqa: F401
from ccxt_1_55_84.btctradeua import btctradeua                      # noqa: F401
from ccxt_1_55_84.btcturk import btcturk                            # noqa: F401
from ccxt_1_55_84.buda import buda                                  # noqa: F401
from ccxt_1_55_84.bw import bw                                      # noqa: F401
from ccxt_1_55_84.bybit import bybit                                # noqa: F401
from ccxt_1_55_84.cdax import cdax                                  # noqa: F401
from ccxt_1_55_84.cex import cex                                    # noqa: F401
from ccxt_1_55_84.coinbase import coinbase                          # noqa: F401
from ccxt_1_55_84.coinbaseprime import coinbaseprime                # noqa: F401
from ccxt_1_55_84.coinbasepro import coinbasepro                    # noqa: F401
from ccxt_1_55_84.coincheck import coincheck                        # noqa: F401
from ccxt_1_55_84.coinegg import coinegg                            # noqa: F401
from ccxt_1_55_84.coinex import coinex                              # noqa: F401
from ccxt_1_55_84.coinfalcon import coinfalcon                      # noqa: F401
from ccxt_1_55_84.coinfloor import coinfloor                        # noqa: F401
from ccxt_1_55_84.coinmarketcap import coinmarketcap                # noqa: F401
from ccxt_1_55_84.coinmate import coinmate                          # noqa: F401
from ccxt_1_55_84.coinone import coinone                            # noqa: F401
from ccxt_1_55_84.coinspot import coinspot                          # noqa: F401
from ccxt_1_55_84.crex24 import crex24                              # noqa: F401
from ccxt_1_55_84.currencycom import currencycom                    # noqa: F401
from ccxt_1_55_84.delta import delta                                # noqa: F401
from ccxt_1_55_84.deribit import deribit                            # noqa: F401
from ccxt_1_55_84.digifinex import digifinex                        # noqa: F401
from ccxt_1_55_84.eqonex import eqonex                              # noqa: F401
from ccxt_1_55_84.equos import equos                                # noqa: F401
from ccxt_1_55_84.exmo import exmo                                  # noqa: F401
from ccxt_1_55_84.exx import exx                                    # noqa: F401
from ccxt_1_55_84.flowbtc import flowbtc                            # noqa: F401
from ccxt_1_55_84.ftx import ftx                                    # noqa: F401
from ccxt_1_55_84.gateio import gateio                              # noqa: F401
from ccxt_1_55_84.gemini import gemini                              # noqa: F401
from ccxt_1_55_84.hbtc import hbtc                                  # noqa: F401
from ccxt_1_55_84.hitbtc import hitbtc                              # noqa: F401
from ccxt_1_55_84.hollaex import hollaex                            # noqa: F401
from ccxt_1_55_84.huobi import huobi                                # noqa: F401
from ccxt_1_55_84.huobijp import huobijp                            # noqa: F401
from ccxt_1_55_84.huobipro import huobipro                          # noqa: F401
from ccxt_1_55_84.idex import idex                                  # noqa: F401
from ccxt_1_55_84.independentreserve import independentreserve      # noqa: F401
from ccxt_1_55_84.indodax import indodax                            # noqa: F401
from ccxt_1_55_84.itbit import itbit                                # noqa: F401
from ccxt_1_55_84.kraken import kraken                              # noqa: F401
from ccxt_1_55_84.kucoin import kucoin                              # noqa: F401
from ccxt_1_55_84.kuna import kuna                                  # noqa: F401
from ccxt_1_55_84.latoken import latoken                            # noqa: F401
from ccxt_1_55_84.lbank import lbank                                # noqa: F401
from ccxt_1_55_84.liquid import liquid                              # noqa: F401
from ccxt_1_55_84.luno import luno                                  # noqa: F401
from ccxt_1_55_84.lykke import lykke                                # noqa: F401
from ccxt_1_55_84.mercado import mercado                            # noqa: F401
from ccxt_1_55_84.mixcoins import mixcoins                          # noqa: F401
from ccxt_1_55_84.ndax import ndax                                  # noqa: F401
from ccxt_1_55_84.novadax import novadax                            # noqa: F401
from ccxt_1_55_84.oceanex import oceanex                            # noqa: F401
from ccxt_1_55_84.okcoin import okcoin                              # noqa: F401
from ccxt_1_55_84.okex import okex                                  # noqa: F401
from ccxt_1_55_84.okex3 import okex3                                # noqa: F401
from ccxt_1_55_84.okex5 import okex5                                # noqa: F401
from ccxt_1_55_84.paymium import paymium                            # noqa: F401
from ccxt_1_55_84.phemex import phemex                              # noqa: F401
from ccxt_1_55_84.poloniex import poloniex                          # noqa: F401
from ccxt_1_55_84.probit import probit                              # noqa: F401
from ccxt_1_55_84.qtrade import qtrade                              # noqa: F401
from ccxt_1_55_84.ripio import ripio                                # noqa: F401
from ccxt_1_55_84.stex import stex                                  # noqa: F401
from ccxt_1_55_84.therock import therock                            # noqa: F401
from ccxt_1_55_84.tidebit import tidebit                            # noqa: F401
from ccxt_1_55_84.tidex import tidex                                # noqa: F401
from ccxt_1_55_84.timex import timex                                # noqa: F401
from ccxt_1_55_84.upbit import upbit                                # noqa: F401
from ccxt_1_55_84.vcc import vcc                                    # noqa: F401
from ccxt_1_55_84.wavesexchange import wavesexchange                # noqa: F401
from ccxt_1_55_84.whitebit import whitebit                          # noqa: F401
from ccxt_1_55_84.xena import xena                                  # noqa: F401
from ccxt_1_55_84.yobit import yobit                                # noqa: F401
from ccxt_1_55_84.zaif import zaif                                  # noqa: F401
from ccxt_1_55_84.zb import zb                                      # noqa: F401

exchanges = [
    'aax',
    'aofex',
    'ascendex',
    'bequant',
    'bibox',
    'bigone',
    'binance',
    'binancecoinm',
    'binanceus',
    'binanceusdm',
    'bit2c',
    'bitbank',
    'bitbay',
    'bitbns',
    'bitcoincom',
    'bitfinex',
    'bitfinex2',
    'bitflyer',
    'bitforex',
    'bitget',
    'bithumb',
    'bitmart',
    'bitmex',
    'bitpanda',
    'bitso',
    'bitstamp',
    'bitstamp1',
    'bittrex',
    'bitvavo',
    'bitz',
    'bl3p',
    'braziliex',
    'btcalpha',
    'btcbox',
    'btcmarkets',
    'btctradeua',
    'btcturk',
    'buda',
    'bw',
    'bybit',
    'cdax',
    'cex',
    'coinbase',
    'coinbaseprime',
    'coinbasepro',
    'coincheck',
    'coinegg',
    'coinex',
    'coinfalcon',
    'coinfloor',
    'coinmarketcap',
    'coinmate',
    'coinone',
    'coinspot',
    'crex24',
    'currencycom',
    'delta',
    'deribit',
    'digifinex',
    'eqonex',
    'equos',
    'exmo',
    'exx',
    'flowbtc',
    'ftx',
    'gateio',
    'gemini',
    'hbtc',
    'hitbtc',
    'hollaex',
    'huobi',
    'huobijp',
    'huobipro',
    'idex',
    'independentreserve',
    'indodax',
    'itbit',
    'kraken',
    'kucoin',
    'kuna',
    'latoken',
    'lbank',
    'liquid',
    'luno',
    'lykke',
    'mercado',
    'mixcoins',
    'ndax',
    'novadax',
    'oceanex',
    'okcoin',
    'okex',
    'okex3',
    'okex5',
    'paymium',
    'phemex',
    'poloniex',
    'probit',
    'qtrade',
    'ripio',
    'stex',
    'therock',
    'tidebit',
    'tidex',
    'timex',
    'upbit',
    'vcc',
    'wavesexchange',
    'whitebit',
    'xena',
    'yobit',
    'zaif',
    'zb',
]

base = [
    'Exchange',
    'Precise',
    'exchanges',
    'decimal_to_precision',
]

__all__ = base + errors.__all__ + exchanges
