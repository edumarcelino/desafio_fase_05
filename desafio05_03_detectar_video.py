import cv2
from IPython.display import display
import PIL.Image
from ultralytics import YOLO
from desafio05_00_config import CANAL_ENVIO
from desafio05_02_alertas import enviar_alerta
import os

# Caminho do vídeo
video_path = "videos/video.mp4"

# ✅ Usa o modelo salvo na pasta 'modelos'
model = YOLO("modelos/best_model.pt")

# Mapeamento das classes
id_para_nome = {
    0: "faca",
    1: "tesoura",
    2: "objeto_cortante_outro"
}

# Variável global para armazenar o último frame salvo
ultimo_frame_salvo = None

# Pasta para salvar os frames detectados
pasta_frames_salvos = "frames_detectados"
os.makedirs(pasta_frames_salvos, exist_ok=True)

def processar_video(path_video, output_path="output_video02_detectado.mp4"):
    global ultimo_frame_salvo

    cap = cv2.VideoCapture(path_video)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    contagem = {nome: 0 for nome in id_para_nome.values()}
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        annotated_frame = results[0].plot()
        out.write(annotated_frame)

        if frame_count % 60 == 0:
            display(PIL.Image.fromarray(annotated_frame))

        for i, box in enumerate(results[0].boxes):
            cls = int(box.cls[0].item())
            nome = id_para_nome.get(cls, "desconhecido")
            score = float(box.conf[0]) * 100

            # Ignora detecção com baixa confiança (< 50%)
            if score < 50.0:
                continue

            contagem[nome] += 1
            mensagem = f"⚠️ Frame {frame_count}: {nome} detectado com {score:.1f}% de confiança"

            # Gera nome único para o frame salvo
            frame_filename = os.path.join(pasta_frames_salvos, f"{nome}_frame{frame_count}_box{i}.jpg")
            cv2.imwrite(frame_filename, annotated_frame)
            ultimo_frame_salvo = frame_filename

            # Envia alerta com a imagem salva
            enviar_alerta(mensagem, via=CANAL_ENVIO, imagem_path=frame_filename)

        frame_count += 1

    cap.release()
    out.release()
    print(f"✅ Vídeo gerado em: {output_path}")

    return contagem

def mostrar_resumo(contagem):
    global ultimo_frame_salvo

    print("\n📊 RESUMO DAS DETECÇÕES:")
    for classe, total in contagem.items():
        print(f"🗂️ {classe.capitalize()}: {total} detecções")

    resumo = "\n".join([f"• {classe}: {total}" for classe, total in contagem.items()])
    mensagem_final = f"📊 Resumo VisionGuard:\n{resumo}"

    if ultimo_frame_salvo:
        enviar_alerta(mensagem_final, via=CANAL_ENVIO, imagem_path=ultimo_frame_salvo)
    else:
        enviar_alerta(mensagem_final, via=CANAL_ENVIO)

# Execução principal
if __name__ == "__main__":
    contagem_final = processar_video(video_path)
    mostrar_resumo(contagem_final)
