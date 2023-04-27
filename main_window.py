from dearpygui import dearpygui as dpg

from app import BaseApp


class MainWindow(BaseApp):
    def __init__(self, win, *args, **kwargs):
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
        self.window = win
        self.layout = None

        super().__init__(*args, **kwargs)

        with dpg.font_registry():
            with dpg.font("DroidSans.ttf", 16) as font1:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

        dpg.bind_font(font1)

        dpg.configure_app(load_init_file="open_pose_app.ini")

    def init_ui(self):
        dpg.push_container_stack(self.window)

        self.layout = dpg.add_table(header_row=False, resizable=True,
                                    no_host_extendX=False, row_background=True, delay_search=True)
        dpg.push_container_stack(self.layout)
        if True:
            self.left_column = dpg.add_table_column(width_stretch=True, init_width_or_weight=0.0)
            dpg.add_table_column(width_fixed=True, init_width_or_weight=300)

            dpg.push_container_stack(dpg.add_table_row())
            if True:
                self.layout_1_6 = dpg.add_table(header_row=False, resizable=True,
                                                no_host_extendX=False, row_background=True, delay_search=True)
                dpg.push_container_stack(self.layout_1_6)

                with dpg.item_handler_registry(tag="work_table_handler") as handler:
                    dpg.add_item_resize_handler(callback=lambda a, b, c: print(a, b, c))


                if True:
                    self.left_column_2 = dpg.add_table_column(width_stretch=True)
                    dpg.bind_item_handler_registry(self.left_column_2, "work_table_handler")

                    with dpg.table_row():
                        self.canvas = dpg.add_drawlist(width=500, height=600)

                    with dpg.table_row():
                        with dpg.group(horizontal=True):
                            dpg.add_button(label="Button", arrow=True, direction=dpg.mvDir_Left)
                            dpg.add_button(label="Button", arrow=True, direction=dpg.mvDir_Right)

                    with dpg.table_row():
                        self.frame_slider = dpg.add_slider_int(callback=self.set_current_frame)
                dpg.pop_container_stack()

        with dpg.group():
            with dpg.group(horizontal=True, horizontal_spacing=0.3):
                self.score_text = dpg.add_text(default_value="delta")
                self.elapsed_text = dpg.add_text(default_value="elapsed")
                self.fps_text = dpg.add_text(default_value="fps")
            with dpg.group(horizontal=True, horizontal_spacing=0.3):
                dpg.add_button(label="Save Ini File",
                               callback=lambda: dpg.save_init_file("custom_layout.ini"))

            dpg.highlight_table_column(self.layout, 0, [255, 0, 0, 100])
            dpg.highlight_table_column(self.layout, 1, [255, 255, 200, 100])

            dpg.pop_container_stack()
            dpg.pop_container_stack()
            dpg.pop_container_stack()

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
        rect = dpg.get_item_rect_size(self.window)
        par = dpg.get_item_parent(self.canvas)
        # dpg.configure_item(self.layout, height=rect[1] - 40)
        dpg.configure_item(self.canvas, height=rect[1] - 100)
        # inner_width = rect[2]
        # inner_height = rect[3]
        # gap = 4
        # left_panel_width = 200
        # dpg.configure_item(self.left_panel, width=left_panel_width, height=inner_height - gap * 4, pos=[gap, gap + gap])
        # dpg.configure_item(self.right_panel, width=inner_width - left_panel_width - gap * 3,
        #                    height=inner_height - gap * 4, pos=[left_panel_width + gap + gap, gap + gap])
        #
        # dpg.configure_item(self.canvas, width=rect[0], height=rect[1])
        # dpg.configure_item(self.frame_slider, width=rect[0], pos=(0, rect[1] - 22))

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
