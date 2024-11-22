from datetime import datetime
from typing import List

# 1. Мероприятие
class Event:
    def __init__(self, name: str, date_time: datetime, venue: 'Venue'):
        self.name = name
        self.date_time = date_time  # время проведения
        self.venue = venue  # место проведения

# 2. Место проведения
class Venue:
    def __init__(self, name: str, place: str, capacity: int):
        self.name = name
        self.place = place
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity  # вместимость
        self.seats: List['Seat'] = []  # список мест

# 3. Место (на мероприятии)
class Seat:
    def __init__(self, row: int, number: int):
        self.row = row
        self.number = number
        self.is_available = True  # доступность

# 4. Билет
class Ticket:
    def __init__(self, event: 'Event', seat: 'Seat', category: 'Category'):
        self.event = event
        self.seat = seat
        self.category = category

    def book(self):  # функция для бронирования
        if self.seat.is_available:
            print(f'Seat {self.seat.row}-{self.seat.number} is booked')
            self.seat.is_available = False
        else:
            raise ValueError("Seat is already booked")

# 5. Категория
class Category:
    def __init__(self, name: str, price_multiplier: float):
        self.name = name
        self.price_multiplier = price_multiplier

# 6. Пользователь
class User:
    def __init__(self, user_name: str, email: str):
        self.name = user_name
        self.email = email

# 7. Заказ
class Order:
    def __init__(self, user: 'User', tickets: List['Ticket'] = []):
        self.user = user
        self.tickets = tickets
        self.is_paid = False

    def calculate_total_price(self) -> float:
        return sum(ticket.category.price_multiplier for ticket in self.tickets)

    def pay(self):
        if self.is_paid:
            raise ValueError("Order is already paid")
        self.is_paid = True

# 8. Оплата
class Payment:
    def __init__(self, order: Order, amount: float):
        self.order = order
        self.amount = amount
        self.is_successful = False
        self.payment_date = None

    def apply_discount(self, discount: 'Discount'):
        self.amount -= discount.apply(self.amount)

    def process(self):
        if self.amount < self.order.calculate_total_price():
            raise ValueError("Insufficient payment")
        self.is_successful = True
        self.payment_date = datetime.now()
        self.order.pay()

# 9. Скидка
class Discount:
    def __init__(self, code: str, percentage: float):
        self.code = code
        self.percentage = percentage

    def apply(self, total_price: float) -> float:
        return total_price * (self.percentage / 100)

# 10. Отзыв
class Feedback:
    def __init__(self, user: User, event: Event):
        self.user = user
        self.event = event
        self.rating = None
        self.comment = None

    def set_rating(self, rating: int):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self.rating = rating

    def set_comment(self, comment: str):
        self.comment = comment

    def __str__(self):
        return f"Feedback by {self.user.name} for {self.event.name} - Rating: {self.rating}, Comment: {self.comment or 'No comment'}"
