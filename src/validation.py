from datetime import datetime
from src.database import get_connection

# Valida si el domumento ya exite
def document_exists(document):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM students WHERE document = ?", (document,))
    result = cursor.fetchone()
    conn.close()
    return result is not None
    

# Valida el documento
def valid_document(document):
    if not document.isdigit():
        print("❌ El documento debe contener solo numeros")
        return False
    if len(document) != 10:
        print("❌ El documento debe contener 10 digitos")
        return False
    return True

#  Validada el formato de la fecha
def valid_date(date_str):
    try:
        date_str = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.today()
        if date_str > today:
            print("❌ La fecha no puede ser en el futuro.")
            return False
        return True
    except ValueError:
        print("❌ Formato inválido. Usa YYYY-MM-DD.")
        return False
