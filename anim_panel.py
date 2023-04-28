from dearpygui import dearpygui as dpg
from time import sleep, process_time_ns
import threading


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

        self.current_frame = None
        self.is_playing = False
        self.last_time = process_time_ns() // 1000000
        self.elapsed = 0
        self.updater = None

        with dpg.drawlist(pos=(0, 0), width=800, height=600) as self.canvas:
            self.canvas_bg = dpg.draw_rectangle((0, 0), (300, 300), fill=(60, 60, 60), tag="canvas_bg")

        with dpg.group(horizontal=True) as self.buttons:
            dpg.add_button(label="prev", parent=self.buttons)
            dpg.add_button(label="stop", parent=self.buttons)
            self.btn_play = dpg.add_button(label="Play", callback=self.play_stop, parent=self.buttons)
            dpg.add_button(label="next", parent=self.buttons)

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
        buttons_height = 20
        canvas_height = height - buttons_height - slider_height - 40
        buttons_y = canvas_height - 10
        slider_y = buttons_y + buttons_height + 5
        dpg.configure_item(self.canvas,
                           pos=(0, 0),
                           width=width - padding,
                           height=canvas_height - padding
                           )

        dpg.configure_item(self.buttons,
                           pos=(200, buttons_y),
                           # width=width - padding
                           )
        dpg.configure_item(self.canvas_bg,
                           pmin=(0, 0),
                           pmax=(width - padding, canvas_height),
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

    def start_play(self):
        if self.is_playing:
            return

        dpg.configure_item(self.btn_play, label="||")

        self.is_playing = True
        self.updater = threading.Thread(target=self.on_update)
        self.updater.start()

    def play_stop(self):
        if self.is_playing:
            self.stop_play()
        else:
            self.start_play()

    def stop_play(self):
        if not self.is_playing:
            return
        self.is_playing = False
        dpg.configure_item(self.btn_play, label="Play")

    def close(self):
        self.is_playing = False
        self.updater.join()

    def on_update(self):
        while self.is_playing:
            sleep(0)
            ntime = process_time_ns() // 1000000
            delta = ntime - self.last_time
            if delta > (1000.0 / 60):
                self.last_time = ntime
                self.elapsed += delta
                frame = self.elapsed // 30
                if self.current_frame != frame:
                    self.current_frame = frame
                    self.on_frame(frame)

    def on_frame(self, frame):
        self.set_frame(frame)
