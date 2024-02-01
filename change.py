from PIL import Image
import os

def delete_all_files(directory_path):
    # ディレクトリ内の全てのファイルを取得
    all_files = [f for f in os.listdir(directory_path)]

    # ファイルを削除
    for file_name in all_files:
        file_path = os.path.join(directory_path, file_name)
        
        # ファイルかどうかを確認して削除
        if os.path.isfile(file_path):
            os.remove(file_path)

def delete_jpg_files(directory_path):
    # ディレクトリ内の .jpg ファイルを取得
    jpg_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.jpg')]

    # .jpg ファイルを削除
    for jpg_file in jpg_files:
        file_path = os.path.join(directory_path, jpg_file)
        os.remove(file_path)

def convert_jpg_to_png_pred(directory):
    # 保存先ディレクトリが存在しない場合は作成
    os.makedirs(directory, exist_ok=True)

    # 指定のディレクトリから jpg の画像ファイルを探す
    jpg_files = [f for f in os.listdir(directory) if f.lower().endswith('.jpg')]

    for index, jpg_file in enumerate(jpg_files, start=1):
        jpg_path = os.path.join(directory, jpg_file)

        # 画像を開いて変換
        with Image.open(jpg_path) as img:
            # 保存先のファイルパスを生成
            png_filename = f'image_{index}.png'
            png_path = os.path.join(directory, png_filename)

            # 画像を PNG に変換して保存
            img.save(png_path, 'PNG')

    # JPGの画像を削除
    delete_jpg_files(directory)

def convert_jpg_to_png_emb(directory, new_png_filename=None):
    # 保存先ディレクトリが存在しない場合は作成
    os.makedirs(directory, exist_ok=True)

    # 指定のディレクトリから jpg の画像ファイルを探す
    jpg_files = [f for f in os.listdir(directory) if f.lower().endswith('.jpg')]

    for index, jpg_file in enumerate(jpg_files, start=1):
        jpg_path = os.path.join(directory, jpg_file)

        # 画像を開いて変換
        with Image.open(jpg_path) as img:
            # 新しいファイル名が指定されていればそれを使用し、そうでなければエラーを発生
            if new_png_filename is None:
                raise ValueError("新しいファイル名を指定してください。")

            index_new_png_filename = new_png_filename + f'_{index}.png'

            png_path = os.path.join(directory, index_new_png_filename)

            # 画像を PNG に変換して保存
            img.save(png_path, 'PNG')

    # JPGの画像を削除
    delete_jpg_files(directory)




