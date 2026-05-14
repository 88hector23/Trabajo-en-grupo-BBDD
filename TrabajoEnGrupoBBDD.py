import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

# Usamos la ruta completa para que no haya pérdida
ruta_llave = r"C:\Users\hecto\PyCharmMiscProject\trabajo-en-grupo-bbdd-firebase-adminsdk-fbsvc-febdc95cfe.json"

cred = credentials.Certificate(ruta_llave)
firebase_admin.initialize_app(cred)
db = firestore.client()

print("✅ Conexión a Firestore establecida correctamente.")

def agregar_muestra(nombre, especializacion): #CREATE
 try:
 # Los datos se preparan como un Diccionario (JSON)
    datos_doctor = {
        'nombre': nombre,
        'especializacion': especializacion,
        'fecha_registro': datetime.now(timezone.utc),
        'estado': 'pendiente' # Añadimos un estado por defecto
    }

 # .add() genera un ID automático y devuelve una tupla (tiempo, referencia_documento)
    update_time, doc_ref = db.collection('doctores').add(datos_doctor)
    print(f"🟢 Muestra agregada con éxito. ID asignado: {doc_ref.id}")

 except Exception as e:
    print(f"❌ Error al agregar al doctor: {e}")

def leer_muestras():  # READ
    print("\n--- Listado de Muestras Registradas ---")
    try:
        # .stream() trae los datos iterables
        docs = db.collection('doctores').order_by('fecha_registro').stream()
        contador = 0

        for doc in docs:
            data = doc.to_dict()  # Convierte el documento de Firestore a un Diccionario de Python
            print(f"ID: {doc.id} | Nombre: {data.get('nombre', 'N/A')} | Estado: {data.get('estado', 'N/A')}")
            contador += 1

        if contador == 0:
            print("No hay doctores registrados actualmente.")

    except Exception as e:
        print(f"❌ Error al leer los doctores: {e}")

def actualizar_muestra(doc_id, nuevos_datos):  # UPDATE
    try:
        doc_ref = db.collection('doctores').document(doc_id)
        doc_ref.update(nuevos_datos)
        print(f"🟡 Doctor {doc_id} actualizado correctamente.")
    except Exception as e:
        print(f"❌ Error al actualizar (¿Seguro que el ID existe?):{e}")
def borrar_muestra(doc_id): #DELETE
    try:
        doc_ref = db.collection('doctor').document(doc_id)
        doc_ref.delete()
        print(f"🔴 Doctor {doc_id} eliminado definitivamente.")
    except Exception as e:
        print(f"❌ Error al intentar borrar: {e}")

def menu():
    while True:
        print("\n" + "="*30)
        print("🔬 GESTOR DEL HOSPITAL")
        print("="*30)
        print("1. Agregar doctor")
        print("2. Lista de doctores")
        print("3. Actualizar doctor")
        print("4. Eliminar doctor")
        print("5. Salir")

        opcion = input("\nSeleccione una opción (1-5): ")
        if opcion == "1":
            nombre = input("Ingrese el nombre del doctor: ").strip()
 # Validación básica
            if not nombre:
                print("⚠️ El nombre no puede estar vacío.")
                continue
            especializacion = input("Ingrese especialización: ")
            agregar_muestra(nombre, especializacion)

        elif opcion == "2":
            leer_muestras()

        elif opcion == "3":
            leer_muestras() # Mostramos la lista para que el alumno copie el ID
            doc_id = input("\nCopie y pegue el ID del doctor a actualizar: ").strip()
            actualizar_muestra(doc_id, {'estado': 'procesada'})
        elif opcion == "4":
            leer_muestras()
            doc_id = input("\nCopie y pegue el ID del doctor a borrar: ").strip()
            confirmacion = input("¿Está seguro? (s/n): ").lower()
            if confirmacion == 's':
                borrar_muestra(doc_id)
        elif opcion == "5":
            print("Saliendo del gestor...")
        break
    else:
            print("⚠️ Opción no válida. Intente nuevamente.")


# Este bloque asegura que el menú solo se ejecute si corremos el archivo directamente
if __name__ == "__main__":
    menu()
