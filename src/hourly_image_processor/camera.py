# src/hourly_image_processor/camera.py

import datetime as dt
import subprocess
from pathlib import Path


def take_picture(
    root_directory="/home/knut/projects/hourly-image-processor/data/temp",
    width=1920,
    height=1080,
) -> Path:

    now = dt.datetime.now()

    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    hour = now.strftime("%H")

    directory = Path(root_directory) / year / month / day
    directory.mkdir(parents=True, exist_ok=True)

    filename = directory / f"img{year}{month}{day}-{hour}.jpg"

    subprocess.run(
        [
            "rpicam-still",
            "--output", str(filename),
            "--width", str(width),
            "--height", str(height),
            "--nopreview",
        ],
        check=True,
    )

    return filename