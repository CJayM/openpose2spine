import glob
import pygame
import os
import os.path
import json

# from pygame.locals import *

DIR_WITH_POSES = r"D:\develop\godot\Glazovs_doors\openpose\pose_walk"
ANIM_NAME = "walk"
# DIR_WITH_POSES = r"D:\develop\godot\Glazovs_doors\openpose\openpose_run_forward_flip"
# ANIM_NAME = "run_forward_flip"
DIR_WITH_POSES = r"D:\develop\godot\Glazovs_doors\openpose\openpose_kick"
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


def run_pygame(frames):
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    time = pygame.time.get_ticks()
    getTicksLastFrame = time

    current_frame = 0.0
    max_frames = len(frames)
    while True:
        time = pygame.time.get_ticks()
        delta_time = (time - getTicksLastFrame) / 30.0
        getTicksLastFrame = time

        current_frame = current_frame + delta_time
        if (current_frame >= max_frames):
            current_frame = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        window.fill((127, 127, 127))

        frame = int(current_frame)

        # draw edges
        for i in range(NUM_EDGES):
            edge = EDGES_INDEXES[i]
            pos1 = get_bone_pos(edge[0], frame, frames)
            pos2 = get_bone_pos(edge[1], frame, frames)
            if pos1 and pos2:
                pygame.draw.line(window, EDGE_COLORS[i], pos1, pos2, 5)

        # draw points
        for i in range(NUM_POINTS):
            coord = get_bone_pos(i, frame, frames)
            color = BONE_COLORS[i]
            if coord:
                pygame.draw.circle(window, color, coord, 5, 0)

        pygame.display.update()


if __name__ == "__main__":
    imgs = list_all_files(DIR_WITH_POSES, ANIM_NAME)
    frames = extract_frames(imgs)
    run_pygame(frames)
