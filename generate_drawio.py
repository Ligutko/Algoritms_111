"""
generate_drawio.py
Генерує .drawio файли для всіх 3 блок-схем лабораторної роботи.
Відкрити: app.diagrams.net  або  desktop draw.io app.
"""

# ── XML helpers ────────────────────────────────────────────────────────────────

def _e(s: str) -> str:
    """Escape text for XML attribute value."""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("←", "&#8592;").replace("→", "&#8594;")
             .replace("≤", "&#8804;").replace("≥", "&#8805;")
             .replace("−", "&#8722;").replace("△", "&#9651;")
             .replace("×", "&#215;"))

# ── Styles ─────────────────────────────────────────────────────────────────────

_F = "fontFamily=DejaVu Sans;"   # not strictly needed but kept for clarity

SS  = ("ellipse;whiteSpace=wrap;html=1;fillColor=#E8EAF6;strokeColor=#1A237E;"
       "strokeWidth=2;fontStyle=1;fontColor=#1A237E;fontSize=11;")
SE  = ("ellipse;whiteSpace=wrap;html=1;fillColor=#FFEBEE;strokeColor=#B71C1C;"
       "strokeWidth=2;fontStyle=1;fontColor=#B71C1C;fontSize=11;")
SP  = ("shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;"
       "html=1;fillColor=#BBDEFB;strokeColor=#0D47A1;strokeWidth=2;"
       "fontStyle=1;fontColor=#0D47A1;fontSize=9;")
SR  = ("rounded=0;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1565C0;"
       "strokeWidth=2;fontColor=#1565C0;fontSize=9;")
SD  = ("rhombus;whiteSpace=wrap;html=1;fillColor=#EDE7F6;strokeColor=#4A148C;"
       "strokeWidth=2;fontColor=#4A148C;fontSize=9;")
SG  = ("rounded=0;whiteSpace=wrap;html=1;fillColor=#C8E6C9;strokeColor=#1B5E20;"
       "strokeWidth=2;fontColor=#1B5E20;fontSize=9;")
SR2 = ("rounded=0;whiteSpace=wrap;html=1;fillColor=#FFEBEE;strokeColor=#B71C1C;"
       "strokeWidth=2;fontColor=#B71C1C;fontSize=9;")

# edge styles
_ED = ("edgeStyle=orthogonalEdgeStyle;html=1;strokeColor=#263238;"
       "strokeWidth=1.5;labelBackgroundColor=#ffffff;fontSize=8;fontStyle=1;")
_EL = ("edgeStyle=orthogonalEdgeStyle;html=1;strokeColor=#546E7A;"
       "strokeWidth=1.5;labelBackgroundColor=#ffffff;fontSize=8;fontStyle=1;")


# ── Builder class ──────────────────────────────────────────────────────────────

