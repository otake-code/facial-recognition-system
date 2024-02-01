from change import convert_jpg_to_png_emb, delete_all_files
from embedding_arcface import embedding_face

# パスと名前を指定してその中で1人の登録を行う
def registration(directory_path, name):

    # 登録したい画像ファイルのディレクトリのパス
    directory = directory_path

    # 画像をPNGに変換して名前を{name}_{n}.pngにする
    convert_jpg_to_png_emb(directory, name)

    # 画像を埋め込みcsvファイルを作成する
    embedding_face(directory)

    # ディレクトリ内のファイルを削除
    delete_all_files(directory)


