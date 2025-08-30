from src.queries import add_student, list_students, find_student_by_document, delete_stundent, update_student
from src.validation import valid_date, valid_document, document_exists, student_id_exists
def menu_students():
    while True:
        print("\n📚 MINI SIGA - Menu Estudiantes")
        print("1. 💾 Registrar estudiante")
        print("2. 🧾 Listar Estudiantes")
        print("3. 🔍 Buscar estudiante por documento")
        print("4. 🗑️  Eliminar estudiante por su ID")
        print("5. ✏️  Editar registro de estudiante")
        print("0. Salir")

        option = int(input("Ingrese una opción: "))

        if option == 1:
            while True:
                document = input("Ingrese numero de documento: ")
                if not valid_document(document):
                    continue
                if document_exists(document):
                    print("❌ El documento ya existe")
                else:
                    break


            name = input("Ingrese su nombre: ")
            surname = input("Ingrese su apellido: ")
            email = input("Ingrese su correo: ")
            
            while True:
                birthdate = input("Ingrese su fecha de nacimiento (YYYY-MM-DD): ")
                if valid_date(birthdate):
                    break
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
        elif option == 5:
            try:
                student_id =  int(input("Ingrese el id del estudiante que desea editar: "))
                if not student_id_exists(student_id):
                    print("❌ No existe ningún estudiante con ese ID.")
                    return
                name = input("Nuevo nombre: ")
                surname = input("Nuevo apellido: ")
                while True:
                    document = input("Nuevo documento: ")
                    if valid_document(document):
                        break
                while True:
                    birthdate = input("Nueva fecha de nacimiento (YYYY-MM-DD): ")
                    if valid_date(birthdate):
                        break
                email = input("Nuevo correo: ")
                update_student(student_id,document, name, surname, email, birthdate)
            except Exception as err:
                print(f"Error al editar estudiante {err}")
        elif option == 0:
            print("👋 Saliendo del programa")
            break
        else:
            print("❌ Opcion invalida. Intenta de nuevo")