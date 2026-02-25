"""
Flowchart for find_unique_elements (Symmetric Difference A △ B)
ДСТУ / ГОСТ 19.701-90 — uniform shapes, clean connected arrows.

ALL rectangles     : w=5.6, h=0.72
ALL diamonds       : w=5.6, h=1.40
ALL ovals          : w=3.6, h=0.72
ALL parallelograms : w=5.6, h=0.72
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ─── Canvas ───────────────────────────────────────────────────────────────────
FIG_W, FIG_H = 14, 40
CX = 7.0

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.axis("off")
fig.patch.set_facecolor("#FFFFFF")

# ─── UNIFORM shape dimensions ─────────────────────────────────────────────────
OW,  OH  = 3.6,  0.72    # Oval  (start / end)
PW,  PH  = 5.6,  0.72    # Parallelogram  (I/O)
RW,  RH  = 5.6,  0.72    # Rectangle  (process)
DW,  DH  = 5.6,  1.40    # Diamond  (decision)
DHW = DW / 2              # 2.8  — half-width
DHH = DH / 2              # 0.70 — half-height

# ─── Colours ──────────────────────────────────────────────────────────────────
C_S  = "#1A237E"          # start/end border
C_IO = "#0D47A1"          # I/O border
C_P  = "#1565C0"          # process border
C_D  = "#4A148C"          # decision border
C_G  = "#1B5E20"          # green (append)
C_AR = "#263238"          # arrow / line
C_LB = "#546E7A"          # loop-back line

F_S  = "#E8EAF6"
F_IO = "#BBDEFB"
F_P  = "#E3F2FD"
F_D  = "#EDE7F6"
F_G  = "#C8E6C9"

LW   = 1.8                # shape line-width
ALW  = 1.5                # arrow line-width
FS   = 9.0                # label font-size
FS_D = 8.5                # font-size inside diamonds (two-line)
FONT = "DejaVu Sans"

# ─── Y positions (block centres, decreasing top to bottom) ────────────────────
GAP  = 0.85               # gap between consecutive blocks
GAPX = 1.20               # wider gap at section breaks

def ny(yc, hc, hn, g=GAP):
    """Centre of next block below."""
    return yc - hc - g - hn

y1  = 38.3                              # START  (oval)
y2  = ny(y1,  OH/2,  PH/2)             # INPUT  (para)
y3  = ny(y2,  PH/2,  RH/2)             # sorted_B  (rect)
y4  = ny(y3,  RH/2,  RH/2)             # i=0  (rect)
y5  = ny(y4,  RH/2,  DHH)              # i < len(A)?  (diamond)
y6  = ny(y5,  DHH,   DHH)              # search(sorted_B, A[i])==-1?  (diamond)
y7  = ny(y6,  DHH,   RH/2)             # uniq_A.append(A[i])  (rect)
y8  = ny(y7,  RH/2,  RH/2)             # i = i+1  (rect)
y9  = ny(y8,  RH/2,  RH/2, GAPX)      # sorted_A  (rect)
y10 = ny(y9,  RH/2,  RH/2)             # j=0  (rect)
y11 = ny(y10, RH/2,  DHH)              # j < len(B)?  (diamond)
y12 = ny(y11, DHH,   DHH)              # search(sorted_A, B[j])==-1?  (diamond)
y13 = ny(y12, DHH,   RH/2)             # uniq_B.append(B[j])  (rect)
y14 = ny(y13, RH/2,  RH/2)             # j = j+1  (rect)
y15 = ny(y14, RH/2,  RH/2, GAPX)      # result = sorted(set(...))  (rect)
y16 = ny(y15, RH/2,  PH/2)             # OUTPUT  (para)
y17 = ny(y16, PH/2,  OH/2)             # END  (oval)

# ─── Drawing helpers ──────────────────────────────────────────────────────────

def draw_oval(cy, text, c=C_S, fc=F_S):
    patch = mpatches.FancyBboxPatch(
        (CX - OW/2, cy - OH/2), OW, OH,
        boxstyle="round,pad=0.08",
        lw=LW, edgecolor=c, facecolor=fc, zorder=3)
    ax.add_patch(patch)
    ax.text(CX, cy, text, ha="center", va="center",
            fontsize=FS, fontfamily=FONT, fontweight="bold",
            color=c, zorder=4)

def draw_para(cy, text, c=C_IO, fc=F_IO):
    sk = 0.22
    xs = [CX-PW/2+sk, CX+PW/2+sk, CX+PW/2-sk, CX-PW/2-sk]
    ys = [cy-PH/2,    cy-PH/2,    cy+PH/2,    cy+PH/2   ]
    p = mpatches.Polygon(list(zip(xs, ys)), closed=True,
                         lw=LW, edgecolor=c, facecolor=fc, zorder=3)
    ax.add_patch(p)
    ax.text(CX, cy, text, ha="center", va="center",
            fontsize=FS, fontfamily=FONT, fontweight="bold",
            color=c, zorder=4)

def draw_rect(cy, text, c=C_P, fc=F_P, fs=FS):
    p = mpatches.FancyBboxPatch(
        (CX - RW/2, cy - RH/2), RW, RH,
        boxstyle="square,pad=0",
        lw=LW, edgecolor=c, facecolor=fc, zorder=3)
    ax.add_patch(p)
    ax.text(CX, cy, text, ha="center", va="center",
            fontsize=fs, fontfamily=FONT, color=c, zorder=4)

def draw_diamond(cy, text, c=C_D, fc=F_D):
    xs = [CX,       CX+DHW,  CX,       CX-DHW ]
    ys = [cy+DHH,   cy,      cy-DHH,   cy     ]
    p = mpatches.Polygon(list(zip(xs, ys)), closed=True,
                         lw=LW, edgecolor=c, facecolor=fc, zorder=3)
    ax.add_patch(p)
    ax.text(CX, cy, text, ha="center", va="center",
            fontsize=FS_D, fontfamily=FONT, color=c,
            multialignment="center", zorder=4)

# ─── Arrow / line helpers ─────────────────────────────────────────────────────

def arr_down(x, y_from, y_to):
    """Straight downward arrow."""
    ax.annotate("",
                xy=(x, y_to), xytext=(x, y_from),
                arrowprops=dict(arrowstyle="-|>", color=C_AR,
                                lw=ALW, mutation_scale=13),
                zorder=2)

def arr_h(x_from, x_to, y):
    """Horizontal arrow (left or right)."""
    ax.annotate("",
                xy=(x_to, y), xytext=(x_from, y),
                arrowprops=dict(arrowstyle="-|>", color=C_LB,
                                lw=ALW, mutation_scale=13),
                zorder=2)

def polyline(xs, ys):
    """Multi-segment line (no arrowhead)."""
    ax.plot(xs, ys, color=C_LB, lw=ALW,
            solid_capstyle="round", zorder=2)

def lbl(x, y, text, ha="left"):
    ax.text(x, y, text, ha=ha, va="center",
            fontsize=8.2, fontfamily=FONT,
            fontweight="bold", color=C_D, zorder=5)

# ─── Routing columns ──────────────────────────────────────────────────────────
X_SKIP  = CX + 3.6   # inner skip: "Ні" from search diamond → goes to i++/j++
X_EXIT  = CX + 4.6   # outer exit: "Ні" from loop diamond   → goes to next section
X_BACK  = CX - 4.3   # loop-back  column (both loops)

# ──────────────────────────────────────────────────────────────────────────────
#  TITLE
# ──────────────────────────────────────────────────────────────────────────────
ax.text(CX, 39.6, "Блок-схема алгоритму: Симетрична різниця  A △ B",
        ha="center", va="center", fontsize=11.5, fontfamily=FONT,
        fontweight="bold", color="#1A237E", zorder=5)
ax.plot([0.5, FIG_W-0.5], [39.15, 39.15], color="#1A237E", lw=1.0)
ax.text(CX, 38.82,
        "find_unique_elements(arr_a, arr_b)  ·  Лабораторна робота · Варіант 2",
        ha="center", va="center", fontsize=8.5, color="#546E7A",
        fontfamily=FONT, zorder=5)

# ──────────────────────────────────────────────────────────────────────────────
#  DRAW ALL BLOCKS
# ──────────────────────────────────────────────────────────────────────────────
draw_oval    (y1,  "ПОЧАТОК")
draw_para    (y2,  "Введення:  масив A,  масив B")
draw_rect    (y3,  "sorted_B  ←  quick_sort( copy(B) )")
draw_rect    (y4,  "i  ←  0 ;   uniq_A  ←  [ ]")
draw_diamond (y5,  "i  <  len(A) ?")
draw_diamond (y6,  "interpolation_search\n( sorted_B, A[i] )  =  −1 ?")
draw_rect    (y7,  "uniq_A.append( A[i] )",    c=C_G, fc=F_G)
draw_rect    (y8,  "i  ←  i + 1")
draw_rect    (y9,  "sorted_A  ←  quick_sort( copy(A) )")
draw_rect    (y10, "j  ←  0 ;   uniq_B  ←  [ ]")
draw_diamond (y11, "j  <  len(B) ?")
draw_diamond (y12, "interpolation_search\n( sorted_A, B[j] )  =  −1 ?")
draw_rect    (y13, "uniq_B.append( B[j] )",    c=C_G, fc=F_G)
draw_rect    (y14, "j  ←  j + 1")
draw_rect    (y15, "result  ←  sorted( set( uniq_A + uniq_B ) )")
draw_para    (y16, "Виведення:  result   ( A △ B )")
draw_oval    (y17, "КІНЕЦЬ",  c="#B71C1C", fc="#FFEBEE")

# ──────────────────────────────────────────────────────────────────────────────
#  STRAIGHT ARROWS  (main vertical flow)
# ──────────────────────────────────────────────────────────────────────────────
arr_down(CX, y1  - OH/2,  y2  + PH/2)
arr_down(CX, y2  - PH/2,  y3  + RH/2)
arr_down(CX, y3  - RH/2,  y4  + RH/2)
arr_down(CX, y4  - RH/2,  y5  + DHH)
arr_down(CX, y5  - DHH,   y6  + DHH)   ; lbl(CX + 0.12, (y5-DHH+y6+DHH)/2, "Так")
arr_down(CX, y6  - DHH,   y7  + RH/2)  ; lbl(CX + 0.12, (y6-DHH+y7+RH/2)/2, "Так")
arr_down(CX, y7  - RH/2,  y8  + RH/2)
arr_down(CX, y9  - RH/2,  y10 + RH/2)
arr_down(CX, y10 - RH/2,  y11 + DHH)
arr_down(CX, y11 - DHH,   y12 + DHH)   ; lbl(CX + 0.12, (y11-DHH+y12+DHH)/2, "Так")
arr_down(CX, y12 - DHH,   y13 + RH/2)  ; lbl(CX + 0.12, (y12-DHH+y13+RH/2)/2, "Так")
arr_down(CX, y13 - RH/2,  y14 + RH/2)
arr_down(CX, y15 - RH/2,  y16 + PH/2)
arr_down(CX, y16 - PH/2,  y17 + OH/2)

# ──────────────────────────────────────────────────────────────────────────────
#  LOOP A — loop-back:  bottom of i++ → left column → up → left tip of diamond5
# ──────────────────────────────────────────────────────────────────────────────
polyline([CX - RW/2, X_BACK, X_BACK], [y8, y8, y5])
arr_h(X_BACK, CX - DHW, y5)

# ──────────────────────────────────────────────────────────────────────────────
#  LOOP A — "Ні" exit:  right tip of diamond5 → right exit col → down → rect9
# ──────────────────────────────────────────────────────────────────────────────
lbl(CX + DHW + 0.1, y5 + 0.25, "Ні")
polyline([CX + DHW, X_EXIT, X_EXIT], [y5, y5, y9])
arr_h(X_EXIT, CX + RW/2, y9)

# ──────────────────────────────────────────────────────────────────────────────
#  SKIP A — "Ні" from search diamond6 → right skip col → down → top of i++ rect
# ──────────────────────────────────────────────────────────────────────────────
lbl(CX + DHW + 0.1, y6 + 0.25, "Ні")
polyline([CX + DHW, X_SKIP, X_SKIP], [y6, y6, y8])
arr_h(X_SKIP, CX + RW/2, y8)

# ──────────────────────────────────────────────────────────────────────────────
#  LOOP B — loop-back:  bottom of j++ → left column → up → left tip of diamond11
# ──────────────────────────────────────────────────────────────────────────────
polyline([CX - RW/2, X_BACK, X_BACK], [y14, y14, y11])
arr_h(X_BACK, CX - DHW, y11)

# ──────────────────────────────────────────────────────────────────────────────
#  LOOP B — "Ні" exit:  right tip of diamond11 → right exit col → down → rect15
# ──────────────────────────────────────────────────────────────────────────────
lbl(CX + DHW + 0.1, y11 + 0.25, "Ні")
polyline([CX + DHW, X_EXIT, X_EXIT], [y11, y11, y15])
arr_h(X_EXIT, CX + RW/2, y15)

# ──────────────────────────────────────────────────────────────────────────────
#  SKIP B — "Ні" from search diamond12 → right skip col → down → top of j++ rect
# ──────────────────────────────────────────────────────────────────────────────
lbl(CX + DHW + 0.1, y12 + 0.25, "Ні")
polyline([CX + DHW, X_SKIP, X_SKIP], [y12, y12, y14])
arr_h(X_SKIP, CX + RW/2, y14)

# ──────────────────────────────────────────────────────────────────────────────
#  SECTION DIVIDERS
# ──────────────────────────────────────────────────────────────────────────────
ax.text(0.5, (y1 + OH/2) + 0.55,
        "── Крок 1: пошук унікальних елементів A ──",
        ha="left", va="center", fontsize=7.2, color="#90A4AE",
        fontfamily=FONT, style="italic")

for ydiv, caption in [
    ((y8 + y9) / 2,   "── Крок 2: пошук унікальних елементів B ──"),
    ((y14 + y15) / 2, "── Крок 3: об'єднання та дедублікація ──"),
]:
    ax.plot([0.4, FIG_W-0.4], [ydiv, ydiv],
            color="#B0BEC5", lw=0.7, linestyle=":", zorder=1)
    ax.text(0.5, ydiv + 0.26, caption,
            ha="left", va="center", fontsize=7.2, color="#90A4AE",
            fontfamily=FONT, style="italic")

# ──────────────────────────────────────────────────────────────────────────────
#  LEGEND
# ──────────────────────────────────────────────────────────────────────────────
LX, LY, LLW, LLH = 0.35, 0.5, 5.8, 6.2
ax.add_patch(mpatches.FancyBboxPatch((LX, LY), LLW, LLH,
    boxstyle="round,pad=0.12", lw=0.8, edgecolor="#B0BEC5",
    facecolor="#FAFAFA", zorder=1))
ax.text(LX + LLW/2, LY + LLH - 0.32,
        "Умовні позначення  (ГОСТ 19.701-90)",
        ha="center", va="center", fontsize=8.5, fontweight="bold",
        color="#37474F", fontfamily=FONT)

items = [
    ("oval",    F_S,  C_S,  "Початок / Кінець"),
    ("para",    F_IO, C_IO, "Введення / Виведення"),
    ("rect",    F_P,  C_P,  "Оператор / Процес"),
    ("diamond", F_D,  C_D,  "Умова / Рішення"),
    ("rect",    F_G,  C_G,  "Додавання до результату"),
]
for k, (shape, fc, ec, caption) in enumerate(items):
    ix = LX + 0.32
    iy = LY + LLH - 0.80 - k * 0.95
    sw, sh = 1.1, 0.42
    if shape == "oval":
        ip = mpatches.FancyBboxPatch((ix, iy-sh/2), sw, sh,
            boxstyle="round,pad=0.06", lw=1.0, edgecolor=ec, facecolor=fc)
    elif shape == "para":
        d = 0.09
        ip = mpatches.Polygon(
            [(ix+d,    iy-sh/2), (ix+sw+d, iy-sh/2),
             (ix+sw-d, iy+sh/2), (ix-d,    iy+sh/2)],
            closed=True, lw=1.0, edgecolor=ec, facecolor=fc)
    elif shape == "diamond":
        ip = mpatches.Polygon(
            [(ix+sw/2, iy+sh/2), (ix+sw, iy),
             (ix+sw/2, iy-sh/2), (ix,    iy)],
            closed=True, lw=1.0, edgecolor=ec, facecolor=fc)
    else:
        ip = mpatches.FancyBboxPatch((ix, iy-sh/2), sw, sh,
            boxstyle="square,pad=0", lw=1.0, edgecolor=ec, facecolor=fc)
    ax.add_patch(ip)
    ax.text(ix + sw + 0.18, iy, caption,
            va="center", ha="left", fontsize=8.2, fontfamily=FONT, color="#263238")

iy_loop = LY + 0.42
polyline([LX+0.32, LX+1.42], [iy_loop, iy_loop])
arr_h(LX+0.32, LX+1.42, iy_loop)
ax.text(LX+1.62, iy_loop, "Лінія повернення / виходу з циклу",
        va="center", ha="left", fontsize=8.2, fontfamily=FONT, color="#263238")

# ──────────────────────────────────────────────────────────────────────────────
#  Footer
# ──────────────────────────────────────────────────────────────────────────────
ax.text(FIG_W - 0.3, 0.18,
        "DSA LAB · Variant 2 · find_unique_elements() · 2026",
        ha="right", va="bottom", fontsize=6.5,
        color="#90A4AE", fontfamily=FONT, style="italic")

# ──────────────────────────────────────────────────────────────────────────────
#  SAVE
# ──────────────────────────────────────────────────────────────────────────────
plt.tight_layout(pad=0)
plt.savefig("flowchart.svg", format="svg",
            bbox_inches="tight", facecolor="#FFFFFF", dpi=300)
plt.close()
print("OK  flowchart.svg збережено")
