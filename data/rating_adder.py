import pandas as pd
import numpy as np

for i in range(1,10):
    data = pd.read_csv(f"data/cat{i}.csv", header=None)
    default = np.ones(shape=(len(data)))*50
    data["rating"] = default
    data.to_csv(f"data/cat{i}_with_ratings.csv", index = False)
