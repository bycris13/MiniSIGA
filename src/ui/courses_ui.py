from src.queries import add_course, list_course, find_course_by_id, edit_course, delete_course
from src.validation import valid_credits, course_id_exists
def menu_courses():
    while True:
        print("\n📚 MINI SIGA - Menú de Cursos")
        print("1. ➕ Registrar curso")
        print("2. 📋 Listar cursos")
        print("3. 🔍 Buscar curso por código")
        print("4. 🗑️  Eliminar curso por código")
        print("5. ✏️  Editar curso")
        print("0. Volver al menú principal")

        option = int(input("Ingrese una opcion: "))

        if option == 1:
            try:
                name = input("Ingresa el nombre del curso: ")
                teacher = input("Ingresa el docente del curso: ")
                credits = int(input("Creditos: "))      
                if valid_credits(credits):
                    add_course(name, teacher, credits)
            except ValueError:
                print("❌ Ocurrio un error al registrar.")
        elif option == 2:
            list_course()
        elif option == 3:
            course_id = int(input("Ingrese el id del curso que desea buscar: "))
            find_course_by_id(course_id)
        elif option == 4:
            course_id = int(input("Ingrese el ID del curso que desea eliminar: "))
            delete_course(course_id)
        elif option == 5:
            course_id = int(input("ID del curso a editar: "))
            if not course_id_exists(course_id):
                print("❌ No existe ningún curso con ese ID.")
                return
            name = input("Ingresa el nombre del curso: ")
            teacher = input("Docente del curso: ")
            credits = int(input("Creditos: "))
            if valid_credits(credits):
                edit_course(course_id, name, teacher, credits)
        elif option == 0:
            break