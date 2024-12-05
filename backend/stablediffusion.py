import pandas as pd

from config import config


class StableDiffusion:

    def __init__(self, model, test=False):
        self.model = model
        self.pipeline = model.setup_pipeline()
        self.adjectives = pd.read_csv("data/adjectives.csv").iloc[0:(10 if test else 100)]
        self.categories = pd.read_csv("data/categories.csv")
        self.tags = [pd.read_csv("data/cat" + str(i) + ".csv").iloc[0:(10 if test else 100)] for i in range(1, len(self.categories) + 1)]

    def get_random_adjectives(self, n):
        return self.adjectives.sample(n)

    def get_random_tags(self, n, category_id):
        return self.tags[category_id - 1].sample(n)

    def generate_random_prompt(self, n, category_id):
        adjectives = self.get_random_adjectives(n)
        tags = self.get_random_tags(n, category_id)
        all_tags = [[] for _ in range(n)]
        prompts = []
        for i in range(n):
            tag_f = adjectives.iloc[i].values[0]
            tag_s = tags.iloc[i].values[0]
            prompts.append(tag_f + " " + tag_s)
            all_tags[i].append(tag_f)
            all_tags[i].append(tag_s)
        return prompts, all_tags

    def generate_image(self, prompt, img_id, steps=config['steps']):
        image = self.model.generate_image(prompt, int(steps))
        image.save("images/image" + str(img_id) + ".png")
