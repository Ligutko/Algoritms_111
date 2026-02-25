"""
Flowchart — Interpolation Search (інтерполяційний пошук)
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
FIG_W, FIG_H = 14, 24
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
DHW = DW / 2    # 2.8
DHH = DH / 2    # 0.70

# ── Palette ───────────────────────────────────────────────────────────────────
C_S  = "#1A237E"; F_S  = "#E8EAF6"
C_IO = "#0D47A1"; F_IO = "#BBDEFB"
C_P  = "#1565C0"; F_P  = "#E3F2FD"
C_D  = "#4A148C"; F_D  = "#EDE7F6"
C_G  = "#1B5E20"; F_G  = "#C8E6C9"
C_R  = "#B71C1C"; F_R  = "#FFEBEE"
C_AR = "#263238"; C_LB = "#546E7A"
LW, ALW = 1.8, 1.5
FS, FS_D, FONT = 9.0, 8.5, "DejaVu Sans"

# ── Y positions ───────────────────────────────────────────────────────────────
GAP, GAPX = 0.85, 1.20

def ny(yc, hc, hn, g=GAP):
    return yc - hc - g - hn

y1  = 22.0                              # ПОЧАТОК          oval
y2  = ny(y1,  OH/2, PH/2)              # INPUT            para    20.43
y3  = ny(y2,  PH/2, RH/2)              # init low, high   rect    18.86
y4  = ny(y3,  RH/2, DHH)               # LOOP diamond            16.95
y5  = ny(y4,  DHH,  RH/2)              # mid formula      rect    15.04
y6  = ny(y5,  RH/2, DHH)               # arr[mid]=key?    diamond 13.13
y7  = ny(y6,  DHH,  DHH)               # arr[mid]<key?    diamond 10.88
y8a = ny(y7,  DHH,  RH/2)              # low  ← mid+1     rect     9.07  (Так from y7)
y8b = ny(y8a, RH/2, RH/2)              # high ← mid−1     rect     7.50  (Ні  from y7)
y9  = ny(y8b, RH/2, PH/2, GAPX)        # OUTPUT           para     5.58
y10 = ny(y9,  PH/2, OH/2)              # КІНЕЦЬ           oval     4.01

# ── Routing columns ───────────────────────────────────────────────────────────
XBO    = CX - 4.3   # loop-back: y8a,y8b → d4 left tip
X_SKIP = CX + 3.2   # d7 Ні → bypass y8a → y8b right edge
X_FIND = CX + 3.9   # d6 Так (found) → down to y9 right edge
X_EXIT = CX + 4.6   # d4 Ні (not found) → down to y9 right edge

# ── Draw helpers (identical to other charts) ──────────────────────────────────

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
ax.text(CX, 23.6, "Блок-схема алгоритму:  Інтерполяційний пошук",
        ha="center", va="center", fontsize=11.5, fontfamily=FONT,
        fontweight="bold", color="#1A237E", zorder=5)
ax.plot([0.5, FIG_W-0.5], [23.15, 23.15], color="#1A237E", lw=1.0)
ax.text(CX, 22.82,
        "interpolation_search(arr, key)  ·  відсортований масив  ·  Лабораторна робота · Варіант 2",
        ha="center", va="center", fontsize=8.5, color="#546E7A",
        fontfamily=FONT, zorder=5)

# ── BLOCKS ────────────────────────────────────────────────────────────────────
draw_oval    (y1, "ПОЧАТОК")
draw_para    (y2, "Введення:  arr (відсортований),  key")
draw_rect    (y3, "low  ←  0 ;   high  ←  len(arr)  −  1")
draw_diamond (y4, "low ≤ high  ТА  arr[low] ≤ key ≤ arr[high] ?")
draw_rect    (y5, "mid  ←  low  +  (key − arr[low]) × (high − low)\n"
                  "              /  (arr[high] − arr[low])", fs=8.2)
draw_diamond (y6, "arr[ mid ]  =  key ?")
draw_diamond (y7, "arr[ mid ]  <  key ?")
draw_rect    (y8a, "low   ←  mid  +  1",  c=C_G, fc=F_G)
draw_rect    (y8b, "high  ←  mid  −  1",  c=C_R, fc=F_R)
draw_para    (y9,  "Виведення:  результат  ( pos = mid  або  −1 )")
draw_oval    (y10, "КІНЕЦЬ", c="#B71C1C", fc="#FFEBEE")

# ── MAIN FLOW arrows ──────────────────────────────────────────────────────────
arr_down(CX, y1  - OH/2,  y2  + PH/2)
arr_down(CX, y2  - PH/2,  y3  + RH/2)
arr_down(CX, y3  - RH/2,  y4  + DHH)
# d4 Так → y5
arr_down(CX, y4  - DHH,   y5  + RH/2)  ; lbl(CX+0.12, (y4-DHH+y5+RH/2)/2, "Так")
# y5 → d6
arr_down(CX, y5  - RH/2,  y6  + DHH)
# d6 Ні → d7
arr_down(CX, y6  - DHH,   y7  + DHH)   ; lbl(CX+0.12, (y6-DHH+y7+DHH)/2, "Ні")
# d7 Так → y8a
arr_down(CX, y7  - DHH,   y8a + RH/2)  ; lbl(CX+0.12, (y7-DHH+y8a+RH/2)/2, "Так")
# y9 → y10
arr_down(CX, y9  - PH/2,  y10 + OH/2)

# ── LOOP-BACK A: y8a (low←mid+1) → left col → up → d4 left tip ──────────────
poly([CX-RW/2, XBO, XBO], [y8a, y8a, y4])
arr_h(XBO, CX-DHW, y4)

# ── LOOP-BACK B: y8b (high←mid−1) → left col → up → d4 left tip ─────────────
poly([CX-RW/2, XBO], [y8b, y8b])
# XBO vertical already drawn; add segment from y8b (lower) up to y8a (covered by above)
# Need explicit y8b to y4 on XBO column (shares column with y8a path)
ax.plot([XBO, XBO], [y8b, y8a-RH/2-GAP/2],   # merge into the existing XBO vertical
        color=C_LB, lw=ALW, solid_capstyle="round", zorder=2)

# ── SKIP: d7 Ні (arr[mid]>key) → right skip col → y8b right edge ─────────────
lbl(CX+DHW+0.1, y7+0.28, "Ні")
poly([CX+DHW, X_SKIP, X_SKIP], [y7, y7, y8b])
arr_h(X_SKIP, CX+RW/2, y8b)

# ── FOUND EXIT: d6 Так → right found col → y9 right edge ─────────────────────
lbl(CX+DHW+0.1, y6+0.28, "Так")
poly([CX+DHW, X_FIND, X_FIND], [y6, y6, y9])
arr_h(X_FIND, CX+PW/2, y9)

# ── NOT-FOUND EXIT: d4 Ні → right exit col → y9 right edge ───────────────────
lbl(CX+DHW+0.1, y4+0.28, "Ні")
poly([CX+DHW, X_EXIT, X_EXIT], [y4, y4, y9])
arr_h(X_EXIT, CX+PW/2, y9)

# ── FORMULA annotation ────────────────────────────────────────────────────────
ax.text(CX, y5, "",  zorder=6)  # placeholder (text already in block)

# ── SECTION DIVIDERS ─────────────────────────────────────────────────────────
for ydiv, cap in [
    ((y3+y4)/2,    "── Цикл інтерполяційного пошуку ──"),
    ((y8b+y9)/2,   "── Завершення: виведення результату ──"),
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
    ("rect",    F_G,  C_G,  "low  ←  mid + 1  (елемент лівіше)"),
    ("rect",    F_R,  C_R,  "high ←  mid − 1  (елемент правіше)"),
]
for k, (sh, fc, ec, cap) in enumerate(leg):
    ix, iy = LX+0.32, LY+LLH-0.78-k*0.80
    sw, sh2 = 1.1, 0.38
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
            fontsize=7.8, fontfamily=FONT, color="#263238")

iy_l = LY+0.38
poly([LX+0.32, LX+1.42], [iy_l, iy_l])
arr_h(LX+0.32, LX+1.42, iy_l)
ax.text(LX+1.62, iy_l, "Лінія повернення / виходу з циклу",
        va="center", ha="left", fontsize=7.8, fontfamily=FONT, color="#263238")

ax.text(FIG_W-0.3, 0.18,
        "DSA LAB · Variant 2 · interpolation_search() · 2026",
        ha="right", va="bottom", fontsize=6.5,
        color="#90A4AE", fontfamily=FONT, style="italic")

# ── SAVE ─────────────────────────────────────────────────────────────────────
plt.tight_layout(pad=0)
plt.savefig("flowchart_interpolation.svg", format="svg",
            bbox_inches="tight", facecolor="#FFFFFF", dpi=300)
plt.close()
print("OK  flowchart_interpolation.svg збережено")
