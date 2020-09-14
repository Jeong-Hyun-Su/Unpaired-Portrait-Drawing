"""General-purpose test script for image-to-image translation.

Once you have trained your model with train.py, you can use this script to test the model.
It will load a saved model from --checkpoints_dir and save the results to --results_dir.

It first creates model and dataset given the option. It will hard-code some parameters.
It then runs inference for --num_test images and save results to an HTML file.

Example (You need to train models first or download pre-trained models from our website):
    Test a CycleGAN model (both sides):
        python test.py --dataroot ./datasets/maps --name maps_cyclegan --model cycle_gan

    Test a CycleGAN model (one side only):
        python test.py --dataroot datasets/horse2zebra/testA --name horse2zebra_pretrained --model test --no_dropout

    The option '--model test' is used for generating CycleGAN results only for one side.
    This option will automatically set '--dataset_mode single', which only loads the images from one set.
    On the contrary, using '--model cycle_gan' requires loading and generating results in both directions,
    which is sometimes unnecessary. The results will be saved at ./results/.
    Use '--results_dir <directory_path_to_save_result>' to specify the results directory.

    Test a pix2pix model:
        python test.py --dataroot ./datasets/facades --name facades_pix2pix --model pix2pix --direction BtoA

See options/base_options.py and options/test_options.py for more test options.
See training and test tips at: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/docs/tips.md
See frequently asked questions at: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/docs/qa.md
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
dirs = os.getcwd()
os.chdir(os.path.join(dirs, "Drawing"))

from Drawing.util import util
from Drawing.util.visualizer import save_images
from Drawing.options.test_options import TestOptions
from Drawing.data import create_dataset
from Drawing.util import html
import argparse
import time
from io import BytesIO
from scipy.misc import imresize
from PIL import Image


def app(model, svec):
    opt = TestOptions().parse()  # get test options
    opt.sinput = 'svec'
    opt.svec = svec
    opt.model_suffix = "_A"

    dataset = create_dataset(opt)

    if opt.eval:
        model.eval()
    for i, data in enumerate(dataset):
        if i >= opt.num_test:  # only apply our model to opt.num_test images.
            break
        model.set_input(data)  # unpack data from data loader
        model.test()           # run inference
        visuals = model.get_current_visuals()  # get image results

        aspect_ratio = opt.aspect_ratio

        # 라벨, 이미지 get
        _, data, _ = visuals.items()
        label, im_data = data

        # 변환
        im = util.tensor2im(im_data)
        # reshape
        h, w, _ = im.shape
        if aspect_ratio > 1.0:
            im = imresize(im, (h, int(w * aspect_ratio)), interp='bicubic')
        if aspect_ratio < 1.0:
            im = imresize(im, (int(h / aspect_ratio), w), interp='bicubic')

        # Send Image
        image = Image.fromarray(im)

        byte_io = BytesIO()
        image.save(byte_io, "PNG")
        byte_io.seek(0)

        return byte_io