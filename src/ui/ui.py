from src.ui.students_ui import menu_students

def menu():
    while True:
        print("\n📚 MINI SIGA - Menú Principal")
        print("1. 💾 Estuiantes")
        print("0. Salir")

        option = int(input("Ingrese una opción: "))
        if option == 1:
            menu_students()
        elif option == 0:
            break
