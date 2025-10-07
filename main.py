import os
import cv2
import argparse
from pathlib import Path

def resize_and_convert_fast(input_dir, max_side=1000):
    input_dir = Path(input_dir)
    output_dir = Path("resized_jpg")
    output_dir.mkdir(exist_ok=True)

    valid_ext = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}

    for file_path in input_dir.iterdir():
        if file_path.suffix.lower() not in valid_ext:
            continue
        if not file_path.is_file():
            continue

        try:
            # Rasmdan meta ma'lumotni o‘qimasdan to‘g‘ridan-to‘g‘ri numpy array sifatida o‘qish
            img = cv2.imread(str(file_path))
            if img is None:
                print(f"❌ Failed to read {file_path.name}")
                continue

            h, w = img.shape[:2]
            longest_side = max(w, h)

            if longest_side > max_side:
                scale = max_side / float(longest_side)
                new_w, new_h = int(w * scale), int(h * scale)
                img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
            else:
                new_w, new_h = w, h

            # BGR → RGB shart emas, chunki cv2 imwrite jpg uchun BGR ni qabul qiladi
            out_path = output_dir / f"{file_path.stem}.jpg"

            # .jpg formatda yozamiz (95% sifat)
            cv2.imwrite(str(out_path), img, [cv2.IMWRITE_JPEG_QUALITY, 95])

            print(f"✅ Saved: {out_path.name} ({new_w}x{new_h})")

        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")

    print(f"\n🚀 All done! Converted images saved to: {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", required=True, help="Path to the images folder")
    parser.add_argument("--max-size", type=int, default=1000, help="Max side length (default=1000)")
    args = parser.parse_args()

    resize_and_convert_fast(args.images, args.max_size)
