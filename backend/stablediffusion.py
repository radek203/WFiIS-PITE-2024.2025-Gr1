import pandas as pd
import torch
from diffusers import BitsAndBytesConfig, SD3Transformer2DModel
from diffusers import StableDiffusion3Pipeline
from enum import Enum
from transformers import T5EncoderModel


class ImageModel(Enum):
    SD35LT = "stabilityai/stable-diffusion-3.5-large-turbo"
    SD35L = "stabilityai/stable-diffusion-3.5-large"
    SD3MD = "stabilityai/stable-diffusion-3-medium-diffusers"


class StableDiffusion:

    def __init__(self, model=ImageModel.SD35LT, test=False):
        self.model_id = model.value
        self.pipeline = self.setup_pipeline()
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

    def setup_pipeline(self):
        nf4_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="fp4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        model_nf4 = SD3Transformer2DModel.from_pretrained(
            self.model_id,
            subfolder="transformer",
            quantization_config=nf4_config,
            torch_dtype=torch.bfloat16
        )
        t5_nf4 = T5EncoderModel.from_pretrained("diffusers/t5-nf4", torch_dtype=torch.bfloat16)

        pipeline = StableDiffusion3Pipeline.from_pretrained(
            self.model_id,
            transformer=model_nf4,
            text_encoder_3=t5_nf4,
            torch_dtype=torch.bfloat16
        )
        pipeline.enable_model_cpu_offload()
        return pipeline

    def generate_image(self, prompt, img_id, steps=24):
        image = self.pipeline(
            prompt=prompt,
            num_inference_steps=steps,
            guidance_scale=4.5,
            max_sequence_length=512,
        ).images[0]
        image.save("images/image" + str(img_id) + ".png")
