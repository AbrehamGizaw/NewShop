import os

ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'webp', 'jiff', 'jfif']
ALLOWED_FILE_EXTENSIONS = ['doc', 'docx', 'pdf', 'xlsx']
LIMITED_FILE_SIZE_MB = 8

BASIC_GENDER_TYPES = {
    # Name : Description
    'male': 'male',
    'female': 'female'
}


ENV_CONFIG_PATH = os.path.join('InternationalB2BVentures', 'settings', 'env.json')
