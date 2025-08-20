from pydantic import BaseModel
from typing import Optional


class Negociation(BaseModel):
    produit_id: str
    prix_propose: float
    message: Optional[str] = None