from enum import Enum
from typing import Optional, List
from pydantic import BaseModel
import uuid

class TipoPase(str, Enum):
    DAY_PASS = "DAY_PASS"
    PASE_5_DIAS = "PASE_5_DIAS"
    WORKPASS_40 = "WORKPASS_40"
    CHISPA_20 = "CHISPA_20"
    NINGUNO = "NINGUNO"
    SOLO_HORA = "SOLO_HORA"

class ClienteBase(BaseModel):
    nombre_adulto: str
    email_adulto: str
    telefono_emergencia: str
    nombre_nino: str
    edad_nino: int
    tipo_pase_activo: TipoPase = TipoPase.NINGUNO

class ClienteInDB(ClienteBase):
    id_adulto: str
    slots_disponibles: int = 0

class CRMInternal:
    def __init__(self):
        self.clientes: dict[str, ClienteInDB] = {}
        self.empresas_b2b: dict[str, str] = {} # email domain -> discount_code
    
    def register_client(self, client_data: ClienteBase) -> ClienteInDB:
        id_adulto = str(uuid.uuid4())
        
        # Determine slots based on pass
        slots = 0
        if client_data.tipo_pase_activo == TipoPase.DAY_PASS:
            slots = 1
        elif client_data.tipo_pase_activo == TipoPase.PASE_5_DIAS:
            slots = 5
        elif client_data.tipo_pase_activo == TipoPase.WORKPASS_40:
            slots = 40 # hours essentially, simplified
        elif client_data.tipo_pase_activo == TipoPase.CHISPA_20:
            slots = 20
        elif client_data.tipo_pase_activo == TipoPase.SOLO_HORA:
            slots = 1
            
        cliente_db = ClienteInDB(
            **client_data.dict(),
            id_adulto=id_adulto,
            slots_disponibles=slots
        )
        
        self.clientes[id_adulto] = cliente_db
        return cliente_db
        
    def get_client(self, id_adulto: str) -> Optional[ClienteInDB]:
        return self.clientes.get(id_adulto)

    def register_b2b_company(self, domain: str) -> str:
        code = f"CORP15-{domain.split('.')[0].upper()}"
        self.empresas_b2b[domain] = code
        return code

# In-memory instance
crm_db = CRMInternal()
