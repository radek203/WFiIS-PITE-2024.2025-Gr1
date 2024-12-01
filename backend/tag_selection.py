#tag selection
#plik backend connection
#csv id zdj i tagi uzyte i za kazda generacja dopisujesz do tej csv i usuwac najstarsze pozniej czy cos;
import pandas as pd
import numpy as np

def update_tags_rating(tags, update):
    # dla kazdego taga w tags znajdz tag w plikach csv i dodaj to ratingu update
    for tag in tags:
        for i in range(1,10):
            df = pd.read_csv(f"data/cat{i}_with_ratings.csv")
            df_tags = np.array(df["0"]) #change header in csv TODO
            if tag in df_tags:
                df.loc[df["0"] == tag, "rating"] += update
            df.to_csv(f"data/cat{i}_with_ratings.csv", index=False)
            break
                