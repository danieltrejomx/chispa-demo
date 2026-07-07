from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from crm import crm_db, ClienteBase
from booking_engine import booking_engine, Reserva
from events import EventConfig, calculate_event_cost
import uvicorn
import os

app = FastAPI(title="Chispa API Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints
@app.post("/api/crm/register")
def register_client(client: ClienteBase):
    if client.edad_nino < 1 or client.edad_nino > 10:
        raise HTTPException(status_code=400, detail="Edad del niño fuera del rango de ludoteca (1-10 años).")
    return crm_db.register_client(client)

@app.post("/api/booking/book")
def book_slot(reserva: Reserva):
    # Verify client exists and has slots
    client = crm_db.get_client(reserva.id_adulto)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
    if client.slots_disponibles <= 0:
        raise HTTPException(status_code=400, detail="No tienes pases disponibles")
        
    success = booking_engine.book_slot(reserva)
    if not success:
        raise HTTPException(status_code=409, detail="Aforo completo, elige otro horario")
        
    client.slots_disponibles -= 1
    return {"message": "Reserva confirmada", "reserva": reserva, "slots_restantes": client.slots_disponibles}

@app.post("/api/b2b/register")
def register_b2b(domain: str):
    if "." not in domain:
        raise HTTPException(status_code=400, detail="Dominio inválido")
    code = crm_db.register_b2b_company(domain)
    return {"discount_code": code}

@app.post("/api/events/quote")
def quote_event(config: EventConfig):
    cost = calculate_event_cost(config)
    return {"total_cost": cost}

# Static file serving
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/{view}.html")
def read_view(view: str):
    file_path = os.path.join(static_dir, f"{view}.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Page not found")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
