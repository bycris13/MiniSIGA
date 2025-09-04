from src.queries import add_enrollment, student_id_exists, course_id_exists,list_enrollments,find_enrollments,update_grade,delete_enrollment
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
        elif option == 3:
            find_enrollments()
        elif option == 4:  # 👈 NUEVO
            try:
                enrollment_id = int(input("Ingrese el ID de la matrícula: "))
                grade = float(input("Ingrese la nota (0.0 - 5.0): "))
                if grade < 0 or grade > 5:
                    print("❌ La nota debe estar entre 0.0 y 5.0.")
                    continue
                update_grade(enrollment_id, grade)
            except ValueError:
                print("❌ Debe ingresar un número válido.")
        elif option == 5:
            try:
                enrollment_id = int(input("🗑️ Ingrese el ID de la matrícula a eliminar: "))
                if delete_enrollment(enrollment_id):
                    print("✅ Matrícula eliminada correctamente")
                else:
                    print("❌ No se encontró matrícula con ese ID.")
            except ValueError:
                print("❌ Error: ID inválido.")

        elif option == 0:
            break
                