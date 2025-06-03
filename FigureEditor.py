from tkinter import Tk, Toplevel, Canvas, Frame, Listbox, messagebox, END
from tkinter.ttk import Label, Button, Entry, Style
from abc import abstractmethod, ABC
from math import radians, cos, sin
import sys, os


class Shape(ABC):
    scale = 30

    @abstractmethod
    def move(self, dx, dy):
        pass

    @abstractmethod
    def rotate(self, angle, center_x, center_y):
        pass

    @abstractmethod
    def resize(self, *args):
        pass

    @abstractmethod
    def draw(self, canvas):
        pass

    @abstractmethod
    def info(self, index):
        pass


class Circle(Shape):
    def __init__(self, radius, point):
        self.radius = radius * Shape.scale
        self.x = point[0] * Shape.scale + 320
        self.y = - point[1] * Shape.scale + 310
        self.angle = 0
        self.rotate_x = round((self.x - 320) / Shape.scale, 2)
        self.rotate_y = - round((self.y - 310) / Shape.scale, 2)
        self.rotate_point_new = False

    def move(self, dx, dy):
        self.x += dx * Shape.scale
        self.y -= dy * Shape.scale
        self.rotate_x = round((self.x - 320) / Shape.scale, 2)
        self.rotate_y = - round((self.y - 310) / Shape.scale, 2)
        self.rotate_point_new = True

    def rotate(self, angle, center_x, center_y):
        rotate_point_x = self.rotate_x
        rotate_point_y = self.rotate_y

        if (self.rotate_x, self.rotate_y) != (center_x, center_y):
            self.rotate_point_new = True
            rotate_point_x = center_x
            rotate_point_y = center_y

        center_x_screen = rotate_point_x * Shape.scale + 320
        center_y_screen = - rotate_point_y * Shape.scale + 310

        x = self.x - center_x_screen
        y = self.y - center_y_screen

        rad = radians(-angle)

        new_x = round(x * cos(rad) - y * sin(rad) + center_x_screen, 2)
        new_y = round(x * sin(rad) + y * cos(rad) + center_y_screen, 2)

        if not (20 <= new_x <= 620 and 10 <= new_y <= 610):
            return False

        if self.rotate_point_new:
            self.rotate_x = rotate_point_x
            self.rotate_y = rotate_point_y
            self.rotate_point_new = False
        self.x = new_x
        self.y = new_y
        self.angle = angle

        return True

    def resize(self, *args):
        self.radius = args[0] * Shape.scale

    def draw(self, canvas):
        canvas.create_oval(self.x - self.radius, self.y - self.radius,
                           self.x + self.radius, self.y + self.radius,
                           outline='red', width=2)

    def info(self, index):
        return (f"{index}) Круг: x = {round((self.x - 320) / Shape.scale, 3)}, y = {- round((self.y - 310) / Shape.scale, 3)}, "
                f"r = {round(self.radius / Shape.scale, 3)}, угол относительно ({self.rotate_x}, {self.rotate_y}) = {self.angle}")


