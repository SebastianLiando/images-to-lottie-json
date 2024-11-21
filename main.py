import glob
import logging
import os
import json

from lottie import objects
from lottie.utils import script
from PIL import Image

ANIMATION_WIDTH = 752
ANIMATION_HEIGHT = 715

# Get the parent folder of this script
script_folder_path = os.path.dirname(os.path.abspath(__file__))
lottie_json_output_path = f"{script_folder_path}/out"


def make_lottie_from_images(images_folder, image_format='png', basename='out', frame_rate=60, width=ANIMATION_WIDTH, height=ANIMATION_HEIGHT):
    images = glob.glob(f"{images_folder}/*.{image_format}")

    # Assumption is every image is a frame
    animation = objects.Animation(len(images), frame_rate)

    animation.width = width
    animation.height = height

    for frame, image in enumerate(images):
        img = objects.assets.Image().load(image)
        animation.assets.append(img)
        layer = objects.ImageLayer(img.id)
        ly = animation.add_layer(layer)
        ly.in_point = frame
        ly.out_point = frame+1  # every image stays for one frame only

    script.script_main(animation, path=lottie_json_output_path,
                       basename=basename, formats=['json'])


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler("script.log"),
                            logging.StreamHandler()
                        ])
    
    os.makedirs(lottie_json_output_path, exist_ok=True)

    # Load config.json as JSON object
    config = {}
    with open(f"{script_folder_path}/config.json") as f:
        config = json.load(f)

    # list folders inside folder input
    folders = glob.glob(f"{script_folder_path}/input/*")
    for folder in folders:
        logging.info(f"Processing {folder}")

        # Get only the folder name from the absolute folder path
        folder_name = os.path.basename(folder)
        logging.info(f'Animation name: {folder_name}.json')

        # Get the size of the image by examining the first file in the folder.
        # This is assuming that all images in the sequence are of the same size.
        first_file = glob.glob(f"{folder}/*")[0]

        # Get the image file format
        file_format = os.path.splitext(first_file)[1][1:]
        logging.info(f'Image format: {file_format}')

        first_img = Image.open(first_file)

        width, height = first_img.width, first_img.height
        logging.info(f"Image size: {width} x {height}")

        # Load frame rate from config file, otherwise defaults to 60 FPS
        frame_rate = config['frame_rate'].get(folder_name, 60)
        logging.info(f"Frame rate: {frame_rate} FPS")

        make_lottie_from_images(
            images_folder=folder,
            image_format=file_format,
            basename=folder_name,
            frame_rate=frame_rate,
            width=width,
            height=height
        )


if __name__ == "__main__":
    main()
