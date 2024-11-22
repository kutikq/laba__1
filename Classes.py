from datetime import datetime


class Event:
    def __init__(self, name: str, date_time: datetime, venue: 'Venue'):
        self.name=name
        self.datetime=date_time
        self.Venue=venue

class Venue:
    def __init__(self, name:str, place:str, capacity: int):
        self.name = name
        self.place = place
        self.capacity = capacity
        self.seats: List['Seat'] = [] 

class Seat:
    def __init__(self, row:int , number:int):
        self.row = row
        self.number = number
        self.is_avaible = True

    def book (self):
        while self.is_avaible:
            try:
                print(f'Seat is booked')
            except Exception as e:
                print(f'Error! {e}')



