import os
import sys

dir = os.getcwd()
exp = 'pretrained'
imgsize = 512
dataroot = 'examples'
epoch = '200'
gpu_id = '0'

def seq_style(vec):
    os.chdir(os.path.join(dir, "Drawing"))
    # for vec in [[1, 0, 0], [0, 1, 0], [0, 0, 1]]:
    svec = '%d,%d,%d' % (vec[0], vec[1], vec[2])
    img1 = 'imagesstyle%d-%d-%d' % (vec[0], vec[1], vec[2])
    print('results/%s/test_%s/index%s.html' % (exp, epoch, img1[6:]))
    os.system('python test.py --dataroot %s --name %s --model test --output_nc 1 --no_dropout --model_suffix _A --num_test 1000 --epoch %s --imagefolder %s --sinput svec --svec %s --crop_size %d --load_size %d --gpu_ids %s' % (dataroot, exp, epoch, img1, svec, imgsize, imgsize, gpu_id))

    os.chdir(dir)
