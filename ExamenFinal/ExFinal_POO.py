#EXAMEN FINAL DE POO
#JOSE EMILIO OYERVIDE MOSCOSO
#AGOSTO 2023

import tkinter as tk
import random
import mysql.connector
from tkinter import messagebox
from InterfazPreguntas import CrearPreguntaApp

class PreguntasApp:
    #CREACION DE LA PRIMERA INTERFAZ GRAFICA
    def __init__(self, root, nombre):
        self.root = root
        self.nombre = nombre
        self.preguntas_correctas = 0
        self.preguntas_incorrectas = 0
        self.pregunta_label = tk.Label(root,font=("Helvetica", 14), bg="purple", fg="white", text="")
        self.respuestas_buttons = [tk.Button(root, text="",font=("Helvetica", 14), bg="red", fg="white", command=lambda i=i: self.verificar_respuesta(i)) for i in range(4)]
        self.resultado_label = tk.Label(root, text="")
        self.result_button = tk.Button(root, text="Ver mis resultados",font=("Helvetica", 14), bg="blue", fg="white", command=self.mostrar_resultados)
        self.salir_button = tk.Button(root, text="Salir",font=("Helvetica", 14), bg="pink", fg="white", command=exit)

        self.pregunta_label.pack(pady=10)
        for button in self.respuestas_buttons:
            button.pack(pady=5)
        self.resultado_label.pack(pady=10)
        self.result_button.pack(pady=5)
        self.salir_button.pack(pady=5)

        #CONEXION CON LA BASE DE DATOS
        self.conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Emilio12345.",
            database="neoguias"
        )
        self.cursor = self.conexion.cursor()

        self.obtener_nueva_pregunta()

    def obtener_nueva_pregunta(self):
        pregunta, opciones = self.obtener_pregunta_aleatoria_db()
        self.respuesta_correcta = opciones[0]
        random.shuffle(opciones)  # Barajar las opciones
        self.pregunta_actual = pregunta
        self.pregunta_label.config(text=pregunta)
        for i, button in enumerate(self.respuestas_buttons):
            button.config(text=opciones[i])
        self.resultado_label.config(text="")

    def verificar_respuesta(self, opcion_seleccionada):
        if self.respuestas_buttons[opcion_seleccionada]['text'] == self.respuesta_correcta:
            tk.messagebox.showinfo("¡Correcto!", "Tu respuesta es correcta.")
            self.preguntas_correctas += 1
        else:
            tk.messagebox.showerror("¡Incorrecto!", "Tu respuesta es incorrecta.")
            self.preguntas_incorrectas += 1

        self.obtener_nueva_pregunta()

    def mostrar_resultados(self):
        tk.messagebox.showinfo("Resultados", f"{self.nombre}, tus resultados son:\nPreguntas correctas: {self.preguntas_correctas}\nPreguntas incorrectas: {self.preguntas_incorrectas}")
        self.conexion.close()
        self.root.destroy()
        
    def obtener_pregunta_aleatoria_db(self):
        self.cursor.execute("SELECT pregunta, respuesta_correcta, opcion2, opcion3, opcion4 FROM table_preguntas ORDER BY RAND() LIMIT 1")
        pregunta, respuesta_correcta, opcion2, opcion3, opcion4 = self.cursor.fetchone()
        return pregunta, [respuesta_correcta, opcion2, opcion3, opcion4]


def abrir_interfaz_preguntas():
    nombre = nombre_entry.get()
    if nombre:
        root.withdraw()  # Oculta la ventana actual
        root_preguntas = tk.Tk()
        root_preguntas.geometry("400x400")
        root_preguntas.title("Juego de Preguntas")
        app_preguntas = PreguntasApp(root_preguntas, nombre)
        root_preguntas.mainloop()
    else:
        tk.messagebox.showerror("Error", "Debes ingresar un nombre.")

def crear_nuevas_preguntas():
    root = tk.Tk()
    root.geometry("400x400")
    app = CrearPreguntaApp(root)
    root.mainloop()
    
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    root.title("Inicio")
    
    nombre_label = tk.Label(root, text="Ingresa tu nombre:")
    nombre_entry = tk.Entry(root)
    ingresar_button = tk.Button(root, text="Ingresar",font=("Helvetica", 14), bg="green", fg="white", command=abrir_interfaz_preguntas)
    ingresarpreguntas_button = tk.Button(root, text="Ingresar nuevas preguntas",font=("Helvetica", 14), bg="gray", fg="white", command=crear_nuevas_preguntas)

    nombre_label.pack(pady=10)
    nombre_entry.pack(pady=5)
    ingresar_button.pack(pady=10)
    ingresarpreguntas_button.pack(pady=10)
    root.configure(bg="blue")
    root.mainloop()
