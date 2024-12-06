import pandas as pd


def rate_callback(user_id, ratings, category_id, tags):
    new_row = {
        "userId": user_id,
        "categoryId": category_id,
        "rating": ratings,
        "tags": tags
    }
    save_row_to_file(new_row)


def save_row_to_file(new_row):
    data = pd.read_csv("data/ratings.csv")
    new_row_df = pd.DataFrame([new_row], columns=data.columns)
    updated_data = pd.concat([data, new_row_df], ignore_index=True)
    updated_data.to_csv("data/ratings.csv", index=False)


def get_number_of_rows():
    data = pd.read_csv("data/ratings.csv")
    return data.shape[0]


def get_top_3_categories():
    data = pd.read_csv("data/ratings.csv")
    category_sum = data.groupby("categoryId")["rating"].sum().reset_index()
    sorted_categories = category_sum.sort_values(by = "rating", ascending = False).reset_index(drop=True)
    if len(sorted_categories)>3 and sorted_categories.loc[2, "rating"] == sorted_categories.loc[3, "rating"]:
        top_3_categories = pd.concat([sorted_categories.iloc[:2], sorted_categories.iloc[2:4].sample(1)]).reset_index(drop=True)
    else:
        top_3_categories = sorted_categories.iloc[:3].reset_index(drop=True)
    return top_3_categories


def get_top_category():
    data = pd.read_csv("data/ratings.csv")
    category_sum_1 = data.groupby("categoryId")["rating"].sum().reset_index()
    top_category = category_sum_1.sort_values(by = "rating", ascending = False).head(1)
    return top_category
