import tkinter as tk
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883, 60)

def send_open():
    client.publish("smartdoor/control", "OPEN")

def send_closed():
    client.publish("smartdoor/control", "CLOSED")

root = tk.Tk()
root.title("Door Control Panel")
root.geometry("300x200")

tk.Label(root, text="Door Control", font=("Arial", 16)).pack(pady=15)

tk.Button(
    root, text="DOOR OPEN", bg="red", fg="white",
    width=20, height=2, command=send_open
).pack(pady=10)

tk.Button(
    root, text="DOOR CLOSED", bg="green", fg="white",
    width=20, height=2, command=send_closed
).pack(pady=10)

root.mainloop()