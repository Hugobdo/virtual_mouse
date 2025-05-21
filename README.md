# Virtual Mouse

## Descrição
Virtual Mouse é um aplicativo de controle gestual que permite manipular o cursor do mouse usando movimentos das mãos capturados pela webcam. Utilizando visão computacional e reconhecimento de gestos, o sistema permite mover o cursor e realizar cliques sem tocar em dispositivos físicos.

## Funcionalidades
- **Mão Direita**: Controla o movimento do cursor
- **Mão Esquerda**: Realiza cliques do mouse
  - Pinça entre polegar e indicador: clique esquerdo
  - Pinça entre polegar e dedo médio: clique direito
- **Calibração Automática**: Mantenha a mão aberta e parada para calibrar

## Requisitos
- Python 3.6 ou superior
- Webcam funcional
- Iluminação adequada para detecção das mãos

## Instalação
1. Clone o repositório ou baixe os arquivos
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Como Usar
1. Execute o programa:
   ```
   python virtual_mouse.py
   ```
2. Posicione-se em frente à webcam
3. Siga as instruções na tela para calibração:
   - Mantenha a mão aberta e parada para calibrar automaticamente
4. Controle o mouse:
   - Use a mão direita para mover o cursor
   - Use a mão esquerda para fazer cliques
5. Para sair, pressione ESC ou a tecla 'q'

## Parâmetros Configuráveis
O código contém diversos parâmetros que podem ser ajustados para melhorar a experiência conforme sua necessidade:
- `ALPHA`: Suavização do movimento (0.2 padrão)
- `CONFIRM_FRAMES`: Frames necessários para confirmar um clique (2 padrão)
- `ACTIVE_RANGE`: Sensibilidade do movimento (0.35 padrão)
- `DEADZONE_REL`: Zona morta para pequenos movimentos (0.05 padrão)

## Dicas de Uso
- Mantenha-se em um ambiente bem iluminado
- Evite movimentos bruscos durante a calibração
- Experimente ajustar os parâmetros se a detecção não estiver ideal para seu ambiente

## Tecnologias Utilizadas
- OpenCV: Processamento de imagem e vídeo
- MediaPipe: Reconhecimento e rastreamento de mãos
- NumPy: Processamento numérico
- Pynput: Controle programático do mouse
