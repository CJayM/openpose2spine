from dearpygui import dearpygui as dpg


class AnimPanel:
    def __init__(self, width, height, parent=None):
        self.animation = None
        self.skeletal = None
        self.width = width
        self.height = height
        self.parent = parent
        self.canvas = None
        self.canvas_bg = None
        self.bone_ids = []

        with dpg.drawlist(pos=(0, 0), width=800, height=600) as self.canvas:
            self.canvas_bg = dpg.draw_rectangle((0, 0), (300, 300), fill=(60, 60, 60), tag="canvas_bg")

        self.time_slider = dpg.add_slider_int(default_value=0, min_value=0, max_value=100, indent=0, width=100,
                                              callback=self.set_current_frame
                                              )

    def set_skeletal(self, skeletal):
        self.skeletal = skeletal
        for i in range(skeletal.bones_count):
            with dpg.draw_node(parent=self.canvas) as bone:
                self.bone_ids.append(bone)
                dpg.draw_circle((0, 0), 5, fill=skeletal.get_color(i))

    def resize(self, width, height):
        self.width = width
        self.height = height

        padding = 20
        slider_height = 20
        slider_y = height - slider_height - padding - padding - 5
        dpg.configure_item(self.canvas,
                           pos=(0, 0),
                           width=width - padding,
                           height=height
                           )

        dpg.configure_item(self.canvas_bg,
                           pmin=(0, 0),
                           pmax=(width - padding - padding, slider_y - 10),
                           color=(0, 0, 0)
                           )

        dpg.configure_item(self.time_slider,
                           pos=(0, slider_y),
                           width=width - padding,
                           height=slider_height
                           )

    def set_animation(self, animation):
        self.animation = animation
        dpg.configure_item(self.time_slider, min_value=0, max_value=animation.frames_count - 1)

    def set_frame(self, frame):
        frame = frame % self.animation.frames_count
        dpg.set_value(self.time_slider, frame)

        frame_data = self.animation.frames[frame]
        for i in range(self.skeletal.bones_count):
            pos = frame_data[i]
            dpg.apply_transform(self.bone_ids[i], dpg.create_translation_matrix(pos))

    def set_current_frame(self, a, b, c):
        print("SET", a, b, c)
