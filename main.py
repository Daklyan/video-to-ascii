import shutils

from PIL import Image
from ascii import convert_image_to_ascii


def main():
    print("".join(convert_image_to_ascii("./test.jpg", 100, 50)))


if __name__ == "__main__":
    main()
