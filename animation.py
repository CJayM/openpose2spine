import glob
import os
import os.path
import json


def list_all_frames(dir_path, name):
    images = glob.glob('{}_*_keypoints.json'.format(name), root_dir=dir_path)
    return images


class Animation:
    def __init__(self):
        self.dir_path = None
        self.frames_count = 0
        self.name = None
        self.frames = []

    def read_from_dir(self, dir_path, anim_name):
        self.name = anim_name
        self.dir_path = dir_path
        json_frames = list_all_frames(dir_path, anim_name)
        self.frames = self.extract_frames(json_frames)
        self.frames_count = len(self.frames)

    def extract_frames(self, json_frames):
        res = []
        for name in json_frames:
            full_path = os.path.join(self.dir_path, name)
            with open(full_path, "r") as file:
                data = json.load(file)
                all_data = data["people"][0]["pose_keypoints_2d"]
                points = []
                for i in range(0, len(all_data), 3):
                    points.append((all_data[i], all_data[i + 1]))
                res.append(points)
        return res
