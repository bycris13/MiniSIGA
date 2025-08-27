from src.queries import add_student, list_students, find_student_by_document, delete_stundent
def menu():
    while True:
        print("\n📚 MINI SIGA - Menú Principal")
        print("1. 💾 Registrar estudiante")
        print("2. 🧾 Listar Estudiantes")
        print("3. 🔍 Buscar esrudiante por documento")
        print("4. 🗑️ Eliminar estudiante por su ID")
        print("0. Salir")

        option = int(input("Ingrese una opción: "))

        if option == 1:
            document = input("Ingrese numero de documento: ")
            name = input("Ingrese su nombre: ")
            surname = input("Ingrese su apellido: ")
            email = input("Ingrese su correo: ")
            birthdate = input("Ingrese su fecha de nacimiento (YYYY-MM-DD): ")
            add_student(document,name,surname,email,birthdate)
        elif option == 2:
            list_students()
        elif option == 3:
            document = input('Ingrese el documento del estudiante que desea buscar: ')
            find_student_by_document(document)
        elif option == 4:
            try:
                student_id = int(input("Ingrese el id del estudiante a eliminar: "))
                delete_stundent(student_id)
            except Exception as err:
                print(f"❌ No se encontro el estudiante {err}")
        elif option == 0:
            print("👋 Saliendo del programa")
            break
        else:
            print("❌ Opcion invalida. Intenta de nuevo")