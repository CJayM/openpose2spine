from dearpygui import dearpygui as dpg

from layouts import Grid

if __name__ == '__main__':
    from random import randint


    def bind_button_theme():
        while True:
            item = yield
            rgb = randint(0, 255), randint(0, 255), randint(0, 255)
            with dpg.theme() as theme:
                with dpg.theme_component(0):
                    dpg.add_theme_color(dpg.mvThemeCol_Button, [*rgb, 80])
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [*rgb, 255])
            dpg.bind_item_theme(item, theme)


    def create_button():
        themes = bind_button_theme().send
        themes(None)
        while True:
            tag = dpg.generate_uuid()
            item = dpg.add_button(label=tag, tag=tag)
            themes(item)
            yield item


    # create_button = create_button().__next__  # ye olde' button factory

    dpg.create_context()
    dpg.create_viewport(title="Grid Demo", width=600, height=600, min_height=10, min_width=10)
    dpg.setup_dearpygui()

    with dpg.window(no_scrollbar=True, no_background=True) as win:
        grid = Grid(win, cols=6, rows=6, padding=(4, 5), spacing=(4, 5))

        # Without additional arguments, items will expand and shrink to the cell's size.
        # grid.pack(create_button(),  0,  2)  # first row
        # grid.pack(create_button(), -1,  0)  # last row

        # You can clamp an item's width/height and include an alignment option. Valid
        # options are 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', and 'c'.
        grid.pack(dpg.add_button(label="Canvas"), 0, 0, 3, 5)
        grid.pack(dpg.add_button(label="Time buttons"), 4, 0, 4, 5, max_height=25)
        grid.pack(dpg.add_button(label="Time slider"), 5, 0, 5, 5, anchor="n")
        # grid.pack(create_button(), 1, 1, max_width=25, anchor="n")   # north (centered)
        # grid.pack(create_button(), 4, 4, max_height=25, anchor="w")

    dpg.set_primary_window(win, True)
    dpg.show_viewport()
    # Be sure to add the grid's redraw method to a callback. Otherwise it won't resize!
    dpg.set_viewport_resize_callback(grid.redraw)

    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
