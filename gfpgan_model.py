from gfpgan import GFPGANer
import torch
import numpy as np
from PIL import Image

def gfpgan_gogo(input_img_path, output_img_path):
    img = Image.open(input_img_path)
    original_img = img.copy()
    np_img = np.array(img)

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    model = GFPGANer(model_path='GFPGAN/GFPGANv1.4.pth', upscale=1, arch='clean', channel_multiplier=2, bg_upsampler=None, device=device)
    np_img_bgr = np_img[:, :, ::-1]
    _, _, gfpgan_output_bgr = model.enhance(np_img_bgr, has_aligned=False, only_center_face=False, paste_back=True)
    np_img = gfpgan_output_bgr[:, :, ::-1]

    restored_img = Image.fromarray(np_img)
    result_img = Image.blend(
        original_img, restored_img, 1
    )

    result_img.save(output_img_path)