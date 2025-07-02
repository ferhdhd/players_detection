Claro, aqui está uma documentação detalhada e didática do seu projeto de detecção de jogadores, escrita em Markdown.

# Documentação do Projeto: Detecção de Jogadores em Vídeos de Futebol

## Visão Geral do Projeto

Este projeto tem como objetivo detectar e rastrear jogadores, árbitros e a bola em um vídeo de uma partida de futebol. Ele utiliza o modelo de detecção de objetos YOLOv8 para identificar os elementos em cada frame do vídeo e o `ByteTrack` para rastrear esses objetos ao longo do tempo. O resultado final é um novo vídeo com anotações visuais, como elipses em volta dos jogadores e árbitros e um triângulo sobre a bola, facilitando a visualização e análise do jogo.

## Estrutura do Projeto

O projeto é composto pelos seguintes arquivos:

  - `main.py`: O script principal que orquestra todo o processo.
  - `tracker.py`: Contém a classe `Tracker`, responsável pela detecção e rastreamento dos objetos.
  - `video.py`: Funções para ler e salvar vídeos.
  - `bbox.py`: Funções auxiliares para manipulação de caixas delimitadoras (bounding boxes).
  - `.gitignore`: Arquivo para especificar o que o Git deve ignorar.
  - **Pastas**:
      - `videos/`: Onde os vídeos de entrada devem ser colocados.
      - `videos_saida/`: Onde os vídeos processados são salvos.
      - `models/`: Contém os modelos de detecção de objetos (ex: `best-yolo8.pt`).
      - `stub/`: Usado para salvar e carregar os "tracks" dos objetos, acelerando execuções futuras.

## Componentes Principais

### `main.py`

É o ponto de entrada do programa. O fluxo de execução é o seguinte:

1.  **Leitura do Vídeo**: Carrega os frames do vídeo de entrada (`videos/teste2.mp4`) utilizando a função `read_video`.
2.  **Inicialização do Rastreador**: Cria uma instância da classe `Tracker`, passando o caminho do modelo YOLO treinado (`models/best-yolo8.pt`).
3.  **Obtenção dos Rastreamentos**: Chama o método `get_object_tracks` para detectar e rastrear os objetos no vídeo. Os resultados podem ser salvos e lidos de um arquivo `stub` para evitar o reprocessamento.
4.  **Desenho das Anotações**: Utiliza o método `draw_annotations` para desenhar as elipses e triângulos nos frames do vídeo.
5.  **Salvamento do Vídeo**: Salva os frames com as anotações em um novo arquivo de vídeo (`videos_saida/output.avi`).

### `tracker.py`

Esta é a classe central do projeto.

#### `Tracker(model_path)`

  - **`__init__(self, model_path)`**: O construtor inicializa o modelo YOLO a partir do caminho fornecido e o rastreador `sv.ByteTrack`.

#### Métodos Principais

  - **`detect_frames(self, frames)`**: Recebe uma lista de frames e realiza a detecção de objetos em lotes (`batch`) para otimizar o desempenho. Utiliza o modelo YOLO para prever a posição dos objetos em cada frame.

  - **`get_object_tracks(self, frames, read_from_stub=False, stub_path=None)`**: Este é o método principal para obter os rastreamentos.

      - Ele primeiro verifica se deve ler os rastreamentos de um arquivo `stub` para economizar tempo.
      - Caso contrário, ele chama `detect_frames` para obter as detecções.
      - Processa as detecções, frame a frame, para associar um ID de rastreamento a cada objeto detectado (jogadores, árbitros).
      - Uma atenção especial é dada aos "goalkeepers" (goleiros), que são reclassificados como "player" para simplificar o rastreamento.
      - Armazena as informações de rastreamento (bounding box) em um dicionário estruturado por tipo de objeto (`players`, `referees`, `ball`) e por frame.
      - Se um `stub_path` for fornecido, ele salva os rastreamentos em um arquivo para uso futuro.

  - **`draw_ellipse(self, frame, bbox, color, track_id=None)`**: Desenha uma elipse na parte inferior da caixa delimitadora (`bbox`) de um objeto para representá-lo. Também pode desenhar um retângulo com o ID de rastreamento (`track_id`) do objeto.

  - **`draw_triangle(self, frame, bbox, color)`**: Desenha um triângulo acima da caixa delimitadora da bola para destacá-la.

  - **`draw_annotations(self, video_frames, tracks)`**: Itera sobre cada frame do vídeo e sobre os dicionários de rastreamento para desenhar as anotações.

      - Desenha elipses vermelhas para jogadores.
      - Desenha elipses amarelas para árbitros.
      - Desenha um triângulo verde para a bola.
      - Retorna uma nova lista de frames com as anotações.

### `video.py`

Este módulo contém funções para manipulação de vídeo usando a biblioteca `OpenCV`.

  - **`read_video(path)`**: Abre um arquivo de vídeo, lê todos os frames um por um e os retorna como uma lista.
  - **`save_video(output_frames, output_path)`**: Recebe uma lista de frames e um caminho de saída, e cria um novo arquivo de vídeo `.avi` com esses frames.

### `bbox.py`

Fornece funções de utilidade para trabalhar com caixas delimitadoras (`bounding boxes`).

  - **`get_center_of_bbox(bbox)`**: Calcula e retorna a coordenada central `(x, y)` de uma caixa delimitadora.
  - **`get_bbox_width(bbox)`**: Calcula e retorna a largura de uma caixa delimitadora.

## Como Executar o Projeto

1.  **Instale as dependências**:
    ```bash
    pip install ultralytics supervision opencv-python numpy
    ```
2.  **Estrutura de Pastas**: Certifique-se de que as pastas `videos`, `videos_saida`, `models`, e `stub` existem no diretório raiz do projeto.
3.  **Posicione os Arquivos**:
      - Coloque o vídeo que deseja processar na pasta `videos/`.
      - Coloque o arquivo do modelo treinado (`.pt`) na pasta `models/`.
4.  **Ajuste os Caminhos**: Em `main.py`, certifique-se de que os caminhos para o vídeo de entrada e para o modelo estão corretos.
    ```python
    # main.py
    video_frames = read_video('videos/seu_video.mp4')
    tracker = Tracker("models/seu_modelo.pt")
    ```
5.  **Execute o Script**:
    ```bash
    python main.py
    ```
6.  **Verifique a Saída**: O vídeo processado com as anotações será salvo na pasta `videos_saida/`.

## Dependências

  - **ultralytics**: Para carregar e usar o modelo YOLO.
  - **supervision**: Para o rastreamento de objetos (`ByteTrack`).
  - **opencv-python (`cv2`)**: Para manipulação de vídeo e desenho de formas.
  - **numpy**: Para cálculos numéricos e manipulação de arrays.
  - **pickle**: Para salvar e carregar os dados de rastreamento (`stubs`).
