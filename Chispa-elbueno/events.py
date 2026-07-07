from typing import List
from pydantic import BaseModel

class EventConfig(BaseModel):
    capacidad: int
    adicionales: List[str]

# Base prices for 4 hours
PRICES_BASE = {
    25: 15000,
    50: 25000,
    85: 35000
}

PRICES_ADICIONALES = {
    "show_tematico": 5000,
    "decoracion": 3000,
    "carrito_monchis": 2500,
    "pastel_premium": 1500
}

def calculate_event_cost(config: EventConfig) -> int:
    base_cost = PRICES_BASE.get(config.capacidad, PRICES_BASE[25])
    
    addons_cost = 0
    for addon in config.adicionales:
        addons_cost += PRICES_ADICIONALES.get(addon, 0)
        
    return base_cost + addons_cost
