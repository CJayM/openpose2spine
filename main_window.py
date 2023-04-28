from dearpygui import dearpygui as dpg
import threading

from anim_panel import AnimPanel
from app import BaseApp
from time import sleep, process_time_ns


class MainWindow(BaseApp):
    def __init__(self, *args, **kwargs):
        self.anim_panel = None
        self.btn_play = None
        self.second_wnd = None
        self.current_frame = None
        self.elapsed_text = None
        self.elapsed = 0
        self.score_text = None
        self.skeletal = None
        self.window = None
        self.layout = None

        self.is_playing = False
        self.animation_updates = 0
        self.elapsed = 0
        self.updater = None
        self.last_time = process_time_ns() // 1000000

        super().__init__(*args, **kwargs)

        with dpg.font_registry():
            with dpg.font("DroidSans.ttf", 16) as font1:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

        dpg.bind_font(font1)
        # dpg.configure_app(load_init_file="open_pose_app.ini")

    def start_play(self):
        if self.is_playing:
            return

        dpg.configure_item(self.btn_play, label="Stop")

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

    def update_second_layout(self):
        full_width = dpg.get_viewport_width()
        full_height = dpg.get_viewport_height()
        item_cfg = dpg.get_item_configuration(self.window)
        second_pos = (item_cfg["width"], 0)
        second_width = full_width - item_cfg["width"]
        dpg.configure_item(self.second_wnd, pos=second_pos, width=second_width, height=full_height)

        self.anim_panel.resize(second_width, full_height)

    def on_parent_resize(self):
        self.update_second_layout()

    def init_ui(self):
        with dpg.window(tag="root", no_scrollbar=True, no_title_bar=True, no_close=True,
                        pos=(0, 0), width=300, no_move=True) as left_window:
            self.window = left_window

            with dpg.group(horizontal=True, tag="anim_buttons_group"):
                self.btn_play = dpg.add_button(label="Play", callback=self.play_stop)

            with dpg.group():
                with dpg.group(horizontal=True, horizontal_spacing=0.3):
                    self.score_text = dpg.add_text(default_value="delta")
                    self.elapsed_text = dpg.add_text(default_value="elapsed")
                with dpg.group(horizontal=True, horizontal_spacing=0.3):
                    dpg.add_button(label="Save Ini File",
                                   callback=lambda: dpg.save_init_file("custom_layout.ini"))

        with dpg.window(tag="second", pos=(300, 0), width=100, height=200, no_title_bar=True, no_scrollbar=True,
                        no_close=True,
                        no_move=True, no_resize=True, no_bring_to_front_on_focus=True) as second_wnd:
            self.second_wnd = second_wnd
            self.anim_panel = AnimPanel(800, 600, parent=self.second_wnd)

            with dpg.item_handler_registry(tag="left_panel_handler") as handler:
                dpg.add_item_resize_handler(callback=self.on_parent_resize)

            dpg.bind_item_handler_registry("root", "left_panel_handler")

    def set_skeletal(self, skeletal):
        self.skeletal = skeletal
        self.anim_panel.set_skeletal(skeletal)

    def set_animation(self, animation):
        self.anim_panel.set_animation(animation)

    def on_resize(self, id, rect):
        full_height = dpg.get_viewport_height()
        dpg.configure_item(self.window, height=full_height)
        self.update_second_layout()

    def on_frame(self, frame):
        self.anim_panel.set_frame(frame)

        # draw edges
        # for i in range(NUM_EDGES):
        #     edge = EDGES_INDEXES[i]
        #     pos1 = get_bone_pos(edge[0], frame, frames)
        #     pos2 = get_bone_pos(edge[1], frame, frames)
        #     if pos1 and pos2:
        #         pygame.draw.line(window, EDGE_COLORS[i], pos1, pos2, 5)
        #
        # # draw points
        # for i in range(NUM_POINTS):
        #     coord = get_bone_pos(i, frame, frames)
        #     color = BONE_COLORS[i]
        # if coord:
        # tag = "root node"
        # tag = "bone_{}".format(i)
        # dpg.apply_transform(tag, dpg.create_translation_matrix(coord))

        # dpg.apply_transform("planet node 1", dpg.create_rotation_matrix(math.pi * planet1_angle / 180.0,
        #                                                                 [0, 0, -1]) * dpg.create_translation_matrix(
        #     [planet1_distance, 0]))

    def on_draw(self, delta: float):
        pass