class Square(Shape):
    def __init__(self, points):
        self.a = (abs(points[2] - points[0])) * Shape.scale
        self.x = (points[2] + points[0]) / 2 * Shape.scale + 320
        self.y = (- points[3] - points[1]) / 2 * Shape.scale + 310
        self.angle = 0
        self.rotate_x = round((self.x - 320) / Shape.scale, 2)
        self.rotate_y = - round((self.y - 310) / Shape.scale, 2)
        self.rotate_point_new = False

    def move(self, dx, dy):
        self.x += dx * Shape.scale
        self.y -= dy * Shape.scale
        self.rotate_x = round((self.x - 320) / Shape.scale, 2)
        self.rotate_y = - round((self.y - 310) / Shape.scale, 2)
        self.rotate_point_new = True

    def rotate(self, angle, center_x, center_y):
        rotate_point_x = self.rotate_x
        rotate_point_y = self.rotate_y

        if (self.rotate_x, self.rotate_y) != (center_x, center_y):
            self.rotate_point_new = True
            rotate_point_x = center_x
            rotate_point_y = center_y

        center_x_screen = rotate_point_x * Shape.scale + 320
        center_y_screen = - rotate_point_y * Shape.scale + 310

        x = self.x - center_x_screen
        y = self.y - center_y_screen

        rad = radians(-angle)

        new_x = round(x * cos(rad) - y * sin(rad) + center_x_screen, 2)
        new_y = round(x * sin(rad) + y * cos(rad) + center_y_screen, 2)

        if not (20 <= new_x <= 620 and 10 <= new_y <= 610):
            return False

        if self.rotate_point_new:
            self.rotate_x = rotate_point_x
            self.rotate_y = rotate_point_y
            self.rotate_point_new = False
        self.x = new_x
        self.y = new_y
        self.angle = angle

        return True

    def resize(self, *args):
        self.a = args[0] * Shape.scale

    def draw(self, canvas):
        half_a = self.a / 2
        angle_rad = radians(-self.angle)
        points = [
            (self.x + half_a * cos(angle_rad) - half_a * sin(angle_rad),
             self.y + half_a * sin(angle_rad) + half_a * cos(angle_rad)),  # Верхний правый угол

            (self.x - half_a * cos(angle_rad) - half_a * sin(angle_rad),
             self.y - half_a * sin(angle_rad) + half_a * cos(angle_rad)),  # Верхний левый угол

            (self.x - half_a * cos(angle_rad) + half_a * sin(angle_rad),
             self.y - half_a * sin(angle_rad) - half_a * cos(angle_rad)),  # Нижний левый угол

            (self.x + half_a * cos(angle_rad) + half_a * sin(angle_rad),
             self.y + half_a * sin(angle_rad) - half_a * cos(angle_rad))  # Нижний правый угол
        ]
        canvas.create_polygon(points, fill='', outline='orange', width=2)

    def info(self, index):
        return (f"{index}) Квадрат: x = {round((self.x - 320) / Shape.scale, 3)}, y = {- round((self.y - 310) / Shape.scale, 3)}, "
                f"a = {round(self.a / Shape.scale)}, угол относительно ({self.rotate_x}, {self.rotate_y}) = {self.angle}")


class Rectangle(Shape):
    def __init__(self, points):
        self.a = (abs(points[2] - points[0])) * Shape.scale
        self.b = (abs(points[3] - points[1])) * Shape.scale
        self.x = (points[2] + points[0]) / 2 * Shape.scale + 320
        self.y = (- points[3] - points[1]) / 2 * Shape.scale + 310
        self.angle = 0
        self.rotate_x = round((self.x - 320) / Shape.scale, 2)
        self.rotate_y = - round((self.y - 310) / Shape.scale, 2)
        self.rotate_point_new = False

    def move(self, dx, dy):
        self.x += dx * Shape.scale
        self.y -= dy * Shape.scale
        self.rotate_x = round((self.x - 320) / Shape.scale, 2)
        self.rotate_y = - round((self.y - 310) / Shape.scale, 2)
        self.rotate_point_new = True

    def rotate(self, angle, center_x, center_y):
        rotate_point_x = self.rotate_x
        rotate_point_y = self.rotate_y

        if (self.rotate_x, self.rotate_y) != (center_x, center_y):
            self.rotate_point_new = True
            rotate_point_x = center_x
            rotate_point_y = center_y

        center_x_screen = rotate_point_x * Shape.scale + 320
        center_y_screen = - rotate_point_y * Shape.scale + 310

        x = self.x - center_x_screen
        y = self.y - center_y_screen

        rad = radians(-angle)

        new_x = round(x * cos(rad) - y * sin(rad) + center_x_screen, 2)
        new_y = round(x * sin(rad) + y * cos(rad) + center_y_screen, 2)

        if not (20 <= new_x <= 620 and 10 <= new_y <= 610):
            return False

        if self.rotate_point_new:
            self.rotate_x = rotate_point_x
            self.rotate_y = rotate_point_y
            self.rotate_point_new = False
        self.x = new_x
        self.y = new_y
        self.angle = angle

        return True

    def resize(self, *args):
        self.a = args[0] * Shape.scale
        self.b = args[1] * Shape.scale

    def draw(self, canvas):
        half_a, half_b = self.a / 2, self.b / 2
        angle_rad = radians(-self.angle)
        points = [
            (self.x + half_a * cos(angle_rad) - half_b * sin(angle_rad),
             self.y + half_a * sin(angle_rad) + half_b * cos(angle_rad)), # Верхний правый угол

            (self.x - half_a * cos(angle_rad) - half_b * sin(angle_rad),
             self.y - half_a * sin(angle_rad) + half_b * cos(angle_rad)), # Верхний левый угол

            (self.x - half_a * cos(angle_rad) + half_b * sin(angle_rad),
             self.y - half_a * sin(angle_rad) - half_b * cos(angle_rad)), # Нижний левый угол

            (self.x + half_a * cos(angle_rad) + half_b * sin(angle_rad),
             self.y + half_a * sin(angle_rad) - half_b * cos(angle_rad)) # Нижний правый угол
        ]
        canvas.create_polygon(points, fill='', outline='green', width=2)

    def info(self, index):
        return (f"{index}) Прямоугольник: x = {round((self.x - 320) / Shape.scale, 3)}, y = {- round((self.y - 310) / Shape.scale, 3)}, "
                f"a = {round(self.a / Shape.scale, 3)}, b = {round(self.b / Shape.scale, 3)}, угол относительно ({self.rotate_x}, {self.rotate_y}) = {self.angle}")


