import pandas as pd
import numpy as np

def update_tags_rating(tags, update):
    for tag in tags:
        df = pd.read_csv(f"data/ratings.csv")
        df_tags = np.array(df["tags"]) #change header in csv TODO
        for tags_str in df_tags:
            tags_arr = tags_str.split("|")
            if tag in tags_arr:
                if df.loc[df["tags"] == tags_str, "rating"] - update <= 10 and df.loc[df["tags"] == tags_str, "rating"] - update >=1:
                    df.loc[df["tags"] == tags_str, "rating"] += update
        df.to_csv(f"data/ratings.csv", index=False)