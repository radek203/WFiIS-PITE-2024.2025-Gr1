import torch
from diffusers import BitsAndBytesConfig, SD3Transformer2DModel
from diffusers import StableDiffusion3Pipeline
from transformers import T5EncoderModel


class StableDiffusion:

    def __init__(self):
        self.model_id = "stabilityai/stable-diffusion-3.5-large-turbo"
        self.pipeline = self.setup_pipeline()

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

    def generate_image(self, prompt, filename):
        image = self.pipeline(
            prompt=prompt,
            num_inference_steps=4,
            guidance_scale=0.0,
            max_sequence_length=512,
        ).images[0]
        image.save("./Images/" + filename + ".png")
