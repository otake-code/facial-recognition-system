# -*- coding: utf-8 -*-

#これが４３班メインコード
#初回はutils.pyをまず実行 そのあとにこのコード これによりdeviceList.jsonが作成
#utils.py lock.py line.py predict_aki.py deviceList.json akiフォルダを使用
import os
import csv
from itertools import combinations, product

import numpy as np
import onnx
import onnxruntime as ort
import torchvision.transforms as transforms
from PIL import Image
import cv2
import os
from camera import douga

from change import delete_all_files
from lock import judge
from line import perform_notification


#動画を撮影する
douga()

model_name = 'models/efficientnetv2_arcface.onnx'
optimal_threshold = 0.4

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

# 入力名を取得
input_name = onnx_model.graph.input[0].name

# 推論対象の画像ファイルを取得
image_dir = "aki/facecut"
image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.png')]

# "face.csv"からエンベディングを読み込む
csv_file = 'aki/embet/okada/okada_1.csv'
csv_embeddings = []
with open(csv_file, 'r') as filename:
    csv_reader = csv.reader(filename)
    for row in csv_reader:
        for value in row:
            csv_embeddings.append(float(value))

np_csv_embeddings = np.array(csv_embeddings)

# 類似度判断の関数
def is_same_person(embedding1, embedding2, threshold):
    embedding1 = embedding1.flatten()
    embedding2 = embedding2.flatten()
    cos_sim = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    return cos_sim >= threshold, cos_sim

# 百分率の計算
def percentage(cos_sim):
    return round(-23.71 * cos_sim ** 2 + 49.98 * cos_sim + 73.69, 2)


# 新しい画像とCSVのエンベディングとの類似度を計算
success_count = 0  # 類似度が90%以上の成功したカウント
total_count = 0  # 処理した総画像数

for image_file in image_files:
    image = Image.open(image_file).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)  # バッチ次元を追加
    image = image.numpy()
    embedding = ort_session.run(None, {input_name: image})[0]  # 'input'をinput_nameに変更


    similarity, cos_sim = is_same_person(embedding, np_csv_embeddings, optimal_threshold)
    total_count += 1  # 総画像数をカウント

    if percentage(cos_sim) >= 70:
        success_count+=1 #成功数のカウント
        print("{}, 岡田の画像, 類似度= {}%, 【成功○】 ".format(image_file, percentage(cos_sim)))

    else:
        print("{}, 岡田の画像, 類似度= {}%, 【失敗×】 ".format(image_file, percentage(cos_sim)))


# 成功した割合を計算
success_ratio = success_count / total_count
print("一致率 ={}%".format(success_ratio))
# 1割以上成功していれば本人とみなす
if success_ratio > 0:
    picture=""
    print("高齢者である可能性が高いです。O") # perform_notification 関数を必要なパラメータで呼び出す
    perform_notification(picture) #LINEにおしらせ
    judge() #ドアの開閉
else:
    print("高齢者である可能性が低いです。X")

delete_all_files("aki/facecut")
