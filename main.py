import dearpygui.dearpygui as dpg
from animation import Animation
from skeletal import Skeletal

DIR_WITH_POSES = r"D:\develop\openpose2spine\animations\pose_walk"
ANIM_NAME = "walk"
DIR_WITH_POSES = r"D:\develop\openpose2spine\animations\openpose_run_forward_flip"
ANIM_NAME = "run_forward_flip"
DIR_WITH_POSES = r"D:\develop\openpose2spine\animations\openpose_kick"
ANIM_NAME = "kick"
import assets

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


if __name__ == "__main__":
    skeletal = Skeletal()
    animation = Animation()
    animation.read_from_dir(DIR_WITH_POSES, ANIM_NAME)

    from main_window import MainWindow

    dpg.create_context()
    assets.init_fonts()
    dpg.create_viewport(title="OpenPose data Converter")
    # dpg.show_font_manager()
    # dpg.show_style_editor()
    # dpg.show_item_registry()
    main_app = MainWindow()
    dpg.show_viewport()
    dpg.setup_dearpygui()

    main_app.set_skeletal(skeletal)
    main_app.set_animation(animation)

    try:
        dpg.start_dearpygui()
    finally:
        dpg.destroy_context()

    pass
