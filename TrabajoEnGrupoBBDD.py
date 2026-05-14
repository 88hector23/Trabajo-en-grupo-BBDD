import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

# =========================
# CONEXIÓN A FIREBASE
# =========================

ruta_llave = r"C:\Users\hecto\PyCharmMiscProject\trabajo-en-grupo-bbdd-firebase-adminsdk-fbsvc-febdc95cfe.json"

cred = credentials.Certificate(ruta_llave)
firebase_admin.initialize_app(cred)

db = firestore.client()

print("✅ Conexión a Firestore establecida correctamente.")


# =========================
# CRUD DOCTORES
# =========================

def agregar_doctor(nombre, especializacion):
    try:
        datos_doctor = {
            'nombre': nombre,
            'especializacion': especializacion,
            'fecha_registro': datetime.now(timezone.utc),
            'estado': 'pendiente'
        }

        update_time, doc_ref = db.collection('doctores').add(datos_doctor)

        print(f"🟢 Doctor agregado con éxito. ID: {doc_ref.id}")

    except Exception as e:
        print(f"❌ Error al agregar doctor: {e}")


def leer_doctores():
    print("\n--- LISTA DE DOCTORES ---")

    try:
        docs = db.collection('doctores').order_by('fecha_registro').stream()

        contador = 0

        for doc in docs:
            data = doc.to_dict()

            print(
                f"ID: {doc.id} | "
                f"Nombre: {data.get('nombre', 'N/A')} | "
                f"Especialización: {data.get('especializacion', 'N/A')} | "
                f"Estado: {data.get('estado', 'N/A')}"
            )

            contador += 1

        if contador == 0:
            print("⚠️ No hay doctores registrados.")

    except Exception as e:
        print(f"❌ Error al leer doctores: {e}")


def actualizar_doctor(doc_id, nuevos_datos):
    try:
        doc_ref = db.collection('doctores').document(doc_id)

        if doc_ref.get().exists:
            doc_ref.update(nuevos_datos)
            print(f"🟡 Doctor {doc_id} actualizado correctamente.")
        else:
            print("⚠️ El doctor no existe.")

    except Exception as e:
        print(f"❌ Error al actualizar doctor: {e}")


def borrar_doctor(doc_id):
    try:
        doc_ref = db.collection('doctores').document(doc_id)

        if doc_ref.get().exists:
            doc_ref.delete()
            print(f"🔴 Doctor {doc_id} eliminado correctamente.")
        else:
            print("⚠️ El doctor no existe.")

    except Exception as e:
        print(f"❌ Error al borrar doctor: {e}")


# =========================
# CRUD PACIENTES
# =========================

def agregar_paciente(nombre, dni):
    try:
        datos_paciente = {
            'nombre': nombre,
            'DNI': dni,
            'fecha_registro': datetime.now(timezone.utc),
            'estado': 'pendiente'
        }

        update_time, doc_ref = db.collection('pacientes').add(datos_paciente)

        print(f"🟢 Paciente agregado con éxito. ID: {doc_ref.id}")

    except Exception as e:
        print(f"❌ Error al agregar paciente: {e}")


def leer_pacientes():
    print("\n--- LISTA DE PACIENTES ---")

    try:
        docs = db.collection('pacientes').order_by('fecha_registro').stream()

        contador = 0

        for doc in docs:
            data = doc.to_dict()

            print(
                f"ID: {doc.id} | "
                f"Nombre: {data.get('nombre', 'N/A')} | "
                f"DNI: {data.get('DNI', 'N/A')} | "
                f"Estado: {data.get('estado', 'N/A')}"
            )

            contador += 1

        if contador == 0:
            print("⚠️ No hay pacientes registrados.")

    except Exception as e:
        print(f"❌ Error al leer pacientes: {e}")


def actualizar_paciente(doc_id, nuevos_datos):
    try:
        doc_ref = db.collection('pacientes').document(doc_id)

        if doc_ref.get().exists:
            doc_ref.update(nuevos_datos)
            print(f"🟡 Paciente {doc_id} actualizado correctamente.")
        else:
            print("⚠️ El paciente no existe.")

    except Exception as e:
        print(f"❌ Error al actualizar paciente: {e}")


# =========================
# MENÚ PRINCIPAL
# =========================

def menu():

    while True:

        print("\n" + "=" * 30)
        print("🏥 GESTOR DEL HOSPITAL")
        print("=" * 30)

        print("1. Agregar doctor")
        print("2. Listar doctores")
        print("3. Actualizar doctor")
        print("4. Eliminar doctor")
        print("5. Agregar paciente")
        print("6. Listar pacientes")
        print("7. Actualizar paciente")
        print("8. Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        # =========================
        # DOCTORES
        # =========================

        if opcion == "1":

            nombre = input("Nombre del doctor: ").strip()

            if not nombre:
                print("⚠️ El nombre no puede estar vacío.")
                continue

            especializacion = input("Especialización: ").strip()

            agregar_doctor(nombre, especializacion)

        elif opcion == "2":

            leer_doctores()

        elif opcion == "3":

            leer_doctores()

            doc_id = input("\nID del doctor a actualizar: ").strip()

            nuevo_estado = input("Nuevo estado: ").strip()

            actualizar_doctor(doc_id, {
                'estado': nuevo_estado
            })

        elif opcion == "4":

            leer_doctores()

            doc_id = input("\nID del doctor a borrar: ").strip()

            confirmacion = input("¿Seguro? (s/n): ").lower()

            if confirmacion == "s":
                borrar_doctor(doc_id)

        # =========================
        # PACIENTES
        # =========================

        elif opcion == "5":

            nombre = input("Nombre del paciente: ").strip()

            if not nombre:
                print("⚠️ El nombre no puede estar vacío.")
                continue

            dni = input("DNI: ").strip()

            agregar_paciente(nombre, dni)

        elif opcion == "6":

            leer_pacientes()

        elif opcion == "7":

            leer_pacientes()

            doc_id = input("\nID del paciente a actualizar: ").strip()

            nuevo_estado = input("Nuevo estado: ").strip()

            actualizar_paciente(doc_id, {
                'estado': nuevo_estado
            })

        elif opcion == "8":

            print("👋 Saliendo del sistema...")
            break

        else:

            print("⚠️ Opción no válida.")


# =========================
# EJECUCIÓN
# =========================

if __name__ == "__main__":
    menu()
