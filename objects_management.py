import math
import random


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius


class ObjectManager:
    def __init__(self, canvas, window_width, window_height, object_num, object_radius,
                 should_generate_start_stop = None, start_stop_distance = None):
        self.canvas = canvas
        self.window_width = window_width
        self.window_height = window_height
        self.object_num = object_num  # object number
        self.object_radius = object_radius
        self.objects = []  # store all objects
        self.object_tag_in_canvas = []  # store the tag of the objects in canvas
        self.last_selected_object_index = -1
        self.should_generate_start_stop = should_generate_start_stop
        self.start_stop_distance = start_stop_distance

    def update_object(self, object_index):
        if object_index >= 0:  # a target has been selected
            if self.last_selected_object_index != object_index:
                last_object_tag = self.object_tag_in_canvas[self.last_selected_object_index]
                # update object according to their tag
                if self.last_selected_object_index ==  0:
                    self.canvas.itemconfig(last_object_tag, fill="blue", width=0)
                elif self.last_selected_object_index == 1:
                    self.canvas.itemconfig(last_object_tag, fill="red", width=0)
                else:
                    self.canvas.itemconfig(last_object_tag, fill="green", width=0)
                self.last_selected_object_index = object_index

                # object_tag is used to find the object in canvas, so that we can update the object
                object_tag = self.object_tag_in_canvas[object_index]
                self.canvas.itemconfig(object_tag, fill="pink", outline="gray", width=4)  # red indicates the selected target
        else:  # no target has been selected, we change the previously selected target to green
            last_object_tag = self.object_tag_in_canvas[self.last_selected_object_index]
            # update object according to their tag
            self.canvas.itemconfig(last_object_tag, fill="green", width=0)
            self.last_selected_object_index = object_index

    def paint_objects(self, color, objects):
        for t in objects:
            tag = self.canvas.create_oval(t.x - t.radius, t.y - t.radius, t.x + t.radius, t.y + t.radius, fill=color,
                                          outline=color, width=0)
            # add object's tag to the list, so they can be accessed according to their tag
            # note that objects are indexed in the same order in both objects and object_tag_in_canvas lists
            self.object_tag_in_canvas.append(tag)

    def generate_random_targets(self):
        if self.should_generate_start_stop:
            start_object = Circle(self.object_radius, self.window_height-self.object_radius, self.object_radius)
            self.objects.append(start_object)
            self.paint_objects("blue" , [start_object])
            is_in_frame = False
            stop_object = None
            while not is_in_frame:
                stop_object = Circle(start_object.x + self.start_stop_distance * math.sin(math.radians(random.randint(0 , 360))),
                                     start_object.y + self.start_stop_distance * math.cos(math.radians(random.randint(0 , 360))),
                                     self.object_radius)
                is_in_frame = self.is_in_frame(stop_object.x, stop_object.y)
            self.objects.append(stop_object)
            self.paint_objects("red" , [stop_object])

        i = 2
        distractor_objects = []
        while i < self.object_num + 2:
            new_object = Circle(random.randint(self.object_radius, self.window_width - self.object_radius),
                                random.randint(self.object_radius, self.window_height - self.object_radius),
                                self.object_radius)
            overlap = False
            for j in self.objects:
                if self.check_two_targets_overlap(new_object, j):
                    overlap = True
                    break

            for j in distractor_objects:
                if self.check_two_targets_overlap(new_object, j):
                    overlap = True
                    break

            if not overlap:  # if the new object does not overlap with others, add it to the objects list.
                distractor_objects.append(new_object)
                i += 1

        self.paint_objects("green", distractor_objects)
        self.objects.extend(distractor_objects)
        print(self.objects)
        return self.objects

    def is_in_frame(self, x, y):
        if self.object_radius <= x <= (self.window_width - self.object_radius) and self.object_radius <= y <= (self.window_height - self.object_radius):
            return True
        return False


    def check_two_targets_overlap(self, t1, t2):
        if math.hypot(t1.x - t2.x, t1.y - t2.y) > (t1.radius + t2.radius):
            return False
        else:
            return True

    def change_target_color(self, object_index):
        object_tag = self.object_tag_in_canvas[object_index]
        self.canvas.itemconfig(object_tag, fill="yellow", width=0)


    # def _euclidean_distance(self, point_1, point_2):
    #     return math.hypot(point_1.x - point_2.x,
    #                       point_1.y - point_2.y)
