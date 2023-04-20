import glob
import os
import os.path
import json
import math

DIR_WITH_POSES = r"D:\develop\openpose2spine\animations\pose_walk"
ANIM_NAME = "walk"
DIR_WITH_POSES = r"D:\develop\openpose2spine\animations\openpose_run_forward_flip"
ANIM_NAME = "run_forward_flip"
DIR_WITH_POSES = r"D:\develop\openpose2spine\animations\openpose_kick"
ANIM_NAME = "kick"


def list_all_files(dir_path, name):
    images = glob.glob('{}_*_keypoints.json'.format(name), root_dir=dir_path)
    return images


def extract_frames(images):
    res = []
    for name in images:
        full_path = os.path.join(DIR_WITH_POSES, name)
        with open(full_path, "r") as file:
            data = json.load(file)
            all_data = data["people"][0]["pose_keypoints_2d"]
            points = []
            for i in range(0, len(all_data), 3):
                points.append((all_data[i], all_data[i + 1]))
            res.append(points)
    return res


BONE_COLORS = [
    (153, 0, 61),
    (153, 51, 0),
    (153, 102, 0),
    (153, 153, 0),
    (102, 153, 0),
    (51, 153, 00),
    (00, 153, 00),
    (00, 153, 51),
    (00, 153, 102),
    (00, 153, 153),
    (00, 102, 153),
    (00, 51, 153),
    (00, 00, 153),
    (51, 00, 153),
    (102, 00, 153),
    (153, 00, 153),
    (153, 00, 102),
    (153, 00, 51),

]

NUM_POINTS = len(BONE_COLORS)

EDGES_INDEXES = [
    (0, 1),
    (0, 15),
    (0, 16),
    (1, 8),
    (1, 2),
    (1, 5),
    (2, 3),
    (3, 4),
    (5, 6),
    (6, 7),
    (8, 9),
    (8, 12),
    (9, 10),
    (10, 11),
    (11, 22),
    (11, 24),
    (12, 13),
    (13, 14),
    (14, 21),
    (14, 19),
    (15, 17),
    (16, 18),
    (19, 20),
    (22, 23),
]

EDGE_COLORS = [
    (153, 0, 51),
    (153, 0, 102),
    (143, 0, 214),
    (153, 0, 0),
    (153, 51, 0),
    (102, 153, 0),
    (153, 102, 0),
    (153, 153, 0),
    (51, 153, 0),
    (0, 153, 0),
    (0, 153, 51),
    (0, 102, 153),
    (0, 153, 102),
    (0, 153, 153),
    (0, 153, 153),
    (0, 153, 153),
    (0, 51, 153),
    (0, 0, 153),
    (0, 0, 153),
    (0, 0, 153),
    (153, 0, 153),
    (51, 0, 153),
    (0, 0, 153),
    (0, 0, 153),
]

NUM_EDGES = len(EDGES_INDEXES)


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


WIN_SIZE = (850, 600)
bones = []


class Skeletal:
    def __init__(self):
        self.bones_count = NUM_POINTS
        self.frames_count = 0
        self.frames = []

    def get_color(self, index: int):
        return BONE_COLORS[index]

    def add_frames(self, frames):
        self.frames.extend(frames)
        self.frames_count = len(self.frames)


if __name__ == "__main__":
    imgs = list_all_files(DIR_WITH_POSES, ANIM_NAME)
    frames = extract_frames(imgs)

    skeletal = Skeletal()
    skeletal.add_frames(frames)

    from app import MainWindow

    main_app = MainWindow()
    main_app.set_skeletal(skeletal)
    main_app.show_window()
    main_app.exec()
