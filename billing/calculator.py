"""
billing.calculator
"""

from __future__ import annotations
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Tuple, Dict

TAX_RATE: float = 0.21
BOOKING_FEE_PER_TICKET: float = 0.50
LOYALTY_POINT_RATE: float = 0.02

SUPPORTED_CURRENCIES: Dict[str, float] = {
    "EUR": 1.0,
    "USD": 0.92,
    "GBP": 1.15,
}

COUPON_CODES: Dict[str, float] = {
    "SPORT10": 0.10,
    "NEWUSER5": 0.05,
    "BLACKFRIDAY": 0.25,
}


def _round(value: float) -> float:
    return float(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def price_with_tax(net: float) -> float:
    if net < 0:
        raise ValueError("net must be non‑negative")
    return _round(net * (1 + TAX_RATE))


def apply_coupon(gross: float, coupon: str | None = None) -> float:
    disc = COUPON_CODES.get(coupon.upper() if coupon else "", 0.0)
    return _round(gross * (1 - disc))


def compute_subtotal(unit_price: float, qty: int) -> float:
    if qty <= 0:
        raise ValueError("qty must be positive")
    return _round(unit_price * qty)


def booking_fee(qty: int) -> float:
    return _round(BOOKING_FEE_PER_TICKET * qty)


def compute_total(unit_price: float, qty: int, coupon: str | None = None) -> float:
    subtotal = compute_subtotal(unit_price, qty)
    gross = price_with_tax(subtotal + booking_fee(qty))
    return apply_coupon(gross, coupon)


def validate_coupon(code: str) -> bool:
    return code.upper() in COUPON_CODES


def split_payment(total: float, parts: int) -> List[float]:
    if parts <= 0:
        raise ValueError("parts must be > 0")
    part = _round(total / parts)
    amounts = [part] * parts
    diff = _round(total - sum(amounts))
    amounts[-1] = _round(amounts[-1] + diff)
    return amounts


def convert_currency(amount_eur: float, to: str) -> float:
    rate = SUPPORTED_CURRENCIES.get(to.upper())
    if rate is None:
        raise KeyError(f"Unsupported currency {to}")
    return _round(amount_eur / rate)


def parse_iso_date(date_str: str) -> datetime:
    return datetime.fromisoformat(date_str)


def compute_refund(total_paid: float, percentage: float) -> float:
    if not 0 <= percentage <= 1:
        raise ValueError("percentage 0..1")
    return _round(total_paid * percentage)


def bulk_discount(qty: int) -> float:
    if qty >= 20:
        return 0.15
    elif qty >= 10:
        return 0.08
    return 0.0


def compute_bulk_total(unit_price: float, qty: int) -> float:
    subtotal = compute_subtotal(unit_price, qty)
    discount = bulk_discount(qty)
    subtotal = _round(subtotal * (1 - discount))
    return price_with_tax(subtotal)


def tax_breakdown(net: float) -> Tuple[float, float]:
    tax = _round(net * TAX_RATE)
    return net, tax


def validate_tax_number(tax_num: str) -> bool:
    return tax_num.startswith("LV") and len(tax_num) == 12


def apply_dynamic_tax(net: float, country: str) -> float:
    rate = 0.21 if country.upper() == "LV" else 0.20
    return _round(net * (1 + rate))


def loyalty_points_earned(net: float) -> int:
    return int(net * LOYALTY_POINT_RATE)


def apply_loyalty_discount(gross: float, points: int) -> float:
    discount = _round(points * 0.01)  # every point = 1 cent
    return max(0.0, _round(gross - discount))


def cap_price(price: float, cap: float) -> float:
    return min(price, cap)


def round_money(value: float, decimals: int = 2) -> float:
    return float(Decimal(str(value)).quantize(Decimal((0, (1,), -decimals)), rounding=ROUND_HALF_UP))


def is_weekend_rate(date: datetime) -> bool:
    return date.weekday() >= 5
