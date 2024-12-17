import pandas as pd
import backend.scikit_impl as sc

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

    def generate_random_prompts(self):
        prompts = []
        categories = [i for i in range(1, 10)]
        all_tags = [[] for _ in categories]
        for category_id in categories:
            adjectives = self.get_random_adjectives(1)
            tags = self.get_random_tags(1, category_id)
            tag_f = adjectives.iloc[0].values[0]
            tag_s = tags.iloc[0].values[0]
            prompt = tag_f + " " + tag_s
            all_tags[category_id - 1].append(tag_f)
            all_tags[category_id - 1].append(tag_s)
            prompts.append(prompt)
        return prompts, all_tags, categories

    def generate_image(self, prompt, img_id, steps):
        image = self.model.generate_image(prompt, int(steps))
        image.save("images/image" + str(img_id) + ".png")

    # This function should return n (9) best prompts
    def generate_prompt_from_best_tags(self, user_id, n=9):
        scikit = sc.ScikitImpl(config['debug'])
        scikit.train()
        tags_combinations, _, top_categories = scikit.get_top_n_ratings(user_id, n)
        prompts = []
        all_tags = [[] for _ in range(n)]
        for i, tags in enumerate(tags_combinations):
            tags = tags.split("|")
            adjectives = self.get_random_adjectives(3)
            prompt = ""
            for j, tag in enumerate(tags):
                tag_f = adjectives.iloc[j].values[0]
                tag_s = tag
                prompt += tag_f + " " + tag_s + " and "
                all_tags[i].append(tag_f)
                all_tags[i].append(tag_s)
            prompt = prompt[:-5]
            prompts.append(prompt)
        return prompts, all_tags, top_categories
