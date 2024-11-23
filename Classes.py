from datetime import datetime
from typing import List, Optional
import json
from xml.etree import ElementTree as ET

# 1. Мероприятие
class Event:
    def __init__(self, name: str, date_time: datetime, venue: 'Venue'):
        self.name = name
        self.date_time = date_time  # время проведения
        self.venue = venue  # место проведения

    def to_json(self):
        return {
            'name': self.name,
            #для сериализации формата datetime нужна команда self.date_time.isoformat
            'date_time': self.date_time.isoformat() if self.date_time else None,
            #т.к. содержит Venue надо и для него написать функцию сериализации
            'venue': self.venue.to_json() if self.venue else None  # Сериализация venue
        }  
       
    @staticmethod
    def from_json(js):
        name = js['name']
        #снова какие-то выкрутасы с date_time(сначала получаем строку, потом преобразуем в формат datetime)
        date_time_str = js.get('date_time')  
        date_time = datetime.fromisoformat(date_time_str) if date_time_str else None  # Преобразуем в datetime
        venue = Venue.from_json(js.get('venue')) if js.get('venue') else None     #ну тут просто функция вызываем
        return Event (name, date_time, venue)

    def to_xml(self) -> ET.Element:
        event_elem = ET.Element("Event")
        ET.SubElement(event_elem, "Name").text = self.name
        ET.SubElement(event_elem, "DateTime").text = self.date_time.isoformat() if self.date_time else None #снова в ISO формат
        if self.venue:
            event_elem.append(self.venue.to_xml())
        return event_elem
    
    @staticmethod
    def from_xml(elem: ET.Element) -> 'Event':
        name = elem.find("Name").text
        date_time_str = elem.find("DateTime").text
        date_time = datetime.fromisoformat(date_time_str) if date_time_str else None
        venue_elem = elem.find("Venue")
        venue = Venue.from_xml(venue_elem) if venue_elem is not None else None
        return Event(name, date_time, venue)

# 2. Место проведения
class Venue:
    def __init__(self, name: str, place: str, capacity: int, seats: Optional[List['Seat']] = None):
        self.name = name
        self.place = place
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity  # вместимость
        self.seats: List['Seat'] = seats if seats else []# список мест

    def to_json(self):
        return {
            'name' : self.name,
            'place' : self.place,            
            'capacity' :  self.capacity,
            #аааааа, опять содежит список мест, снова писать def to_json
            'seats': [seat.to_json() for seat in self.seats]  # Список мест
        }
    
    @staticmethod
    def from_json(js):
        name = js['name']
        place = js['place']
        capacity = js['capacity']
        #десериализация листа
        seats = Seat.from_json_list(js['seats'])
        return Venue(name, place, capacity, seats )
    
    def to_xml(self) -> ET.Element:
        venue_elem = ET.Element("Venue")
        ET.SubElement(venue_elem, "Name").text = self.name
        ET.SubElement(venue_elem, "Place").text = self.place
        ET.SubElement(venue_elem, "Capacity").text = str(self.capacity)
        seats_elem = ET.SubElement(venue_elem, "Seats")     #опять список(ну и зчем делал с ивентом сериализацию :((((((
        for seat in self.seats:
            seats_elem.append(seat.to_xml())
        return venue_elem
    
    @staticmethod
    def from_xml(elem: ET.Element) -> 'Venue':
        name = elem.find("Name").text
        place = elem.find("Place").text
        capacity = int(elem.find("Capacity").text)
        seats_elem = elem.find("Seats")
        seats = [Seat.from_xml(seat_elem) for seat_elem in seats_elem] if seats_elem is not None else []
        return Venue(name, place, capacity, seats)

