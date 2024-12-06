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

def get_top_n_categories(n, userId):
    data = pd.read_csv("data/ratings.csv")
    specific_user_data = data[data["userId"] == userId]
    category_sum = specific_user_data.groupby("categoryId")["rating"].sum().reset_index()
    top_category = category_sum.sort_values(by = "rating", ascending = False).head(n)
    return top_category
