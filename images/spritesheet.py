from PIL import Image
import os

def create_spritesheet(images, output_path):
    images = [Image.open(image) for image in images]

    # Assuming all images have the same size
    width, height = images[0].size

    spritesheet = Image.new("RGBA", (width * len(images), height))

    for i, image in enumerate(images):
        spritesheet.paste(image, (i * width, 0))

    spritesheet.save(output_path)


def change_black_to_transparency(image_path):
    image = Image.open(image_path)
    image = image.convert("RGBA")

    data = image.getdata()
    new_data = []
    threshold = 30

    for item in data:
        # Define a threshold for near-black values
        if item[0] < threshold and item[1] < threshold and item[2] < threshold:
            new_data.append((0, 0, 0, 0))  # Set near-black values to transparent
        else:
            new_data.append(item)

    image.putdata(new_data)
    return image

def main():
    # Get all .png files in the current working directory
    images = [file for file in os.listdir() if file.lower().endswith('.png')]

    if not images:
        print("No .png images found in the working directory.")
        return

    spritesheet_path = os.path.join(os.getcwd(),'gifs\\spritesheet.png')

    # Create spritesheet
    create_spritesheet(images, spritesheet_path)

    # Change black to transparency in the spritesheet
    spritesheet_with_transparency = change_black_to_transparency(spritesheet_path)

    # Save the final spritesheet with transparency
    spritesheet_with_transparency.save('spritesheet_with_transparency.png')
    print("Spritesheet with transparency saved: spritesheet_with_transparency.png")

if __name__ == "__main__":
    main()