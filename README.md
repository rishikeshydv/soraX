# SoraX 1.0 Readme

![SoraX Logo](/frontend/public/FrontEnd.png)

## Video Merger
![SoraX Logo](/frontend/public/VideoMerger.png)

SoraX 1.0 is an AI Video Generator designed to create dynamic video content with variable time limits. It leverages cutting-edge technologies to provide a seamless experience for users.

## Roadmap

* [x] Implement the base architecture
  * [ ] Models
    * [x] Text Encoder（based on Stable Diffusion XL's [Text Encoder](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/text_encoder_2/model.safetensors)）
    * [x] VideoDiT（based on [Facebook DiT](https://github.com/facebookresearch/DiT)）
    * [ ] VideoVAE
  * [x] Scheduler（based on [DDIM](https://arxiv.org/abs/2010.02502)）
  * [x] Trainer（based on [PyTorch-lightning](https://lightning.ai/docs/pytorch/stable/)）
* [x] Validate on small datasets
  * [x] [Pixabay100](https://github.com/ECNU-CILAB/Pixabay100)
* [ ] Train Video Encoder & Decoder on large datasets
* [ ] Train VideoDiT on large datasets

## Technologies Used

- **Backend**: Typescript, Go
- **Database**: Firebase
- **Frontend**: React, ShadCN
- **Payment Integration**: Stripe

## Features

### Authentication & Authorization
SoraX incorporates robust authentication and authorization mechanisms to ensure secure access to its features and resources.

### Crypto Payment
Users can conveniently make payments using cryptocurrencies, ensuring flexibility and security in transactions.

### Online Storage for Videos
SoraX provides online storage for generated videos, offering users a certain amount of free space to store their content.

## Usage

To utilize SoraX, follow these steps:

1. **Sign Up or Log In**: Create an account or log in to access the platform.
2. **Select Time Limit**: Choose the desired time limit for your video generation.
3. **Input Prompt**: Provide a prompt for the AI generator. The number of minutes determines the number of words in your prompt.
4. **Generate Video**: Initiate the video generation process.
5. **Payment**: Complete the payment process if applicable.
6. **Access Generated Video**: Once generated, access your video from the provided storage space.

## Getting Started

To get started with SoraX locally for development purposes, follow these steps:

1. **Clone Repository**: Clone the SoraX repository to your local machine.
2. **Install Dependencies**: Install all necessary dependencies using package managers like npm or yarn.
3. **Configure Environment Variables**: Set up environment variables for Firebase and Stripe integration.
4. **Run Backend**: Start the backend server using the provided scripts.
5. **Run Frontend**: Launch the frontend application to interact with SoraX.

## Progress

- [x] Authentication/Authorization
- [x] FrontEnd
- [x] Firebase Initialize
- [x] Realtime Firebase
- [x] Prompt Generator
- [x] Video Generator
- [x] Load Balancer for Prompts
- [x] Video Merger

### Training

```python
from soraX.data import TextVideoDataset
from soraX.models import SDXLTextEncoder2
from soraX.trainers.v1 import LightningVideoDiT
import lightning as pl
import torch


if __name__ == '__main__':
    # dataset and data loader
    dataset = TextVideoDataset("data/pixabay100", "data/pixabay100/metadata.json",
                               num_frames=64, height=64, width=64)
    train_loader = torch.utils.data.DataLoader(dataset, shuffle=True, batch_size=1, num_workers=8)

    # model
    model = LightningVideoDiT(learning_rate=1e-5)
    model.text_encoder.load_state_dict_from_diffusers("models/text_encoder/model.safetensors")

    # train
    trainer = pl.Trainer(max_epochs=100000, accelerator="gpu", devices="auto", callbacks=[
        pl.pytorch.callbacks.ModelCheckpoint(save_top_k=-1)
    ])
    trainer.fit(model=model, train_dataloaders=train_loader)
```

While the training program is running, you can launch `tensorboard` to see the training loss.

```
tensorboard --logdir .
```

### Inference

* Synthesize a video in the pixel space.

```python
from soraX.models import SDXLTextEncoder2, VideoDiT
from soraX.pipelines import PixelVideoDiTPipeline
from soraX.data import save_video
import torch


# models
text_encoder = SDXLTextEncoder2.from_diffusers("models/text_encoder/model.safetensors")
denoising_model = VideoDiT.from_pretrained("models/denoising_model/model.safetensors")

# pipeline
pipe = PixelVideoDiTPipeline(torch_dtype=torch.float16, device="cuda")
pipe.fetch_models(text_encoder, denoising_model)

# generate a video
prompt = "woman, flowers, plants, field, garden"
video = pipe(prompt=prompt, num_inference_steps=100)

# save the video (the resolution is 64*64, we enlarge it to 512*512 here)
save_video(video, "output.mp4", upscale=8)
```

* Encode a video into the latent space, and then decode it.


```python
from soraX.models import SDVAEEncoder, SVDVAEDecoder
from soraX.data import load_video, tensor2video, concat_video, save_video
import torch
from tqdm import tqdm


frames = load_video("data/pixabay100/videos/168572 (Original).mp4",
                    num_frames=1024, height=1024, width=1024, random_crop=False)
frames = frames.to(dtype=torch.float16, device="cpu")

encoder = SDVAEEncoder.from_diffusers("models/vae/model.safetensors").to(dtype=torch.float16, device="cuda")
decoder = SVDVAEDecoder.from_diffusers("models/vae/model.safetensors").to(dtype=torch.float16, device="cuda")

with torch.no_grad():
    print(frames.shape)
    latents = encoder.encode_video(frames, progress_bar=tqdm)
    print(latents.shape)
    decoded_frames = decoder.decode_video(latents, progress_bar=tqdm)

video = tensor2video(concat_video([frames, decoded_frames]))
save_video(video, "video.mp4", fps=24)
```


### Results (Experimental)

We trained a denoising model using a small dataset [Pixabay100](https://github.com/ECNU-CILAB/Pixabay100). This model serves to demonstrate that our training code is capable of fitting the training data properly, with a resolution of 64*64.
|airport, people, crowd, busy|beach, ocean, waves, water, sand|bee, honey, insect, beehive, nature|coffee, beans, caffeine, coffee, shop|
|-|-|-|-|
|![](assets/airport_people_crowd_busy.gif)|![](assets/beach_ocean_waves_water_sand.gif)|![](assets/bee_honey_insect_beehive_nature.gif)|![](assets/coffee_beans_caffeine_coffee_shop.gif)|
|fish, underwater, aquarium, swim|forest, woods, mystical, morning|ocean, beach, sunset, sea, atmosphere|hair, wind, girl, woman, people|
|![](assets/fish_underwater_aquarium_swim.gif)|![](assets/forest_woods_mystical_morning.gif)|![](assets/ocean_beach_sunset_sea_atmosphere.gif)|![](assets/hair_wind_girl_woman_people.gif)|
|reeds, grass, wind, golden, sunshine|sea, ocean, seagulls, birds, sunset|woman, flowers, plants, field, garden|wood, anemones, wildflower, flower|
|![](assets/reeds_grass_wind_golden_sunshine.gif)|![](assets/sea_ocean_seagulls_birds_sunset.gif)|![](assets/woman_flowers_plants_field_garden.gif)|![](assets/wood_anemones_wildflower_flower.gif)|
