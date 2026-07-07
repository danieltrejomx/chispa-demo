from datetime import datetime, date, time
from typing import List, Dict
from pydantic import BaseModel

MAX_AFORO_COWORKING = 50
MAX_AFORO_LUDOTECA = 30
RATIO_NANNYS = 5 # 1 nanny for 5 kids

class SlotTime(BaseModel):
    start_time: str # HH:MM
    end_time: str # HH:MM

class Reserva(BaseModel):
    id_adulto: str
    fecha: date
    hora_inicio: str
    hora_fin: str
    adultos: int = 1
    ninos: int = 1

class BookingEngine:
    def __init__(self):
        self.reservas: List[Reserva] = []
        
    def check_availability(self, fecha: date, hora_inicio: str, adultos: int = 1, ninos: int = 1) -> bool:
        # Simplified logic: count all reservations for that specific hour/date
        current_adults = 0
        current_kids = 0
        
        for r in self.reservas:
            if r.fecha == fecha and r.hora_inicio == hora_inicio:
                current_adults += r.adultos
                current_kids += r.ninos
                
        if (current_adults + adultos) > MAX_AFORO_COWORKING:
            return False
            
        if (current_kids + ninos) > MAX_AFORO_LUDOTECA:
            return False
            
        return True

    def book_slot(self, reserva: Reserva) -> bool:
        if self.check_availability(reserva.fecha, reserva.hora_inicio, reserva.adultos, reserva.ninos):
            self.reservas.append(reserva)
            return True
        return False

# In-memory instance
booking_engine = BookingEngine()
