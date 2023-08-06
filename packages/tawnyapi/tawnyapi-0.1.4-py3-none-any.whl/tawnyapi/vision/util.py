
import base64
from typing import List
import imutils
import cv2


def _resize_img(img, resize=None):
    if resize is None or (img.shape[1] <= resize and img.shape[2] <= resize):
        return img

    dim = None
    (h, w) = img.shape[:2]

    # height
    if h >= w:
        r = resize / float(h)
        dim = (int(w * r), resize)

    # width
    else:
        r = resize / float(w)
        dim = (resize, int(h * r))

    return cv2.resize(img, dim)


def _get_base64_images(images, resize=None, images_already_encoded=False):
    b64_images = []
    for img in images:
        if not images_already_encoded:
            img = _resize_img(img, resize=resize)
            _, buffer = cv2.imencode('.tif', img)
            b64_images.append(base64.b64encode(buffer).decode('ascii'))
        else:
            b64_images.append(base64.b64encode(img).decode('ascii'))
    return b64_images


def _load_images_from_paths(img_paths: List[str], load_as_bytes=False):
    images = []
    for img_path in img_paths:
        if load_as_bytes:
            with open(img_path, "rb") as f_in:
                images.append(f_in.read())
        else:
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            images.append(img)
    return images
