from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    telephone: str
    mot_de_passe: str
    role: str = "acheteur" # acheteur, vendeur, admin


class UserLogin(BaseModel):
    email: EmailStr
    mot_de_passe: str