import os
import time
import cv2 as o
import numpy as np
from .patterns import stack_2_images, tile_chess, parang, ceplok

def cut(img):
    # crop image
    gray = o.cvtColor(img, o.COLOR_BGR2GRAY)
    th, threshed = o.threshold(gray, 240, 255, o.THRESH_BINARY_INV)

    kernel = o.getStructuringElement(o.MORPH_ELLIPSE, (11,11))
    morphed = o.morphologyEx(threshed, o.MORPH_CLOSE, kernel)

    cnts, _ = o.findContours(morphed, o.RETR_EXTERNAL, o.CHAIN_APPROX_SIMPLE)
    cnt = sorted(cnts, key=o.contourArea)[-1]
    x,y,w,h = o.boundingRect(cnt)
    new_img = img[y:y+h, x:x+w]

    return new_img        

def transBg(img):   
    gray = o.cvtColor(img, o.COLOR_BGR2GRAY)
    th, threshed = o.threshold(gray, 240, 255, o.THRESH_BINARY_INV)

    kernel = o.getStructuringElement(o.MORPH_ELLIPSE, (11,11))
    morphed = o.morphologyEx(threshed, o.MORPH_CLOSE, kernel)

    roi, _ = o.findContours(morphed, o.RETR_EXTERNAL, o.CHAIN_APPROX_SIMPLE)

    mask = np.zeros(img.shape, img.dtype)

    o.fillPoly(mask, roi, (255,)*img.shape[2], )

    masked_image = o.bitwise_and(img, mask)

    return masked_image

def fourChannels(img):
    height, width, channels = img.shape
    if channels < 4:
        new_img = o.cvtColor(img, o.COLOR_BGR2BGRA)
        return new_img

    return img

def create_pattern(produk, monumen, motif):
    folder = 'static/img'
    monumen_img = os.path.join(os.getcwd(), folder, monumen+'.jpg')
    motif_img = os.path.join(os.getcwd(), folder, motif+'.jpg')

    monumen_img = o.imread(monumen_img)
    motif_img = o.imread(motif_img)

    # monumen_img = o.imread(monumen_img, -1)

    # set to 4 channels
    monumen_img = fourChannels(monumen_img)
    motif_img = fourChannels(motif_img)

    # remove white background
    monumen_img = cut(monumen_img)
    motif_img = cut(motif_img)

    # set background transparent
    monumen_img = transBg(monumen_img)
    motif_img = transBg(motif_img)

    # o.imwrite(os.path.join(os.getcwd(), 'static/img/patterns/img2.png'), monumen_img)

    if motif == 'parang':
        motif_img = motif_img[:200, :200]  # need to be checked more

    # check again
    m, n = 400, 400

    monumen_img = o.resize(monumen_img, (m, n))
    motif_img = o.resize(motif_img, (m, n))

    if produk == 'fabric':
        cols = 5
        rows = 3
    else:
        cols = 8
        rows = 3

    if motif == 'truntum':
        tmp = stack_2_images(monumen_img, img_gap=motif_img)
        img_result = tile_chess(tmp, rows, cols,
                                img_gap=motif_img)
    elif motif == 'parang':
        # img_result = parang(monumen_img, rows, cols,
        #                     img_gap=motif_img)
        tmp = stack_2_images(monumen_img, img_gap=motif_img)
        img_result = tile_chess(tmp, rows, cols,
                                img_gap=motif_img)
    else:
        # img_result = ceplok(monumen_img, rows, cols,
        #                     img_gaps=[motif_img, motif_img])
        tmp = stack_2_images(monumen_img, img_gap=motif_img)
        img_result = tile_chess(tmp, rows, cols,
                                img_gap=motif_img)

    timestamp = str(time.time()).split('.')[0]
    save_dir = os.path.join(os.getcwd(), 'static/img/patterns')

    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    filename = os.path.join(save_dir, 'result_{}.png'.format(timestamp))
    o.imwrite(filename, img_result)

    return timestamp
