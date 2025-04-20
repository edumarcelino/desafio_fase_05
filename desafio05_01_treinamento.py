# Importa a biblioteca Roboflow para baixar datasets da plataforma
from roboflow import Roboflow

# Bibliotecas padrão
import os
import shutil
import torch  # Utilizada para verificar se a GPU está disponível

from datetime import datetime

# Biblioteca do YOLOv8 (Ultralytics)
from ultralytics import YOLO

from pathlib import Path

if __name__ == "__main__":

    # -------------------------------
    # Verifica se a GPU está disponível
    # -------------------------------
    usa_gpu = torch.cuda.is_available()
    print(f"GPU disponível: {usa_gpu}")

    # -------------------------------
    # Faz o download do dataset com Roboflow
    # -------------------------------
    rf = Roboflow(api_key="hApyf07gICxTJlulxK5j")
    project = rf.workspace("fiap-cxe1i").project("desafio-fase-05")
    dataset = project.version(1).download("yolov8")
    dataset_name = dataset.location.split('/')[-1]

    # -------------------------------
    # Cria o arquivo de configuração data.yaml
    # -------------------------------
    yaml_path = os.path.join(os.getcwd(), "data.yaml")
    train_path = os.path.join(dataset.location, "train", "images")
    val_path = os.path.join(dataset.location, "valid", "images")

    with open(yaml_path, "w") as f:
        f.write(f"""train: {train_path.replace(os.sep, '/')}
val: {val_path.replace(os.sep, '/')}
nc: 3
names: ['faca', 'tesoura', 'objeto_cortante_outro']
""")
    print(f"Arquivo YAML criado em: {yaml_path}")

    # -------------------------------
    # Carrega o modelo base YOLOv8 e treina
    # -------------------------------
    model = YOLO('yolov8n.pt')  
    model.train(
        data='data.yaml',
        epochs=100,
        imgsz=640,
        patience=10,  # Parar se não melhorar em 10 épocas
        device=0 if usa_gpu else 'cpu'
    )

    # -------------------------------
    # Copia o melhor modelo do último treinamento
    # -------------------------------
    train_dirs = sorted(Path("runs/detect").glob("train*"), key=os.path.getmtime, reverse=True)
    modelo_treinado_origem = train_dirs[0] / "weights" / "best.pt"

    # Caminho final desejado
    pasta_modelos = Path("modelos")
    pasta_modelos.mkdir(parents=True, exist_ok=True)
    modelo_destino_final = pasta_modelos / "best_model.pt"

    if modelo_treinado_origem.exists():
        shutil.copy(modelo_treinado_origem, modelo_destino_final)
        print(f"✅ Modelo final salvo em: {modelo_destino_final}")
    else:
        print("❌ Erro: modelo não encontrado após o treinamento.")
