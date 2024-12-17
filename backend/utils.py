import pandas as pd 


def get_top_n_categories(n, user_id):
    data = pd.read_csv("data/ratings.csv")
    specific_user_data = data[data["userId"] == user_id]
    specific_user_data = specific_user_data[~specific_user_data["categoryId"].str.contains(r'\|', na=False)]
    category_sum = specific_user_data.groupby("categoryId")["rating"].sum().reset_index()
    top_category = category_sum.sort_values(by="rating", ascending=False).head(n)
    return top_category