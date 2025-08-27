from datetime import datetime

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
