import tkinter as tk
import area_cursor
import objects_management as om


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)  # Call tk.Frame.__init__(master)
        self.master = master  # Update the master object after tk.Frame() makes necessary changes to it
        window_width = 1500
        window_height = 800
        self.canvas = tk.Canvas(self.master, width=window_width, height=window_height)
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.mouse_left_button_press)
        self.canvas.bind("<Motion>", self.mouse_move)

        object_num = 20  # object total number
        object_radius = 20  # object radius
        self.object_manage = om.ObjectManager(self.canvas, window_width, window_height, object_num, object_radius, True, 40)
        objects = self.object_manage.generate_random_targets()

        self.cursor = area_cursor.AreaCursor(self.canvas, objects)
        self.object_index = 0

    def mouse_left_button_press(self, event):
        self.cursor.update_cursor(event.x, event.y)
        self.object_index = self.cursor.get_selected_object()
        print(self.object_index)  # print the index of the selected object
        self.object_manage.change_target_color(self.object_index)

    def mouse_move(self, event):
        self.cursor.update_cursor(event.x, event.y)

        self.object_index = self.cursor.get_selected_object()
        self.object_manage.update_object(self.object_index)


if __name__ == '__main__':
    master = tk.Tk()
    master.config(cursor="none")  # hid cursor in canvas
    master.resizable(0, 0)
    app = Application(master=master)
    app.mainloop()  # mainloop() tells Python to run the Tkinter event loop. This method listens for events, such as button clicks or key-presses, and blocks any code that comes after it from running until the window it's called on is closed.
