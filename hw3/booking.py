import random
import string
import smtplib


def calc_price(base_price: float, discount: float, count: int) -> float:
    if discount < 0 or discount > 100:
        raise ValueError("Discount must be between 0 and 100")
    if count <= 0:
        raise ValueError("Count must be a positive integer")
    total = base_price * count * (1 - discount / 100)
    return round(total, 2)


def check_availability(event_id: int, seats_requested: int) -> bool:
    if seats_requested <= 0:
        raise ValueError("Seats requested must be positive")
    available_seats = get_available_seats(event_id)  # Assume external call
    return available_seats >= seats_requested


def apply_promo_code(order_id: int, promo_code: str) -> bool:
    if not is_promo_valid(promo_code):
        return False
    if is_promo_limit_reached(promo_code):
        return False
    apply_promo_to_order(order_id, promo_code)
    return True


def generate_booking_ref(user_id: int, event_id: int) -> str:
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"BOOK-{user_id}-{event_id}-{suffix}"


def send_notification_email(email: str, booking_details: dict) -> bool:
    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login("user", "password")
            message = f"Subject: Booking Confirmation\n\nDetails: {booking_details}"
            server.sendmail("noreply@example.com", email, message)
        return True
    except Exception:
        return False



def get_available_seats(event_id: int) -> int:
    pass  # Implemented externally


def is_promo_valid(promo_code: str) -> bool:
    pass  # Implemented externally


def is_promo_limit_reached(promo_code: str) -> bool:
    pass  # Implemented externally


def apply_promo_to_order(order_id: int, promo_code: str) -> None:
    pass  # Implemented externally