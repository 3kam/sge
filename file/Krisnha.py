import cv2
import numpy as np
import random

# IMPORTS & CONSTANTS
RESIZE_SCALE = 1.0
MAX_SIDE = 1000
GAUSSIAN_SIGMA = 1.0
BILATERAL_SIGMA = 15.0

FRAME_BLOCK_SIZE = 10
CRT_FRAME = "krishna"
NUM_FADE_OUT = 12
RANDOM_SEED = 42

FADE_OUT_PROG = "linear"
EDGE_THICKNESS = 1
GLOW_THICKNESS = 3
REFLECTION_HEIGHT_RATIO = 0.25

DISPLAY_BRIGHTNESS = 24
DISPLAY_CONTRAST = 1.2
FULL_SCREEN = True


def load_and_preprocess_img(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")

    h, w = img.shape[:2]
    scale = min(1.0, MAX_SIDE / max(h, w))
    new_w = int(w * scale)
    new_h = int(h * scale)
    img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    canvas = np.zeros((MAX_SIDE, MAX_SIDE, 3), dtype=np.uint8)
    x_off = (MAX_SIDE - new_w) // 2
    y_off = (MAX_SIDE - new_h) // 2
    canvas[y_off:y_off + new_h, x_off:x_off + new_w] = img
    return canvas


def make_base_edge_layers(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    edges = cv2.Canny(gray, 100, 200)

    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=EDGE_THICKNESS)

    # ENHANCE EDGE INTENSITY
    edges = cv2.add(edges, edges)

    # BASE COLOR LAYER
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue = hsv[:, :, 0].astype(np.float32)
    base1 = cv2.applyColorMap((hue * (255.0 / 180.0)).astype(np.uint8), cv2.COLORMAP_JET)
    base2 = cv2.applyColorMap(edges, cv2.COLORMAP_JET)
    color_layer = cv2.add(base1, base2)

    inner_glow = cv2.GaussianBlur(color_layer, (0, 0), sigmaX=3, sigmaY=3)
    outer_glow = cv2.GaussianBlur(color_layer, (0, 0), sigmaX=9, sigmaY=9)

    glow = cv2.addWeighted(color_layer, 1.0, inner_glow, 0.4, 0)
    glow = cv2.addWeighted(glow, 1.0, outer_glow, 0.4, 0)

    # AUTO_CONTRAST
    val_pixels = color_layer[edges > 0]
    if len(val_pixels) > 0:
        p98 = np.percentile(val_pixels, 98)
        if p98 > 0:
            combined = cv2.convertScaleAbs(glow, alpha=255.0 / p98, beta=0)
        else:
            combined = glow
    else:
        combined = glow

    return combined.astype(np.uint8)


def block_rendering(img, block_size):
    h, w = img.shape[:2]
    gh = (h + block_size - 1) // block_size
    gw = (w + block_size - 1) // block_size
    pts = []
    for gh_i in range(gh):
        for gw_i in range(gw):
            pts.append((gh_i, gw_i))

    intensity = np.mean(img, axis=2)
    blocks_info = []
    for gh_i, gw_i in pts:
        y1 = gh_i * block_size
        x1 = gw_i * block_size
        block = intensity[y1:y1 + block_size, x1:x1 + block_size]
        blocks_info.append((np.mean(block), gh_i, gw_i))

    blocks_info.sort(key=lambda x: x[0], reverse=True)
    return blocks_info


def get_block_grid_reveal_img(img, block_size):
    h, w = img.shape[:2]
    blocks_info = block_rendering(img, block_size)
    out = np.zeros_like(img)
    for val, gh_i, gw_i in blocks_info:
        y1 = gh_i * block_size
        y2 = min(h, y1 + block_size)
        x1 = gw_i * block_size
        x2 = min(w, x1 + block_size)
        out[y1:y2, x1:x2] = img[y1:y2, x1:x2]
    return out


def draw_disks(canvas, blocks):
    for val, gh_i, gw_i in blocks:
        y = gh_i * FRAME_BLOCK_SIZE + FRAME_BLOCK_SIZE // 2
        x = gw_i * FRAME_BLOCK_SIZE + FRAME_BLOCK_SIZE // 2
        radius = int((val / 255.0) * (FRAME_BLOCK_SIZE / 2))
        if radius > 0:
            cv2.circle(canvas, (x, y), radius, (255, 255, 255), -1, lineType=cv2.LINE_AA)
    return canvas


def add_reflection(frame, ratio):
    h, w = frame.shape[:2]
    refl_h = int(h * ratio)
    refl = cv2.flip(frame[-refl_h:, :], 0)
    refl = cv2.GaussianBlur(refl, (0, 0), sigmaX=15, sigmaY=15)

    out = np.zeros((h + refl_h, w, 3), dtype=np.uint8)
    out[:h, :] = frame

    for i in range(refl_h):
        alpha = 0.35 * (1.0 - (i / refl_h))
        out[h + i, :] = cv2.addWeighted(refl[i:i + 1, :], alpha, out[h + i:h + i + 1, :], 0.0, 0)[0]
    return out


def prepare_for_screen(frame):
    display = cv2.convertScaleAbs(frame, alpha=DISPLAY_CONTRAST, beta=DISPLAY_BRIGHTNESS)
    return display


def show_frame(frame, delay=1):
    display_frame = prepare_for_screen(frame)
    cv2.imshow(CRT_FRAME, display_frame)
    key = cv2.waitKey(delay) & 0xFF
    return key == ord('q') or key == 27


def crossfade(frame_a, frame_b, t):
    return cv2.addWeighted(frame_a, 1.0 - t, frame_b, t, 0)


def main():
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    base = load_and_preprocess_img("krishna.png")
    h, w = base.shape[:2]

    canny_img = make_base_edge_layers(base)
    refl_frame = add_reflection(canny_img, REFLECTION_HEIGHT_RATIO)

    cv2.namedWindow(CRT_FRAME, cv2.WINDOW_NORMAL)
    if FULL_SCREEN:
        cv2.setWindowProperty(CRT_FRAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    full_blocks = block_rendering(canny_img, FRAME_BLOCK_SIZE)
    delay = int(1000 / 30)

    # 1. DISK REVEAL
    disk_frames = int(1.5 * 30)
    fps_disk = int(len(full_blocks) / disk_frames) + 1
    blocks_per_frame = max(1, fps_disk)

    for i in range(disk_frames):
        target = min(len(full_blocks), (i + 1) * blocks_per_frame)
        sub_blocks = full_blocks[:target]
        canvas = np.zeros_like(canny_img)
        frame = draw_disks(canvas, sub_blocks)

        frame = add_reflection(frame, REFLECTION_HEIGHT_RATIO)
        if show_frame(frame, delay):
            return

    # 2. BLOCK GRID REVEAL
    reveal_frames = int(2.0 * 30)
    grid_step = max(1, int(len(full_blocks) / reveal_frames))
    for i in range(reveal_frames):
        count = min(len(full_blocks), (i + 1) * grid_step)
        sub = full_blocks[:count]
        canvas = np.zeros_like(canny_img)
        for _, gh_i, gw_i in sub:
            y1 = gh_i * FRAME_BLOCK_SIZE
            y2 = min(h, y1 + FRAME_BLOCK_SIZE)
            x1 = gw_i * FRAME_BLOCK_SIZE
            x2 = min(w, x1 + FRAME_BLOCK_SIZE)
            canvas[y1:y2, x1:x2] = canny_img[y1:y2, x1:x2]
        frame = add_reflection(canvas, REFLECTION_HEIGHT_RATIO)
        if show_frame(frame, delay):
            return

    # 3. HOLD FULL CANNY EDGE IMAGE
    full_frame = add_reflection(canny_img, REFLECTION_HEIGHT_RATIO)
    if show_frame(full_frame, 1000):
        return

    # 4. CROSSFADE TO ORIGINAL IMAGE
    crossfade_frames = int(1.0 * 30)
    for i in range(crossfade_frames):
        t = (i + 1) / crossfade_frames
        frame = crossfade(canny_img, base, t)
        frame = add_reflection(frame, REFLECTION_HEIGHT_RATIO)
        if show_frame(frame, delay):
            return

    # 5. HOLD FINAL
    final_hold_frames = int(2.0 * 30)
    final_frame = add_reflection(base, REFLECTION_HEIGHT_RATIO)
    for _ in range(final_hold_frames):
        if show_frame(final_frame, delay):
            return

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()