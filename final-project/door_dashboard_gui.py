import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import subprocess
import sys
import paho.mqtt.client as mqtt

# ---------- HELPER: GET LATEST SESSION ----------
def get_latest_session():
    conn = sqlite3.connect("door_log.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(session_id) FROM door_events")
    session = cursor.fetchone()[0]
    conn.close()
    return session

# ---------- DATABASE VIEW ----------
def show_database():
    # Always fetch the CURRENT session when button is clicked
    current_session = get_latest_session()

    db_window = tk.Toplevel(root)
    db_window.title("Door Activity Database")
    db_window.geometry("600x480")
    db_window.protocol("WM_DELETE_WINDOW", db_window.destroy)

    frame = tk.Frame(db_window, padx=15, pady=15)
    frame.pack(fill="both", expand=True)

    conn = sqlite3.connect("door_log.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, event, timestamp FROM door_events WHERE session_id=?",
        (current_session,)
    )
    rows = cursor.fetchall()

    cursor.execute(
        "SELECT COUNT(*) FROM door_events WHERE session_id=? AND event='OPEN'",
        (current_session,)
    )
    open_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM door_events WHERE session_id=? AND event='CLOSED'",
        (current_session,)
    )
    close_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT event FROM door_events WHERE session_id=? ORDER BY id DESC LIMIT 1",
        (current_session,)
    )
    last_event = cursor.fetchone()

    conn.close()

    # Determine correct system status
    if last_event and last_event[0] == "CLOSED":
        status_text = "SECURE – Door is closed"
        status_color = "green"
    else:
        status_text = "UNSECURE – Door is open"
        status_color = "red"

    # ---------- UI ----------
    tk.Label(frame, text="Review Door Activity",
             font=("Arial", 16)).pack(pady=10)

    tk.Label(frame, text=f"Total Events: {open_count + close_count}",
             font=("Arial", 11)).pack(anchor="w")

    tk.Label(frame, text=f"Door OPEN Count: {open_count}",
             font=("Arial", 11)).pack(anchor="w")

    tk.Label(frame, text=f"Door CLOSED Count: {close_count}",
             font=("Arial", 11)).pack(anchor="w", pady=(0, 10))

    tk.Label(frame, text="System Status:",
             font=("Arial", 11, "bold")).pack(anchor="w")

    tk.Label(frame, text=status_text,
             font=("Arial", 13),
             fg=status_color).pack(anchor="w", pady=(0, 15))

    # ---------- Event Table ----------
    table_container = tk.Frame(frame)
    table_container.pack(fill="both", expand=True)

    columns = ("ID", "Event", "Timestamp")
    tree = ttk.Treeview(table_container, columns=columns, show="headings")

    v_scroll = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview)
    h_scroll = ttk.Scrollbar(table_container, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    tree.grid(row=0, column=0, sticky="nsew")
    v_scroll.grid(row=0, column=1, sticky="ns")
    h_scroll.grid(row=1, column=0, sticky="ew")

    table_container.rowconfigure(0, weight=1)
    table_container.columnconfigure(0, weight=1)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=180)

    for row in rows:
        tree.insert("", tk.END, values=row)

# ---------- VIEW PLOT ----------
def view_plot():
    subprocess.Popen([sys.executable, "view_plot.py"])

# ---------- MQTT CALLBACK ----------
def on_message(client, userdata, msg):
    state = msg.payload.decode()
    if state == "OPEN":
        status_label.config(text="Door Status: OPEN", fg="red")
        messagebox.showwarning("Security Alert", "Door OPEN detected!")
    elif state == "CLOSED":
        status_label.config(text="Door Status: CLOSED", fg="green")

client = mqtt.Client()
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.subscribe("smartdoor/status")

def mqtt_loop():
    client.loop()
    root.after(100, mqtt_loop)

# ---------- MAIN DASHBOARD ----------
root = tk.Tk()
root.title("Smart Door Security Sensor")
root.geometry("430x330")

tk.Label(root, text="Smart Door Security Dashboard",
         font=("Arial", 16)).pack(pady=15)

status_label = tk.Label(root, text="Door Status: UNKNOWN",
                        font=("Arial", 14))
status_label.pack(pady=20)

tk.Button(root, text="See Database",
          width=22, height=2,
          command=show_database).pack(pady=5)

tk.Button(root, text="View Plot",
          width=22, height=2,
          command=view_plot).pack(pady=5)

mqtt_loop()
root.mainloop()