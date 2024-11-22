from datetime import datetime

#1.Меропприятие
class Event:
    def __init__(self, name: str, date_time: datetime, venue: 'Venue'):
        self.name=name
        self.datetime=date_time #время проведения
        self.Venue=venue    #место проведения

#2.Место ппроведения 
class Venue:
    def __init__(self, name:str, place:str, capacity: int):
        self.name = name
        self.place = place
        self.capacity = capacity    #вместимость
        self.seats: List['Seat'] = []   #список мест

#3.Место(на мероприятии)
class Seat:
    def __init__(self, row:int , number:int):
        self.row = row
        self.number = number
        self.is_avaible = True  #доступность(чисто фикция)

    
#4.Билет
class Ticket:
    def __init__(self, event: 'Event', seat = 'Seat', category = 'Category'):
        self.Event = event
        self.Seat = seat
        self.Category = category

    def book (self):    #функция для бронирования
        while self.Seat.is_avaible:
            try:
                print(f'Seat is booked')
                self.Seat.is_avaible = False
            except Exception as e:
                print(f'Error! {e}')

#5. Категория
class Category:
    def __init__(self, name_cat: str, pricemultiplier: float):
        self.cat= name_cat
        self.multiplier = pricemultiplier
    
class 