class Builder:
    OW, OH = 160, 50
    RW, RH = 260, 60
    PW, PH = 260, 60
    DW, DH = 260, 80
    CX = 390          # horizontal centre

    def __init__(self):
        self._cells: list[str] = []
        self._nid = 100

    def _id(self):
        self._nid += 1
        return str(self._nid)

    # ── vertex helpers ─────────────────────────────────────────────────────────

    def _v(self, label, style, x, y, w, h) -> str:
        i = self._id()
        self._cells.append(
            f'<mxCell id="{i}" value="{_e(label)}" style="{style}" '
            f'vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" '
            f'as="geometry"/></mxCell>')
        return i

    def oval_s(self, cy) -> str:
        return self._v("ПОЧАТОК", SS, self.CX-self.OW//2, cy-self.OH//2, self.OW, self.OH)

    def oval_e(self, cy) -> str:
        return self._v("КІНЕЦЬ", SE, self.CX-self.OW//2, cy-self.OH//2, self.OW, self.OH)

    def para(self, cy, label) -> str:
        return self._v(label, SP, self.CX-self.PW//2, cy-self.PH//2, self.PW, self.PH)

    def rect(self, cy, label, style=None) -> str:
        return self._v(label, style or SR, self.CX-self.RW//2, cy-self.RH//2, self.RW, self.RH)

    def rect_g(self, cy, label) -> str:
        return self.rect(cy, label, SG)

    def rect_r(self, cy, label) -> str:
        return self.rect(cy, label, SR2)

    def diam(self, cy, label) -> str:
        return self._v(label, SD, self.CX-self.DW//2, cy-self.DH//2, self.DW, self.DH)

    # ── edge helpers ───────────────────────────────────────────────────────────

    def _edge(self, src, tgt, label, style, pts=None,
              ex=0.5, ey=1.0, nx=0.5, ny=0.0) -> str:
        i = self._id()
        sty = (style +
               f"exitX={ex};exitY={ey};exitDx=0;exitDy=0;"
               f"entryX={nx};entryY={ny};entryDx=0;entryDy=0;")
        pts_xml = ""
        if pts:
            pts_xml = ('<Array as="points">'
                       + "".join(f'<mxPoint x="{p[0]}" y="{p[1]}"/>' for p in pts)
                       + "</Array>")
        self._cells.append(
            f'<mxCell id="{i}" value="{_e(label)}" style="{sty}" '
            f'edge="1" source="{src}" target="{tgt}" parent="1">'
            f'<mxGeometry relative="1" as="geometry">{pts_xml}</mxGeometry>'
            f'</mxCell>')
        return i

    def e_down(self, src, tgt, label=""):
        """Straight downward arrow."""
        return self._edge(src, tgt, label, _ED, ex=0.5, ey=1, nx=0.5, ny=0)

    def e_lb(self, src, tgt, pts, label=""):
        """Loop-back: exits left, enters left."""
        return self._edge(src, tgt, label, _EL, pts=pts, ex=0, ey=0.5, nx=0, ny=0.5)

    def e_skip_r(self, src, tgt, pts, label=""):
        """Skip: exits right, enters right."""
        return self._edge(src, tgt, label, _EL, pts=pts, ex=1, ey=0.5, nx=1, ny=0.5)

    def e_exit_r(self, src, tgt, pts, label=""):
        """Exit to output: exits right side, enters right side."""
        return self._edge(src, tgt, label, _EL, pts=pts, ex=1, ey=0.5, nx=1, ny=0.5)

    # ── output ─────────────────────────────────────────────────────────────────

    def xml(self, ph=1500) -> str:
        body = "\n    ".join(self._cells)
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" '
            f'tooltips="1" connect="1" arrows="1" fold="1" page="1" '
            f'pageScale="1" pageWidth="850" pageHeight="{ph}" math="0" shadow="0">\n'
            f'  <root>\n'
            f'    <mxCell id="0"/>\n'
            f'    <mxCell id="1" parent="0"/>\n'
            f'    {body}\n'
            f'  </root>\n'
            f'</mxGraphModel>')

    def save(self, fname, ph=1500):
        with open(fname, "w", encoding="utf-8") as f:
            f.write(self.xml(ph))
        print(f"OK  {fname}")


# ═══════════════════════════════════════════════════════════════════════════════
#  1.  INTERPOLATION SEARCH
# ═══════════════════════════════════════════════════════════════════════════════

def build_interpolation():
    d = Builder()
    G = 50  # gap

    # ── Y centres (computed: prev_bottom + GAP + half_next) ───────────────────
    cy_start  = 60
    cy_input  = cy_start  + d.OH//2 + G + d.PH//2   # 165
    cy_init   = cy_input  + d.PH//2 + G + d.RH//2   # 275
    cy_loop   = cy_init   + d.RH//2 + G + d.DH//2   # 395
    cy_mid    = cy_loop   + d.DH//2 + G + d.RH//2   # 515
    cy_found  = cy_mid    + d.RH//2 + G + d.DH//2   # 635
    cy_cmp    = cy_found  + d.DH//2 + G + d.DH//2   # 765
    cy_low    = cy_cmp    + d.DH//2 + G + d.RH//2   # 885
    cy_high   = cy_low    + d.RH//2 + G + d.RH//2   # 995
    cy_out    = cy_high   + d.RH//2 + G*2 + d.PH//2 # 1105
    cy_end    = cy_out    + d.PH//2 + G + d.OH//2   # 1210

    # ── Routing X columns ─────────────────────────────────────────────────────
    XL   = 100   # loop-back (left)
    XL2  = 110   # second loop-back (slight offset)
    XR1  = 585   # skip cmp→high
    XR2  = 640   # found exit
    XR3  = 695   # not-found exit

    # ── Blocks ────────────────────────────────────────────────────────────────
    n_start = d.oval_s(cy_start)
    n_input = d.para  (cy_input, "Введення:  arr  (відсортований масив),   key  (шуканий елемент)")
    n_init  = d.rect  (cy_init,  "low  ←  0 ;     high  ←  len(arr)  −  1")
    n_loop  = d.diam  (cy_loop,  "low ≤ high  ТА\narr[low] ≤ key ≤ arr[high] ?")
    n_mid   = d.rect  (cy_mid,   "mid  ←  low  +  (key − arr[low]) × (high − low) / (arr[high] − arr[low])")
    n_found = d.diam  (cy_found, "arr[ mid ]  =  key ?")
    n_cmp   = d.diam  (cy_cmp,   "arr[ mid ]  <  key ?")
    n_low   = d.rect_g(cy_low,   "low   ←  mid  +  1")
    n_high  = d.rect_r(cy_high,  "high  ←  mid  −  1")
    n_out   = d.para  (cy_out,   "Виведення:  позиція = mid   або   −1  (не знайдено)")
    n_end   = d.oval_e(cy_end)

    # ── Edges: main vertical flow ─────────────────────────────────────────────
    d.e_down(n_start, n_input)
    d.e_down(n_input, n_init)
    d.e_down(n_init,  n_loop)
    d.e_down(n_loop,  n_mid,  "Так")
    d.e_down(n_mid,   n_found)
    d.e_down(n_found, n_cmp,  "Ні")       # not found yet → compare
    d.e_down(n_cmp,   n_low,  "Так")      # arr[mid] < key  → go right
    d.e_down(n_out,   n_end)

    # ── Loop-backs ────────────────────────────────────────────────────────────
    d.e_lb(n_low,  n_loop, [(XL,  cy_low),  (XL,  cy_loop)])   # low → loop
    d.e_lb(n_high, n_loop, [(XL2, cy_high), (XL2, cy_loop)])   # high → loop

    # ── Right-side skip/exits ─────────────────────────────────────────────────
    d.e_skip_r(n_cmp,   n_high, [(XR1, cy_cmp),   (XR1, cy_high)],  "Ні")  # → go left
    d.e_exit_r(n_found, n_out,  [(XR2, cy_found), (XR2, cy_out)],   "Так") # found!
    d.e_exit_r(n_loop,  n_out,  [(XR3, cy_loop),  (XR3, cy_out)],   "Ні")  # not found

    d.save("flowchart_interpolation.drawio", ph=cy_end + 150)


# ═══════════════════════════════════════════════════════════════════════════════
#  2.  QUICK SORT  (iterative, Lomuto partition)
# ═══════════════════════════════════════════════════════════════════════════════

def build_quicksort():
    d = Builder()
    G = 50

    cy_start  = 60
    cy_input  = cy_start  + d.OH//2 + G + d.PH//2    # 165
    cy_stack  = cy_input  + d.PH//2 + G + d.RH//2    # 275
    cy_dout   = cy_stack  + d.RH//2 + G + d.DH//2    # 395   ← OUTER LOOP
    cy_pop    = cy_dout   + d.DH//2 + G + d.RH//2    # 515
    cy_dlow   = cy_pop    + d.RH//2 + G + d.DH//2    # 635
    cy_init   = cy_dlow   + d.DH//2 + G + d.RH//2    # 755
    cy_din    = cy_init   + d.RH//2 + G + d.DH//2    # 875   ← INNER LOOP
    cy_dcmp   = cy_din    + d.DH//2 + G + d.DH//2    # 1005
    cy_swap   = cy_dcmp   + d.DH//2 + G + d.RH//2    # 1125   green
    cy_jinc   = cy_swap   + d.RH//2 + G + d.RH//2    # 1235
    cy_part   = cy_jinc   + d.RH//2 + G*2 + d.RH//2  # 1415   +extra gap
    cy_push   = cy_part   + d.RH//2 + G + d.RH//2    # 1525
    cy_out    = cy_push   + d.RH//2 + G*2 + d.PH//2  # 1685
    cy_end    = cy_out    + d.PH//2 + G + d.OH//2     # 1790

    # Routing columns
    XL_IN  = 115   # inner loop-back  (jinc  → din)
    XL_OUT =  85   # outer loop-back  (push  → dout)
    XL_D   =  70   # dlow "Ні" return  (dlow  → dout)

    XR_SKP = 580   # skip: dcmp "Ні" → jinc (bypass swap)
    XR_IEX = 635   # inner exit: din "Ні" → partition
    XR_OEX = 690   # outer exit: dout "Ні" → output

    # ── Blocks ────────────────────────────────────────────────────────────────
    n_start = d.oval_s(cy_start)
    n_input = d.para  (cy_input, "Введення:  масив arr")
    n_stack = d.rect  (cy_stack, "stack  ←  [ ( 0,  len(arr) − 1 ) ]")
    n_dout  = d.diam  (cy_dout,  "stack  не\nпорожній ?")
    n_pop   = d.rect  (cy_pop,   "( low,  high )  ←  stack.pop()")
    n_dlow  = d.diam  (cy_dlow,  "low  <  high ?")
    n_init  = d.rect  (cy_init,  "pivot ← arr[high] ;   i ← low − 1 ;   j ← low")
    n_din   = d.diam  (cy_din,   "j  <  high ?")
    n_dcmp  = d.diam  (cy_dcmp,  "arr[ j ]  ≤  pivot ?")
    n_swap  = d.rect_g(cy_swap,  "i  ←  i + 1 ;     swap( arr[i],  arr[j] )")
    n_jinc  = d.rect  (cy_jinc,  "j  ←  j + 1")
    n_part  = d.rect  (cy_part,  "swap( arr[i+1],  arr[high] ) ;     pi  ←  i + 1")
    n_push  = d.rect  (cy_push,  "stack.push( low, pi−1 ) ;   stack.push( pi+1, high )")
    n_out   = d.para  (cy_out,   "Виведення:  arr  (відсортований)")
    n_end   = d.oval_e(cy_end)

    # ── Main vertical flow ────────────────────────────────────────────────────
    d.e_down(n_start, n_input)
    d.e_down(n_input, n_stack)
    d.e_down(n_stack, n_dout)
    d.e_down(n_dout,  n_pop,  "Так")
    d.e_down(n_pop,   n_dlow)
    d.e_down(n_dlow,  n_init, "Так")
    d.e_down(n_init,  n_din)
    d.e_down(n_din,   n_dcmp, "Так")
    d.e_down(n_dcmp,  n_swap, "Так")
    d.e_down(n_swap,  n_jinc)
    d.e_down(n_part,  n_push)
    d.e_down(n_out,   n_end)

    # ── Inner loop-back:  jinc → din ─────────────────────────────────────────
    d.e_lb(n_jinc, n_din,  [(XL_IN, cy_jinc), (XL_IN, cy_din)])

    # ── Outer loop-back:  push → dout ────────────────────────────────────────
    d.e_lb(n_push, n_dout, [(XL_OUT, cy_push), (XL_OUT, cy_dout)])

    # ── dlow "Ні" (low>=high, skip partition) → dout ─────────────────────────
    d.e_lb(n_dlow, n_dout, [(XL_D, cy_dlow), (XL_D, cy_dout)], "Ні")

    # ── Skip swap:  dcmp "Ні" → jinc ─────────────────────────────────────────
    d.e_skip_r(n_dcmp, n_jinc, [(XR_SKP, cy_dcmp), (XR_SKP, cy_jinc)], "Ні")

    # ── Inner exit:  din "Ні" → partition ────────────────────────────────────
    d.e_exit_r(n_din, n_part,  [(XR_IEX, cy_din),  (XR_IEX, cy_part)],  "Ні")

    # ── Outer exit:  dout "Ні" → output ──────────────────────────────────────
    d.e_exit_r(n_dout, n_out,  [(XR_OEX, cy_dout), (XR_OEX, cy_out)],   "Ні")

    d.save("flowchart_quicksort.drawio", ph=cy_end + 150)


# ═══════════════════════════════════════════════════════════════════════════════
#  3.  SYMMETRIC DIFFERENCE  (find_unique_elements)
# ═══════════════════════════════════════════════════════════════════════════════

def build_symmetric():
    d = Builder()
    G = 50

    cy_start   = 60
    cy_input   = cy_start   + d.OH//2 + G + d.PH//2    # 165

    # ── SECTION A ─────────────────────────────────────────────────────────────
    cy_sortb   = cy_input   + d.PH//2 + G*2 + d.RH//2  # 325   (+1 extra gap)
    cy_inita   = cy_sortb   + d.RH//2 + G + d.RH//2    # 435
    cy_loopa   = cy_inita   + d.RH//2 + G + d.DH//2    # 555   ← LOOP A
    cy_searcha = cy_loopa   + d.DH//2 + G + d.DH//2    # 685
    cy_appa    = cy_searcha + d.DH//2 + G + d.RH//2    # 805   green
    cy_iinc    = cy_appa    + d.RH//2 + G + d.RH//2    # 915

    # ── SECTION B ─────────────────────────────────────────────────────────────
    cy_sorta   = cy_iinc    + d.RH//2 + G*2 + d.RH//2  # 1075  (+1 extra gap)
    cy_initb   = cy_sorta   + d.RH//2 + G + d.RH//2    # 1185
    cy_loopb   = cy_initb   + d.RH//2 + G + d.DH//2    # 1305  ← LOOP B
    cy_searchb = cy_loopb   + d.DH//2 + G + d.DH//2    # 1435
    cy_appb    = cy_searchb + d.DH//2 + G + d.RH//2    # 1555   green
    cy_jinc    = cy_appb    + d.RH//2 + G + d.RH//2    # 1665

    # ── SECTION COMBINE ───────────────────────────────────────────────────────
    cy_result  = cy_jinc    + d.RH//2 + G*2 + d.RH//2  # 1825
    cy_out     = cy_result  + d.RH//2 + G + d.PH//2    # 1935
    cy_end     = cy_out     + d.PH//2 + G + d.OH//2    # 2040

    # Routing columns
    XL     =  85   # loop-backs (both A and B)
    XL2    = 100   # secondary loop-back offset
    XR_SKP = 580   # inner skip (search "Ні" → iinc / jinc)
    XR_EXA = 640   # loop A exit (loopa "Ні" → sorta)
    XR_EXB = 695   # loop B exit (loopb "Ні" → result)

    # ── Blocks ────────────────────────────────────────────────────────────────
    n_start   = d.oval_s (cy_start)
    n_input   = d.para   (cy_input,   "Введення:  масив A,      масив B")
    n_sortb   = d.rect   (cy_sortb,   "sorted_B  ←  quick_sort( copy(B) )")
    n_inita   = d.rect   (cy_inita,   "i  ←  0 ;     uniq_A  ←  [ ]")
    n_loopa   = d.diam   (cy_loopa,   "i  <  len(A) ?")
    n_searcha = d.diam   (cy_searcha, "interpolation_search\n( sorted_B,  A[i] )  =  −1 ?")
    n_appa    = d.rect_g (cy_appa,    "uniq_A.append( A[i] )")
    n_iinc    = d.rect   (cy_iinc,    "i  ←  i + 1")
    n_sorta   = d.rect   (cy_sorta,   "sorted_A  ←  quick_sort( copy(A) )")
    n_initb   = d.rect   (cy_initb,   "j  ←  0 ;     uniq_B  ←  [ ]")
    n_loopb   = d.diam   (cy_loopb,   "j  <  len(B) ?")
    n_searchb = d.diam   (cy_searchb, "interpolation_search\n( sorted_A,  B[j] )  =  −1 ?")
    n_appb    = d.rect_g (cy_appb,    "uniq_B.append( B[j] )")
    n_jinc    = d.rect   (cy_jinc,    "j  ←  j + 1")
    n_result  = d.rect   (cy_result,  "result  ←  sorted( set( uniq_A + uniq_B ) )")
    n_out     = d.para   (cy_out,     "Виведення:  result   ( A △ B )")
    n_end     = d.oval_e (cy_end)

    # ── Main vertical flow ────────────────────────────────────────────────────
    d.e_down(n_start,   n_input)
    d.e_down(n_input,   n_sortb)
    d.e_down(n_sortb,   n_inita)
    d.e_down(n_inita,   n_loopa)
    d.e_down(n_loopa,   n_searcha, "Так")
    d.e_down(n_searcha, n_appa,    "Так")
    d.e_down(n_appa,    n_iinc)
    d.e_down(n_sorta,   n_initb)
    d.e_down(n_initb,   n_loopb)
    d.e_down(n_loopb,   n_searchb, "Так")
    d.e_down(n_searchb, n_appb,    "Так")
    d.e_down(n_appb,    n_jinc)
    d.e_down(n_result,  n_out)
    d.e_down(n_out,     n_end)

    # ── Loop-backs ────────────────────────────────────────────────────────────
    d.e_lb(n_iinc, n_loopa, [(XL,  cy_iinc), (XL,  cy_loopa)])
    d.e_lb(n_jinc, n_loopb, [(XL2, cy_jinc), (XL2, cy_loopb)])

    # ── Skip append (search "Ні" → increment) ────────────────────────────────
    d.e_skip_r(n_searcha, n_iinc, [(XR_SKP, cy_searcha), (XR_SKP, cy_iinc)], "Ні")
    d.e_skip_r(n_searchb, n_jinc, [(XR_SKP, cy_searchb), (XR_SKP, cy_jinc)], "Ні")

    # ── Loop exit (loop "Ні" → next section) ─────────────────────────────────
    d.e_exit_r(n_loopa, n_sorta,  [(XR_EXA, cy_loopa), (XR_EXA, cy_sorta)],  "Ні")
    d.e_exit_r(n_loopb, n_result, [(XR_EXB, cy_loopb), (XR_EXB, cy_result)], "Ні")

    d.save("flowchart.drawio", ph=cy_end + 150)


# ── Run all ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    build_interpolation()
    build_quicksort()
    build_symmetric()
    print("\nГотово! Відкрийте файли на  app.diagrams.net")
