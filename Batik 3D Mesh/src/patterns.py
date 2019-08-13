import numpy as np
from scipy import ndimage
import cv2 as o
import os


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

def stack_2_images(img, img_gap):
    m = n = img.shape[0]
    img = ndimage.rotate(img, 45)
    img = ndimage.rotate(img, -45)
    img = o.resize(img, (m, n))

    tmp = img.copy().astype(np.int32)
    tmp[tmp > 0] = -999

    img_gap = tmp + img_gap.copy().astype(np.int32)
    img_gap[img_gap < 0] = 0
    img_gap = img_gap.astype(np.uint8)

    return img_gap + img


def tile_full(img, rows, cols):
    img_result = np.concatenate([img for _ in range(cols)], axis=1)
    img_result = np.concatenate([img_result for _ in range(rows)], axis=0)

    return img_result


def tile_chess(img, rows, cols, img_gap=None):
    if type(img_gap) is not np.ndarray:
        img_gap = np.zeros((img.shape[0], img.shape[1], 3),
                           dtype='uint8')

    temp1 = np.concatenate([img if i % 2 == 0 else img_gap
                            for i in range(cols)], axis=1)
    temp2 = np.concatenate([img if i % 2 == 1 else img_gap
                            for i in range(cols)], axis=1)
    img_result = np.concatenate([temp1 if i % 2 == 0 else temp2
                                 for i in range(rows)], axis=0)

    return img_result


def tile_stripe(img, rows, cols, orientation='h', img_gap=None):
    assert orientation in ['h', 'v'], 'Not available'

    if orientation == 'h':
        axises = (0, 1)
    else:
        axises = (1, 0)
        tmp = cols
        cols = rows
        rows = tmp

    if type(img_gap) is not np.ndarray:
        img_gap = np.zeros((img.shape[0], img.shape[1], 3),
                           dtype='uint8')

    img_result = np.concatenate([img if i % 2 == 0 else img_gap
                                 for i in range(rows)],
                                axis=axises[0])
    img_result = np.concatenate([img_result for _ in range(cols)],
                                axis=axises[1])

    return img_result


def edges_cutted(img, rows, cols, mode=1, ceplok=False, img_gap=None):
    assert mode in [1, 2], 'Mode not allowed'

    if ceplok:
        assert img_gap is not None, \
            'Banji mode, img_gap should not be None'

    img_l = img[0:img.shape[0], 0:int(img.shape[0]/2)]

    level = int(img.shape[0]/2)  # where to cut
    sub = 0  # offset

    if ceplok:
        sub = int(img.shape[0]/5)

    if mode == 1:  # to produce front layer image (main)
        indices = np.triu_indices(level, sub)
    else:  # to produce background layer image (secondary)
        indices = np.tril_indices(level, sub)

    np.fliplr(img_l)[indices] = 0
    np.fliplr(np.flipud(img_l))[indices] = 0

    img_r = np.fliplr(img_l)

    img_result = np.hstack([img_l, img_r])

    if ceplok:
        if mode == 2:
            img_gap = None

    # # set to 4 channels
    # img_result = fourChannels(img_result)

    # # remove white background
    # img_result = cut(img_result)

    # # set background transparent
    # img_result = transBg(img_result)

    # # o.imwrite(os.path.join(os.getcwd(), 'static/img/patterns/img3.png'), img_result)        

    return tile_chess(img_result, rows, cols, img_gap=img_gap)


def parang(img, rows, cols, img_gap=None):
    if type(img_gap) is not np.ndarray:
        img_gap = np.zeros((img.shape[0],
                            img.shape[1], 3), dtype='uint8')

    img_f = edges_cutted(img, rows, cols, mode=1, img_gap=img_gap)
    img_b = edges_cutted(img_gap, rows, cols, mode=2)

    return img_f + img_b


def ceplok(img, rows, cols, img_gaps):
    img_f = edges_cutted(img, rows, cols, mode=1,
                         ceplok=True, img_gap=img_gaps[0])
    img_b = edges_cutted(img_gaps[1], rows, cols, mode=2,
                         ceplok=True, img_gap=img)

    return img_f + img_b
