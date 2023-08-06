import abc

import torch
import torchvision
import clip
import numpy as np
from PIL import Image

import matplotlib.pyplot as plt


class ImageGenerator(metaclass=abc.ABCMeta):
    def __init__(self, ):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"USING {self.device}")

        self.clip_input_img_size = 224

        self.clip_model, _clip_preprocess = clip.load(
            "ViT-B/32",
            device=self.device,
        )
        self.clip_model = self.clip_model.eval()

        self.clip_norm_trans = torchvision.transforms.Normalize(
            (0.48145466, 0.4578275, 0.40821073),
            (0.26862954, 0.26130258, 0.27577711),
        )

        self.aug_transform = torch.nn.Sequential(
            torchvision.transforms.RandomHorizontalFlip(),
            torchvision.transforms.RandomAffine(24, (.1, .1)),
        ).to(self.device)

    def augment(
        self,
        img_batch,
        target_img_width,
        target_img_height,
        num_crops=32,
        crop_scaler=1,
    ):
        x_pad_size = target_img_width // 2
        y_pad_size = target_img_height // 2
        img_batch = torch.nn.functional.pad(
            img_batch,
            (
                x_pad_size,
                x_pad_size,
                y_pad_size,
                y_pad_size,
            ),
            mode='constant',
            value=0,
        )

        img_batch = self.aug_transform(img_batch)

        min_img_size = min(target_img_width, target_img_height)

        augmented_img_list = []
        for crop in range(num_crops):
            crop_size = int(
                torch.normal(
                    1.2,
                    .3,
                    (),
                ).clip(.43, 1.9) * min_img_size)

            if crop > num_crops - 4:
                crop_size = int(min_img_size * 1.4)

            offsetx = torch.randint(
                0,
                int(target_img_width * 2 - crop_size),
                (),
            )
            offsety = torch.randint(
                0,
                int(target_img_height * 2 - crop_size),
                (),
            )
            augmented_img = img_batch[:, :, offsety:offsety + crop_size,
                                      offsetx:offsetx + crop_size, ]
            augmented_img = torch.nn.functional.interpolate(
                augmented_img,
                (int(224 * crop_scaler), int(224 * crop_scaler)),
                mode='bilinear',
                align_corners=True,
            )
            augmented_img_list.append(augmented_img)

        img_batch = torch.cat(augmented_img_list, 0)

        up_noise = 0.11
        img_batch = img_batch + up_noise * torch.rand(
            (img_batch.shape[0], 1, 1, 1)).to(self.device) * torch.randn_like(
                img_batch, requires_grad=False)

        return img_batch

    def get_clip_img_encodings(
        self,
        img_batch: torch.Tensor,
        do_preprocess: bool = True,
    ):
        if do_preprocess:
            img_batch = self.clip_norm_trans(img_batch)
            img_batch = torch.nn.functional.upsample_bilinear(
                img_batch,
                (self.clip_input_img_size, self.clip_input_img_size),
            )

        img_logits = self.clip_model.encode_image(img_batch)
        img_logits = img_logits / img_logits.norm(dim=-1, keepdim=True)

        return img_logits

    def get_clip_text_encodings(
        self,
        text: str,
    ):
        tokenized_text = clip.tokenize([text])
        tokenized_text = tokenized_text.to(self.device).detach().clone()

        text_logits = self.clip_model.encode_text(tokenized_text)
        text_logits = text_logits / text_logits.norm(dim=-1, keepdim=True)

        return text_logits

    def compute_clip_loss(
        self,
        img_batch: torch.Tensor,
        text: str,
        loss_type: str = 'cosine_similarity',
    ):
        img_logits = self.get_clip_img_encodings(img_batch)
        text_logits = self.get_clip_text_encodings(text)

        img_logits = img_logits.clip(-.1, .1)
        text_logits = text_logits.clip(-.1, .1)

        loss = 0
        if loss_type == 'cosing_similarity':
            loss += -torch.cosine_similarity(text_logits, img_logits).mean()
        if loss_type == "spherical_distance":
            loss = (text_logits - img_logits).norm(
                dim=-1).div(2).arcsin().pow(2).mul(2).mean()

        return loss

    # @abc.abstractmethod
    def generate_from_prompt(
        self,
        *args,
        **kwargs,
    ):
        raise NotImplementedError(
            '`generate_from_prompt` method must be defined by the user.')

    def load_img(
        self,
        img_path: str,
    ):
        img_pil = Image.open(img_path)
        img_pil = img_pil.convert('RGB')

        img_tensor = torch.tensor(np.asarray(img_pil)).to(
            self.device).float()[None, :]
        img_tensor /= 255.
        img_tensor = img_tensor.permute(0, 3, 1, 2)

        return img_tensor


