# 🔍 Projeto FIAP - Desafio 05 - Desenvolvimento de Aplicativo de Objetos Cortantes: Detecção Automatizada de Objetos Cortantes em Vídeos

Este projeto tem como objetivo identificar automaticamente objetos cortantes (como facas e tesouras) em vídeos, com o intuito de alertar operadores humanos e registrar as ocorrências. A aplicação combina **visão computacional** com **automação de alertas**, sendo ideal para ambientes sensíveis.

---

## 📦 Funcionalidades

- 📹 Processamento de vídeos com o modelo **YOLOv8**
- 🧠 Detecção de objetos cortantes
- 🖼️ Salvamento automático de frames com alta confiança
- ⚠️ Envio de alertas com imagens por canal definido
- 📊 Geração de resumo das detecções

---

## 🧰 Ferramentas e Tecnologias

- [Ultralytics YOLOv8](https://docs.ultralytics.com) – Detecção de objetos em tempo real
- [Roboflow](https://app.roboflow.com/fiap-cxe1i/desafio-fase-05/1) – Criação e anotação do dataset
- Python + OpenCV – Manipulação de vídeo e imagens
- PIL (Pillow) – Conversão de imagens para visualização
- `cv2`, `ultralytics`, `IPython.display` – Processamento

---

## 📂 Estrutura do Projeto

```bash
├── modelos/                        # Modelo YOLOv8 treinado (.pt)
├── videos/                         # Vídeo de entrada
├── config.env                      # Arquivo de configurações
├── frames_detectados/              # Frames salvos com alta confiança (alta de 50%)
├── desafio05_00_config.py          # Configurações do canal de envio
├── desafio05_01_treinamento.py     # Arquivo de treinamento do modelo
├── desafio05_02_alertas.py         # Configurações de alertas
├── desafio05_03_detectar_video.py  # Execução do processamento
└── README.md                       # Este documento
