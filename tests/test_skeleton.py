"""
Starter tests for Mutation Shootout.
"""
import pytest, sys, os
from datetime import datetime
from billing import (
    price_with_tax, apply_coupon, compute_total, compute_subtotal,
    booking_fee, convert_currency, validate_coupon, split_payment,
    parse_iso_date, compute_refund, bulk_discount, compute_bulk_total,
    tax_breakdown, validate_tax_number, apply_dynamic_tax,
    loyalty_points_earned, apply_loyalty_discount, cap_price,
    round_money, is_weekend_rate
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestPriceWithTax:
    def test_positive_value(self):
        assert price_with_tax(100) == 121.0

    def test_zero_returns_zero(self):
        assert price_with_tax(0) == 0.0

    @pytest.mark.parametrize("negative", [-1.0, -100])
    def test_negative_raises(self, negative):
        with pytest.raises(ValueError):
            price_with_tax(negative)
    
    def test_negative_raises(self):
        with pytest.raises(ValueError) as exc:
            price_with_tax(-10)
        assert "net must be non‑negative" in str(exc.value)


class TestApplyCoupon:
    def test_valid_coupon(self):
        assert apply_coupon(100, "SPORT10") == 90.0

    def test_invalid_coupon(self):
        assert apply_coupon(100, "FAKE") == 100.0

    def test_none_coupon(self):
        assert apply_coupon(100, None) == 100.0

    def test_case_insensitive(self):
        assert apply_coupon(100, "sport10") == 90.0
    
    def test_newuser5_coupon(self):
        assert apply_coupon(100, "NEWUSER5") == 95.0
        assert apply_coupon(100, "newuser5") == 95.0


class TestComputeSubtotal:
    def test_normal(self):
        assert compute_subtotal(10, 3) == 30.0

    @pytest.mark.parametrize("qty", [0, -1])
    def test_invalid_qty(self, qty):
        with pytest.raises(ValueError):
            compute_subtotal(10, qty)


class TestBookingFee:
    def test_positive(self):
        assert booking_fee(3) == 1.5

    def test_zero(self):
        assert booking_fee(0) == 0.0


class TestComputeTotal:
    def test_no_coupon(self):
        total = compute_total(10, 2)
        assert total > 0

    def test_with_coupon(self):
        t1 = compute_total(10, 2, "SPORT10")
        t2 = compute_total(10, 2, None)
        assert t1 < t2


class TestValidateCoupon:
    def test_valid(self):
        assert validate_coupon("SPORT10")
        assert validate_coupon("sport10")

    def test_invalid(self):
        assert not validate_coupon("BADCODE")


class TestSplitPayment:
    def test_even(self):
        assert split_payment(10, 2) == [5.0, 5.0]

    def test_uneven(self):
        assert split_payment(10, 3) == [3.33, 3.33, 3.34]

    def test_zero_parts(self):
        with pytest.raises(ValueError):
            split_payment(10, 0)


class TestConvertCurrency:
    def test_usd(self):
        assert convert_currency(92, "USD") == 100.0

    def test_gbp(self):
        assert convert_currency(115, "GBP") == 100.0

    def test_eur(self):
        assert convert_currency(100, "EUR") == 100.0

    def test_unknown_currency(self):
        with pytest.raises(KeyError):
            convert_currency(100, "JPY")
    
    def test_convert_currency_usd(self):
        assert convert_currency(92, "USD") == 100.0
        assert convert_currency(9.2, "USD") == 10.0


class TestParseIsoDate:
    def test_iso_format(self):
        d = parse_iso_date("2024-06-08T12:30:00")
        assert isinstance(d, datetime)
        assert d.year == 2024 and d.month == 6 and d.day == 8


class TestComputeRefund:
    @pytest.mark.parametrize("pct,expected", [(1, 100.0), (0.5, 50.0), (0, 0.0)])
    def test_refund(self, pct, expected):
        assert compute_refund(100, pct) == expected

    @pytest.mark.parametrize("pct", [-0.1, 1.1])
    def test_invalid_pct(self, pct):
        with pytest.raises(ValueError):
            compute_refund(100, pct)


class TestBulkDiscount:
    def test_none(self):
        assert bulk_discount(5) == 0.0

    def test_8_percent(self):
        assert bulk_discount(10) == 0.08

    def test_15_percent(self):
        assert bulk_discount(20) == 0.15


class TestComputeBulkTotal:
    def test_discount_compare(self):
        total_9 = compute_bulk_total(10, 9)
        total_10 = compute_bulk_total(10, 10)
        total_20 = compute_bulk_total(10, 20)
        assert total_9 / 9 > total_10 / 10 > total_20 / 20
        assert total_9 < total_10 < total_20


class TestTaxBreakdown:
    def test_breakdown(self):
        net, tax = tax_breakdown(100)
        assert net == 100
        assert tax == 21.0


class TestValidateTaxNumber:
    def test_valid(self):
        assert validate_tax_number("LV1234567890")

    def test_invalid(self):
        assert not validate_tax_number("EE12345678901")
        assert not validate_tax_number("LV123")


class TestApplyDynamicTax:
    def test_lv(self):
        assert apply_dynamic_tax(100, "LV") == 121.0

    def test_other(self):
        assert apply_dynamic_tax(100, "EE") == 120.0


class TestLoyaltyPointsEarned:
    def test_points(self):
        assert loyalty_points_earned(100) == 2
        assert loyalty_points_earned(50) == 1


class TestApplyLoyaltyDiscount:
    def test_normal(self):
        assert apply_loyalty_discount(100, 100) == 99.0

    def test_cap_at_zero(self):
        assert apply_loyalty_discount(0.5, 100) == 0.0
    
    def test_apply_loyalty_discount_usual(self):
        assert apply_loyalty_discount(10.0, 100) == 9.0

    def test_apply_loyalty_discount_never_negative(self):
        assert apply_loyalty_discount(0.5, 100) == 0.0
    
    def test_apply_loyalty_discount_zero_points(self):
        assert apply_loyalty_discount(10.0, 0) == 10.0
    
    def test_apply_loyalty_discount_zero_gross(self):
        assert apply_loyalty_discount(0.0, 100) == 0.0


class TestCapPrice:
    def test_price_below_cap(self):
        assert cap_price(90, 100) == 90

    def test_price_above_cap(self):
        assert cap_price(110, 100) == 100


class TestRoundMoney:
    def test_default(self):
        assert round_money(1.234) == 1.23
        assert round_money(1.235) == 1.24

    def test_one_decimal(self):
        assert round_money(1.25, 1) == 1.3
        assert round_money(1.24, 1) == 1.2
        assert round_money(1.28, 1) == 1.3
    
    def test_round_down(self):
        assert round_money(1.234) == 1.23

    def test_round_up(self):
        assert round_money(1.235) == 1.24

    def test_round_one_decimal_down(self):
        assert round_money(1.24, 1) == 1.2

    def test_round_one_decimal_up(self):
        assert round_money(1.25, 1) == 1.3

    def test_zero(self):
        assert round_money(0.0) == 0.0


class TestIsWeekendRate:
    def test_weekday(self):
        assert not is_weekend_rate(datetime(2024, 6, 6))

    def test_saturday(self):
        assert is_weekend_rate(datetime(2024, 6, 8))

    def test_sunday(self):
        assert is_weekend_rate(datetime(2024, 6, 9))