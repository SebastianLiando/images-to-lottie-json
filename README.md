## Image Frames to Lottie JSON Converter
This is a Python script to combine image frames into a single animation and export it as Lottie JSON.

### Getting Started
1. Install the required dependencies: `pip install -r requirements.txt`
2. Duplicate `config.template.json` and rename it to `config.json`
3. Create `input` folder in the root directory
4. Create a child folder inside `input` folder. Place your image frames in this folder. The name of the folder will be the animation name. Make sure that the order of the files are the order of the image frames.
5. Run the script using `python main.py`. This script will go through each folder in the `input` folder and generate Lottie JSON for each one.

#### Modifying Frame Rate of Specific Animations
By default, generated animations will be in 60 FPS. You can configure a specific animation to be a specific framerate in `config.json` under `frame_rate`. The key will be the folder name and the value will be the FPS.

For example, if you have the image frames under the folder `typhoon` and you want it to be 30 FPS, this will be the config:

```json
{
    "frame_rate": {
        "typhoon": 30
    } 
}
```