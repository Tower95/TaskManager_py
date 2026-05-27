import os
from database import TaskManagerDB 
from blessed import Terminal
import re

term = Terminal()
counts= dict()

def clean_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    print("\n--- TASK MANAGER v1.0 (CLI) ---")
    print("1. Ver tareas")
    print("2. Agregar tarea")
    print("3. Borrar tarea")
    print("4. Dar por conluida tarea")
    print("5. Salir")

def get_selection_mouse(x,y):
    option = 0
    if x >= 1 and x<= 31:
       if y>=4 and y<=8 :
           match y:
                case 4:
                   option = 1
                case 5:
                    option = 2
                case 6:
                    option = 3
                case 7:
                    option = 4
                case 8:
                    option = 5
                case _:
                    print("opcion no valida")
    return option

def input_allowed(prompt):
    print(prompt, end='', flush=True)
    tecla = term.inkey(timeout=None)
    return tecla
            

def excecute():
    db = TaskManagerDB()
    if not term.does_mouse():
        print("This example won't work on your terminal!")
    else:
        with term.fullscreen(), term.cbreak(), term.mouse_enabled():
            # Forzamos el modo SGR extendido (el estándar moderno de Ubuntu)
            print('\x1b[?1006h', end='', flush=True)
            
            while True:
                inp = term.inkey(timeout=None)
                
                if inp.name and 'MOUSE' in inp.name:
                    counts[inp.name] = counts.get(inp.name, 0) + 1
                    
                    # --- PARSEO ULTRA EXACTO PARA TU UBUNTU ---
                    secuencia_cruda = str(repr(inp))
                    
                    # Eliminamos las comillas y los caracteres de escape para dejar solo el texto limpio: <0;26;17m
                    if '<' in secuencia_cruda:
                        texto_limpio = secuencia_cruda.split('<')[1].replace("'", "").replace("m", "").replace("M", "")
                        # texto_limpio ahora es exactamente: "0;26;17"
                        
                        partes = texto_limpio.split(';')
                        if len(partes) >= 3:
                            mouse_x = int(partes[1])  # El segundo número es la Columna X (26)
                            mouse_y = int(partes[2])  # El tercer número es la Fila Y (17)
                    else:
                        mouse_x = getattr(inp, 'x', 0)
                        mouse_y = getattr(inp, 'y', 0)

                    with term.synchronized_output():
                        print(term.home + term.clear)
                        menu()
                        print(get_selection_mouse(mouse_x, mouse_y))
                        print(f"Mouse Modifier Example, press Ctrl+c to quit")
                        print(f"button={inp.name} | Fila(Y)={mouse_y} | Columna(X)={mouse_x}")
                        print(f"Clicks acumulados: {counts}")
                        # Línea de debug para que veas qué está enviando tu Ubuntu:
                        print(f"Secuencia cruda detectada: {secuencia_cruda}")
                        
    
                        opcion = get_selection_mouse(mouse_x, mouse_y) # input("Selecciona una opción: ")

                        if opcion == 1:
                            clean_screen()
                            tasks = db.list_task()
                            if not tasks:
                                print("No hay tareas pendientes. ¡Relájate! 😎")
                            for t in tasks: 

                                emoji = '✅' 
                                status = t['status']

                                if status == 'pending':
                                    emoji = '⏳'
                                
                                    
                                print(f"[{t['id']:2}] [{emoji}][{t['title']:30}] - [{t['status']:7}] ({t['created_at']})") 
                            input_allowed("Presiona Enter para volver al menú...")
                    if opcion == 2:
                        title = input("Titulo: ")
                        desc = input("Descripción: ")
                        db.insert_task(title,desc)
                        print("¡Tarea anotada!")

                    elif opcion ==3:
                        task_id = input("ID de la tarea a borrar: ")
                        db.soft_delete(task_id)
                        print(f"Tarea {task_id} enviada a la papaelera.")

                    elif opcion == 4:
                        task_id = input("ID de la tarea a borrar: ")
                        db.complete_task(task_id)
                        print(f"Tarea {task_id} marcada como completada ✅ ")

                    elif opcion == 5:
                        print("¡Adiós! que tengas un día productivo .")
                    

                    else:
                        print("Opción no válida, intenta de nueveo.")

if __name__ == "__main__":
    excecute()

