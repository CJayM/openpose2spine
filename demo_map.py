"""Example: display map"""

import dearpygui.dearpygui as dpg
import dearpygui_map as dpg_map
from dearpygui_map import tile_source

dpg.create_context()

server = tile_source.TileServer(
    name="Yandex",
    # base_url="http://sat01.maps.yandex.net",
    # base_url="http://{subdomain}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    base_url="https://sat01.maps.yandex.net/tiles?&x={y}&y={y}&z=4",
    subdomains=["01", "02", "03", "04"],
    max_zoom_level=19,
    license_text="",
    thread_limit=4,
)

with dpg.window(label="Map demo"):
    dpg_map.add_map_widget(
        width=800, height=600, center=(0, 0), zoom_level=4, tile_server=server
    )

dpg.create_viewport(title="Dear PyGui map widget demo", width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
