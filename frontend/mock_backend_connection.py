import backend.tag_selection as ts
import pandas as pd
import numpy as np

def get_image_file_names():
    for i in range(0,10):
        yield f"images/placeholder{i}.png"

def like_callback(file_name):
    data = pd.read_csv("data/temp_images.csv")
    filestem = file_name.split("/")[-1].split(".")[0]
    tags = np.array(data[data["file_name"] == filestem]["tags"])[0]
    cat_id = np.array(data[data["file_name"] == filestem]["categoryId"])[0]
    ts.update_tags_rating(tags, 10, cat_id)

    print(file_name)


def dislike_callback(file_name):
    data = pd.read_csv("data/temp_images.csv")
    tags = np.array(data[data["file_name"] == file_name.split("/")[-1].split(".")[0]]["tags"])[0]
    ts.update_tags_rating(tags, 1)
    print(file_name)