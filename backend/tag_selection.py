import pandas as pd
import numpy as np

def update_tags_rating(tags, update, cat_id):
    df = pd.read_csv(f"data/ratings.csv")
    newrow = pd.DataFrame({"userId": 1, "categoryId": cat_id, "rating": update, "tags": tags}, index=[0])
    df = pd.concat([df, newrow], ignore_index=True)
    df.to_csv(f"data/ratings.csv", index=False)