if __name__ == "__main__":
    prompt = "The image of a rainy landscape"

    anti_prompt = "The image of a sunny landscape"
    co_prompt = "The image of a cloudy landscape"

    anti_img_path = "./sunny.jpg"
    co_img_path = "./rainy.jpg"

    image_generator = ImageGenerator()

    prompt_embed = image_generator.get_clip_text_encodings(prompt)
    anti_prompt_embed = image_generator.get_clip_text_encodings(anti_prompt)
    co_prompt_embed = image_generator.get_clip_text_encodings(co_prompt)

    anti_img = image_generator.load_img(anti_img_path)
    anti_img_embed = image_generator.get_clip_img_encodings(anti_img)

    co_img = image_generator.load_img(co_img_path)
    co_img_embed = image_generator.get_clip_img_encodings(co_img)

    prompt_embed = prompt_embed.clip(-.1, .1)
    anti_prompt_embed = anti_prompt_embed.clip(-.1, .1)
    co_prompt_embed = co_prompt_embed.clip(-.1, .1)
    anti_img_embed = anti_img_embed.clip(-.1, .1)
    co_img_embed = co_img_embed.clip(-.1, .1)

    # XXX: SINGLE HIST
    bins = np.linspace(-.5, .5, 256)

    plt.figure(figsize=(16, 12))

    plt.hist(
        prompt_embed.detach().cpu().numpy().flatten(),
        bins,
        alpha=0.5,
        label='PROMPT',
    )
    plt.hist(
        anti_prompt_embed.detach().cpu().numpy().flatten(),
        bins,
        alpha=0.5,
        label='ANTI PROMPT',
    )
    plt.hist(
        co_prompt_embed.detach().cpu().numpy().flatten(),
        bins,
        alpha=0.5,
        label='CO PROMPT',
    )
    plt.hist(
        anti_img_embed.detach().cpu().numpy().flatten(),
        bins,
        alpha=0.5,
        label='ANTI IMG',
    )
    plt.hist(
        co_img_embed.detach().cpu().numpy().flatten(),
        bins,
        alpha=0.5,
        label='CO IMG',
    )

    plt.legend(loc='upper right')

    plt.savefig('hist.png', dpi=200)

    # XXX: MULTIPLE HIST
    bins = np.linspace(-.5, .5, 256)

    plt.figure(figsize=(16, 12))
    plt.hist(
        prompt_embed.detach().cpu().numpy().flatten(),
        alpha=0.5,
        label='PROMPT',
        bins=bins,
    )
    plt.hist(
        anti_prompt_embed.detach().cpu().numpy().flatten(),
        alpha=0.5,
        label='ANTI PROMPT',
        bins=bins,
    )
    plt.legend(loc='upper right')
    plt.savefig('hist-prompt-antiprompt.png', dpi=200)

    plt.figure(figsize=(16, 12))
    plt.hist(
        prompt_embed.detach().cpu().numpy().flatten(),
        alpha=0.5,
        label='PROMPT',
        bins=bins,
    )
    plt.hist(
        co_prompt_embed.detach().cpu().numpy().flatten(),
        alpha=0.5,
        label='CO PROMPT',
        bins=bins,
    )
    plt.legend(loc='upper right')
    plt.savefig('hist-prompt-coprompt.png', dpi=200)

    plt.figure(figsize=(16, 12))
    plt.hist(
        prompt_embed.detach().cpu().numpy().flatten(),
        alpha=0.5,
        label='PROMPT',
        bins=bins,
    )
    plt.hist(
        anti_img_embed.detach().cpu().numpy().flatten(),
        alpha=0.5,
        label='ANTI IMG',
        bins=bins,
    )
    plt.legend(loc='upper right')
    plt.savefig('hist-prompt-antiimg.png', dpi=200)

    plt.figure(figsize=(16, 12))
    plt.hist(
        prompt_embed.detach().cpu().numpy().flatten(),
        alpha=0.5,
        label='PROMPT',
        bins=bins,
    )
    plt.hist(
        co_img_embed.detach().cpu().numpy().flatten(),
        alpha=0.5,
        label='CO IMG',
        bins=bins,
    )
    plt.legend(loc='upper right')
    plt.savefig('hist-prompt-coimg.png', dpi=200)

    # XXX: MULTIPLE PLOTS

    plt.figure(figsize=(16, 12))
    plt.plot(
        prompt_embed.detach().cpu().numpy().flatten(),
        alpha=0.5,
        label='PROMPT',
    )
    plt.plot(
        anti_prompt_embed.detach().cpu().numpy().flatten(),
        alpha=0.5,
        label='ANTI PROMPT',
    )
    plt.legend(loc='upper right')
    plt.savefig('plot-prompt-antiprompt.png', dpi=200)

    plt.figure(figsize=(16, 12))
    plt.plot(
        prompt_embed.detach().cpu().numpy().flatten(),
        alpha=0.5,
        label='PROMPT',
    )
    plt.plot(
        co_prompt_embed.detach().cpu().numpy().flatten(),
        alpha=0.5,
        label='CO PROMPT',
    )
    plt.legend(loc='upper right')
    plt.savefig('plot-prompt-coprompt.png', dpi=200)

    plt.figure(figsize=(16, 12))
    plt.plot(
        prompt_embed.detach().cpu().numpy().flatten(),
        alpha=0.5,
        label='PROMPT',
    )
    plt.plot(
        anti_img_embed.detach().cpu().numpy().flatten(),
        alpha=0.5,
        label='ANTI IMG',
    )
    plt.legend(loc='upper right')
    plt.savefig('plot-prompt-antiimg.png', dpi=200)

    plt.figure(figsize=(16, 12))
    plt.plot(
        prompt_embed.detach().cpu().numpy().flatten(),
        alpha=0.5,
        label='PROMPT',
    )
    plt.plot(
        co_img_embed.detach().cpu().numpy().flatten(),
        alpha=0.5,
        label='CO IMG',
    )
    plt.legend(loc='upper right')
    plt.savefig('plot-prompt-coimg.png', dpi=200)
