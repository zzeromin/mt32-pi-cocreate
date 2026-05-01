import os
from PIL import Image

def update_gallery(directory='process', target_width=800):
    if not os.path.exists(directory):
        print(f"Directory {directory} not found.")
        return

    # 수정 시간 순서대로 파일 리스트 생성
    files = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(directory, filename)
            files.append({
                'name': filename,
                'path': filepath,
                'mtime': os.path.getmtime(filepath)
            })

    # 파일 수정 시간 기준 정렬
    files.sort(key=lambda x: x['mtime'])

    print(f"Found {len(files)} files. Processing and re-indexing...")

    new_indices = []
    temp_files = []

    for i, file_info in enumerate(files):
        filename = file_info['name']
        filepath = file_info['path']
        output_name = f"tmp_process{i}_small.png"
        output_path = os.path.join(directory, output_name)
        
        try:
            with Image.open(filepath) as img:
                w, h = img.size
                # 너비가 target_width보다 클 경우 리사이징
                if w > target_width:
                    print(f"Resizing {filename} ({w}px -> {target_width}px)...")
                    new_h = int(h * (target_width / w))
                    img = img.resize((target_width, new_h), Image.Resampling.LANCZOS)
                
                # 최적화된 PNG 파일로 저장
                img.convert('RGB').save(output_path, 'PNG', optimize=True)
                print(f"Saved {output_name}")
                temp_files.append(output_name)
                new_indices.append(i)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # 이전 파일 정리 (기존 JPG 및 small.png 파일 삭제)
    for file_info in files:
        try:
            os.remove(file_info['path'])
            print(f"Deleted old file: {file_info['name']}")
        except Exception as e:
            print(f"Error deleting {file_info['name']}: {e}")

    # 임시 파일을 최종 파일명으로 변경
    final_indices = []
    for i, temp_name in enumerate(temp_files):
        final_name = f"process{i}_small.png"
        try:
            os.rename(os.path.join(directory, temp_name), os.path.join(directory, final_name))
            final_indices.append(i)
        except Exception as e:
            print(f"Error renaming {temp_name}: {e}")

    print(f"Gallery updated. Total images: {len(final_indices)}")
    print(f"New PROCESS_PHOTOS array: {final_indices}")
    return final_indices

if __name__ == "__main__":
    # 'process' 폴더가 있는 frontend/mt32pi/ 경로에서 실행해야 함
    update_gallery()
