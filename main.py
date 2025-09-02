import os
import argparse
from PIL import Image, ImageOps

def resize_images(input_dir):
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)

        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff")):
            try:
                with Image.open(file_path) as img:
                    # EXIF orientatsiyasini tekislash
                    img = ImageOps.exif_transpose(img)

                    w, h = img.size

                    if w <= 1000 and h <= 1000:
                        print(f"Skip (small): {filename} ({w}x{h})")
                        continue

                    if w == h:
                        new_size = (1000, 1000)
                    else:
                        if w > h:
                            scale = 1000 / float(w)
                        else:
                            scale = 1000 / float(h)
                        new_size = (int(w * scale), int(h * scale))

                    resized = img.resize(new_size, Image.LANCZOS)
                    resized.save(file_path)

                    print(f"Resized: {filename} -> {new_size}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", required=True, help="Path to the images folder")
    args = parser.parse_args()

    resize_images(args.images)
