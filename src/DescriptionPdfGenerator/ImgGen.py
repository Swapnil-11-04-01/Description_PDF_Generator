from diffusers import DiffusionPipeline
import torch
import warnings

warnings.filterwarnings("ignore")

class ImgGen:
    def __init__(self):
        self.pipe = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float32,  # Use torch.float32 instead of torch.float16
            use_safetensors=True,
            variant="fp32"  # Use variant="fp32" instead of variant="fp16"
        )

    def img_generator(self, summary):
        prompt = summary
        image = self.pipe(prompt=prompt).images[0]
        return image