class Menu:
    _application_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)

    def __init__(self, form):
        self.form = form
        self.form.title("Редактор фигур")
        self.form.geometry("{}x{}+{}+{}".format(1460, 620, (form.winfo_screenwidth() - 1460) // 2,
                                               (form.winfo_screenheight() - 620) // 2))
        self.form.resizable(False, False)
        self.form.iconbitmap(default=os.path.join(Menu._application_path, 'icon.ico'))
        self.form.bind("<F1>", lambda i: self.__onClickKeyF1())

        self.canvas = Canvas(form, width=650, height=620, bg='white')
        self.canvas.grid(row=0, column=2, rowspan=6)

        Style().configure(style=".", foreground="black", font=('Segoe UI', 13))

        self.menu_frame = Frame()
        self.menu_frame.grid(row=0, column=0, padx=5, pady=5, sticky='n')

        Label(self.menu_frame, text="Меню редактирования:").grid(row=0, column=0, padx=5, pady=5, sticky='n')
        Button(self.menu_frame, text="Добавить круг", command=self.__add_circle).grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        Button(self.menu_frame, text="Добавить квадрат", command=self.__add_square).grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        Button(self.menu_frame, text="Добавить прямоугольник", command=self.__add_rectangle).grid(row=3, column=0, padx=5, pady=5, sticky='ew')
        self.button_move = Button(self.menu_frame, text="Переместить фигуру", command=self.__move)
        self.button_move.grid(row=4, column=0, padx=5, pady=5, sticky='ew')
        self.button_rotate = Button(self.menu_frame, text="Изменить угол поворота", command=self.__rotate)
        self.button_rotate.grid(row=5, column=0, padx=5, pady=5, sticky='ew')
        self.button_resize = Button(self.menu_frame, text="Изменить размер", command=self.__resize)
        self.button_resize.grid(row=6, column=0, padx=5, pady=5, sticky='ew')
        self.button_delete = Button(self.menu_frame, text="Удалить фигуру", command=self.__delete)
        self.button_delete.grid(row=7, column=0, padx=5, pady=5, sticky='ew')

        self.button_move.config(state='disabled')
        self.button_rotate.config(state='disabled')
        self.button_resize.config(state='disabled')
        self.button_delete.config(state='disabled')

        self.shape_frame = Frame()
        self.shape_frame.grid(row=0, column=1, rowspan=6, padx=5, pady=5, sticky='ns')

        Label(self.shape_frame, text="Список фигур:").pack(anchor='n', padx=20, pady=5)
        self.shape_listbox = Listbox(self.shape_frame, width=80, font=('Segoe UI', 10))
        self.shape_listbox.pack(expand=True, fill='both', padx=5, pady=5)

        self.shapes = []

        self.__draw_axes()

    def __draw_axes(self):
        self.canvas.create_line(320, 10, 320, 610, fill='black') # Вертикальная ось
        self.canvas.create_line(20, 310, 620, 310, fill='black') # Горизонтальная ось
        self.canvas.create_text(335, 10, text='Y', fill='black')
        self.canvas.create_text(635, 310, text='X', fill='black')
        self.canvas.create_text(315, 320, text='0', fill='black')

        scale = 30 # масштаб поля: 1 единица = 30 пикселей
        for i in range(-10, 11):
            if i != 0: # сетка
                self.canvas.create_line(20, 310 - i * scale, 620, 310 - i * scale, fill='lightgray')
                self.canvas.create_line(320 + i * scale, 10, 320 + i * scale, 610, fill='lightgray')

            self.canvas.create_line(315, 310 - i * scale, 325, 310 - i * scale, fill='black') # Риска Y
            self.canvas.create_line(320 + i * scale, 305, 320 + i * scale, 315, fill='black') # Риска X

            if i != 0:
                self.canvas.create_text(300, 310 - i * scale, text=str(i), fill='black') # Подпись Y
                self.canvas.create_text(320 + i * scale, 325, text=str(i), fill='black') # Подпись X

    def __update_listbox(self):
        self.shape_listbox.delete(0, END)
        for i in range(len(self.shapes)):
            self.shape_listbox.insert(i + 1, self.shapes[i].info(i + 1))

        status = 'normal' if self.shapes else 'disabled'
        self.button_move.config(state=status)
        self.button_rotate.config(state=status)
        self.button_resize.config(state=status)
        self.button_delete.config(state=status)

    def __screen_message(self, title, label, action = None):
        def __screen_message_function():
            if action == 'Move':        __shape_move()
            elif action == 'Rotate':    __shape_rotate()
            elif action == 'Resize':    __shape_resize()
            elif action == 'Circle':    __shape_circle()
            elif action == 'Square':    __shape_square()
            elif action == 'Rectangle': __shape_rectangle()
            else:                       __shape_delete()

        def __shape_circle():
            try:
                point = tuple(map(float, entry_a.get().split()))
                if len(point) != 2:
                    messagebox.showerror("Некорректные координаты", "Точка должна состоять из 2 координат!")
                    return
                radius = float(entry_b.get())
                if 0 < radius <= 20 and -10 <= point[0] <= 10 and -10 <= point[1] <= 10:
                    __final(Circle(radius, point))
                else:
                    messagebox.showerror("Некорректный радиус и/или центр круга", "Радиус должен быть больше 0 и не превышать 20 клеток, а точка - в диапазоне от -10 до 10!")
            except ValueError:
                messagebox.showerror("Некорректный ввод", "Введите целые числа без спец. символов!")
            finally:
                return

        def __shape_square():
            try:
                points = tuple(map(float, entry_a.get().split())) + tuple(map(float, entry_b.get().split()))
                if len(points) != 4:
                    messagebox.showerror("Некорректные координаты", "Точки должны состоять из 2 координат!")
                    return
                for i in points:
                    if not (-10 <= i <= 10):
                        messagebox.showerror("Некорректные координаты", "Точки должны быть в диапазоне от -10 до 10!")
                        return
                if points[2] != points[0] and points[3] != points[1] and abs(points[2] - points[0]) == abs(points[3] - points[1]):
                    __final(Square(points))
                else:
                    messagebox.showerror("Некорректные координаты", "Расстояние по X и Y между точками должно быть одинаковым, при этом точки должны лежать на разных вертикальных и горизонтальных прямых!")
            except ValueError:
                messagebox.showerror("Некорректный ввод", "Введите целые числа или вещественные числа с точкой!")
            finally:
                return

        def __shape_rectangle():
            try:
                points = tuple(map(float, entry_a.get().split())) + tuple(map(float, entry_b.get().split()))
                if len(points) != 4:
                    messagebox.showerror("Некорректные координаты", "Точки должны состоять из 2 координат!")
                    return
                for i in points:
                    if not (-10 <= i <= 10):
                        messagebox.showerror("Некорректные координаты", "Точки должны быть в диапазоне от -10 до 10!")
                        return
                if points[2] != points[0] and points[3] != points[1]:
                    __final(Rectangle(points))
                else:
                    messagebox.showerror("Некорректные координаты", "Точки должны лежать на разных вертикальных и горизонтальных прямых!")
            except ValueError:
                messagebox.showerror("Некорректный ввод", "Введите целые числа или вещественные числа с точкой!")
            finally:
                return
        
        def __shape_move():
            try:
                index = int(entry_id.get())
                if 0 < index <= len(self.shapes):
                    figure = self.shapes[index - 1]
                    dx, dy = float(entry_a.get()), float(entry_b.get())
                    if -10 <= (figure.x - 320) / 30 + dx <= 10 and -10 <= (figure.y - 310) / 30 - dy <= 10:
                        figure.move(dx, dy)
                        __final(figure)
                    else:
                        messagebox.showerror("Некорректное смещение", "Смещение не должно превышать диапазон сетки от -10 до 10 клеток!")
                else:
                    messagebox.showerror("Некорректный номер в списке", "Введите существующий номер из списка фигур!")
            except ValueError:
                messagebox.showerror("Некорректный ввод", "Введите номер в списке целым числом, а также смещение позиции целыми числа или вещественными числами позиций с точкой!")
            finally:
                return

        def __shape_rotate():
            try:
                index = int(entry_id.get())
                if 0 < index <= len(self.shapes):
                    figure = self.shapes[index - 1]
                    try:               center_x = float(entry_a.get())
                    except ValueError: center_x = figure.rotate_x
                    try:               center_y = float(entry_b.get())
                    except ValueError: center_y = figure.rotate_y
                    if -10 <= center_x <= 10 and -10 <= center_y <= 10:
                        angle = float(entry_c.get())
                        if figure.rotate(angle, center_x, center_y):
                            __final(figure)
                        else:
                            messagebox.showerror("Некорректный поворот", "Центр фигуры должен оставаться в поле сетки!")
                    else:
                        messagebox.showerror("Некорректная точка поворота", "Координаты точки поворота не должны превышать диапазон сетки от -10 до 10 клеток!")
                else:
                    messagebox.showerror("Некорректный номер в списке", "Введите существующий номер из списка фигур!")
            except ValueError:
                messagebox.showerror("Некорректный ввод", "Введите номер в списке целым числом, а также градусы и точку поворота целымм числами или вещественнымм числами с точкой!")
            finally:
                return

        def __shape_resize():
            try:
                index = int(entry.get())
                if 1 <= index <= len(self.shapes):
                    formDialog.destroy()
                    self.__screen_message_resize(self.shapes[index - 1], index - 1)
                else:
                    messagebox.showerror("Некорректный номер в списке", "Введите существующий номер из списка фигур!")
            except ValueError:
                messagebox.showerror("Некорректный ввод", "Введите номер в списке целым числом!")
            finally:
                return

        def __shape_delete():
            try:
                index = int(entry.get())
                if 1 <= index <= len(self.shapes):
                    figure = self.shapes[index - 1]
                    __final(figure)
                else:
                    messagebox.showerror("Некорректный номер в списке", "Введите существующий номер из списка фигур!")
            except ValueError:
                messagebox.showerror("Некорректный ввод", "Введите номер в списке целым числом!")
            finally:
                return
                
        def __final(figure):
            if action == 'Delete':
                self.shapes.remove(figure)
            elif action not in ('Move', 'Rotate'):
                self.shapes.append(figure)
            self.__update_listbox()
            self.__redraw()
            formDialog.destroy()

        if action == 'Rotate':               x, y = 720, 250
        elif action == 'Move':               x, y = 400, 200
        elif action in ('Delete', 'Resize'): x, y = 320, 150
        else:                                x, y = 500, 150

        formDialog = Toplevel(self.form)
        formDialog.title(title)
        formDialog.geometry("{}x{}+{}+{}".format(x, y, (formDialog.winfo_screenwidth() - x) // 2,
                                                 (formDialog.winfo_screenheight() - y) // 2))
        formDialog.resizable(False, False)
        formDialog.protocol("WM_DELETE_WINDOW", lambda: formDialog.destroy())
        formDialog.grab_set()

        Label(formDialog, text=label, font=('Helvetica', 14)).grid(row=0, column=0, columnspan=2, pady=5, sticky='n')

        if action not in ('Delete', 'Resize'):
            if action in ('Move', 'Rotate'):
                Label(formDialog, text="номер фигуры из списка = ", font=('Helvetica', 14)).grid(row=1, column=0, pady=5, sticky='e')
                entry_id = Entry(formDialog, font=('Helvetica', 14), width=10)
                entry_id.grid(row=1, column=1, pady=5, sticky='w')
                row_a = 2
                row_b = 3
            else:
                row_a = 1
                row_b = 2

            if action == 'Circle':
                text_a = "Координаты центра = "
                text_b = "Радиус = "
            elif action in ('Square', 'Rectangle'):
                text_a = "Координаты 1 точки = "
                text_b = "Координаты 2 точки = "
            elif action == 'Move':
                text_a = "dx = "
                text_b = "dy = "
            else:
                text_a = "координата X точки поворота = "
                text_b = "координата Y точки поворота = "

            Label(formDialog, text=text_a, font=('Helvetica', 14)).grid(row=row_a, column=0, pady=5, sticky='e')
            entry_a = Entry(formDialog, font=('Helvetica', 14), width=10)
            entry_a.grid(row=row_a, column=1, pady=5, sticky='w')

            Label(formDialog, text=text_b, font=('Helvetica', 14)).grid(row=row_b, column=0, pady=5, sticky='e')
            entry_b = Entry(formDialog, font=('Helvetica', 14), width=10)
            entry_b.grid(row=row_b, column=1, pady=5, sticky='w')

            if action == 'Rotate':
                Label(formDialog, text="кол-во градусов относительно точки = ", font=('Helvetica', 14)).grid(row=4, column=0, pady=5, sticky='e')
                entry_c = Entry(formDialog, font=('Helvetica', 14), width=10)
                entry_c.grid(row=4, column=1, pady=5, sticky='w')
        else:
            entry = Entry(formDialog, font=('Helvetica', 14), width=10)
            entry.grid(row=1, column=0, columnspan=2, pady=5, sticky='n')

        row_button = 3 if action not in ('Move', 'Rotate') else 4 if action != 'Rotate' else 5
        Button(formDialog, text="OK", command=__screen_message_function).grid(row=row_button, column=0, padx=5, pady=10, sticky='nsew')
        Button(formDialog, text="Отмена", command=formDialog.destroy).grid(row=row_button, column=1, padx=5, pady=10, sticky='nsew')

        # Центрирование
        rows = (0, 1, 2) if action in ('Delete', 'Resize') else (0, 1, 2, 3) if action not in ('Move', 'Rotate') else (0, 1, 2, 3, 4) if action != 'Rotate' else (0, 1, 2, 3, 4, 5)
        for i in rows:
            if i < 2: formDialog.grid_columnconfigure(i, weight=1)
            formDialog.grid_rowconfigure(i, weight=1)

        formDialog.mainloop()

    def __screen_message_resize(self, figure, figure_id):
        def __shape_resize():
            nonlocal cond_circle, cond_square
            try:
                if cond_circle:
                    radius = float(entry_a.get())
                    if 0 < radius <= 20:
                        self.shapes[figure_id].radius = radius * Shape.scale
                    else:
                        messagebox.showerror("Некорректный радиус и/или центр круга", "Радиус должен быть больше 0 и не превышать 20 клеток, а точка - в диапазоне от -10 до 10!")
                        return
                elif cond_square:
                    new_a = float(entry_a.get())
                    if 0 < new_a <= 20:
                        self.shapes[figure_id].a = new_a * Shape.scale
                    else:
                        messagebox.showerror("Некорректная сторона", "Сторона должна быть больше 0 и не превышать 20 клеток!")
                        return
                else:
                    new_a, new_b = float(entry_a.get()), float(entry_b.get())
                    if 0 < new_a <= 20 and 0 < new_b <= 20:
                        self.shapes[figure_id].a = new_a * Shape.scale
                        self.shapes[figure_id].b = new_b * Shape.scale
                    else:
                        messagebox.showerror("Некорректные стороны", "Стороны должны быть больше 0 и не превышать 20 клеток!")
                        return
                __final()
            except ValueError:
                messagebox.showerror("Некорректный ввод", "Введите номер в списке целым числом!")
            finally:
                return
        
        def __final():
            self.__update_listbox()
            self.__redraw()
            formDialogResize.destroy()

        cond_circle, cond_square, cond_rectangle = isinstance(figure, Circle), isinstance(figure, Square), isinstance(figure, Rectangle)

        if cond_rectangle: x, y = 450, 150
        else:              x, y = 350, 100

        formDialogResize = Toplevel(self.form)
        formDialogResize.title("Новые размеры фигуры")
        formDialogResize.geometry("{}x{}+{}+{}".format(x, y, (formDialogResize.winfo_screenwidth() - x) // 2,
                                                             (formDialogResize.winfo_screenheight() - y) // 2))
        formDialogResize.resizable(False, False)
        formDialogResize.protocol("WM_DELETE_WINDOW", lambda: formDialogResize.destroy())
        formDialogResize.grab_set()

        text_label = "Новый радиус круга: " if cond_circle else "Новая длина квадрата: " if cond_square else "Новая ширина прямоугольника (a): "

        Label(formDialogResize, text=text_label, font=('Helvetica', 14)).grid(row=0, column=0, pady=5, sticky='e')
        entry_a = Entry(formDialogResize, font=('Helvetica', 14), width=10)
        entry_a.grid(row=0, column=1, pady=5, sticky='w')

        if cond_rectangle:
            Label(formDialogResize, text="Новая высота прямоугольника (b): ", font=('Helvetica', 14)).grid(row=1, column=0, pady=5, sticky='e')
            entry_b = Entry(formDialogResize, font=('Helvetica', 14), width=10)
            entry_b.grid(row=1, column=1, pady=5, sticky='w')

        row_button = 2 if cond_rectangle else 1

        Button(formDialogResize, text="OK", command=__shape_resize).grid(row=row_button, column=0, padx=5, pady=10, sticky='nsew')
        Button(formDialogResize, text="Отмена", command=formDialogResize.destroy).grid(row=row_button, column=1, padx=5, pady=10, sticky='nsew')

        # Центрирование
        for i in range(2):
            formDialogResize.grid_rowconfigure(i, weight=1)
            formDialogResize.grid_columnconfigure(i, weight=1)
        if cond_rectangle:
            formDialogResize.grid_rowconfigure(2, weight=1)

        formDialogResize.mainloop()

    def __add_circle(self):
        self.__screen_message("Круг", "Введите радиус и коордианты центра через пробел:", 'Circle')

    def __add_square(self):
        self.__screen_message("Квадрат", "Введите коордианты двух точек через пробел в каждой:", 'Square')

    def __add_rectangle(self):
        self.__screen_message("Прямоугольник", "Введите коордианты двух точек через пробел в каждой:", 'Rectangle')

    def __move(self):
        self.__screen_message("Перемещение", "Введите номер фигуры и её смещение:", 'Move')

    def __rotate(self):
        self.__screen_message("Поворот", "Введите градусы угла и точку поворота (при отсутствии используется из списка):", 'Rotate')

    def __resize(self):
        self.__screen_message("Изменение размера", "Введите номер фигуры:", 'Resize')
    
    def __delete(self):
        self.__screen_message("Удаление", "Введите номер фигуры:", 'Delete')

    def __redraw(self):
        self.canvas.delete("all")
        self.__draw_axes()
        for shape in self.shapes:
            shape.draw(self.canvas)

    def __onClickKeyF1(self):
        def onCloseFormRef(): formRef.destroy()

        formRef = Toplevel()
        formRef.geometry("{}x{}+{}+{}".format(425, 115, (formRef.winfo_screenwidth() - 425) // 2,
                                              (formRef.winfo_screenheight() - 115) // 2))
        formRef.resizable(False, False)
        formRef.title('О программе')
        formRef.iconbitmap(default=os.path.join(Menu._application_path, 'icon.ico'))
        Label(formRef, text="Редактор фигур - версия 1.0.\n© KitsuruDev, 2025. Все права защищены",
              font=('Segoe UI', 16)).place(x=8, y=8, width=400, height=92)
        formRef.protocol("WM_DELETE_WINDOW", onCloseFormRef)
        formRef.grab_set()
        formRef.mainloop()


if __name__ == "__main__":
    formMain = Tk()
    app = Menu(formMain)
    formMain.mainloop()