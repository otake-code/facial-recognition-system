import os
import csv
from itertools import combinations

import numpy as np
import onnx
import onnxruntime as ort
import torchvision.transforms as transforms
from PIL import Image

def save_embeddings_to_csv(embeddings, image_files, output_directory):
    # 保存先ディレクトリが存在しない場合は作成
    os.makedirs(output_directory, exist_ok=True)

    for image_file, embedding in zip(image_files, embeddings):

        # ディレクトリ名を取得
        directory_name = os.path.splitext(os.path.basename(image_file))[0].split('_')[0]

        # 対応するディレクトリを作成
        subdirectory_path = os.path.join(output_directory, directory_name)
        os.makedirs(subdirectory_path, exist_ok=True)

        # CSVファイルのパスを生成
        csv_filename = os.path.join(subdirectory_path, os.path.basename(image_file).replace('.png', '.csv'))

        # CSVファイルに書き込む
        with open(csv_filename, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            for value in embedding:
                csv_writer.writerow(value)

def embedding_face(directory):

    model_name = 'models/efficientnetv2_arcface.onnx'
    optimal_threshold = 0.4

    # 保存先ディレクトリの指定
    output_directory = 'aki/embet'

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

    # 入力名を取得
    input_name = onnx_model.graph.input[0].name

    # 埋め込み対象の画像ファイルを取得
    image_dir = directory
    image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.png')]

    # 画像を読み込み、前処理を行い、モデルで推論を行う
    embeddings = []
    for image_file in image_files:
        image = Image.open(image_file).convert('RGB')
        image = transform(image)
        image = image.unsqueeze(0)  # バッチ次元を追加
        image = image.numpy()
        embedding = ort_session.run(None, {input_name: image})[0]  # 'input'をinput_nameに変更
        embeddings.append(embedding)

    save_embeddings_to_csv(embeddings, image_files, output_directory)
