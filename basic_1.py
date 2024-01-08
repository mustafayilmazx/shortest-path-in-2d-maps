import tkinter as tk

class Shape:
    def __init__(self, name, num_sides):
        self.name = name
        self.num_sides = num_sides
        self.coordinates = []

    def add_coordinate(self, x, y):
        self.coordinates.append((x, y))

    def get_coordinate_options(self):
        return ["Köşe {}: ({}, {})".format(i+1, x, y) for i, (x, y) in enumerate(self.coordinates)]

def add_shape():
    shape_name = shape_name_entry.get()
    num_sides = int(shape_sides_entry.get())
    new_shape = Shape(shape_name, num_sides)
    shapes[shape_name] = new_shape
    update_shape_options()  # Şekiller listesini güncelle


def update_shape_options():
    menu = shape_list_menu["menu"]
    menu.delete(0, "end")  # Mevcut menü öğelerini temizle

    for shape_name in shapes.keys():
        menu.add_command(label=shape_name, command=lambda value=shape_name: on_shape_select(value))

def on_shape_select(value):
    current_shape.set(value)
    update_corner_options()

def update_corner_options():
    selected_shape_name = current_shape.get()
    if selected_shape_name not in shapes:
        return

    selected_shape = shapes[selected_shape_name]
    corner_options = selected_shape.get_coordinate_options()
    corner_menu = corner_list_menu["menu"]
    corner_menu.delete(0, "end")
    for corner_option in corner_options:
        corner_menu.add_command(label=corner_option, command=lambda value=corner_option: tk._setit(current_corner, value))

def draw_shape():
    selected_shape = shapes[current_shape.get()]
    if selected_shape.coordinates:
        points = [coord for point in selected_shape.coordinates for coord in point]
        canvas.delete("all")
        canvas.create_polygon(points, outline='white', fill='blue', width=2)

root = tk.Tk()
root.title("Harita Çizer")

# Canvas Oluşturma
canvas = tk.Canvas(root, width=400, height=400, bg='black')
canvas.pack(side=tk.LEFT)

# Kontrol Paneli
control_panel = tk.Frame(root)
control_panel.pack(side=tk.RIGHT, fill=tk.Y)

# Şekil İsmi Girişi
shape_name_entry = tk.Entry(control_panel)
shape_name_entry.pack()

# Köşe Sayısı Girişi
shape_sides_entry = tk.Entry(control_panel)
shape_sides_entry.pack()

# Şekil Ekleme Butonu
add_shape_button = tk.Button(control_panel, text="Şekil Ekle", command=add_shape)
add_shape_button.pack()

# Şekillerin Listesi için OptionMenu Oluşturma
shapes = {}
current_shape = tk.StringVar(root)
# Başlangıçta hiçbir şekil olmadığı için geçici bir değer atıyoruz
current_shape.set("Şekil Seçin")
shape_list_menu = tk.OptionMenu(control_panel, current_shape, "Şekil Seçin")
shape_list_menu.pack()

# Köşelerin Listesi için OptionMenu Oluşturma
current_corner = tk.StringVar(root)
current_corner.set("Köşe Seçin")
corner_list_menu = tk.OptionMenu(control_panel, current_corner, "Köşe Seçin")
corner_list_menu.pack()

# Çizim Butonu
draw_button = tk.Button(control_panel, text="Çiz", command=draw_shape)
draw_button.pack()

current_shape.trace("w", update_corner_options)

root.mainloop()
