from animation import Animation
from skeletal import Skeletal

DIR_WITH_POSES = r"D:\develop\openpose2spine\animations\pose_walk"
ANIM_NAME = "walk"
DIR_WITH_POSES = r"D:\develop\openpose2spine\animations\openpose_run_forward_flip"
ANIM_NAME = "run_forward_flip"
DIR_WITH_POSES = r"D:\develop\openpose2spine\animations\openpose_kick"
ANIM_NAME = "kick"


def get_succes_prev_frame(index, frame, frames):
    start_frame = frame

    while frames[frame][index] == (0, 0):
        frame = frame - 1
        if frame < 0:
            frame = len(frames) - 1
        if frame == start_frame:
            return -1

    return frame


def get_succes_next_frame(index, frame, frames):
    start_frame = frame
    max_frame = len(frames) - 1
    while frames[frame][index] == (0, 0):
        frame = frame + 1
        if frame > max_frame:
            frame = 0
        if frame == start_frame:
            return -1

    return frame


def get_bone_pos(index, frame, frames):
    coord = frames[frame][index]
    if coord != (0, 0):
        return coord

    prev_frame = get_succes_prev_frame(index, frame, frames)
    next_frame = get_succes_next_frame(index, frame, frames)

    if prev_frame == next_frame:
        return None
    if prev_frame == -1 or next_frame == -1:
        return None
    distance = next_frame - prev_frame
    pos1 = frames[prev_frame][index]
    pos2 = frames[next_frame][index]
    delta_x = (pos2[0] - pos1[0]) / distance
    delta_y = (pos2[1] - pos1[1]) / distance
    cur_offset = prev_frame - frame

    return (pos1[0] + delta_x * cur_offset, pos1[0] + delta_y * cur_offset)


def status_bar_gui():
    imgui.text("Some status")
    imgui.same_line()
    # imgui.progress_bar(0.3, hello_imgui.em_to_vec2(7.0, 1.0))  # type: ignore


def show_menu_gui():
    if imgui.begin_menu("My Menu"):
        clicked, _ = imgui.menu_item("Test me", "", False)
        if clicked:
            pass
        imgui.end_menu()


def show_app_menu_items():
    clicked, _ = imgui.menu_item("A Custom app menu item", "", False)
    if clicked:
        pass


if __name__ == "__main__":
    skeletal = Skeletal()
    animation = Animation()
    animation.read_from_dir(DIR_WITH_POSES, ANIM_NAME)

    # from main_window import MainWindow
    #
    # main_app = MainWindow()
    # main_app.set_skeletal(skeletal)
    # main_app.set_animation(animation)
    # main_app.show_window()
    # main_app.exec()

    from imgui_bundle import hello_imgui as hi

    from imgui_bundle import imgui, immapp


    # hi.set_assets_folder(demo_utils.demos_assets_folder())

    def gui():
        imgui.text("Hello, world!")


    app_params = hi.AppWindowParams(window_title="OpenPose data Converter", restore_previous_geometry=True)
    app_params.window_geometry.size = (800, 600)
    window_params = hi.ImGuiWindowParams(menu_app_title="File", show_status_bar=True, show_status_fps=False,
                                         show_menu_bar=True,
                                         default_imgui_window_type=hi.DefaultImGuiWindowType.provide_full_screen_dock_space,
                                         enable_viewports=True)

    split_root_horizontal = hi.DockingSplit()
    split_root_horizontal.initial_dock = "MainDockSpace"
    split_root_horizontal.new_dock = "LeftSpace"
    split_root_horizontal.direction = imgui.Dir_.left
    split_root_horizontal.ratio = 0.25

    commands_window = hi.DockableWindow()
    commands_window.label = "Command"
    commands_window.can_be_closed = False
    commands_window.dock_space_name = "LeftSpace"
    commands_window.gui_function = imgui.show_user_guide

    # A Window named "Dear ImGui Demo" will be placed in "MainDockSpace"
    dear_imgui_demo_window = hi.DockableWindow()
    dear_imgui_demo_window.label = "Dear ImGui Demo"
    dear_imgui_demo_window.dock_space_name = "MainDockSpace"
    dear_imgui_demo_window.can_be_closed = False
    dear_imgui_demo_window.gui_function = imgui.show_user_guide

    docking_params = hi.DockingParams(docking_splits=[split_root_horizontal, ],
                                      dockable_windows=[
                                          commands_window,
                                          dear_imgui_demo_window,
                                      ]
                                      )

    # Finally, transmit these windows to HelloImGui

    runner_params = hi.RunnerParams(app_window_params=app_params, imgui_window_params=window_params,
                                    docking_params=docking_params)
    runner_params.fps_idling.fps_idle = 2

    runner_params.callbacks.show_status = status_bar_gui
    runner_params.callbacks.show_menus = show_menu_gui
    runner_params.callbacks.show_app_menu_items = show_app_menu_items

    hi.run(runner_params)
