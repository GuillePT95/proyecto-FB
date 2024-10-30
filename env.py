import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

Mail = os.getenv("Mail")
Mail_password = os.getenv("Mail_password")

print("Mail:", Mail)
print("Mail_password:", Mail_password)
