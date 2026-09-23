# src/hourly_image_processor/image_processor.py

from datetime import datetime
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFont, ImageDraw


def process_image(
    image_path: Path,
    output_path: Path | None = None,
    max_width: int = 1920,
    quality: int = 90,
) -> Path:
    """
    Behandler et bilde:
      - åpner bildet
      - korrigerer EXIF-rotasjon
      - skalerer ned dersom bildet er større enn max_width
      - gjør en liten kontrastforbedring
      - lagrer som JPEG

    Returnerer filnavnet til det behandlede bildet.
    """

    image_path = Path(image_path)
    timestamp = datetime.strptime(image_path.stem, "img%Y%m%d-%H")
    timestamp_text =  timestamp.strftime("%d.%m.%Y-%H")

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    if output_path is None:
        output_path = image_path

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(image_path) as image:

        # Sørg for RGB før lagring som JPEG
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        myFont = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 65)
        # Skaler ned, men aldri opp
        if image.width > max_width:
            new_height = round(
                image.height * max_width / image.width
            )

            image = image.resize(
                (max_width, new_height),
                Image.Resampling.LANCZOS,
            )
        draw = ImageDraw.Draw(image) 
        text = timestamp_text
        x = 750
        y = 975

        # Finn størrelsen på teksten
        bbox = draw.textbbox((x, y), text, font=myFont)

        # Litt luft rundt teksten
        padding = 10

    # Tegn hvit bakgrunn
        draw.rectangle(
            (
                bbox[0] - padding,
                bbox[1] - padding,
                bbox[2] + padding,
                bbox[3] + padding,
            ),
            fill="white",
        )

        # Tegn teksten
        draw.text(
            (x, y),
            text,
            font=myFont,
            fill="black",
        )     
        # Svak kontrastforbedring
        image = ImageEnhance.Contrast(image).enhance(1.05)

        image.save(
            output_path,
            format="JPEG",
            quality=quality,
            optimize=True,
        )

    return output_path