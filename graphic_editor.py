import tkinter as tk
from tkinter.colorchooser import askcolor


class Drawable:
    """Абстрактный класс для рисуемых объектов"""

    def __init__(self, canvas, color, thickness):
        self.canvas = canvas
        self.color = color
        self.thickness = thickness

    def draw(self):
        raise NotImplementedError("Метод 'draw' должен быть реализован в подклассах.")


class Point(Drawable):
    def __init__(self, canvas, x, y, color, thickness):
        super().__init__(canvas, color, thickness)
        self.x = x
        self.y = y
        self.draw()

    def draw(self):
        self.item = self.canvas.create_oval(
            self.x - self.thickness // 2,
            self.y - self.thickness // 2,
            self.x + self.thickness // 2,
            self.y + self.thickness // 2,
            fill=self.color,
            outline=self.color
        )


class Line(Drawable):
    def __init__(self, canvas, x1, y1, x2, y2, color, thickness):
        super().__init__(canvas, color, thickness)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.draw()

    def draw(self):
        self.item = self.canvas.create_line(
            self.x1, self.y1, self.x2, self.y2,
            fill=self.color, width=self.thickness
        )


class Circle(Drawable):
    def __init__(self, canvas, x1, y1, x2, y2, color, thickness):
        super().__init__(canvas, color, thickness)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.draw()

    def draw(self):
        self.item = self.canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2,
            outline=self.color, width=self.thickness
        )


class Square(Drawable):
    def __init__(self, canvas, x1, y1, x2, y2, color, thickness):
        super().__init__(canvas, color, thickness)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.draw()

    def draw(self):
        self.item = self.canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2,
            outline=self.color, width=self.thickness
        )


class Triangle(Drawable):
    def __init__(self, canvas, x1, y1, x2, y2, color, thickness):
        super().__init__(canvas, color, thickness)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.draw()

    def draw(self):
        half_side = abs(self.x2 - self.x1) / 2
        height = abs(self.y2 - self.y1)
        self.item = self.canvas.create_polygon(
            self.x1, self.y1,
            self.x1 - half_side, self.y1 + height,
            self.x1 + half_side, self.y1 + height,
            outline=self.color, fill="", width=self.thickness
        )


class DrawingEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Графический редактор")

        self.current_color = "#000000"
        self.current_thickness = 3  # Изменено начальное значение толщины на 3
        self.history = []

        self.canvas = tk.Canvas(root, bg="white", width=600, height=400)
        self.canvas.pack()

        self.create_toolbar()
        self.bind_canvas_events()
        self.drawing_mode = None
        self.temp_shape = None

    def create_toolbar(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack()

        tk.Button(toolbar, text="Цвет", command=self.choose_color).pack(side=tk.LEFT)
        tk.Label(toolbar, text="Толщина:").pack(side=tk.LEFT)
        self.thickness_entry = tk.Entry(toolbar, width=3)
        self.thickness_entry.insert(0, str(self.current_thickness))
        self.thickness_entry.pack(side=tk.LEFT)

        tk.Button(toolbar, text="Точка", command=self.set_point_mode).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Линия", command=self.set_line_mode).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Круг", command=self.set_circle_mode).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Квадрат", command=self.set_square_mode).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Треугольник", command=self.set_triangle_mode).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Рисование", command=self.set_draw_mode).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Отменить", command=self.undo).pack(side=tk.LEFT)

    def bind_canvas_events(self):
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def choose_color(self):
        color = askcolor(color=self.current_color)[1]
        if color:
            self.current_color = color

    def get_thickness(self):
        try:
            return int(self.thickness_entry.get())
        except ValueError:
            return self.current_thickness

    def set_point_mode(self):
        self.drawing_mode = "point"

    def set_line_mode(self):
        self.drawing_mode = "line"

    def set_circle_mode(self):
        self.drawing_mode = "circle"

    def set_square_mode(self):
        self.drawing_mode = "square"

    def set_triangle_mode(self):
        self.drawing_mode = "triangle"

    def set_draw_mode(self):
        self.drawing_mode = "draw"

    def on_click(self, event):
        self.start_x, self.start_y = event.x, event.y
        thickness = self.get_thickness()

        if self.drawing_mode == "point":
            point = Point(self.canvas, event.x, event.y, self.current_color, thickness)
            self.history.append(point.item)
        elif self.drawing_mode == "line":
            self.temp_shape = Line(self.canvas, event.x, event.y, event.x, event.y, self.current_color, thickness)
        elif self.drawing_mode == "circle":
            self.temp_shape = Circle(self.canvas, event.x, event.y, event.x, event.y, self.current_color, thickness)
        elif self.drawing_mode == "square":
            self.temp_shape = Square(self.canvas, event.x, event.y, event.x, event.y, self.current_color, thickness)
        elif self.drawing_mode == "triangle":
            self.temp_shape = Triangle(self.canvas, event.x, event.y, event.x, event.y, self.current_color, thickness)
        elif self.drawing_mode == "draw":
            self.last_x, self.last_y = event.x, event.y

    def on_drag(self, event):
        if self.drawing_mode == "draw":
            thickness = self.get_thickness()
            line = self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                fill=self.current_color, width=thickness
            )
            self.history.append(line)
            self.last_x, self.last_y = event.x, event.y
        elif self.drawing_mode in {"line", "circle", "square", "triangle"}:
            if self.temp_shape:
                self.canvas.delete(self.temp_shape.item)
            if self.drawing_mode == "line":
                self.temp_shape = Line(self.canvas, self.start_x, self.start_y, event.x, event.y, self.current_color,
                                       self.get_thickness())
            elif self.drawing_mode == "circle":
                self.temp_shape = Circle(self.canvas, self.start_x, self.start_y, event.x, event.y, self.current_color,
                                         self.get_thickness())
            elif self.drawing_mode == "square":
                self.temp_shape = Square(self.canvas, self.start_x, self.start_y, event.x, event.y, self.current_color,
                                         self.get_thickness())
            elif self.drawing_mode == "triangle":
                self.temp_shape = Triangle(self.canvas, self.start_x, self.start_y, event.x, event.y,
                                           self.current_color, self.get_thickness())

    def on_release(self, event):
        if self.temp_shape:
            self.history.append(self.temp_shape.item)
            self.temp_shape = None

    def undo(self):
        if self.history:
            last_item = self.history.pop()
            self.canvas.delete(last_item)


root = tk.Tk()
app = DrawingEditor(root)
root.mainloop()