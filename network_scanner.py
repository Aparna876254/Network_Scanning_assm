import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import csv
from datetime import datetime

results = []

# scan full network
def scan_network():
    base_ip = entry.get()
    output_box.delete(1.0, tk.END)
    results.clear()

    def worker():
        for i in range(1, 255):
            ip = base_ip + "." + str(i)

            try:
                result = subprocess.run(
                    ["ping", "-c", "1", "-W", "1", ip],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                status = "UP" if result.returncode == 0 else "DOWN"
                time_now = datetime.now().strftime("%H:%M:%S")
                msg = f"[{time_now}] {ip} is {status}\n"

                root.after(0, lambda m=msg: update_output(m))
                results.append([ip, status])

            except:
                pass

        root.after(0, lambda: update_output("\nScan Completed\n"))

    threading.Thread(target=worker, daemon=True).start()


# save to csv
def save_csv():
    if not results:
        output_box.insert(tk.END, "\nNo data to save\n")
        return

    with open("new_network.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["IP", "Status"])
        writer.writerows(results)

    output_box.insert(tk.END, "\nSaved to new_network.csv\n")


def update_output(msg):
    output_box.insert(tk.END, msg)
    output_box.see(tk.END)
    
# GUI
root = tk.Tk()
root.title("Network Scanner GUI")
root.geometry("700x500")

tk.Label(root, text="Enter Base IP (e.g., 192.168.1)").pack()

entry = tk.Entry(root, width=40)
entry.pack(pady=5)

tk.Button(root, text="Start Scan", command=scan_network).pack(pady=5)
tk.Button(root, text="Save to CSV", command=save_csv).pack(pady=5)

output_box = scrolledtext.ScrolledText(root, width=80, height=20)
output_box.pack(pady=10)

root.mainloop()
