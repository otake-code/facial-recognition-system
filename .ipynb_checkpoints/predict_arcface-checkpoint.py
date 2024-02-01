import os
import csv
from itertools import combinations

import numpy as np
import onnx
import onnxruntime as ort
import torchvision.transforms as transforms
from PIL import Image
from collections import Counter

# 類似度判断の関数
def is_same_person(embedding1, embedding2, threshold):
    embedding1 = embedding1.flatten()
    embedding2 = embedding2.flatten()
    cos_sim = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    return cos_sim >= threshold, cos_sim

# 百分率の計算
def percentage(cos_sim):
    return round(-23.71 * cos_sim ** 2 + 49.98 * cos_sim + 73.69, 2)

# predict_imgディレクトリから正解率が最も高い人の名前を返す関数
def face_recofnition(directory):

    model_name = 'models/efficientnetv2_arcface.onnx'

    # 画像の前処理を定義
    mean_value = [0.485, 0.456, 0.406]
    std_value = [0.229, 0.224, 0.225]
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=mean_value,
            std=std_value
        )
    ])

    # ONNXモデルをロード
    onnx_model = onnx.load(model_name)
    ort_session = ort.InferenceSession(model_name)

    # 署名表示
    for prop in onnx_model.metadata_props:
        if prop.key == "signature":
            print(prop.value)

    # 入力名を入力する変数を取得
    input_name = onnx_model.graph.input[0].name

    # 推論対象の画像ファイルを取得
    image_dir = directory
    image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.png')]

    # CSVファイルが保存されているディレクトリのパスを指定
    csv_directory = 'embedding_csv/'

     # ディレクトリ内の要素を取得
    csv_directory_contents = os.listdir(csv_directory)

    # ディレクトリ内のサブディレクトリを取得
    subdirectories = [d for d in csv_directory_contents if os.path.isdir(os.path.join(csv_directory, d))]

    # 類似度の閾値
    similarity_threshold = 0.4

    # Trueになったcsvファイルの名前を格納する配列
    true_csv = []

    # それぞれのディレクトリ内のCSVファイルを処理
    for subdirectory in subdirectories:

        subdirectory_path = os.path.join(csv_directory, subdirectory)
        print(f"Subdirectory: {subdirectory}")

        # サブディレクトリ内のファイルを取得
        files_in_subdirectory = os.listdir(subdirectory_path)

        for predict_file in image_files:

            image = Image.open(predict_file).convert('RGB')
            image = transform(image)
            image = image.unsqueeze(0)  # バッチ次元を追加
            image = image.numpy()
            embedding = ort_session.run(None, {input_name: image})[0]  # 'input'をinput_nameに変更

            for csv_file in files_in_subdirectory:

                if csv_file.endswith(".csv"):

                    csv_file_path = os.path.join(subdirectory_path, csv_file)
                    
                    # CSVファイルからembeddingsを読み込む
                    csv_embeddings = []
                    with open(csv_file_path, 'r') as filename:
                        csv_reader = csv.reader(filename)
                        for row in csv_reader:
                            for value in row:
                                csv_embeddings.append(float(value))

                    np_csv_embeddings = np.array(csv_embeddings)

                    is_same, cos_similarity = is_same_person(embedding, np_csv_embeddings, similarity_threshold)
                    similarity_percentage = percentage(cos_similarity)
                    print(f"{csv_file} - {predict_file} similarity: {similarity_percentage}% - result: {is_same}")

                    # Trueが出たらそのcsvファイルの名前を格納
                    if is_same == True:
                        true_csv.append(subdirectory)
    
    # 一番多くTrueを出した名前を返すもしくは知らない人である名前を返す
    if true_csv:
        # Counterを使用して各要素の出現回数を辞書に保存
        element_counts = Counter(true_csv)

        # 一番多く出現した要素とその出現回数を取得
        most_common_element, most_common_count = element_counts.most_common(1)[0]

        return most_common_element

    else:

        return "I don't know"