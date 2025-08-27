import asyncio
from app.database import users_collection

async def test_db():
    try:
        # On tente de récupérer un document
        user = await users_collection.find_one({})
        if user:
            print("Connexion à MongoDB OK, premier document :", user)
        else:
            print("Connexion à MongoDB OK, mais la collection est vide.")
    except Exception as e:
        print("Erreur DB :", e)

asyncio.run(test_db())
