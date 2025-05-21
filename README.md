# Avatar IA para Câmera Virtual

Este projeto cria uma câmera virtual com um avatar personalizado que pode ser usado em aplicativos como Microsoft Teams, Zoom, Google Meet e outros.

## Funcionalidades

- Detecta os movimentos e expressões faciais usando MediaPipe
- Mapeia esses movimentos para um avatar simples 2D
- Cria uma câmera virtual que pode ser selecionada em aplicativos de videoconferência

## Requisitos

- Python 3.7 ou superior
- Webcam funcional
- Windows 10/11 (para usar com o OBS Virtual Camera ou outros drivers de câmera virtual)

## Instalação

1. Clone este repositório ou baixe os arquivos

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Para o Windows, você precisa instalar um driver de câmera virtual:
   - Opção 1: Instale o [OBS Studio](https://obsproject.com/) que inclui o OBS Virtual Camera
   - Opção 2: Instale o [Unity Capture](https://github.com/schellingb/UnityCapture)

## Como Usar

1. Certifique-se de que sua webcam está conectada e funcionando

2. Execute o script principal:

```bash
python virtual_avatar.py
```

3. Você verá duas janelas: uma mostrando sua webcam original e outra mostrando o avatar

4. A câmera virtual será criada e estará disponível para seleção nos aplicativos de videoconferência

5. No Microsoft Teams, Zoom ou outro aplicativo similar:
   - Acesse as configurações de vídeo
   - Selecione a câmera virtual (geralmente chamada "OBS Virtual Camera" ou similar)

6. Para sair, pressione 'q' na janela do avatar

## Personalização

Você pode modificar o arquivo `virtual_avatar.py` para personalizar:

- Cores do avatar (variáveis `bg_color`, `face_color`, `eye_color`)
- Tipo de avatar (atualmente apenas "simple" está disponível)
- Índice da webcam (se tiver múltiplas câmeras)

## Resolução de problemas

- Se a webcam não for detectada, verifique se está conectada corretamente e não está sendo usada por outro aplicativo
- Se a câmera virtual não aparecer nos aplicativos, reinicie o computador após instalar o driver de câmera virtual
- Se o rastreamento facial não funcionar corretamente, tente melhorar a iluminação do ambiente

## Limitações atuais

- Apenas avatar 2D simples está disponível nesta versão
- É necessário ter uma webcam física para capturar os movimentos faciais

## Próximos passos

- Adicionar mais opções de avatar
- Implementar animações para o avatar
- Adicionar fundos personalizados
