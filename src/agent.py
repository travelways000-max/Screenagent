import os
import time
import threading
import keyboard
import tkinter as tk
from tkinter import messagebox, filedialog
from screen_capture import capture_full_screen, capture_region, save_screenshot
from extractor import extract_data
from excel_writer import save_to_excel, view_all_data
from form_filler import fill_form
from config import AUTO_CAPTURE, AUTO_CAPTURE_INTERVAL


class ScreenAgentApp:
    def __init__(self):
        self.running = False
        self.build_gui()

    def build_gui(self):
        self.root = tk.Tk()
        self.root.title("🤖 Screen Reader Agent v2.0")
        self.root.geometry("400x400")
        self.root.configure(bg="#1e1e2e")

        title = tk.Label(self.root, text="🤖 SCREEN READER AGENT",
                         fg="white", bg="#1e1e2e",
                         font=("Arial", 16, "bold"))
        title.pack(pady=15)

        info = tk.Label(self.root,
                        text="Press Ctrl+Shift+S to capture screen\n"
                             "Press Ctrl+Shift+Q to quit",
                        fg="#a0a0b0", bg="#1e1e2e",
                        font=("Arial", 10))
        info.pack(pady=5)

        self.status = tk.Label(self.root, text="Status: IDLE",
                               fg="yellow", bg="#1e1e2e",
                               font=("Arial", 12, "bold"))
        self.status.pack(pady=10)

        btn1 = tk.Button(self.root, text="📸 Capture Now (Full Screen)",
                         command=self.capture_now, bg="#4CAF50", fg="white",
                         font=("Arial", 11, "bold"), padx=10, pady=5)
        btn1.pack(pady=5)

        btn2 = tk.Button(self.root, text="▭ Capture Region (Drag Mouse)",
                         command=self.capture_region_mode, bg="#2196F3",
                         fg="white", font=("Arial", 11, "bold"),
                         padx=10, pady=5)
        btn2.pack(pady=5)

        btn3 = tk.Button(self.root, text="🔁 Toggle Auto-Capture",
                         command=self.toggle_auto, bg="#FF9800", fg="white",
                         font=("Arial", 11, "bold"), padx=10, pady=5)
        btn3.pack(pady=5)

        btn4 = tk.Button(self.root, text="📊 View All Data",
                         command=view_all_data, bg="#9C27B0", fg="white",
                         font=("Arial", 11, "bold"), padx=10, pady=5)
        btn4.pack(pady=5)

        btn5 = tk.Button(self.root, text="📝 Fill Form with Last Data",
                         command=self.fill_last_form, bg="#F44336", fg="white",
                         font=("Arial", 11, "bold"), padx=10, pady=5)
        btn5.pack(pady=5)

        self.last_data = None

        # Hotkeys
        keyboard.add_hotkey('ctrl+shift+s', self.capture_now)
        keyboard.add_hotkey('ctrl+shift+q', self.root.quit)

        self.root.mainloop()

    def set_status(self, msg, color="yellow"):
        self.status.config(text=f"Status: {msg}", fg=color)
        self.root.update()

    def process_image(self, image):
        self.set_status("Extracting...", "orange")
        data = extract_data(image)
        self.set_status("Saving to Excel...", "orange")
        save_to_excel(data)
        self.last_data = data
        self.set_status("DONE ✅", "lightgreen")
        print(f"📦 Extracted: {data}")

    def capture_now(self):
        try:
            self.set_status("Capturing...", "orange")
            img = capture_full_screen()
            save_screenshot(img)
            self.process_image(img)
        except Exception as e:
            self.set_status(f"Error: {e}", "red")

    def capture_region_mode(self):
        try:
            self.set_status("Drag to select region (3 sec)...", "orange")
            self.root.iconify()
            time.sleep(1)
            import tkinter as tk2
            selector = tk2.Toplevel()
            selector.attributes('-fullscreen', True)
            selector.attributes('-alpha', 0.3)
            selector.configure(bg='yellow')
            canvas = tk2.Canvas(selector, cursor='cross', bg='yellow',
                                highlightthickness=0)
            canvas.pack(fill=tk2.BOTH, expand=True)
            self._start = None
            self._rect = None

            def on_down(e):
                self._start = (e.x_root, e.y_root)

            def on_drag(e):
                if self._rect:
                    canvas.delete(self._rect)
                self._rect = canvas.create_rectangle(
                    self._start[0], self._start[1], e.x_root, e.y_root,
                    outline='red', width=3)

            def on_up(e):
                self._bbox = (self._start[0], self._start[1],
                              e.x_root, e.y_root)
                selector.destroy()

            canvas.bind('<ButtonPress-1>', on_down)
            canvas.bind('<B1-Motion>', on_drag)
            canvas.bind('<ButtonRelease-1>', on_up)
            selector.wait_window()
            self.root.deiconify()

            img = capture_region(self._bbox)
            save_screenshot(img)
            self.process_image(img)
        except Exception as e:
            self.set_status(f"Error: {e}", "red")
            self.root.deiconify()

    def toggle_auto(self):
        if self.running:
            self.running = False
            self.set_status("Auto-capture STOPPED", "yellow")
        else:
            self.running = True
            self.set_status("Auto-capture RUNNING", "lightgreen")
            threading.Thread(target=self._auto_loop, daemon=True).start()

    def _auto_loop(self):
        while self.running:
            try:
                img = capture_full_screen()
                save_screenshot(img)
                self.process_image(img)
            except Exception as e:
                print(f"Auto error: {e}")
            for _ in range(AUTO_CAPTURE_INTERVAL):
                if not self.running:
                    return
                time.sleep(1)

    def fill_last_form(self):
        if self.last_data:
            fill_form(self.last_data)
        else:
            messagebox.showinfo("Info", "No data extracted yet. Capture first.")


if __name__ == "__main__":
    print("🚀 Starting Screen Reader Agent v2.0...")
    print("📋 Hotkeys:")
    print("   Ctrl+Shift+S  →  Capture screen")
    print("   Ctrl+Shift+Q  →  Quit")
    ScreenAgentApp()
