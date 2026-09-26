import tkinter as tk
import sqlite3 as sq


conexion = sq.connect("./data/database.db")     # Conexión con la base de datos
cursor = conexion.cursor()      # Creación de la variable para ejecutar comandos
# Ejecución de código sqlite3
cursor.execute("""
CREATE TABLE IF NOT EXISTS tareas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    descripcion TEXT,
    prioridad TEXT,
    estado TEXT)
""")
conexion.commit()   # Hacer commit de los cambios de la database

# Función para mostrar las tareas
def mostrarTareas():
    espacioMostrar.delete(0, tk.END)

    cursor.execute("SELECT titulo, descripcion, prioridad, estado FROM tareas")
    resultado = cursor.fetchall()

    for tarea in resultado:
        texto = f"{tarea[0]} | {tarea[1]} | {tarea[2]} | {tarea[3]}"
        espacioMostrar.insert(tk.END, texto)


# Función para guardar los datos en la database
def guardarDatos():
    nombreTarea = nombre.get()
    descripcionTarea = descripcion.get()
    prioridadTarea = prioridadVar.get()
    if (nombreTarea.strip() and descripcionTarea.strip() and prioridadTarea.strip()):

        cursor.execute("""
        INSERT INTO tareas (titulo, descripcion, prioridad, estado)
        VALUES (?, ?, ?, 'pendiente')
        """,
        (nombreTarea, descripcionTarea, prioridadTarea)),
        conexion.commit()

        mostrarTareas()

ventana = tk.Tk()

# Introducir título de una tarea
labelNombre = tk.Label(ventana, text="Nombre")
labelNombre.pack()
nombre = tk.Entry()
nombre.pack()

# Introducir descripción de la tarea
labelDescripcion = tk.Label(ventana, text="Descripcion")
labelDescripcion.pack()
descripcion = tk.Entry()
descripcion.pack()

# Seleccionar prioridad
prioridadVar = tk.StringVar()
prioridadVar.set("Media")

labelPrioridad = tk.Label(ventana, text="Prioridad")
labelPrioridad.pack()
prioridad = tk.OptionMenu(ventana, prioridadVar, "Alta", "Media", "Baja")
prioridad.pack()

# Botón para guardar
boton = tk.Button(ventana, text="Guardar Tarea", command=guardarDatos)
boton.pack()

# Mostrar las tareas
espacioMostrar = tk.Listbox(ventana, width=60)
espacioMostrar.pack()


mostrarTareas()
ventana.mainloop()