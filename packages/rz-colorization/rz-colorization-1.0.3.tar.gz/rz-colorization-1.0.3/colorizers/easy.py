import torch
import matplotlib.pyplot as plt
import PIL
import numpy as np
from .eccv16 import eccv16
from .util import preprocess_img, postprocess_tens,load_img


def pipeline(path:str):
    image = load_img(path)
    (tens_l_orig, tens_l_rs) = preprocess_img(image, HW=(256,256))
    colorizer_model = eccv16().eval()
    out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_model(tens_l_rs).cpu())
    return out_img_eccv16