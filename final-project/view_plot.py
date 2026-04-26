import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# --- Load data for latest session ---
conn = sqlite3.connect("door_log.db")
cursor = conn.cursor()

cursor.execute("SELECT MAX(session_id) FROM door_events")
session_id = cursor.fetchone()[0]

cursor.execute(
    "SELECT timestamp, event FROM door_events WHERE session_id=? ORDER BY id",
    (session_id,)
)
rows = cursor.fetchall()

conn.close()

if len(rows) < 2:
    print("Not enough data to plot durations.")
    exit()

# --- Convert timestamps ---
times = [datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S") for r in rows]
states = [1 if r[1] == "OPEN" else 0 for r in rows]

# --- Build step plot ---
plot_times = []
plot_states = []

for i in range(len(times) - 1):
    # start of state
    plot_times.append(times[i])
    plot_states.append(states[i])

    # end of state (just before next event)
    plot_times.append(times[i + 1])
    plot_states.append(states[i])

plt.figure(figsize=(10, 5))
plt.step(plot_times, plot_states, where="post")
plt.yticks([0, 1], ["CLOSED", "OPEN"])
plt.xlabel("Time")
plt.ylabel("Door State")
plt.title("Door Sensor State Duration Over Time")
plt.grid(True)
plt.tight_layout()
plt.show()