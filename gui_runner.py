import tkinter as tk
from tkinter import scrolledtext
import threading
import subprocess
import os

running = False


def run_script(output_box, status_label):
    global running
    running = True
    status_label.config(text="Running...")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    process = subprocess.Popen(
        ["python3", "pdf_to_text_parallel.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd=BASE_DIR   # 👈 ensures correct INPUT_DIR / OUTPUT_DIR resolution
    )

    for line in process.stdout:
        output_box.insert(tk.END, line)
        output_box.see(tk.END)

    process.wait()

    status_label.config(text="Finished")
    running = False


def start_processing(output_box, status_label):
    global running

    if running:
        return

    thread = threading.Thread(
        target=run_script,
        args=(output_box, status_label),
        daemon=True
    )
    thread.start()


def main():
    root = tk.Tk()
    root.title("PDF to Text Converter")

    start_btn = tk.Button(
        root,
        text="Start Processing",
        command=lambda: start_processing(output, status)
    )
    start_btn.pack(pady=10)

    status = tk.Label(root, text="Idle")
    status.pack()

    output = scrolledtext.ScrolledText(root, width=100, height=30)
    output.pack()

    root.mainloop()


if __name__ == "__main__":
    main()



