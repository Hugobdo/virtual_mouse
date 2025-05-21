from collections import deque
import cv2
import mediapipe as mp
import numpy as np
from pynput.mouse import Button, Controller

# ---------------- PARAMS ----------------------------------------------------
ALPHA              = 0.2
CONFIRM_FRAMES     = 2
THRESH_SCALE       = 0.7
THRESH_HYST        = 0.15
ACTIVE_RANGE       = 0.35
DEADZONE_REL       = 0.05
CALIB_FRAMES       = 30
OPEN_PALM_FRAMES   = 15
MOVEMENT_THRESHOLD = 2
Z_CLICK_THRESHOLD  = 0.03
# ---------------------------------------------------------------------------

mouse = Controller()
SCREEN_W, SCREEN_H = 1920, 1080

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

THUMB_TIP, INDEX_TIP, MIDDLE_TIP = 4, 8, 12
IDX_MCP, PINKY_MCP = 5, 17


class MaoBase:
    def __init__(self):
        self.calibrating = True
        self.calibrated = False
        self.calib_samples = []
        self.open_palm_counter = 0
        self.ix_hist = deque(maxlen=OPEN_PALM_FRAMES)
        self.iy_hist = deque(maxlen=OPEN_PALM_FRAMES)

    def calibrar(self, ix, iy):
        self.calib_samples.append((ix, iy))
        if len(self.calib_samples) >= CALIB_FRAMES:
            self.neutral_x = np.median([p[0] for p in self.calib_samples])
            self.neutral_y = np.median([p[1] for p in self.calib_samples])
            self.calibrating = False
            self.calibrated = True
            print("[INFO] Calibração concluída para mão.")


class MaoDireita(MaoBase):
    def __init__(self):
        super().__init__()
        self.prev_cx, self.prev_cy = SCREEN_W // 2, SCREEN_H // 2
        mouse.position = (self.prev_cx, self.prev_cy)

    def mover_cursor(self, ix, iy):
        rel_dx = (ix - self.neutral_x) / ACTIVE_RANGE
        rel_dy = (iy - self.neutral_y) / ACTIVE_RANGE

        if abs(rel_dx) < DEADZONE_REL and abs(rel_dy) < DEADZONE_REL:
            cx, cy = self.prev_cx, self.prev_cy
        else:
            rel_x = np.clip(rel_dx + 0.5, 0.0, 1.0)
            rel_y = np.clip(rel_dy + 0.5, 0.0, 1.0)
            tx, ty = rel_x * SCREEN_W, rel_y * SCREEN_H

            cx = int(self.prev_cx * (1 - ALPHA) + tx * ALPHA)
            cy = int(self.prev_cy * (1 - ALPHA) + ty * ALPHA)

            if abs(cx - self.prev_cx) < MOVEMENT_THRESHOLD:
                cx = self.prev_cx
            if abs(cy - self.prev_cy) < MOVEMENT_THRESHOLD:
                cy = self.prev_cy

        mouse.position = (cx, cy)
        self.prev_cx, self.prev_cy = cx, cy


class MaoEsquerda(MaoBase):
    def __init__(self):
        super().__init__()
        self.l_frames = 0
        self.r_frames = 0
        self.left_pressed = False
        self.right_pressed = False

    def processar_cliques(self, lm, th_close, th_open):
        d_idx = np.hypot(lm[THUMB_TIP].x - lm[INDEX_TIP].x, lm[THUMB_TIP].y - lm[INDEX_TIP].y)
        d_mid = np.hypot(lm[THUMB_TIP].x - lm[MIDDLE_TIP].x, lm[THUMB_TIP].y - lm[MIDDLE_TIP].y)

        # Clique esquerdo: pinch polegar + indicador
        if d_idx < th_close and d_mid > th_open:
            self.l_frames += 1
        else:
            if self.left_pressed:
                mouse.release(Button.left)
                self.left_pressed = False
            self.l_frames = 0

        if not self.left_pressed and self.l_frames >= CONFIRM_FRAMES:
            mouse.press(Button.left)
            self.left_pressed = True

        # Clique direito: pinch polegar + médio
        if d_mid < th_close and d_idx > th_open:
            self.r_frames += 1
        else:
            if self.right_pressed:
                mouse.release(Button.right)
                self.right_pressed = False
            self.r_frames = 0

        if not self.right_pressed and self.r_frames >= CONFIRM_FRAMES:
            mouse.press(Button.right)
            self.right_pressed = True


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)
print(f"[INFO] Webcam em {int(cap.get(3))}x{int(cap.get(4))}")

maos = {"Left": MaoEsquerda(), "Right": MaoDireita()}

print("[INFO] Mantenha a mão aberta e parada para calibrar automaticamente.")
print("       ESC ou q para sair.")

while True:
    ok, frame = cap.read()
    if not ok:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    if res.multi_hand_landmarks and res.multi_handedness:
        for landmarks, handed in zip(res.multi_hand_landmarks, res.multi_handedness):
            label = handed.classification[0].label
            mao = maos[label]

            lm = landmarks.landmark
            ix, iy = lm[INDEX_TIP].x, lm[INDEX_TIP].y

            palm_w = np.hypot(lm[IDX_MCP].x - lm[PINKY_MCP].x, lm[IDX_MCP].y - lm[PINKY_MCP].y)
            th_close = palm_w * THRESH_SCALE
            th_open = th_close + palm_w * THRESH_HYST

            d_idx = np.hypot(lm[THUMB_TIP].x - lm[INDEX_TIP].x, lm[THUMB_TIP].y - lm[INDEX_TIP].y)
            d_mid = np.hypot(lm[THUMB_TIP].x - lm[MIDDLE_TIP].x, lm[THUMB_TIP].y - lm[MIDDLE_TIP].y)

            palm_open = d_idx > th_open and d_mid > th_open

            mao.ix_hist.append(ix)
            mao.iy_hist.append(iy)

            if palm_open:
                var_x = max(mao.ix_hist) - min(mao.ix_hist)
                var_y = max(mao.iy_hist) - min(mao.iy_hist)
                if var_x < 0.005 and var_y < 0.005:
                    mao.open_palm_counter += 1
                else:
                    mao.open_palm_counter = 0
            else:
                mao.open_palm_counter = 0

            if mao.open_palm_counter >= OPEN_PALM_FRAMES and not mao.calibrating and not mao.calibrated:
                mao.calibrating = True
                mao.calib_samples.clear()
                mao.open_palm_counter = 0
                print(f"[INFO] Palma aberta detectada. Iniciando calibração para mão {label}...")

            if mao.calibrating:
                mao.calibrar(ix, iy)
                continue

            if label == "Right":
                mao.mover_cursor(ix, iy)
            elif label == "Left":
                mao.processar_cliques(lm, th_close, th_open)

    if cv2.waitKey(1) & 0xFF in [27, ord('q')]:
        break

cap.release()
cv2.destroyAllWindows()
