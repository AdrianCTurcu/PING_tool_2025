import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import platform
import re

process = None  # ținem procesul curent

def start_ping():
    global process
    ip = ip_entry.get()
    if not ip:
        output_box.insert(tk.END, "Te rog introdu un IP sau host!\n")
        return
    
    output_box.delete(1.0, tk.END)  # curățăm consola
    
    thread = threading.Thread(target=ping_host, args=(ip,))
    thread.daemon = True
    thread.start()

def stop_ping():
    global process
    if process:
        process.terminate()
        output_box.insert(tk.END, "\nPing oprit!\n", "fail")
        output_box.see(tk.END)
        process = None

def ping_host(ip):
    global process
    system_os = platform.system()
    command = ["ping", ip, "-t"] if system_os == "Windows" else ["ping", ip]

    try:
        creation_flag = 0
        if system_os == "Windows":
            creation_flag = subprocess.CREATE_NO_WINDOW  # ascunde consola ping
        
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            creationflags=creation_flag  # important pentru Windows
        )

        for line in iter(process.stdout.readline, ''):
            if process.poll() is not None:
                break

            line_strip = line.strip()
            if re.search(r"Reply from|TTL=", line_strip):
                output_box.insert(tk.END, line_strip + "\n", "success")
            elif re.search(r"timed out|unreachable|fail", line_strip, re.IGNORECASE):
                output_box.insert(tk.END, line_strip + "\n", "fail")
            else:
                output_box.insert(tk.END, line_strip + "\n")
            output_box.see(tk.END)

    except Exception as e:
        output_box.insert(tk.END, f"Eroare: {e}\n", "fail")

# Interfață
root = tk.Tk()
root.title("Ping Tool by Adrian T 2025")
root.geometry("600x480")

# Frame input + "-t"
input_frame = tk.Frame(root)
input_frame.pack(pady=5)

tk.Label(input_frame, text="IP / Host:", font=("Arial", 12)).pack(side="left", padx=5)
ip_entry = tk.Entry(input_frame, width=25, font=("Arial", 12))
ip_entry.pack(side="left", padx=5)

t_label = tk.Label(input_frame, text="-t", font=("Arial", 12), fg="blue")
t_label.pack(side="left", padx=5)

# Butoane Start/Stop
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

ping_button = tk.Button(button_frame, text="Start Ping", font=("Arial", 12), command=start_ping)
ping_button.pack(side="left", padx=5)

stop_button = tk.Button(button_frame, text="Stop Ping", font=("Arial", 12), fg="red", command=stop_ping)
stop_button.pack(side="left", padx=5)

# Consolă Output
output_box = scrolledtext.ScrolledText(root, width=70, height=15, font=("Consolas", 11))
output_box.tag_config("success", foreground="green")
output_box.tag_config("fail", foreground="red")
output_box.pack(pady=10)

# Copyright
copyright_label = tk.Label(root, text="© AdrianT", font=("Arial", 8), anchor="e")
copyright_label.pack(side="bottom", anchor="se", padx=5, pady=5)

root.mainloop()
