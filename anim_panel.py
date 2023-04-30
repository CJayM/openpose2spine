from dearpygui import dearpygui as dpg
from time import sleep, process_time_ns
import threading

import assets
from assets import IconCode, get_themes


def toggle_item(id):
    user_data = dpg.get_item_user_data(id)
    theme1, theme2, is_toggled = user_data
    is_toggled = not is_toggled
    dpg.configure_item(id, user_data=(theme1, theme2, is_toggled))
    dpg.bind_item_theme(id, theme1 if not is_toggled else theme2)


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
        self.dial_plate = None
        self.dial_plate_items = []

        with dpg.drawlist(pos=(0, 0), width=800, height=600) as self.canvas:
            self.canvas_bg = dpg.draw_rectangle((0, 0), (300, 300), fill=(60, 60, 60), tag="canvas_bg")

        theme = get_themes()
        with dpg.group(horizontal=True) as self.buttons:
            self.btn_go_start = dpg.add_button(label=chr(IconCode.backward_fast), parent=self.buttons, width=20,
                                               height=20)
            self.btn_step_prev = dpg.add_button(label=chr(IconCode.backward_step), parent=self.buttons, width=20,
                                                height=20)
            self.btn_stop = dpg.add_button(label="", parent=self.buttons, width=20, height=20)
            self.btn_play = dpg.add_button(label="", callback=self.play_stop, parent=self.buttons
                                           , user_data=(theme.primary_button, theme.primary_button_toggled, False),
                                           width=20, height=20)
            self.btn_step_next = dpg.add_button(label=chr(IconCode.forward_step), parent=self.buttons, width=20,
                                                height=20)
            self.btn_go_end = dpg.add_button(label=chr(IconCode.forward_fast), parent=self.buttons, width=20, height=20)
            self.btn_cycle = dpg.add_button(label=chr(IconCode.arrows_repeat), parent=self.buttons,
                                            callback=self.toggle_repeat,
                                            user_data=(theme.secondary_button, theme.secondary_button_toggled, False),
                                            width=20, height=20)

            self.buttons_ids = [self.btn_go_start, self.btn_step_prev, self.btn_stop, self.btn_play, self.btn_step_next,
                                self.btn_go_end, self.btn_cycle]
            for id in self.buttons_ids:
                dpg.bind_item_font(id, assets.ICONS_FONT)

            dpg.bind_item_theme(self.btn_play, theme.primary_button)
            dpg.bind_item_theme(self.btn_cycle, theme.secondary_button)

            self.time_slider = dpg.add_slider_int(default_value=0, min_value=0, max_value=100, indent=0, width=-1,
                                                  callback=self.set_current_frame
                                                  )

        with dpg.drawlist(pos=(10, 10), width=800, height=20, ) as self.dial_plate:
            self.dial_plate_bg = dpg.draw_rectangle((0, 0), (846, 20), fill=(47, 47, 50), color=(47, 47, 50))

        with dpg.item_handler_registry(tag="anim_panel_handler") as self.anim_panel_handler:
            dpg.add_item_hover_handler(callback=self.on_hover)
            dpg.add_item_focus_handler(callback=self.on_focus)
            dpg.add_item_active_handler(callback=self.on_active)
            dpg.add_item_activated_handler(callback=self.on_activated)
            dpg.add_item_deactivated_handler(callback=self.on_deactivated)
            dpg.add_item_toggled_open_handler(callback=self.on_toggled_open)

        dpg.bind_item_handler_registry(self.time_slider, "anim_panel_handler")

    def toggle_repeat(self, id, data, user_data):
        toggle_item(id)

    def on_hover(self, a, b, c):
        pass
        # print("On Hover", a, b, c)

    def on_focus(self, a, b, c):
        pass
        # print("On Focus", a, b, c)

    def on_active(self, a, b, c):
        pass
        # print("On Active", a, b, c)

    def on_activated(self, a, b, c):
        print("On Activeted", a, b, c)

    def on_deactivated(self, a, b, c):
        print("On Deactiveted", a, b, c)

    def on_toggled_open(self, a, b, c):
        print("On Toggled Open", a, b, c)

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
        buttons_y = canvas_height - 10 + 2
        slider_y = buttons_y + buttons_height + 5
        dpg.configure_item(self.canvas,
                           pos=(0, 0),
                           width=width - padding,
                           height=canvas_height - padding
                           )

        pad = 6
        x = 0
        for id in self.buttons_ids:
            dpg.configure_item(id, pos=(x, buttons_y))
            x += 22
        dpg.configure_item(self.time_slider,
                           pos=(x + pad, buttons_y),
                           width=width - padding - pad - x,
                           height=slider_height
                           )
        dial_plate_width = width - x - padding - pad

        self.update_dial_plate((x, buttons_y), dial_plate_width)
        dpg.configure_item(self.canvas_bg,
                           pmin=(0, 0),
                           pmax=(width - padding, canvas_height),
                           color=(0, 0, 0)
                           )

    def update_dial_plate(self, pos, width):
        pad = 6
        x = pos[0]

        dpg.delete_item(self.dial_plate, children_only=True)
        dpg.configure_item(self.dial_plate,
                           pos=(x + pad, pos[1]),
                           width=width + x,
                           height=20
                           )
        count = self.animation.frames_count

        step = width / count
        frame_width = 1
        for i in range(count):
            item = dpg.draw_rectangle(pmin=(x + step * i + frame_width/2, 0), pmax=(x + step * i + frame_width + frame_width/2, 20),
                                      parent=self.dial_plate,
                                      fill=(127, 127, 127, 50), color=(255, 255, 255, 0))
            self.dial_plate_items.append(item)

        for i in range(0, count, 5):
            item = dpg.draw_rectangle(pmin=(x + step * i + frame_width/2, 0), pmax=(x + step * i + frame_width + frame_width/2, 20),
                                      parent=self.dial_plate,
                                      fill=(180, 160, 160, 50), color=(255, 255, 255, 0))
            self.dial_plate_items.append(item)
            item = dpg.draw_text((x + step * i, 0), str(i), parent=self.dial_plate, size=12)
            self.dial_plate_items.append(item)
        if count % 5 != 0:
            item = dpg.draw_rectangle(pmin=(x + step * count + frame_width/2, 0), pmax=(x + step * count + frame_width + frame_width/2, 20),
                                      parent=self.dial_plate,
                                      fill=(180, 160, 160, 50), color=(255, 255, 255, 0))
            self.dial_plate_items.append(item)

            item = dpg.draw_text((x + step * count - 6, 0), str(count), parent=self.dial_plate, size=12)
            self.dial_plate_items.append(item)

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

    def set_current_frame(self, a, frame, c):
        # print("SET", a, frame, c)
        self.elapsed = frame * 30
        self.set_frame(frame)

    def start_play(self):
        if self.is_playing:
            return

        dpg.configure_item(self.btn_play, label="")
        toggle_item(self.btn_play)
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
        dpg.configure_item(self.btn_play, label="")
        toggle_item(self.btn_play)

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
