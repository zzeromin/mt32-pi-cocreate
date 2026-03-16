import os
from PIL import Image

def resize_images(directory='process', target_width=800):
    if not os.path.exists(directory):
        print(f"Directory {directory} not found.")
        return

    for filename in os.listdir(directory):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            # Only process files that DON'T end in _small.png, 
            # OR if a file IS named _small.png but is very large (> 1MB), we might want to re-process it.
            # But simpler: if processN.png exists, create processN_small.png.
            # If ONLY processN_small.png exists and it's large, resize it.
            
            filepath = os.path.join(directory, filename)
            
            # If it's a "small" file but oversized, or a regular file
            if not filename.endswith('_small.png') or os.path.getsize(filepath) > 1024 * 1024:
                try:
                    with Image.open(filepath) as img:
                        # Original dimensions
                        w, h = img.size
                        if w > target_width:
                            print(f"Resizing {filename}...")
                            new_h = int(h * (target_width / w))
                            img = img.resize((target_width, new_h), Image.Resampling.LANCZOS)
                            
                            # Determine output name
                            if filename.endswith('_small.png'):
                                out_name = filename
                            else:
                                out_name = filename.rsplit('.', 1)[0] + '_small.png'
                            
                            img.save(os.path.join(directory, out_name), optimize=True)
                            print(f"Saved as {out_name}")
                            
                            # If we made a NEW _small file, delete the original large one
                            if out_name != filename:
                                os.remove(filepath)
                                print(f"Deleted original {filename}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    resize_images()
