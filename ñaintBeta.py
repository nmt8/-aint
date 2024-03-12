import tkinter as tk
from tkinter import colorchooser, filedialog
import pickle
from collections import deque




class Naint:
    def __init__(self, root):
        self.root = root
        self.root.title("Ñaint")

        self.color = "#2D2D2A"
        self.brush_size = 2
        self.old_x = None
        self.old_y = None
        self.recent_colors = ["#2D2D2A", "#E63946", "#007EA7", "#F4E409"]
        self.drawn_lines = []
        self.undo_stack = deque(maxlen=1000)

        self.create_widgets()

    def create_widgets(self):
        self.toolbar = tk.Frame(self.root, bg="#f0f0f0", bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.color_preview = tk.Label(self.toolbar, bg=self.color, width=3, relief=tk.RIDGE)
        self.color_preview.pack(side=tk.LEFT, padx=5, pady=5)

        self.color_button = tk.Button(self.toolbar, text="Color", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT, padx=(0, 5), pady=5)

        for color in self.recent_colors:
            recent_color_btn = tk.Button(self.toolbar, bg=color, width=3, relief=tk.RIDGE, command=lambda c=color: self.set_recent_color(c))
            recent_color_btn.pack(side=tk.LEFT, padx=(0, 5), pady=5)

        self.brush_label = tk.Label(self.toolbar, text="Brush Size:", bg="#f0f0f0")
        self.brush_label.pack(side=tk.LEFT, padx=(10, 5), pady=5)

        self.brush_slider = tk.Scale(self.toolbar, from_=1, to=20, orient=tk.HORIZONTAL, length=150, command=self.set_brush_size)
        self.brush_slider.set(self.brush_size)
        self.brush_slider.pack(side=tk.LEFT, padx=(0, 10), pady=5)

        self.clear_button = tk.Button(self.toolbar, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.undo_button = tk.Button(self.toolbar, text="Undo", command=self.undo)
        self.undo_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.save_button = tk.Button(self.toolbar, text="Save", command=self.save_canvas)
        self.save_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.load_button = tk.Button(self.toolbar, text="Load", command=self.load_canvas)
        self.load_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.root.bind("<Control-z>", self.undo)

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose color", color=self.color)[1]
        if color:
            self.color = color
            self.color_preview.config(bg=self.color)

    def paint(self, event):
        if self.old_x and self.old_y:
            line = self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=self.brush_size, fill=self.color, capstyle=tk.ROUND, smooth=tk.TRUE)
            self.drawn_lines.append(line)
            self.undo_stack.append(("draw", line))
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x = None
        self.old_y = None
    
    def set_brush_size(self, size):
        self.brush_size = int(size)
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.drawn_lines.clear()
        self.undo_stack.clear()

    def set_recent_color(self, color):
        self.color = color
        self.color_preview.config(bg=self.color)
    
    def undo(self, event=None):
        pixels_to_remove = 10  # Cantidad de píxeles a eliminar en cada paso de deshacer
        while self.undo_stack and pixels_to_remove > 0:
            action_type, action = self.undo_stack.pop()
            if action_type == "draw":
                self.canvas.delete(action)
                # Actualizamos la cantidad de píxeles que restan por eliminar
                pixels_to_remove -= 1


    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".naint")
        if file_path:
            with open(file_path, "wb") as f:
                pickle.dump([line_coords for line in self.drawn_lines for line_coords in self.canvas.coords(line)], f)

    def load_canvas(self):
        file_path = filedialog.askopenfilename(filetypes=[("Ñaint files", "*.naint")])
        if file_path:
            with open(file_path, "rb") as f:
                self.clear_canvas()
                coords_list = pickle.load(f)
                for i in range(0, len(coords_list), 4):
                    x1, y1, x2, y2 = coords_list[i:i+4]
                    self.canvas.create_line(x1, y1, x2, y2, width=self.brush_size, fill=self.color, capstyle=tk.ROUND, smooth=tk.TRUE)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x650")
    root.configure(bg="#FCFCFC")
    app = Naint(root)
    root.mainloop()
