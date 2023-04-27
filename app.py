import dearpygui.dearpygui as dpg


class BaseApp:
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height

        self.prev_frame = 0
        dpg.set_viewport_resize_callback(self.on_resize)

        self.init_ui()

    def exit(self):
        dpg.stop_dearpygui()

    def __del__(self):
        dpg.destroy_context()

    def show_window(self):
        pass

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
