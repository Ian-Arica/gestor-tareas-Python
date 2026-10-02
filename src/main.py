import tkinter as tk
import sqlite3 as sq
from tkinter import messagebox


connection = sq.connect("./data/database.db")     # Connect to the database
cursor = connection.cursor()      # Create a cursor to execute commands
# Execute SQLite code
cursor.execute("""
CREATE TABLE IF NOT EXISTS tareas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    descripcion TEXT,
    prioridad TEXT,
    estado TEXT)
""")
connection.commit()   # Commit the database changes

# Function to display tasks
def showTasks():
    taskList.delete(0, tk.END)

    cursor.execute("SELECT titulo, descripcion, prioridad, estado FROM tareas")
    results = cursor.fetchall()

    for task in results:
        text = f"{task[0]} | {task[1]} | {task[2]} | {task[3]}"
        taskList.insert(tk.END, text)


# Function to save task data to the database
def saveTaskData():
    taskName = name.get()
    taskDescription = description.get()
    taskPriority = priorityVar.get()
    if (taskName.strip() and taskDescription.strip() and taskPriority.strip()):

        cursor.execute("""
        INSERT INTO tareas (titulo, descripcion, prioridad, estado)
        VALUES (?, ?, ?, 'pendiente')
        """,
        (taskName, taskDescription, taskPriority)),
        connection.commit()

        showTasks()
    else:
        messagebox.showwarning("Alerta!", "La nota no puede tener título o descripción vacía.")


# Function to get select element
def getElement():
    try:
        index = taskList.curselection()[0]
        value = taskList.get(index)
        return value

    except IndexError:
        messagebox.showwarning("Alerta!", "Seleccione un elemento")


# Function to update task data to the database
def updateTaskData():
    cursor.execute("""SELECT * FROM tareas""")
    value = getElement()
    if (value != None):
        vaca = cursor.execute("""SELECT * FROM tareas""")
        print(vaca)


window = tk.Tk()

# Enter a task title
nameLabel = tk.Label(window, text="Nombre")
nameLabel.pack()
name = tk.Entry()
name.pack()

# Enter a task description
descriptionLabel = tk.Label(window, text="Descripcion")
descriptionLabel.pack()
description = tk.Entry()
description.pack()

# Select a priority
priorityVar = tk.StringVar()
priorityVar.set("Media")

priorityLabel = tk.Label(window, text="Prioridad")
priorityLabel.pack()
priorityMenu = tk.OptionMenu(window, priorityVar, "Alta", "Media", "Baja")
priorityMenu.pack()

# Save button
saveButton = tk.Button(window, text="Guardar Tarea", command=saveTaskData)
saveButton.pack()

# Update button
updateButton = tk.Button(window, text="Actualizar Tarea", command=updateTaskData)
updateButton.pack()

# Display tasks
taskList = tk.Listbox(window, width=60)
taskList.pack()


showTasks()
window.mainloop()