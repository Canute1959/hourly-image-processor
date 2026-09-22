from hourly_image_processor.daylight import is_light_enough
from hourly_image_processor.camera import take_picture
from hourly_image_processor.image_processor import proces
from hourly_image_processor.uploader import upload_image

def main():
    if not is_light_enough():
        return

    image = take_picture()

    print(f'Image created: {image}')
    
    image = process_image(image)
    # upload_image(image)


if __name__ == "__main__":
    main()