from hourly_image_processor.daylight import is_light_enough
def main():
    if not is_light_enough():
        return

    image = take_picture()
    image = process_image(image)
    upload_image(image)


if __name__ == "__main__":
    main()