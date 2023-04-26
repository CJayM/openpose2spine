import dearpygui.dearpygui as dpg
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


def gui_left_panel():
    imgui.text("LEFT PANEL")


import random


def random_color():
    """helper function to generate a random color
    Returns:
        (int, int, int, int): tuple with random values between 0 and 255 for the first three values and always 255 for the last
    """
    # generate random color values using random module
    cola = random.randrange(0, 255)
    colb = random.randrange(0, 255)
    colc = random.randrange(0, 255)
    # return the random color with full alpha
    return (cola, colb, colc, 255)


def gui_right_panel(skeletal: Skeletal, animaiton: Animation):
    dpg.text("RIGHT PANEL")
    dpg.same_line()
    if dpg.button("Button"):
        print("Clicked")

    # draw_list = imgui.get_window_draw_list()
    # draw_list.path_clear()
    # draw_list.path_line_to(imgui.ImVec2(80, 80))
    # draw_list.path_arc_to(imgui.ImVec2(80, 80), 30, 0.5, 5.5)
    # draw_list.path_stroke(0xffaacc,
    #                       flags=imgui.ImDrawFlags_.closed, thickness=10)
    #
    # draw_list.path_clear()
    # draw_list.path_line_to(imgui.ImVec2(240, 80))
    # draw_list.path_arc_to(imgui.ImVec2(240, 80), 30, 0.5, 5.5)
    # draw_list.path_stroke(0xfa887f,
    #                       flags=imgui.ImDrawFlags_.round_corners_none, thickness=10)
    #
    # draw_list.add_rect(imgui.ImVec2(20, 135), imgui.ImVec2(60, 190),
    #                    0xffaa44, rounding=5,
    #                    flags=imgui.ImDrawFlags_.round_corners_all, thickness=10)
    # draw_list.add_rect(imgui.ImVec2(100, 135), imgui.ImVec2(140, 190),
    #                    0xff00aa, rounding=5,
    #                    flags=imgui.ImDrawFlags_.round_corners_none, thickness=10)
    # draw_list.add_rect(imgui.ImVec2(180, 135), imgui.ImVec2(220, 190),
    #                    0xff00aa, rounding=5,
    #                    flags=imgui.ImDrawFlags_.round_corners_left, thickness=10)
    # draw_list.add_rect(imgui.ImVec2(260, 135), imgui.ImVec2(300, 190),
    #                    0xff00aa, rounding=5,
    #                    flags=imgui.ImDrawFlags_.round_corners_bottom_right, thickness=10)


    # dpg.add_draw_layer(width=3000, height=3000, tag="asdasd")
    #     for x in range(0, 30):
    #         for y in range(0, 30):
    #             # define a multiplier
    #             multi = 100
    #             # calculate the points of the rectangle
    #             p1 = (x * multi, y * multi)  # upper left corner
    #             p2 = (x * multi + multi, y * multi + multi)  # lower right corner
    #             # get a random color
    #             randcol = random_color()
    #             # draw and fill the rectangle
    #             dpg.draw_rectangle(p1, p2, color=randcol, fill=randcol)


def on_new_frame():
    # print("New frame")
    pass


if __name__ == "__main__":
    skeletal = Skeletal()
    animation = Animation()
    animation.read_from_dir(DIR_WITH_POSES, ANIM_NAME)

    from main_window import MainWindow

    main_app = MainWindow()
    main_app.set_skeletal(skeletal)
    main_app.set_animation(animation)
    main_app.show_window()
    main_app.exec()