import os
from database import TaskManagerDB 

def clean_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    print("\n--- TASK MANAGER v1.0 (CLI) ---")
    print("1. Ver tareas")
    print("2. Agregar tarea")
    print("3. Borrar tarea")
    print("4. Dar por conluida tarea")
    print("5. Salir")

def excecute():

    db = TaskManagerDB()
    while True:
        menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            clean_screen()
            tasks = db.list_task()
            if not tasks:
                print("No hay tareas pendientes. ¡Relájate! 😎")
            for t in tasks: 

                emoji = '✅' 
                status = t['status']

                if status == 'pending':
                    emoji = '⏳'
                
                    
                print(f"[{t['id']}] [{emoji}][{t['title']}] - [{t['status']}] ({t['created_at']})") 

        elif opcion == "2":
            title = input("Titulo: ")
            desc = input("Descripción: ")
            db.insert_task(title,desc)
            print("¡Tarea anotada!")

        elif opcion =="3":
            task_id = input("ID de la tarea a borrar: ")
            db.soft_delete(task_id)
            print(f"Tarea {task_id} enviada a la papaelera.")

        elif opcion == "4":
            task_id = input("ID de la tarea a borrar: ")
            db.complete_task(task_id)
            print(f"Tarea {task_id} marcada como completada ✅ ")

        elif opcion == "5":
            print("¡Adiós! que tengas un día productivo .")
            break

        else:
            print("Opción no válida, intenta de nueveo.")
if __name__ == "__main__":
    excecute()

