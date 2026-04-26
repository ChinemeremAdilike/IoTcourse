import tkinter as tk
import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime
import time

# ---------- SESSION ----------
SESSION_ID = int(time.time())  # unique per run

blinking = False
blink_on = False

def log_event(event):
    conn = sqlite3.connect("door_log.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO door_events (session_id, event, timestamp) VALUES (?, ?, ?)",
        (SESSION_ID, event, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def blink():
    global blink_on
    if blinking:
        blink_on = not blink_on
        indicator.config(bg="red" if blink_on else "white")
        root.after(400, blink)

def on_message(client, userdata, msg):
    global blinking
    state = msg.payload.decode()

    if state == "OPEN":
        blinking = True
        indicator.config(text="ALARM!\nDoor OPEN")
        print("BEEP BEEP BEEP!")
        log_event("OPEN")
        blink()
        client.publish("smartdoor/status", "OPEN")

    elif state == "CLOSED":
        blinking = False
        indicator.config(text="Door CLOSED", bg="green")
        log_event("CLOSED")
        client.publish("smartdoor/status", "CLOSED")

client = mqtt.Client()
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.subscribe("smartdoor/control")

def mqtt_loop():
    client.loop()
    root.after(100, mqtt_loop)

root = tk.Tk()
root.title("Door Sensor Unit")
root.geometry("220x180")

tk.Label(root, text="Sensor Status", font=("Arial", 14)).pack(pady=8)

indicator = tk.Label(
    root, text="Waiting...",
    bg="gray", font=("Arial", 12),
    width=15, height=4
)
indicator.pack(pady=15)

mqtt_loop()
root.mainloop()