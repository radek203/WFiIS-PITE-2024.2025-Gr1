from abc import ABC, abstractmethod

import torch
from diffusers import BitsAndBytesConfig, SD3Transformer2DModel, DiffusionPipeline
from diffusers import StableDiffusion3Pipeline
from transformers import T5EncoderModel

from config import config


class ImageModel(ABC):

    @abstractmethod
    def __init__(self):
        self.model_id = None
        self.pipeline = None
        self.refiner = None
        pass

    @abstractmethod
    def setup_pipeline(self):
        pass

    def generate_image(self, prompt, steps=config['steps']):
        image = self.pipeline(
            prompt=prompt,
            num_inference_steps=steps,
            guidance_scale=4.5,
            max_sequence_length=512,
        ).images[0]
        return image

    @staticmethod
    def get_model(model_id):
        if model_id == "SD35L":
            return ImageModelSD35L()
        elif model_id == "SD3MD":
            return ImageModelSD3MD()
        elif model_id == "SDXL1":
            return ImageModelSDXL1()
        else:
            return ImageModelSD35LT()


class ImageModelSD35LT(ImageModel):

    def __init__(self):
        self.model_id = "stabilityai/stable-diffusion-3.5-large-turbo"

    def setup_pipeline(self):
        nf4_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        model_nf4 = SD3Transformer2DModel.from_pretrained(
            self.model_id,
            subfolder="transformer",
            quantization_config=nf4_config,
            torch_dtype=torch.bfloat16
        )

        t5_nf4 = T5EncoderModel.from_pretrained("diffusers/t5-nf4", torch_dtype=torch.bfloat16)

        self.pipeline = StableDiffusion3Pipeline.from_pretrained(
            self.model_id,
            transformer=model_nf4,
            text_encoder_3=t5_nf4,
            torch_dtype=torch.bfloat16
        )
        self.pipeline.enable_model_cpu_offload()


class ImageModelSD35L(ImageModel):

    def __init__(self):
        self.model_id = "stabilityai/stable-diffusion-3.5-large"

    def setup_pipeline(self):
        nf4_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        model_nf4 = SD3Transformer2DModel.from_pretrained(
            self.model_id,
            subfolder="transformer",
            quantization_config=nf4_config,
            torch_dtype=torch.bfloat16
        )

        self.pipeline = StableDiffusion3Pipeline.from_pretrained(
            self.model_id,
            transformer=model_nf4,
            torch_dtype=torch.bfloat16
        )
        self.pipeline.enable_model_cpu_offload()


class ImageModelSD3MD(ImageModel):

    def __init__(self):
        self.model_id = "stabilityai/stable-diffusion-3-medium-diffusers"

    def setup_pipeline(self):
        self.pipeline = StableDiffusion3Pipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float16
        )
        self.pipeline = self.pipeline.to("cuda")


class ImageModelSDXL1(ImageModel):

    def __init__(self):
        self.model_id = "stabilityai/stable-diffusion-xl-base-1.0"

    def setup_pipeline(self):
        self.pipeline = DiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True
        )
        self.pipeline.to("cuda")
        self.refiner = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-refiner-1.0",
            text_encoder_2=self.pipeline.text_encoder_2,
            vae=self.pipeline.vae,
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16",
        )
        self.refiner.to("cuda")

    def generate_image(self, prompt, steps=config['steps']):
        high_noise_frac = 0.8

        image = self.pipeline(
            prompt=prompt,
            num_inference_steps=steps,
            denoising_end=high_noise_frac,
            output_type="latent",
        ).images
        image = self.refiner(
            prompt=prompt,
            num_inference_steps=steps,
            denoising_start=high_noise_frac,
            image=image,
        ).images[0]
        return image
