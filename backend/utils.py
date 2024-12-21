import pandas as pd


def get_top_n_categories(n, user_id):
    data = pd.read_csv("data/ratings.csv")
    specific_user_data = data[data["userId"] == user_id]
    specific_user_data = specific_user_data[~specific_user_data["categoryId"].astype(str).str.contains(r'\|', na=False)]
    category_sum = specific_user_data.groupby("categoryId")["rating"].sum().reset_index()
    top_category = category_sum.sort_values(by="rating", ascending=False).head(n)
    return top_category


def get_tags_ratings():
    ratings_df = pd.read_csv("data/ratings.csv")
    adjectives_df = pd.read_csv("data/adjectives.csv", header=None)
    return [{"userId": row.userId, "tag": remove_tag(adjectives_df, row.tags), "rating": row.rating, "tags": remove_tag(adjectives_df, row.tags)}
        for _, row in ratings_df.iterrows()
        if '|' in str(row.categoryId)]


def remove_tag(adjectives_df, tags):
    filtered_list = [tag for tag in tags.split('|') if tag not in adjectives_df[0].tolist()]
    return '|'.join(filtered_list)


def get_user_images(user_id):
    data = pd.read_csv("data/ratings.csv")
    specific_user_data = data[data["userId"] == user_id]
    return specific_user_data["id"].values


def save_row_to_file(new_row):
    data = pd.read_csv("data/ratings.csv")
    new_row_df = pd.DataFrame([new_row], columns=data.columns)
    updated_data = pd.concat([data, new_row_df], ignore_index=True)
    updated_data.to_csv("data/ratings.csv", index=False)


def get_number_of_rows():
    data = pd.read_csv("data/ratings.csv")
    return data.shape[0]


def get_existing_users():
    data = pd.read_csv("data/ratings.csv")
    return data.userId.unique()
