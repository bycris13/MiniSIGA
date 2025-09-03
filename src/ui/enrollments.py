from src.queries import add_enrollment, student_id_exists, course_id_exists,list_enrollments
def menu_enrollments():
    while True:
        print("\n📚 MINI SIGA - Menu Matriculas")
        print("1. ➕ Registrar matrícula")
        print("2. 📋 Listar matrículas")
        print("3. 🔍 Buscar matrícula por estudiante o curso")
        print("4. 🧮 Registrar nota")
        print("5. 🗑️  Eliminar matrícula")
        print("0. Salir de matriculas")
    
        option = int(input("Ingrese una opción: "))

        if option == 1:
            try:
                student_id = int(input("👤 Ingrese el id del estudiante a matricular: "))
                if not student_id_exists(student_id):
                    print("❌ No se encontro estudiante con ese id.")
                    continue
                course_id = int(input("📘 Ingrese el id del estcurso a matricular: "))
                if not  course_id_exists(course_id):
                    print("❌ No se encontro curso con ese id.")
                    continue
                add_enrollment(student_id, course_id)
            except ValueError:
                print("❌ Error al ingresar los datos.")
        elif option == 2:
            list_enrollments()
        elif option == 0:
            break
                