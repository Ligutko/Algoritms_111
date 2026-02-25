"""
Flowchart — Quick Sort (ітеративний, зі стеком)
ГОСТ 19.701-90 — однакові блоки, чисті стрілки.

Shapes (ОДНАКОВІ для кожного виду):
  Oval  : w=3.6 h=0.72
  Para  : w=5.6 h=0.72
  Rect  : w=5.6 h=0.72
  Diamond: w=5.6 h=1.40
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Canvas ────────────────────────────────────────────────────────────────────
FIG_W, FIG_H = 14, 29
CX = 7.0

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.axis("off")
fig.patch.set_facecolor("#FFFFFF")

# ── Uniform shape sizes ───────────────────────────────────────────────────────
OW, OH  = 3.6, 0.72
PW, PH  = 5.6, 0.72
RW, RH  = 5.6, 0.72
DW, DH  = 5.6, 1.40
DHW = DW / 2       # 2.8
DHH = DH / 2       # 0.70

# ── Palette (identical to main flowchart) ─────────────────────────────────────
C_S  = "#1A237E"; F_S  = "#E8EAF6"
C_IO = "#0D47A1"; F_IO = "#BBDEFB"
C_P  = "#1565C0"; F_P  = "#E3F2FD"
C_D  = "#4A148C"; F_D  = "#EDE7F6"
C_G  = "#1B5E20"; F_G  = "#C8E6C9"
C_AR = "#263238"; C_LB = "#546E7A"
LW, ALW = 1.8, 1.5
FS, FS_D, FONT = 9.0, 8.5, "DejaVu Sans"

# ── Y positions ───────────────────────────────────────────────────────────────
GAP, GAPX = 0.85, 1.20

def ny(yc, hc, hn, g=GAP):
    return yc - hc - g - hn

y1  = 27.0                             # ПОЧАТОК (oval)
y2  = ny(y1,  OH/2, PH/2)             # INPUT   (para)
y3  = ny(y2,  PH/2, RH/2)             # stack ← [(0, n-1)]   (rect)
y4  = ny(y3,  RH/2, DHH)              # stack не порожній?    (diamond) ← OUTER LOOP TOP
y5  = ny(y4,  DHH,  RH/2)             # (low,high) ← stack.pop()
y6  = ny(y5,  RH/2, DHH)              # low < high?           (diamond)
y7  = ny(y6,  DHH,  RH/2)             # pivot; i; j init      (rect)
y8  = ny(y7,  RH/2, DHH)              # j < high?             (diamond) ← INNER LOOP TOP
y9  = ny(y8,  DHH,  DHH)              # arr[j] ≤ pivot?       (diamond)
y10 = ny(y9,  DHH,  RH/2)             # i++; swap(arr[i],arr[j])  (rect, green)
y11 = ny(y10, RH/2, RH/2)             # j ← j + 1            (rect)
y12 = ny(y11, RH/2, RH/2, GAPX)       # swap+partition end    (rect)
y13 = ny(y12, RH/2, RH/2)             # stack.push(...)       (rect)
y14 = ny(y13, RH/2, PH/2, GAPX)       # Виведення: arr        (para)
y15 = ny(y14, PH/2, OH/2)             # КІНЕЦЬ               (oval)

# ── Routing columns ───────────────────────────────────────────────────────────
XBO  = CX - 4.3   # outer loop-back column (y13→y4  AND  d6-Ні→y4)
XBI  = CX - 3.3   # inner loop-back column (y11→y8)
XSKI = CX + 3.2   # skip append: d9-Ні → bypass y10 → y11
XEXI = CX + 3.9   # inner exit: d8-Ні → y12
XEXO = CX + 4.7   # outer exit: d4-Ні → y14

# ── Draw helpers ─────────────────────────────────────────────────────────────

def draw_oval(cy, text, c=C_S, fc=F_S):
    ax.add_patch(mpatches.FancyBboxPatch(
        (CX-OW/2, cy-OH/2), OW, OH, boxstyle="round,pad=0.08",
        lw=LW, edgecolor=c, facecolor=fc, zorder=3))
    ax.text(CX, cy, text, ha="center", va="center",
            fontsize=FS, fontfamily=FONT, fontweight="bold", color=c, zorder=4)

def draw_para(cy, text, c=C_IO, fc=F_IO):
    sk = 0.22
    xs = [CX-PW/2+sk, CX+PW/2+sk, CX+PW/2-sk, CX-PW/2-sk]
    ys = [cy-PH/2,    cy-PH/2,    cy+PH/2,    cy+PH/2]
    ax.add_patch(mpatches.Polygon(list(zip(xs, ys)), closed=True,
                 lw=LW, edgecolor=c, facecolor=fc, zorder=3))
    ax.text(CX, cy, text, ha="center", va="center",
            fontsize=FS, fontfamily=FONT, fontweight="bold", color=c, zorder=4)

def draw_rect(cy, text, c=C_P, fc=F_P, fs=FS):
    ax.add_patch(mpatches.FancyBboxPatch(
        (CX-RW/2, cy-RH/2), RW, RH, boxstyle="square,pad=0",
        lw=LW, edgecolor=c, facecolor=fc, zorder=3))
    ax.text(CX, cy, text, ha="center", va="center",
            fontsize=fs, fontfamily=FONT, color=c, zorder=4)

def draw_diamond(cy, text, c=C_D, fc=F_D):
    xs = [CX, CX+DHW, CX, CX-DHW]
    ys = [cy+DHH, cy, cy-DHH, cy]
    ax.add_patch(mpatches.Polygon(list(zip(xs, ys)), closed=True,
                 lw=LW, edgecolor=c, facecolor=fc, zorder=3))
    ax.text(CX, cy, text, ha="center", va="center",
            fontsize=FS_D, fontfamily=FONT, color=c,
            multialignment="center", zorder=4)

def arr_down(x, y0, y1):
    ax.annotate("", xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle="-|>", color=C_AR,
                                lw=ALW, mutation_scale=13), zorder=2)

def arr_h(x0, x1, y):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="-|>", color=C_LB,
                                lw=ALW, mutation_scale=13), zorder=2)

def poly(xs, ys):
    ax.plot(xs, ys, color=C_LB, lw=ALW, solid_capstyle="round", zorder=2)

def lbl(x, y, text, ha="left"):
    ax.text(x, y, text, ha=ha, va="center", fontsize=8.2,
            fontfamily=FONT, fontweight="bold", color=C_D, zorder=5)

# ── TITLE ─────────────────────────────────────────────────────────────────────
ax.text(CX, 28.6, "Блок-схема алгоритму:  Quick Sort  (ітеративний)",
        ha="center", va="center", fontsize=11.5, fontfamily=FONT,
        fontweight="bold", color="#1A237E", zorder=5)
ax.plot([0.5, FIG_W-0.5], [28.15, 28.15], color="#1A237E", lw=1.0)
ax.text(CX, 27.82,
        "quick_sort(arr)  ·  розбиття Ломуто  ·  Лабораторна робота · Варіант 2",
        ha="center", va="center", fontsize=8.5, color="#546E7A",
        fontfamily=FONT, zorder=5)

# ── BLOCKS ────────────────────────────────────────────────────────────────────
draw_oval    (y1,  "ПОЧАТОК")
draw_para    (y2,  "Введення:  масив arr")
draw_rect    (y3,  "stack  ←  [ ( 0,  len(arr) − 1 ) ]")
draw_diamond (y4,  "stack  не порожній ?")
draw_rect    (y5,  "( low,  high )  ←  stack.pop()")
draw_diamond (y6,  "low  <  high ?")
draw_rect    (y7,  "pivot←arr[high] ;  i←low−1 ;  j←low")
draw_diamond (y8,  "j  <  high ?")
draw_diamond (y9,  "arr[j]  ≤  pivot ?")
draw_rect    (y10, "i  ←  i + 1 ;  swap( arr[i],  arr[j] )", c=C_G, fc=F_G)
draw_rect    (y11, "j  ←  j + 1")
draw_rect    (y12, "swap( arr[i+1], arr[high] ) ;  pi  ←  i + 1")
draw_rect    (y13, "stack.push( low, pi−1 ) ;  stack.push( pi+1, high )")
draw_para    (y14, "Виведення:  arr  (відсортований)")
draw_oval    (y15, "КІНЕЦЬ", c="#B71C1C", fc="#FFEBEE")

# ── MAIN FLOW arrows ──────────────────────────────────────────────────────────
arr_down(CX, y1  - OH/2,  y2  + PH/2)
arr_down(CX, y2  - PH/2,  y3  + RH/2)
arr_down(CX, y3  - RH/2,  y4  + DHH)
arr_down(CX, y4  - DHH,   y5  + RH/2)  ; lbl(CX+0.12, (y4-DHH+y5+RH/2)/2, "Так")
arr_down(CX, y5  - RH/2,  y6  + DHH)
arr_down(CX, y6  - DHH,   y7  + RH/2)  ; lbl(CX+0.12, (y6-DHH+y7+RH/2)/2, "Так")
arr_down(CX, y7  - RH/2,  y8  + DHH)
arr_down(CX, y8  - DHH,   y9  + DHH)   ; lbl(CX+0.12, (y8-DHH+y9+DHH)/2, "Так")
arr_down(CX, y9  - DHH,   y10 + RH/2)  ; lbl(CX+0.12, (y9-DHH+y10+RH/2)/2, "Так")
arr_down(CX, y10 - RH/2,  y11 + RH/2)
arr_down(CX, y12 - RH/2,  y13 + RH/2)
arr_down(CX, y14 - PH/2,  y15 + OH/2)

# ── INNER LOOP-BACK:  j++ → left-inner col → up → top of d-j<high ─────────────
poly([CX-RW/2, XBI, XBI], [y11, y11, y8])
arr_h(XBI, CX-DHW, y8)

# ── INNER EXIT: d-j<high "Ні" → right-inner col → down → swap block ──────────
lbl(CX+DHW+0.1, y8+0.28, "Ні")
poly([CX+DHW, XEXI, XEXI], [y8, y8, y12])
arr_h(XEXI, CX+RW/2, y12)

# ── SKIP APPEND: d-arr[j]<=pivot "Ні" → skip green → j++ ────────────────────
lbl(CX+DHW+0.1, y9+0.28, "Ні")
poly([CX+DHW, XSKI, XSKI], [y9, y9, y11])
arr_h(XSKI, CX+RW/2, y11)

# ── OUTER LOOP-BACK: stack.push → left-outer col → up → d-stack ─────────────
poly([CX-RW/2, XBO, XBO], [y13, y13, y4])
arr_h(XBO, CX-DHW, y4)

# ── d6 "Ні" (low>=high, skip partition) → left-outer col → up → d-stack ─────
lbl(CX-DHW-0.12, y6+0.0, "Ні", ha="right")
poly([CX-DHW, XBO], [y6, y6])
# XBO vertical line already drawn from y13 up to y4; visually it merges

# ── OUTER EXIT: d-stack "Ні" → right-outer col → down → output ──────────────
lbl(CX+DHW+0.1, y4+0.28, "Ні")
poly([CX+DHW, XEXO, XEXO], [y4, y4, y14])
arr_h(XEXO, CX+PW/2, y14)

# ── SECTION DIVIDERS ─────────────────────────────────────────────────────────
for ydiv, cap in [
    ((y3+y4)/2,   "── Зовнішній цикл (while stack) ──"),
    ((y7+y8)/2,   "── Внутрішній цикл Ломуто (while j < high) ──"),
    ((y11+y12)/2, "── Завершення розбиття / продовження зовн. циклу ──"),
]:
    ax.plot([0.4, FIG_W-0.4], [ydiv, ydiv],
            color="#CFD8DC", lw=0.7, linestyle=":", zorder=1)
    ax.text(0.5, ydiv+0.22, cap, ha="left", va="center",
            fontsize=7.0, color="#90A4AE", fontfamily=FONT, style="italic")

# ── LEGEND ───────────────────────────────────────────────────────────────────
LX, LY, LLW, LLH = 0.3, 0.4, 5.6, 5.8
ax.add_patch(mpatches.FancyBboxPatch((LX, LY), LLW, LLH,
    boxstyle="round,pad=0.12", lw=0.8, edgecolor="#B0BEC5",
    facecolor="#FAFAFA", zorder=1))
ax.text(LX+LLW/2, LY+LLH-0.32, "Умовні позначення  (ГОСТ 19.701-90)",
        ha="center", fontsize=8.5, fontweight="bold",
        color="#37474F", fontfamily=FONT)

leg = [
    ("oval",    F_S,  C_S,  "Початок / Кінець"),
    ("para",    F_IO, C_IO, "Введення / Виведення"),
    ("rect",    F_P,  C_P,  "Оператор / Процес"),
    ("diamond", F_D,  C_D,  "Умова / Рішення"),
    ("rect",    F_G,  C_G,  "Обмін елементів (swap)"),
]
for k, (sh, fc, ec, cap) in enumerate(leg):
    ix, iy = LX+0.32, LY+LLH-0.80-k*0.92
    sw, sh2 = 1.1, 0.42
    if sh == "oval":
        ip = mpatches.FancyBboxPatch((ix, iy-sh2/2), sw, sh2,
             boxstyle="round,pad=0.06", lw=1, edgecolor=ec, facecolor=fc)
    elif sh == "para":
        d = 0.09
        ip = mpatches.Polygon(
             [(ix+d, iy-sh2/2),(ix+sw+d, iy-sh2/2),
              (ix+sw-d, iy+sh2/2),(ix-d, iy+sh2/2)],
             closed=True, lw=1, edgecolor=ec, facecolor=fc)
    elif sh == "diamond":
        ip = mpatches.Polygon(
             [(ix+sw/2, iy+sh2/2),(ix+sw, iy),
              (ix+sw/2, iy-sh2/2),(ix, iy)],
             closed=True, lw=1, edgecolor=ec, facecolor=fc)
    else:
        ip = mpatches.FancyBboxPatch((ix, iy-sh2/2), sw, sh2,
             boxstyle="square,pad=0", lw=1, edgecolor=ec, facecolor=fc)
    ax.add_patch(ip)
    ax.text(ix+sw+0.18, iy, cap, va="center", ha="left",
            fontsize=8.0, fontfamily=FONT, color="#263238")

iy_l = LY+0.42
poly([LX+0.32, LX+1.42], [iy_l, iy_l])
arr_h(LX+0.32, LX+1.42, iy_l)
ax.text(LX+1.62, iy_l, "Лінія повернення / виходу з циклу",
        va="center", ha="left", fontsize=8.0, fontfamily=FONT, color="#263238")

ax.text(FIG_W-0.3, 0.18,
        "DSA LAB · Variant 2 · quick_sort() · 2026",
        ha="right", va="bottom", fontsize=6.5,
        color="#90A4AE", fontfamily=FONT, style="italic")

# ── SAVE ─────────────────────────────────────────────────────────────────────
plt.tight_layout(pad=0)
plt.savefig("flowchart_quicksort.svg", format="svg",
            bbox_inches="tight", facecolor="#FFFFFF", dpi=300)
plt.close()
print("OK  flowchart_quicksort.svg збережено")
