import os
import random
from PIL import Image, ImageDraw

def generate_dataset(dataset_dir="trained_models/dummy_dataset", count=50):
    os.makedirs(os.path.join(dataset_dir, "circle"), exist_ok=True)
    os.makedirs(os.path.join(dataset_dir, "square"), exist_ok=True)
    
    for i in range(count):
        # Circle image
        img_circle = Image.new("RGB", (224, 224), color=(0, 0, 0))
        draw_c = ImageDraw.Draw(img_circle)
        r = random.randint(30, 85)
        cx = random.randint(90, 130)
        cy = random.randint(90, 130)
        color_c = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        draw_c.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color_c)
        img_circle.save(os.path.join(dataset_dir, "circle", f"circle_{i}.jpg"))
        
        # Square image
        img_square = Image.new("RGB", (224, 224), color=(0, 0, 0))
        draw_s = ImageDraw.Draw(img_square)
        w = random.randint(30, 85)
        sx = random.randint(90, 130)
        sy = random.randint(90, 130)
        color_s = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        draw_s.rectangle([sx - w, sy - w, sx + w, sy + w], fill=color_s)
        img_square.save(os.path.join(dataset_dir, "square", f"square_{i}.jpg"))
        
    print(f"Generated synthetic dataset: {count} circles and {count} squares in {dataset_dir}")

if __name__ == "__main__":
    generate_dataset()
