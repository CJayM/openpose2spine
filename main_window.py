from dearpygui import dearpygui as dpg

from app import BaseApp


class MainWindow(BaseApp):
    def __init__(self, *args, **kwargs):
        self.frame_slider = None
        self.animation = None
        self.elapsed_text = None
        self.fps_text = None
        self.elapsed = 0
        self.score_text = None
        self.bone_ids = []
        self.canvas = None
        self.skeletal = None
        self.autoplay = True
        self.window = None
        self.layout = None

        super().__init__(*args, **kwargs)

        with dpg.font_registry():
            with dpg.font("DroidSans.ttf", 16) as font1:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

        dpg.bind_font(font1)
        # dpg.configure_app(load_init_file="open_pose_app.ini")

    def update_second_layout(self):
        full_width = dpg.get_viewport_width()
        full_height = dpg.get_viewport_height()
        item_cfg = dpg.get_item_configuration(self.window)
        second_pos = (item_cfg["width"], 0)
        second_width = full_width - item_cfg["width"]
        dpg.configure_item(self.second_wnd, pos=second_pos, width=second_width, height=full_height)

    def on_parent_resize(self):
        self.update_second_layout()
    def init_ui(self):
        with dpg.window(tag="root", no_scrollbar=True, no_title_bar=True, no_close=True,
                        pos=(0, 0), width=300, no_move=True) as left_window:
            self.window = left_window

            self.canvas = dpg.add_drawlist(pos=(0, 0), width=100, height=100, parent=self.window)

            with dpg.group(horizontal=True, tag="anim_buttons_group"):
                dpg.add_button(label="Button", arrow=True, direction=dpg.mvDir_Left)
                dpg.add_button(label="Button", arrow=True, direction=dpg.mvDir_Right)

            with dpg.group(horizontal=True):
                self.frame_slider = dpg.add_slider_int(callback=self.set_current_frame)

            with dpg.group():
                with dpg.group(horizontal=True, horizontal_spacing=0.3):
                    self.score_text = dpg.add_text(default_value="delta")
                    self.elapsed_text = dpg.add_text(default_value="elapsed")
                    self.fps_text = dpg.add_text(default_value="fps")
                with dpg.group(horizontal=True, horizontal_spacing=0.3):
                    dpg.add_button(label="Save Ini File",
                                   callback=lambda: dpg.save_init_file("custom_layout.ini"))

        with dpg.window(tag="second", pos=(300, 0), width=100, no_title_bar=True, no_scrollbar=True, no_close=True,
                        no_move=True, no_resize=True, no_bring_to_front_on_focus=True) as second_wnd:
            self.second_wnd = second_wnd
            dpg.add_text("Second")

            with dpg.item_handler_registry(tag="left_panel_handler") as handler:
                dpg.add_item_resize_handler(callback=self.on_parent_resize)

            dpg.bind_item_handler_registry("root", "left_panel_handler")
    def set_skeletal(self, skeletal):
        self.skeletal = skeletal

        for i in range(skeletal.bones_count):
            with dpg.draw_node(parent=self.canvas) as bone:
                self.bone_ids.append(bone)
                dpg.draw_circle((0, 0), 5, fill=skeletal.get_color(i))

    def set_animation(self, animation):
        self.animation = animation
        dpg.configure_item(self.frame_slider, min_value=0, max_value=animation.frames_count - 1)

    def on_resize(self, id, rect):
        full_height = dpg.get_viewport_height()
        dpg.configure_item(self.window, height=full_height)
        self.update_second_layout()

    def on_update(self, delta: float):
        pass

    def set_current_frame(self, id, value, data):
        print(value, data)

    def on_hover_in(self, id, value):
        self.autoplay = False

    def on_frame(self, frame):
        if not self.autoplay:
            return

        frame = frame % self.animation.frames_count
        dpg.set_value(self.fps_text, "{:d}".format(frame))
        dpg.set_value(self.frame_slider, frame)

        frame_data = self.animation.frames[frame]
        for i in range(self.skeletal.bones_count):
            dpg.apply_transform(self.bone_ids[i], dpg.create_translation_matrix(frame_data[i]))

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
