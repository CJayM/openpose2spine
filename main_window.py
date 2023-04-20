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
        self.right_panel = None
        self.left_panel = None
        self.skeletal = None
        self.autoplay = True
        super().__init__(*args, **kwargs)

    def init_ui(self):
        dpg.configure_item(self.main_window, no_scrollbar=True)

        with dpg.child_window(width=200, height=300) as left_panel:
            self.left_panel = left_panel

            with dpg.group(horizontal=True):
                self.score_text = dpg.add_text(default_value="delta")
                self.elapsed_text = dpg.add_text(default_value="elapsed")
                self.fps_text = dpg.add_text(default_value="fps")

        with dpg.child_window(width=500, height=500, pos=(220, 8), no_scrollbar=True) as right_panel:
            self.right_panel = right_panel
            self.frame_slider = dpg.add_slider_int(pos=[0, 500], width=500, height=4, indent=0,
                                                   callback=self.set_current_frame)

            with dpg.drawlist(width=500, height=500) as canvas:
                self.canvas = canvas
        with dpg.item_handler_registry(show=False, tag="__frame_slider_handler"):
            # m_release = dpg.add_mouse_release_handler(button=dpg.mvMouseButton_Left)
            # dpg.add_item_clicked_handler(tag=self.frame_slider, callback=self.on_current_frame_drop)
            dpg.add_item_hover_handler(callback=self.on_hover_in)
            # dpg.add_item_clicked_handler(callback=self.on_hover_out)

        dpg.bind_item_handler_registry(self.frame_slider, "__frame_slider_handler")

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
        inner_width = rect[2]
        inner_height = rect[3]
        gap = 4
        left_panel_width = 200
        dpg.configure_item(self.left_panel, width=left_panel_width, height=inner_height - gap * 4, pos=[gap, gap + gap])
        dpg.configure_item(self.right_panel, width=inner_width - left_panel_width - gap * 3,
                           height=inner_height - gap * 4, pos=[left_panel_width + gap + gap, gap + gap])

        rect = dpg.get_item_rect_size(self.right_panel)
        dpg.configure_item(self.canvas, width=rect[0], height=rect[1])
        dpg.configure_item(self.frame_slider, width=rect[0], pos=(0, rect[1] - 22))

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
