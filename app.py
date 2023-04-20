import dearpygui.dearpygui as dpg


class BaseApp:
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.main_window = None

        self.prev_frame = 0

        dpg.create_context()
        dpg.create_viewport(title="OpenPose data Converter", x_pos=0, y_pos=0, width=width, height=height)
        dpg.setup_dearpygui()
        dpg.set_viewport_resize_callback(self.on_resize)

        with dpg.window(tag="Primary Window", autosize=True, no_close=True, no_resize=True, no_collapse=True,
                        no_move=True,
                        no_title_bar=True) as main_window:
            self.main_window = main_window
            self.init_ui()

    def exit(self):
        dpg.stop_dearpygui()

    def __del__(self):
        dpg.destroy_context()

    def show_window(self):
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)

    def on_update(self, delta: float):
        pass

    def on_draw(self, delta: float):
        pass

    def exec(self):
        while dpg.is_dearpygui_running():
            delta_time = dpg.get_delta_time()
            self.elapsed += delta_time
            current_frame = int((self.elapsed * 1000) / 30.0)

            self.on_update(delta_time)
            if current_frame != self.prev_frame:
                self.on_frame(current_frame)
                self.prev_frame = current_frame

            dpg.render_dearpygui_frame()
            self.on_draw(delta_time)

    def init_ui(self):
        pass

    def on_resize(self, id, rect):
        pass


class MainWindow(BaseApp):
    def __init__(self, *args, **kwargs):
        self.elapsed_text = None
        self.fps_text = None
        self.elapsed = 0
        self.score_text = None
        self.bone_ids = []
        self.canvas = None
        self.right_panel = None
        self.left_panel = None
        self.skeletal = None
        super().__init__(*args, **kwargs)

    def init_ui(self):
        with dpg.child_window(tag="left_panel", width=200, height=300) as left_panel:
            self.left_panel = left_panel

            with dpg.group(horizontal=True):
                self.score_text = dpg.add_text(default_value="delta")
                self.elapsed_text = dpg.add_text(default_value="elapsed")
                self.fps_text = dpg.add_text(default_value="fps")

        with dpg.child_window(width=500, height=500, pos=(220, 8)) as right_panel:
            self.right_panel = right_panel

            with dpg.drawlist(width=500, height=500) as canvas:
                self.canvas = canvas

    def set_skeletal(self, skeletal):
        self.skeletal = skeletal

        for i in range(skeletal.bones_count):
            with dpg.draw_node(parent=self.canvas) as bone:
                self.bone_ids.append(bone)
                dpg.draw_circle((0, 0), 5, fill=skeletal.get_color(i))

    def set_animation(self, animation):
        self.animation = animation

    def on_resize(self, id, rect):
        inner_width = rect[2]
        inner_height = rect[3]
        gap = 4
        left_panel_width = 200
        dpg.configure_item(self.left_panel, width=left_panel_width, height=inner_height - gap * 4, pos=[gap, gap + gap])
        dpg.configure_item(self.right_panel, width=inner_width - left_panel_width - gap * 3,
                           height=inner_height - gap * 4, pos=[left_panel_width + gap + gap, gap + gap])

        rect = dpg.get_item_rect_size(self.right_panel)
        dpg.configure_item(self.canvas, width=rect[0], height=rect[1])

    def on_update(self, delta: float):
        pass
        # dpg.set_value(self.score_text, "{:.5f}".format(delta))
        # dpg.set_value(self.elapsed_text, "{:.5f}".format(self.elapsed))

    def on_frame(self, frame):
        frame = frame % self.animation.frames_count
        dpg.set_value(self.fps_text, "{:d}".format(frame))

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
