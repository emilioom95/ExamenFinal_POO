import tkinter as tk
import mysql.connector
from tkinter import messagebox

class CrearPreguntaApp:
    def __init__(self, root):
        self.root = root
        self.pregunta_label = tk.Label(root, text="Pregunta:")
        self.pregunta_entry = tk.Entry(root)
        self.respuesta_correcta_label = tk.Label(root, text="Respuesta correcta:")
        self.respuesta_correcta_entry = tk.Entry(root)
        self.opciones_labels = [tk.Label(root, text=f"Opción {i+2}:") for i in range(3)]
        self.opciones_entries = [tk.Entry(root) for _ in range(3)]
        self.agregar_button = tk.Button(root, text="Agregar Pregunta", command=self.agregar_pregunta)
        self.salir_button = tk.Button(root, text="Salir", command=self.cerrar_app)
        
        self.pregunta_label.pack(pady=10)
        self.pregunta_entry.pack(pady=5)
        self.respuesta_correcta_label.pack(pady=5)
        self.respuesta_correcta_entry.pack(pady=5)

        for i in range(3):
            self.opciones_labels[i].pack(pady=5)
            self.opciones_entries[i].pack(pady=5)

        self.agregar_button.pack(pady=10)
        self.salir_button.pack(pady=10)

        self.conexion = mysql.connector.connect(
            host="127.0.0.1", 
            user="root",
            password="Emilio12345.",
            database="neoguias"
        )
        self.cursor = self.conexion.cursor()

        self.crear_tabla_si_no_existe()

    def crear_tabla_si_no_existe(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS table_preguntas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                pregunta TEXT,
                respuesta_correcta TEXT,
                opcion2 TEXT,
                opcion3 TEXT,
                opcion4 TEXT
            )
        """)
        self.conexion.commit()

    def agregar_pregunta(self):
        pregunta = self.pregunta_entry.get()
        respuesta_correcta = self.respuesta_correcta_entry.get()
        opciones = [entry.get() for entry in self.opciones_entries if entry.get()]
        
        if pregunta and respuesta_correcta and opciones:
            opciones.insert(0, respuesta_correcta)
            self.cursor.execute("INSERT INTO table_preguntas (pregunta, respuesta_correcta, opcion2, opcion3, opcion4) VALUES (%s, %s, %s, %s, %s)",
                                (pregunta, opciones[0], opciones[1], opciones[2], opciones[3]))
            self.conexion.commit()
            self.pregunta_entry.delete(0, tk.END)
            self.respuesta_correcta_entry.delete(0, tk.END)
            for entry in self.opciones_entries:
                entry.delete(0, tk.END)
            tk.messagebox.showinfo("Éxito", "Pregunta con opciones agregada correctamente.")
        else:
            tk.messagebox.showerror("Error", "Debes llenar todos los campos.")

    def cerrar_app(self):
        self.conexion.close()
        self.root.destroy()
    
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    app = CrearPreguntaApp(root)
    root.mainloop()
