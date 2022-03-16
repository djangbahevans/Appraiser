import os

from app.config import settings

static_DIR = settings.STATIC_DIR or os.path.dirname(os.path.relpath(__file__))
image_DIR = "{static_DIR}/images".format(static_DIR=static_DIR)
items_DIR = "{image_DIR}/items".format(image_DIR=image_DIR)
