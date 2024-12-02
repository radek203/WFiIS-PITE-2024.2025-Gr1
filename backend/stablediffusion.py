import pandas as pd


class StableDiffusion:

    def __init__(self, model, test=False):
        self.model = model
        self.pipeline = model.setup_pipeline()
        self.adjectives = pd.read_csv("data/adjectives.csv").iloc[0:(10 if test else 100)]
        self.categories = pd.read_csv("data/categories.csv")
        self.tags = [pd.read_csv("data/cat" + str(i) + ".csv").iloc[0:(10 if test else 100)] for i in range(1, len(self.categories) + 1)]

    def get_random_adjectives(self, n):
        return self.adjectives.sample(n)

    def get_random_tags(self, n):
        category = self.categories.sample(1)
        return self.tags[int(category.iloc[0]["id"]) - 1].sample(n)

    def generate_random_prompt(self, n):
        adjectives = self.get_random_adjectives(n)
        tags = self.get_random_tags(n)
        prompts = []
        for i in range(n):
            prompts.append(adjectives.iloc[i].values[0] + " " + tags.iloc[i].values[0])
        return prompts

    def generate_image(self, prompt, img_id, steps=10):
        image = self.model.generate_image(prompt, steps)
        image.save("images/image" + str(img_id) + ".png")
