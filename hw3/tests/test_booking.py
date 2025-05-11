import pytest
from hw3.booking import (
    calc_price,
    check_availability,
    apply_promo_code,
    generate_booking_ref,
    send_notification_email,
)


@pytest.mark.parametrize("base, discount, count, expected", [
    (100, 10, 2, 180.0),
    (50, 100, 1, 0.0),
])
def test_calc_price_positive(base, discount, count, expected):
    assert calc_price(base, discount, count) == expected


@pytest.mark.parametrize("base, discount, count", [
    (100, -5, 2),
    (100, 110, 1),
    (50, 20, 0),
    (30, 10, -1),
])
def test_calc_price_negative(base, discount, count):
    with pytest.raises(ValueError):
        calc_price(base, discount, count)


@pytest.mark.parametrize("available, requested, expected", [
    (10, 5, True),
    (5, 5, True),
])
def test_check_availability_enough(mocker, available, requested, expected):
    mocker.patch('booking.get_available_seats', return_value=available)
    assert check_availability(1, requested) == expected


@pytest.mark.parametrize("available, requested", [
    (3, 5),
    (0, 1),
])
def test_check_availability_not_enough(mocker, available, requested):
    mocker.patch('booking.get_available_seats', return_value=available)
    assert not check_availability(1, requested)


def test_check_availability_invalid_seats(mocker):
    mocker.patch('booking.get_available_seats', return_value=10)
    with pytest.raises(ValueError):
        check_availability(1, 0)
    with pytest.raises(ValueError):
        check_availability(1, -2)


@pytest.mark.parametrize("is_valid, is_limit, expected", [
    (True, False, True),
    (True, True, False),
    (False, False, False),
])
def test_apply_promo_code(mocker, is_valid, is_limit, expected):
    mocker.patch('booking.is_promo_valid', return_value=is_valid)
    mocker.patch('booking.is_promo_limit_reached', return_value=is_limit)
    assert apply_promo_code(123, 'TESTCODE') == expected


def test_generate_booking_ref_format():
    user_id = 123
    event_id = 456
    ref = generate_booking_ref(user_id, event_id)
    prefix = f"BOOK-{user_id}-{event_id}-"
    assert ref.startswith(prefix)
    assert len(ref) == len(prefix) + 6


def test_generate_booking_ref_unique():
    refs = {generate_booking_ref(1, 1) for _ in range(100)}
    assert len(refs) == 100  # All refs should be unique


def test_send_notification_email_success(mocker):
    mocker.patch('smtplib.SMTP')
    assert send_notification_email('test@example.com', {}) is True


def test_send_notification_email_failure(mocker):
    mocker.patch('smtplib.SMTP', side_effect=Exception('Connection error'))
    assert send_notification_email('test@example.com', {}) is False