# 3. Место (на мероприятии)
class Seat:
    def __init__(self, row: int, number: int, is_avaible : bool = True):
        self.row = row
        self.number = number
        self.is_available = is_avaible 

    def to_json(self):
        return {
        'row' : self.row,
        'number' : self.number,
        'is_avaible' : self.is_available,
    }
    
    @staticmethod
    def from_json(js):
        row = js['row']
        number = js['number']
        is_avaible = js['is_avaible']

        return Seat(row, number, is_avaible )
    
    #для листа отдельную функцию
    @staticmethod
    def from_json_list(json_list):
        #Десериализация списка объектов
        return [Seat.from_json(item) for item in json_list]
    
    def to_xml(self) -> ET.Element:
        seat_elem = ET.Element("Seat")
        ET.SubElement(seat_elem, "Row").text = str(self.row)
        ET.SubElement(seat_elem, "Number").text = str(self.number)
        ET.SubElement(seat_elem, "IsAvailable").text = str(self.is_available)
        return seat_elem
    
    @staticmethod
    def from_xml(elem: ET.Element) -> 'Seat':
        row = int(elem.find("Row").text)
        number = int(elem.find("Number").text)
        is_available = elem.find("IsAvailable").text.lower() == "true"
        return Seat(row, number, is_available)

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
    

#CRUD для ивентов

class EventsManager:
    """Класс для управления CRUD-операциями с объектами Event"""

    def __init__(self):
        self.events_list = []
        self.current_id = 1  # Счетчик для уникальных идентификаторов

    def create(self, name: str, datetime: datetime, venue: Venue):
        """Создает и добавляет новое мероприятие в список"""
        event = Event(name=name, date_time=datetime, venue=venue)
        event.id = self.current_id  # Добавляем уникальный идентификатор
        self.events_list.append(event)  # Добавляем сам объект события
        self.current_id += 1
        return event

    def read_all(self):
        """Возвращает список всех сероприятий"""
        return self.events_list

    def read_by_id(self, event_id):
        """Возвращает мероприятие по его ID"""
        for event in self.events_list:
            if event.id == event_id:
                return event
        return None

    def update(self, event_id: int, name: str = None, date_time: datetime = None, venue: Venue = None):
        """Обновляет данные о мероприятии по его ID"""
        event = self.read_by_id(event_id)
        if event:
            if name is not None:
                event.name = name
            if date_time is not None:
                event.date_time = date_time
            if venue is not None:
                event.venue = venue
            return event
        return None

    def delete(self, event_id):
        """Удаляет мероприятие по его ID"""
        event = self.read_by_id(event_id)
        if event:
            self.events_list.remove(event)
            return f"Event with id {event_id} has been deleted."
        return "Event not found."


manager = EventsManager()

# Считывание и запись данных в формате JSON
def save_to_json(obj, filename: str):
    """Сохраняет объект в файл в формате JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)


def load_from_json(filename: str):
    """Загружает данные из файла JSON и возвращает объект"""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Пытаемся восстановить объект из JSON
        return Event.from_json(data)


# Считывание и запись данных в формате XML
def save_to_xml(obj, filename: str):
    """Сохраняет объект в файл в формате XML"""
    tree = ET.ElementTree(obj.to_xml())
    tree.write(filename, encoding='utf-8', xml_declaration=True)


def load_from_xml(filename: str):
    """Загружает данные из файла XML и возвращает объект"""
    tree = ET.parse(filename)
    root = tree.getroot()
    return Event.from_xml(root)

#создаем спписок мест
seats: List['Seat'] = [
    Seat(row=1, number=1),
    Seat(row=1, number=2),
    Seat(row=1, number=3),
    Seat(row=2, number=1),
    Seat(row=2, number=2),
    Seat(row=2, number=3),
]

# Создаем объект Venue с этим списком мест
venue = Venue("Частилище", "Ад", 666, seats)

#теперь создадим сероприятие
event = Event("BB Streamers Battle" , datetime.now(), venue)

# Сохраняем в JSON
save_to_json(event, "event.json")

# Загружаем из JSON
loaded_event = load_from_json("event.json")
print(loaded_event.name)  # Проверяем

# Сохраняем в XML
save_to_xml(event, "event.xml")

# Загружаем из XML
loaded_event = load_from_xml("event.xml")
print(loaded_event.name)  # Проверяем


