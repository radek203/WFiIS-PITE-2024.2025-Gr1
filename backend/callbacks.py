import pandas as pd

def get_image_data(i):
    return [f"images/image{i}.png", 1, 1, "tag1|tag2|tag3"]


def like_callback(file_name, user_id, category_id, tags):
    new_row = {
        "userId": user_id,
        "categoryId": category_id,
        "rating": 10,
        "tags": tags
    }
    save_row_to_file(new_row)
    print(file_name)


def dislike_callback(file_name, user_id, category_id, tags):
    new_row = {
        "userId": user_id,
        "categoryId": category_id,
        "rating": 1,
        "tags": tags
    }
    save_row_to_file(new_row)
    print(file_name)

def save_row_to_file(new_row):
    data = pd.read_csv("data/ratings.csv")
    new_row_df = pd.DataFrame([new_row], columns=data.columns)
    updated_data = pd.concat([data, new_row_df], ignore_index=True)
    updated_data.to_csv("data/ratings.csv", index=False)

def get_number_of_rows():
    data = pd.read_csv("data/ratings.csv")
    return data.shape[0]
