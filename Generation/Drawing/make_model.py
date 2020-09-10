import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Drawing.options.test_options import TestOptions
from Drawing.models import create_model
from Drawing.util.visualizer import save_images
from Drawing.util import html


def make_model(style):
    vec = list(map(int, style.split("-")))
    svec = '%d,%d,%d' % (vec[0], vec[1], vec[2])

    opt = TestOptions().parse()  # get test options

    opt.sinput = 'svec'
    opt.svec = svec
    opt.name = "pretrained"
    opt.model_suffix = "_A"
    opt.imagefolder = 'imagesstyle%d-%d-%d' % (vec[0], vec[1], vec[2])

    model = create_model(opt)      # create a model given opt.model and other options
    model.setup(opt)               # regular setup: load and print networks; create schedulers

    return model
