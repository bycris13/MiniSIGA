from src.ui.students_ui import menu_students
from src.ui.courses_ui import menu_courses
from src.ui.enrollments import menu_enrollments
def menu():
    while True:
        print("\n📚 MINI SIGA - Menú Principal")
        print("1. 💾 Estudiantes")
        print("2. 📚 Gestión de cursos")
        print("3. 📝 Matrículas")
        print("0. Salir")

        option = int(input("Ingrese una opción: "))
        if option == 1:
            menu_students()
        elif option == 2:
            menu_courses()
        elif option == 3:
            menu_enrollments()
        elif option == 0:
            break
