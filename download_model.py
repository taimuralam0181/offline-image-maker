from diffusers import StableDiffusionPipeline
import torch

print("Downloading model... please wait")

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32
)

pipe.save_pretrained(r"C:\Users\HOTSPOT\OneDrive\Desktop\projectAI\local_models\stable-diffusion")

print("Model downloaded and saved successfully.")