
import tkinter as tk
from tkinter import ttk

class Shape:
    def __init__(self, name, num_sides):
        self.name = name
        self.num_sides = num_sides
        self.coordinates = [(0, 0)] * num_sides

    def set_coordinate(self, index, x, y):
        if index < self.num_sides:
            self.coordinates[index] = (x, y)

    def get_coordinates(self):
        return self.coordinates

    def get_coordinate_options(self):
        return [f"Köşe {i+1} - ({self.coordinates[i][0]}, {self.coordinates[i][1]} )" for i in range(self.num_sides)]

def add_shape():
    shape_name = shape_name_entry.get()
    num_sides = int(shape_sides_entry.get())
    new_shape = Shape(shape_name, num_sides)
    shapes[shape_name] = new_shape
    update_shape_options()

def update_shape_options():
    menu = shape_list_menu["menu"]
    menu.delete(0, "end")

    for shape_name in shapes.keys():
        menu.add_command(label=shape_name, command=lambda value=shape_name: on_shape_select(value))

def on_shape_select(value):
    current_shape.set(value)
    update_corner_options()

def update_corner_options(*args):
    global corner_list_menu
    selected_shape_name = current_shape.get()

    if selected_shape_name not in shapes:
        corner_options = ["Köşe Yok"]
    else:
        selected_shape = shapes[selected_shape_name]
        corner_options = selected_shape.get_coordinate_options()

    if corner_list_menu is not None:
        corner_list_menu.destroy()

    corner_list_menu = ttk.OptionMenu(control_panel, current_corner, *corner_options)
    corner_list_menu.pack()

def update_coordinates():
    selected_shape_name = current_shape.get()
    selected_shape = shapes[selected_shape_name]
    selected_corner_index = int(current_corner.get().split()[1]) - 1

    try:
        new_x = int(x_entry.get())
        new_y = int(y_entry.get())
        selected_shape.set_coordinate(selected_corner_index, new_x, new_y)
        update_corner_options()
        
    except ValueError:
        pass  # Geçersiz girişlerde bir şey yapma

def draw_shape():
    selected_shape = shapes[current_shape.get()]
    if selected_shape.coordinates:
        points = [coord for point in selected_shape.coordinates for coord in point]
        canvas.delete("all")
        canvas.create_polygon(points, outline='black', fill='blue', width=0)

def show_coordinates(event):
    coord_label.config(text=f"Koordinatlar: {event.x}, {event.y}")

root = tk.Tk()
root.title("Harita Çizer")
style = ttk.Style()
style.theme_use('clam')

# Canvas Oluşturma
canvas = tk.Canvas(root, width=400, height=400, bg='black')
canvas.pack(side=tk.LEFT)
canvas.bind("<Motion>", show_coordinates)

# Kontrol Paneli
control_panel = ttk.Frame(root)
control_panel.pack(side=tk.RIGHT, fill=tk.Y)

# Şekil İsmi Girişi
shape_name_entry = ttk.Entry(control_panel)
shape_name_entry.pack()

# Köşe Sayısı Girişi
shape_sides_entry = ttk.Entry(control_panel)
shape_sides_entry.pack()

# Şekil Ekleme Butonu
add_shape_button = ttk.Button(control_panel, text="Şekil Ekle", command=add_shape)
add_shape_button.pack()

# Şekillerin Listesi için OptionMenu Oluşturma
shapes = {}
current_shape = tk.StringVar(root)
current_shape.set("Şekil Seçin")
shape_list_menu = ttk.OptionMenu(control_panel, current_shape, "Şekil Seçin")
shape_list_menu.pack()

# Köşelerin Listesi için OptionMenu Oluşturma
current_corner = tk.StringVar(root)
current_corner.set("Köşe Yok")
corner_list_menu = None

# Koordinat Giriş Alanları
x_entry = ttk.Entry(control_panel)
x_entry.pack()
y_entry = ttk.Entry(control_panel)
y_entry.pack()

# Koordinatları Güncelleme Butonu
update_button = ttk.Button(control_panel, text="Koordinatları Güncelle", command=update_coordinates)
update_button.pack()

# Çizim Butonu
draw_button = ttk.Button(control_panel, text="Çiz", command=draw_shape)
draw_button.pack()

# Mouse Koordinatlarını Gösteren Label
coord_label = ttk.Label(root, text="Koordinatlar: 0, 0")
# set right bottom corner
coord_label.pack(side=tk.BOTTOM)
coord_label.place(relx=1.0, rely=1.0, anchor='se')

current_shape.trace("w", update_corner_options)

root.mainloop()
