"""SVG-чертежи конспектов. Палитра та же, что в vmaiorov-collab/conspectus (3Blue1Brown)."""
import math
import re

BG, BLUE, GREEN, YELLOW, RED, ORANGE, VIOLET, TEXT, MUTED = (
    "#141a24", "#58c4dd", "#83c167", "#ffff00", "#fc6255", "#ff8c1a", "#c78bff", "#dfe7f1", "#9aa4b2")
CELL = '#9aa4b2" fill-opacity="0.16'  # полупрозрачная заливка, читается в обеих темах


class S:
    def __init__(self, w, h, label):
        self.w, self.h, self.label, self.o = w, h, label, []

    def raw(self, s):
        self.o.append(s)
        return self

    def line(self, x1, y1, x2, y2, c=MUTED, w=2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return self.raw(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"{d}/>')

    def arrow(self, x1, y1, x2, y2, c=BLUE, w=3, dash=None):
        a = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - 11 * math.cos(a), y2 - 11 * math.sin(a)
        self.line(x1, y1, bx, by, c, w, dash)
        px, py = 5.5 * -math.sin(a), 5.5 * math.cos(a)
        return self.raw(f'<path d="M{x2:.1f},{y2:.1f} L{bx+px:.1f},{by+py:.1f} L{bx-px:.1f},{by-py:.1f}z" class="solid" fill="{c}"/>')

    def force(self, x1, y1, x2, y2, label="", c=YELLOW, dx=9, dy=4, anchor="start", size=14):
        """Стрелка силы с подписью у острия."""
        self.arrow(x1, y1, x2, y2, c)
        return self.text(x2 + dx, y2 + dy, label, c, size, anchor) if label else self

    def text(self, x, y, s, c=TEXT, size=17, anchor="middle", it=False):
        st = ' font-style="italic"' if it else ""
        # "x_end" -> x с нижним индексом
        s = re.sub(r"_([0-9]+|[A-Za-zА-Яа-я]+)",
                   lambda m: f'<tspan dy="4" font-size="72%">{m.group(1)}</tspan><tspan dy="-4">\u200b</tspan>', s)
        return self.raw(f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" text-anchor="{anchor}"{st}>{s}</text>')

    def rect(self, x, y, w, h, c=BLUE, fill=CELL, r=4):
        return self.raw(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" stroke="{c}" stroke-width="2"/>')

    def circle(self, x, y, r, c=BLUE, fill=CELL):
        return self.raw(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="2"/>')

    def dot(self, x, y, c=TEXT, r=4):
        return self.raw(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" class="solid" fill="{c}"/>')

    def path(self, d, c=BLUE, w=3, fill="none", op=1, dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        fo = "" if fill == CELL else f' fill-opacity="{op}"'
        return self.raw(f'<path d="{d}" fill="{fill}"{fo} stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{da}/>')

    def ground(self, x1, x2, y, up=False):
        """Опора со штриховкой: up=True — потолок (штрихи сверху)."""
        self.line(x1, y, x2, y, TEXT, 2)
        s = -10 if up else 10
        x = x1 + 6
        while x < x2:
            self.line(x, y, x - 8 if not up else x + 8, y + s, MUTED, 1.4)
            x += 14
        return self

    def wall(self, y1, y2, x, left=True):
        self.line(x, y1, x, y2, TEXT, 2)
        s = -10 if left else 10
        y = y1 + 8
        while y < y2:
            self.line(x, y, x + s, y + 8, MUTED, 1.4)
            y += 14
        return self

    def pulley(self, x, y, r=18, c=ORANGE):
        return self.circle(x, y, r, c).dot(x, y, c, 3.5)

    def spring(self, x1, y1, x2, y2, n=8, amp=9, c=GREEN):
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        pts = [(0, 0), (10, 0)]
        for i in range(2 * n):
            pts.append((10 + (L - 20) * (i + .5) / (2 * n), amp if i % 2 else -amp))
        pts += [(L - 10, 0), (L, 0)]
        d = " L".join(f"{x1+ux*t-uy*s:.1f},{y1+uy*t+ux*s:.1f}" for t, s in pts)
        return self.path("M" + d, c, 2.2)

    def support(self, x, y, c=YELLOW):
        """Опора-треугольник: вершина в (x, y)."""
        self.path(f"M{x},{y} L{x-14},{y+24} L{x+14},{y+24}z", c, 2, CELL)
        return self.ground(x - 26, x + 26, y + 24)

    def axes(self, x0, y0, w, h, xl="t", yl="x", below=0):
        self.arrow(x0, y0, x0 + w, y0, MUTED, 2)
        self.arrow(x0, y0 + below, x0, y0 - h, MUTED, 2)
        self.text(x0 + w + 4, y0 + 20, xl, MUTED, 16, "middle", True)
        return self.text(x0 - 10, y0 - h + 6, yl, MUTED, 16, "end", True)

    def svg(self):
        return (f'<svg viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{self.label}" xmlns="http://www.w3.org/2000/svg" '
                f'font-family="-apple-system,Segoe UI,Roboto,sans-serif"><rect width="{self.w}" height="{self.h}" rx="12" fill="{BG}"/>'
                + "".join(self.o) + "</svg>")


F = {}


def fig(fn):
    F[fn.__name__] = fn
    return fn


# ---------- 1. Векторы ----------
@fig
def vec_ops():
    s = S(760, 270, "Adding vectors by the triangle and parallelogram rules, and subtracting")
    s.text(130, 28, "triangle", MUTED, 15).text(385, 28, "parallelogram", MUTED, 15).text(635, 28, "subtraction", MUTED, 15)
    s.arrow(50, 220, 90, 90, BLUE).arrow(90, 90, 220, 100, GREEN).arrow(50, 220, 220, 100, YELLOW)
    s.text(52, 150, "a", BLUE, 19, it=True).text(155, 80, "b", GREEN, 19, it=True).text(165, 185, "a + b", YELLOW, 18)
    s.arrow(290, 220, 320, 100, BLUE).arrow(290, 220, 430, 220, GREEN).arrow(290, 220, 460, 100, YELLOW)
    s.line(320, 100, 460, 100, MUTED, 1.6, "6 6").line(430, 220, 460, 100, MUTED, 1.6, "6 6")
    s.text(290, 150, "a", BLUE, 19, it=True).text(360, 245, "b", GREEN, 19, it=True).text(415, 175, "a + b", YELLOW, 18)
    s.arrow(555, 220, 620, 90, BLUE).arrow(620, 90, 725, 150, RED).arrow(555, 220, 725, 150, YELLOW)
    s.text(565, 150, "a", BLUE, 19, it=True).text(690, 105, "−b", RED, 19, it=True).text(665, 205, "a − b", YELLOW, 18)
    return s.svg()


@fig
def vec_proj():
    s = S(760, 270, "Position vector of point A and projections of a vector onto an axis")
    s.axes(60, 215, 270, 185, "x", "y")
    s.arrow(60, 215, 250, 80, YELLOW).dot(250, 80)
    s.line(250, 80, 250, 215, MUTED, 1.6, "5 5").line(60, 80, 250, 80, MUTED, 1.6, "5 5")
    s.text(268, 74, "A", TEXT, 18).text(250, 240, "x_A", BLUE).text(40, 85, "y_A", GREEN).text(135, 135, "r_A", YELLOW, 18)
    s.arrow(60, 215, 105, 215, BLUE, 4).arrow(60, 215, 60, 170, GREEN, 4).text(90, 236, "i", BLUE, 17, it=True).text(44, 182, "j", GREEN, 17, it=True)
    s.arrow(420, 215, 735, 215, MUTED, 2).text(735, 240, "x", MUTED, 16, it=True)
    s.arrow(470, 150, 670, 60, YELLOW).text(555, 90, "a", YELLOW, 19, it=True)
    s.line(470, 150, 470, 215, MUTED, 1.6, "5 5").line(670, 60, 670, 215, MUTED, 1.6, "5 5")
    s.arrow(470, 215, 670, 215, GREEN, 4).text(570, 200, "a_x = x_end − x_start", GREEN, 15)
    s.text(470, 240, "x_start", MUTED, 15).text(670, 240, "x_end", MUTED, 15)
    return s.svg()


@fig
def vec_forces():
    s = S(520, 300, "Resultant of forces of 6 and 8 newtons")
    ox, oy, k = 120, 260, 27
    s.arrow(ox, oy, ox + 6 * k, oy, BLUE).arrow(ox, oy, ox, oy - 8 * k, GREEN).arrow(ox, oy, ox + 6 * k, oy - 8 * k, YELLOW)
    s.line(ox + 6 * k, oy, ox + 6 * k, oy - 8 * k, MUTED, 1.6, "6 6").line(ox, oy - 8 * k, ox + 6 * k, oy - 8 * k, MUTED, 1.6, "6 6")
    s.text(ox + 80, oy + 24, "F₁ = 6 N", BLUE).text(ox - 50, 140, "F₂ = 8 N", GREEN).text(ox + 150, 120, "F = 10 N", YELLOW)
    s.path(f"M{ox+40},{oy} A40,40 0 0 0 {ox+24},{oy-32}", ORANGE, 2).text(ox + 66, oy - 20, "θ ≈ 53°", ORANGE, 15)
    return s.svg()


# ---------- 2. Кинематика ----------
@fig
def kin_path():
    s = S(640, 220, "Trajectory, distance and displacement")
    s.path("M80,60 C200,-5 330,60 420,50 C560,35 590,120 500,150 C420,180 300,120 120,170", BLUE, 3)
    s.dot(80, 60).dot(120, 170, YELLOW)
    s.arrow(80, 60, 119, 163, YELLOW).text(55, 52, "start", MUTED, 15).text(120, 198, "finish", MUTED, 15)
    s.text(60, 125, "d", YELLOW, 20, it=True).text(390, 28, "trajectory; its length is the distance S", BLUE, 16)
    return s.svg()


@fig
def kin_st_example():
    s = S(640, 300, "Distance–time graph: 12 metres in 3 seconds, a stop, then 22 metres by 10 seconds")
    X = lambda t: 80 + t * 50
    Y = lambda v: 250 - v * 9
    s.axes(80, 250, 540, 230, "t, s", "S, m")
    for t in (3, 5, 10):
        s.line(X(t), 250, X(t), Y({3: 12, 5: 12, 10: 22}[t]), MUTED, 1.2, "4 5").text(X(t), 272, str(t), MUTED, 15)
    for v in (12, 22):
        s.line(80, Y(v), X(10 if v == 22 else 3), Y(v), MUTED, 1.2, "4 5").text(66, Y(v) + 5, str(v), MUTED, 15, "end")
    s.path(f"M{X(0)},{Y(0)} L{X(3)},{Y(12)} L{X(5)},{Y(12)} L{X(10)},{Y(22)}", BLUE)
    s.line(X(0), Y(0), X(10), Y(22), YELLOW, 1.8, "8 6")
    s.text(X(1.1), Y(10), "4 m/s", BLUE).text(X(4), Y(13.4), "0", BLUE).text(X(7), Y(18.8), "2 m/s", BLUE)
    s.text(X(7.6), Y(7.5), "average over 10 s: 2.2 m/s", YELLOW, 15)
    return s.svg()


@fig
def kin_three():
    s = S(760, 250, "Matching graphs of distance, speed and average speed")
    for i, name in enumerate(["S, m", "v, m/s", "⟨v⟩, m/s"]):
        x0 = 55 + i * 250
        s.axes(x0, 200, 180, 165, "t", name)
        for t in range(1, 5):
            s.text(x0 + t * 40, 222, str(t), MUTED, 14)
    Y = lambda v: 200 - v * 12
    s.path(f"M55,200 L135,{Y(8)} L175,{Y(8)} L215,{Y(12)}", BLUE)
    s.text(40, Y(8) + 5, "8", MUTED, 14).text(40, Y(12) + 5, "12", MUTED, 14)
    Y = lambda v: 200 - v * 30
    s.line(305, Y(4), 385, Y(4), GREEN, 3).line(385, Y(0), 425, Y(0), GREEN, 4).line(425, Y(4), 465, Y(4), GREEN, 3)
    s.text(290, Y(4) + 5, "4", MUTED, 14)
    pts = [(2, 4)] + [(t / 10, 8 / (t / 10)) for t in range(21, 31)] + [(t / 10, (8 + 4 * (t / 10 - 3)) / (t / 10)) for t in range(31, 41)]
    d = f"M555,{Y(4)} " + " ".join(f"L{555+t*40:.1f},{Y(v):.1f}" for t, v in pts)
    s.path(d, YELLOW).text(540, Y(4) + 5, "4", MUTED, 14).text(540, Y(3) + 5, "3", MUTED, 14)
    return s.svg()


@fig
def kin_area():
    s = S(640, 260, "Area under the velocity graph equals displacement and carries a sign")
    s.axes(70, 140, 530, 120, "t", "v_x", 100)
    s.path("M70,140 C140,30 270,20 340,140 z", GREEN, 3, GREEN, .25)
    s.path("M340,140 C390,225 470,235 540,215 L540,140 z", RED, 3, RED, .25)
    s.text(200, 100, "S_1 &gt; 0", GREEN, 19).text(440, 185, "S_2 &lt; 0", RED, 19).text(420, 40, "displacement = S_1 + S_2", TEXT, 16)
    s.text(420, 66, "distance = |S_1| + |S_2|", MUTED, 16)
    return s.svg()


@fig
def kin_hill():
    s = S(760, 240, "Speed drops on the track with a hill and rises on the track with a dip")
    for x0, name, up, col in ((60, "track with a hill: T(t)", False, RED), (440, "track with a dip: B(t)", True, GREEN)):
        s.axes(x0, 200, 270, 170, "t", "v")
        y = 110
        dy = -65 if up else 65
        s.path(f"M{x0},{y} L{x0+60},{y} C{x0+100},{y} {x0+95},{y+dy} {x0+135},{y+dy} C{x0+175},{y+dy} {x0+170},{y} {x0+210},{y} L{x0+250},{y}", col, 3)
        s.line(x0, y, x0 + 250, y, MUTED, 1.4, "6 6").text(x0 - 14, y + 5, "s", MUTED, 16)
        s.text(x0 + 135, y + (-20 if up else 25), "A", col, 19).text(x0 + 140, 228, name, TEXT, 15)
    return s.svg()


# ---------- 3. Ускорение ----------
@fig
def acc_trap():
    s = S(560, 270, "Velocity graph at constant acceleration: displacement equals the trapezium area")
    s.axes(80, 220, 430, 190, "t", "v_x")
    s.path("M80,220 L80,160 L400,60 L400,220 z", BLUE, 0, BLUE, .22)
    s.line(80, 160, 460, 41, BLUE, 3).line(400, 60, 400, 220, MUTED, 1.6, "6 6").line(80, 60, 400, 60, MUTED, 1.4, "6 6")
    s.text(58, 165, "v₀ₓ", GREEN).text(56, 66, "v_x(t)", YELLOW, 15).text(400, 244, "t", MUTED)
    s.text(245, 180, "area = Δx", TEXT, 18)
    return s.svg()


@fig
def acc_odd():
    s = S(560, 270, "Distances covered from rest in equal time intervals are in the ratio 1 : 3 : 5")
    s.axes(70, 225, 440, 200, "t", "v")
    for i, (k, c) in enumerate(((1, BLUE), (3, GREEN), (5, YELLOW))):
        x1, x2 = 70 + i * 120, 190 + i * 120
        y1, y2 = 225 - i * 55, 170 - i * 55
        s.path(f"M{x1},225 L{x1},{y1} L{x2},{y2} L{x2},225 z", c, 1.5, c, .28)
        s.text((x1 + x2) / 2 + 10, 212, f"{k}·S₁", c, 17).text(x2, 247, f"{'' if i == 0 else i+1}τ", MUTED, 15)
    s.line(70, 225, 460, 46, TEXT, 2.5)
    return s.svg()


@fig
def acc_back():
    s = S(760, 270, "Position and distance of a body that brakes and turns back")
    s.axes(60, 200, 280, 170, "t", "x")
    s.path("M60,200 Q185,-60 310,200", BLUE).line(185, 70, 185, 200, MUTED, 1.4, "5 5").text(185, 222, "t₀ = v₀/a", MUTED, 15)
    s.text(200, 245, "position x(t)", BLUE, 15)
    s.axes(440, 200, 280, 170, "t", "S")
    s.path("M440,200 Q502,70 565,70", GREEN).path("M565,70 Q627,70 690,-0", GREEN, 0)
    s.path("M565,70 Q620,70 680,25", GREEN).line(565, 70, 565, 200, MUTED, 1.4, "5 5").text(565, 222, "t₀", MUTED, 15)
    s.text(580, 245, "distance S(t) never decreases", GREEN, 15)
    return s.svg()


@fig
def acc_incline():
    s = S(640, 300, "Measured acceleration on an incline versus the sine of the angle")
    pts = [(.08, 31), (.12, 47), (.16, 67), (.24, 122), (.48, 238)]
    X = lambda v: 80 + v * 1000
    Y = lambda a: 250 - a * .85
    s.axes(80, 250, 530, 230, "sin φ", "a, cm/s²")
    for a in (50, 100, 150, 200, 250):
        s.line(80, Y(a), 590, Y(a), '#9aa4b2" stroke-opacity="0.28', 1).text(68, Y(a) + 5, str(a), MUTED, 14, "end")
    k = sum(x * y for x, y in pts) / sum(x * x for x, y in pts)
    s.line(X(0), Y(0), X(.5), Y(.5 * k), YELLOW, 1.8, "8 6")
    for x, a in pts:
        s.dot(X(x), Y(a), BLUE, 6).text(X(x), 272, str(x), MUTED, 14)
    s.text(X(.28), Y(215), f"line through zero: a ≈ {k:.0f}·sin φ", YELLOW, 15)
    return s.svg()


# ---------- 4. Масса ----------
@fig
def mass_two():
    s = S(760, 230, "Two ways to measure mass: a balance and recoiling carts")
    s.text(180, 30, "gravitational mass: balance", MUTED, 15)
    s.support(180, 130).line(70, 118, 290, 118, TEXT, 4)
    s.circle(90, 96, 21, ORANGE).text(90, 102, "m?", ORANGE, 15).rect(250, 76, 44, 40, BLUE).text(272, 102, "m₀", BLUE, 15)
    s.text(560, 30, "inertial mass: carts and a spring", MUTED, 15)
    s.ground(410, 720, 180)
    for x, w, name, c in ((460, 60, "m₁", BLUE), (600, 90, "m₂", GREEN)):
        s.rect(x, 105, w, 55, c).text(x + w / 2, 138, name, c).circle(x + 14, 170, 10, c).circle(x + w - 14, 170, 10, c)
    s.arrow(460, 85, 400, 85, BLUE).text(430, 70, "v₁", BLUE).arrow(660, 85, 705, 85, GREEN).text(690, 70, "v₂", GREEN)
    s.spring(522, 132, 598, 132, 5, 8, YELLOW)
    return s.svg()


# ---------- 5. Ньютон ----------
@fig
def newton_book():
    s = S(640, 250, "Gravity and the normal force; Newton's third law")
    s.ground(50, 290, 190).rect(120, 130, 100, 60)
    s.arrow(170, 160, 170, 60, GREEN).arrow(170, 160, 170, 235, RED).dot(170, 160)
    s.text(190, 72, "N", GREEN, 20, it=True).text(198, 228, "mg", RED, 19, it=True)
    s.rect(380, 100, 80, 60, BLUE).rect(460, 100, 80, 60, ORANGE).text(405, 135, "1", BLUE).text(515, 135, "2", ORANGE)
    s.arrow(458, 130, 355, 130, BLUE).arrow(462, 130, 565, 130, ORANGE)
    s.text(358, 90, "F₁₂", BLUE).text(565, 90, "F₂₁", ORANGE).text(460, 200, "F₁₂ = −F₂₁", TEXT, 19)
    return s.svg()


# ---------- 6. Блоки ----------
@fig
def pul_basic():
    s = S(760, 300, "A fixed pulley redirects the force, a movable pulley halves it")
    s.text(180, 24, "fixed pulley", MUTED, 15).text(540, 24, "movable pulley", MUTED, 15)
    s.ground(100, 260, 50, True).line(180, 50, 180, 90, TEXT).pulley(180, 108, 24)
    s.line(156, 108, 156, 210, TEXT).rect(134, 210, 44, 40).text(156, 236, "m", BLUE)
    s.arrow(204, 108, 204, 220, YELLOW).text(240, 200, "T = mg", YELLOW)
    s.ground(450, 650, 50, True).line(510, 50, 510, 170, TEXT).pulley(536, 170, 26)
    s.path("M510,170 A26,26 0 0 0 562,170", TEXT, 2).arrow(562, 170, 562, 75, YELLOW)
    s.line(536, 170, 536, 225, TEXT).rect(510, 225, 52, 42).text(536, 252, "m", BLUE)
    s.text(600, 105, "T", YELLOW, 19).text(485, 110, "T", YELLOW, 19).text(640, 215, "2T = mg", TEXT, 19)
    return s.svg()


@fig
def pul_cascade():
    s = S(640, 340, "Three movable pulleys in a row: an eightfold gain in force")
    s.ground(60, 580, 40, True)
    xs = [(140, 250), (230, 185), (320, 120)]
    s.line(114, 40, 114, 250, TEXT).path("M114,250 A26,26 0 0 0 166,250", TEXT, 2).line(166, 250, 204, 185, TEXT)
    s.line(204, 40, 204, 185, TEXT, 2).path("M204,185 A26,26 0 0 0 256,185", TEXT, 2).line(256, 185, 294, 120, TEXT)
    s.line(294, 40, 294, 120, TEXT, 2).path("M294,120 A26,26 0 0 0 346,120", TEXT, 2).line(346, 120, 424, 90, TEXT)
    s.pulley(450, 90, 26).line(450, 40, 450, 64, TEXT).line(476, 90, 476, 230, TEXT)
    for x, y in xs:
        s.pulley(x, y, 26)
    s.line(140, 250, 140, 280, TEXT).rect(105, 280, 70, 40).text(140, 307, "m₁", BLUE)
    s.rect(450, 230, 52, 40, GREEN).text(476, 256, "m₂", GREEN)
    s.text(188, 262, "T₁", YELLOW, 16).text(278, 197, "T₂", YELLOW, 16).text(500, 160, "T₃", YELLOW, 16)
    s.text(430, 308, "m₁g = 2T₁ = 4T₂ = 8T₃ = 8m₂g", TEXT, 17)
    return s.svg()


@fig
def lab_weigh():
    s = S(640, 345, "Weighing a heavy load with a weak newtonmeter: knot, slanted string, horizontal force")
    s.ground(110, 230, 40, True).line(170, 40, 300, 190, BLUE, 3).dot(300, 190, TEXT, 6)
    s.line(300, 190, 300, 235, TEXT).rect(268, 235, 64, 45).text(300, 264, "m", BLUE)
    s.arrow(300, 190, 420, 190, YELLOW).rect(420, 176, 130, 28, ORANGE).text(485, 196, "newtonmeter", ORANGE, 14)
    s.arrow(300, 190, 232, 112, GREEN).text(278, 125, "T", GREEN, 19).text(370, 175, "F", YELLOW, 19)
    s.line(170, 190, 300, 190, MUTED, 1.5, "6 6").line(170, 40, 170, 190, MUTED, 1.5, "6 6")
    s.text(235, 215, "x", MUTED, 18, it=True).text(150, 120, "y", MUTED, 18, it=True).text(262, 92, "l", MUTED, 18, it=True)
    s.force(300, 190, 300, 232, "W", RED, 8, -8)
    s.force(300, 280, 300, 332, "mg", RED, 8, -6)
    return s.svg()


# ---------- 7. Гук ----------
@fig
def hooke_graph():
    s = S(700, 330, "Stress–strain diagram of a material")
    s.axes(70, 280, 590, 250, "Δl", "F")
    s.path("M70,280 L230,120 C260,92 285,80 300,82 C330,86 330,100 380,98 C450,95 500,45 540,48 C575,52 595,80 610,102", BLUE, 3)
    for x, y, t, tx, ty in ((230, 120, "limit of proportionality", 345, 160), (268, 90, "elastic limit", 190, 62),
                            (320, 90, "yield point", 380, 130), (540, 48, "ultimate strength", 540, 28), (610, 102, "fracture", 625, 135)):
        s.dot(x, y, YELLOW, 5).text(tx, ty, t, TEXT, 14)
    s.text(170, 230, "F = kΔl", GREEN, 18)
    return s.svg()


@fig
def hooke_connect():
    s = S(760, 250, "Springs in series and in parallel")
    s.text(200, 28, "series", MUTED, 15).text(580, 28, "parallel", MUTED, 15)
    s.wall(80, 180, 50).spring(50, 130, 200, 130).spring(200, 130, 350, 130, 8, 9, BLUE).arrow(350, 130, 390, 130, YELLOW)
    s.text(125, 105, "k₁", GREEN).text(275, 105, "k₂", BLUE).text(200, 210, "1/k = 1/k₁ + 1/k₂", TEXT, 18)
    s.wall(65, 190, 470).spring(470, 95, 640, 95).spring(470, 155, 640, 155, 8, 9, BLUE).line(640, 80, 640, 170, TEXT, 4)
    s.arrow(642, 125, 710, 125, YELLOW).text(555, 75, "k₁", GREEN).text(555, 190, "k₂", BLUE).text(590, 225, "k = k₁ + k₂", TEXT, 18)
    return s.svg()


@fig
def hooke_tasks():
    s = S(760, 345, "Diagrams for the spring combination problems, with forces")
    s.text(130, 25, "problem 1", MUTED, 15).text(390, 25, "problem 2", MUTED, 15).text(630, 25, "problem 3", MUTED, 15)
    s.ground(60, 200, 45, True).spring(130, 45, 130, 115).line(100, 115, 160, 115, TEXT, 3)
    s.spring(100, 115, 100, 205, 6, 8, BLUE).spring(160, 115, 160, 205, 6, 8, BLUE).line(100, 205, 160, 205, TEXT, 3).spring(130, 205, 130, 290)
    s.text(165, 80, "10", GREEN).text(218, 165, "10 and 10", BLUE, 15).text(165, 255, "10 N/m", GREEN, 15)
    s.ground(320, 460, 45, True).spring(390, 45, 390, 140).pulley(390, 172, 30).line(390, 140, 390, 172, TEXT)
    s.line(360, 172, 360, 290, TEXT).ground(335, 385, 290).arrow(420, 172, 420, 270, YELLOW).text(440, 260, "F", YELLOW).text(420, 95, "k", GREEN)
    s.ground(560, 700, 45, True).spring(630, 45, 630, 125).pulley(630, 175, 30).line(630, 125, 630, 175, TEXT)
    s.spring(600, 175, 600, 295, 7, 8, BLUE).ground(575, 625, 295).arrow(660, 175, 660, 275, YELLOW).text(680, 265, "F", YELLOW)
    s.text(660, 90, "k", GREEN).text(573, 240, "k", BLUE)
    s.force(130, 290, 130, 325, "F", YELLOW, 9, -4).force(130, 115, 130, 82, "F", GREEN, -14, 6, "end")
    s.force(100, 115, 100, 148, "F/2", ORANGE, -7, 0, "end").force(160, 115, 160, 148, "F/2", ORANGE, 8, 0)
    s.force(130, 205, 130, 238, "F", ORANGE, -9, 0, "end").force(100, 205, 100, 172, "", GREEN).force(160, 205, 160, 172, "", GREEN)
    s.force(390, 172, 390, 128, "2F", GREEN, 8, 8).force(360, 172, 360, 225, "F", ORANGE, -8, 0, "end")
    s.force(630, 175, 630, 130, "2F", GREEN, 8, 8).force(600, 175, 600, 220, "F", ORANGE, -8, 0, "end")
    return s.svg()


@fig
def hooke_spring_fit():
    s = S(640, 310, "Length per turn grows linearly with the number of turns")
    data = [(18, 20.5), (22, 29.5), (26, 40), (30, 52), (34, 68), (38, 86.5), (42, 108), (46, 120)]
    pts = [(n, L / n) for n, L in data]
    mx = sum(p[0] for p in pts) / len(pts)
    my = sum(p[1] for p in pts) / len(pts)
    k = sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x, y in pts)
    b = my - k * mx
    X = lambda n: 80 + (n - 10) * 13
    Y = lambda v: 260 - v * 68
    s.axes(80, 260, 530, 235, "n", "L/n, cm")
    for v in (1, 2, 3):
        s.line(80, Y(v), 590, Y(v), '#9aa4b2" stroke-opacity="0.28', 1).text(66, Y(v) + 5, str(v), MUTED, 14, "end")
    s.line(X(14), Y(b + k * 14), X(49), Y(b + k * 49), YELLOW, 1.8, "8 6")
    for n, v in pts:
        s.dot(X(n), Y(v), BLUE, 6).text(X(n), 282, str(n), MUTED, 13)
    s.text(X(24), Y(2.75), f"L/n ≈ {b:.2f} + {k:.4f}·n", YELLOW, 16)
    return s.svg()


# ---------- 8. Трение ----------
@fig
def fric_graph():
    s = S(640, 290, "Friction grows with the pull up to a maximum, then becomes kinetic friction")
    s.axes(80, 240, 500, 210, "F (pull)", "F_fr")
    s.path("M80,240 L280,60", BLUE, 3).path("M280,60 L300,95 L540,95", GREEN, 3).line(280, 60, 280, 240, MUTED, 1.4, "5 5")
    s.dot(280, 60, YELLOW, 5).text(300, 45, "breakaway", YELLOW, 15, "start")
    s.text(140, 140, "static: F_fr = F", BLUE, 16).text(430, 125, "sliding: μN", GREEN, 16)
    return s.svg()


# ---------- 9. Статика ----------
@fig
def mom_arm():
    s = S(640, 250, "Moment of a force: force, moment arm and angle")
    s.dot(90, 200, TEXT, 6).text(70, 222, "O", TEXT, 18).line(90, 200, 330, 80, BLUE, 4).arrow(330, 80, 520, 80, YELLOW)
    s.line(60, 80, 330, 80, MUTED, 1.5, "7 6").line(90, 200, 90, 80, GREEN, 3, "7 5")
    s.text(220, 165, "r", BLUE, 20, it=True).text(470, 65, "F", YELLOW, 20, it=True).text(62, 145, "d", GREEN, 20, it=True)
    s.path("M370,80 A40,40 0 0 0 366,62", ORANGE, 2).text(388, 60, "α", ORANGE, 18)
    s.text(430, 175, "M = F·r·sin α = F·d", TEXT, 20)
    return s.svg()


@fig
def st_box():
    s = S(640, 250, "Box by a wall on a pulley system: pulls of 30 and 15 newtons act on the box")
    s.ground(60, 520, 200).wall(50, 200, 540, False).rect(140, 80, 130, 120).text(205, 145, "box", BLUE)
    s.pulley(370, 100, 26).line(270, 100, 370, 100, TEXT)
    s.pulley(460, 165, 22).line(460, 165, 540, 165, TEXT)
    s.path("M270,187 L460,187 A22,22 0 0 0 460,143 L370,126 A26,26 0 0 1 370,74 L450,74", TEXT, 2)
    s.arrow(450, 74, 515, 74, YELLOW).text(485, 60, "F = 15 N", YELLOW, 15)
    s.arrow(270, 100, 330, 100, GREEN).text(305, 88, "2F", GREEN, 15).arrow(270, 187, 330, 187, GREEN).text(305, 177, "F", GREEN, 15)
    s.arrow(200, 196, 80, 196, RED).text(100, 178, "16 N", RED, 15).arrow(140, 110, 70, 110, ORANGE).text(100, 95, "f = ?", ORANGE, 16)
    s.force(205, 150, 205, 235, "Mg", RED).force(230, 200, 230, 45, "N", GREEN)
    s.force(370, 74, 425, 74, "F", ORANGE, -4, -9).force(370, 126, 424, 136, "F", ORANGE, -4, -9)
    s.force(370, 100, 322, 100, "", GREEN).text(325, 118, "2F", GREEN, 14)
    return s.svg()


@fig
def st_friction_pulley():
    s = S(580, 420, "A block held by friction and a movable pulley of mass half m carrying m, with all forces")
    s.ground(30, 290, 130).wall(130, 380, 290, False).rect(90, 80, 90, 50).text(115, 100, "M", BLUE)
    s.line(290, 130, 330, 108, MUTED, 2).pulley(330, 108, 22).line(180, 86, 330, 86, TEXT)
    s.path("M330,86 A22,22 0 0 1 352,108", TEXT, 2).line(352, 108, 352, 250, TEXT)
    s.pulley(352, 250, 30).path("M320,250 A32,32 0 0 1 384,250", TEXT, 2)
    s.line(320, 250, 320, 380, TEXT).ground(295, 350, 380).line(384, 250, 384, 320, TEXT)
    s.rect(364, 320, 40, 34, GREEN).text(384, 342, "m", GREEN)
    s.force(110, 128, 45, 128, "F_fr", RED, 0, -9, "middle")
    s.force(180, 86, 245, 86, "T", YELLOW, -4, -9)
    s.force(150, 105, 150, 35, "N", GREEN).force(150, 105, 150, 190, "Mg", ORANGE)
    s.force(352, 250, 352, 180, "T", YELLOW).force(320, 250, 320, 320, "mg", GREEN, -7, 0, "end")
    s.force(384, 250, 384, 290, "mg", GREEN).force(352, 258, 352, 356, "mg/2", ORANGE, -6, 6, "end")
    s.force(384, 320, 384, 294, "", GREEN).force(384, 354, 384, 405, "mg", RED)
    s.text(500, 150, "T = ?", YELLOW, 19)
    return s.svg()


@fig
def st_lever():
    s = S(640, 305, "Lever: left load through a movable pulley, right load attached directly")
    s.ground(50, 150, 35, True).line(80, 35, 80, 170, TEXT).path("M80,170 A25,25 0 0 0 130,170", TEXT, 2).line(130, 170, 130, 100, TEXT)
    s.pulley(105, 170, 25).line(105, 170, 105, 215, TEXT).rect(85, 215, 40, 36).text(105, 238, "m₁", BLUE, 15)
    s.rect(130, 88, 400, 12).support(430, 100).text(430, 150, "O", TEXT)
    s.line(530, 100, 530, 200, TEXT).rect(505, 200, 50, 40, GREEN).text(530, 226, "m₂", GREEN, 15)
    s.force(130, 100, 130, 130, "m_1g/2", YELLOW, 8, -2)
    s.arrow(555, 200, 555, 260, RED).text(590, 255, "m₂g", RED, 15)
    s.text(280, 78, "l", TEXT, 19, it=True).text(480, 78, "L − l", TEXT, 17, it=True)
    s.force(80, 170, 80, 125, "T", YELLOW, -7, 0, "end").force(130, 170, 130, 140, "T", YELLOW, 8, 8)
    s.force(105, 170, 105, 212, "m_1g", GREEN, 8, -8).force(105, 251, 105, 288, "m_1g", RED)
    s.force(105, 215, 105, 190, "", GREEN).force(430, 100, 430, 45, "N", GREEN, 8, 8)
    s.force(530, 100, 530, 150, "m_2g", ORANGE, -8, 0, "end").force(530, 200, 530, 168, "", ORANGE)
    return s.svg()


@fig
def st_rod():
    s = S(520, 270, "Rod on two strings with a load at a quarter of its length")
    s.ground(60, 440, 40, True).line(100, 40, 100, 130, TEXT).line(400, 40, 400, 130, TEXT).rect(90, 130, 320, 14)
    s.arrow(100, 130, 100, 75, YELLOW).arrow(400, 130, 400, 75, YELLOW).text(75, 90, "T_A", YELLOW, 16).text(428, 90, "T_B", YELLOW, 16)
    s.arrow(250, 137, 250, 215, RED).text(280, 205, "Mg", RED, 16).line(175, 144, 175, 175, TEXT).rect(155, 175, 40, 32).text(175, 197, "m", BLUE)
    s.arrow(175, 207, 175, 252, RED).text(148, 248, "mg", RED, 15)
    s.text(90, 165, "A", TEXT).text(412, 165, "B", TEXT).text(175, 120, "C: AC = L/4", MUTED, 14)
    s.force(175, 144, 175, 168, "", GREEN).force(175, 175, 175, 152, "", GREEN)
    return s.svg()


@fig
def st_seven():
    s = S(640, 330, "Uniform lever of seven divisions: weight, pull of a string from a movable pulley and pivot reaction")
    x = lambda i: 70 + i * 60
    s.rect(x(0), 110, 420, 14)
    for i in range(1, 7):
        s.line(x(i), 110, x(i), 124, MUTED, 1.5)
    s.line(x(0), 110, x(0), 55, TEXT).ground(40, 110, 55, True)
    s.pulley(470, 200, 38).line(x(6), 124, x(6), 200, TEXT).path("M430,200 A40,40 0 0 0 510,200", TEXT, 2)
    s.line(510, 200, 510, 55, TEXT).ground(480, 550, 55, True)
    s.line(470, 200, 470, 262, TEXT).rect(450, 262, 40, 32, BLUE).text(470, 284, "m", BLUE)
    s.support(x(4), 124).force(x(4), 124, x(4), 72, "N", GREEN, 8, 8)
    s.dot(x(3.5), 117, RED, 5).force(x(3.5), 117, x(3.5), 215, "Mg", RED, -8, 0, "end")
    s.force(x(6), 124, x(6), 170, "mg/2", YELLOW, -8, -4, "end").force(510, 200, 510, 154, "mg/2", YELLOW)
    s.force(470, 200, 470, 252, "mg", GREEN, 7, -4).force(470, 294, 470, 322, "mg", RED)
    s.text(x(3.75), 36, "ℓ/2", RED, 15).line(x(3.5), 45, x(4), 45, RED, 2).text(x(5), 36, "2ℓ", YELLOW, 15).line(x(4), 45, x(6), 45, YELLOW, 2)
    s.text(230, 272, "ℓ is one division; the left string is slack", MUTED, 14)
    return s.svg()


@fig
def st_two_masses():
    s = S(580, 310, "Light rod of length 3a with end loads on a string over a pulley, with all forces")
    s.ground(150, 260, 30, True).line(205, 30, 205, 70, TEXT).pulley(205, 70, 20)
    s.line(185, 70, 185, 125, TEXT).rect(165, 125, 40, 34, ORANGE).text(185, 148, "M", ORANGE)
    s.line(225, 70, 225, 210, TEXT).line(105, 210, 465, 210, BLUE, 5).dot(225, 210)
    s.circle(105, 210, 14).circle(465, 210, 14).text(72, 215, "m_1", BLUE).text(498, 215, "m_2", BLUE)
    s.text(165, 232, "a", TEXT, 18, it=True).text(345, 232, "2a", TEXT, 18, it=True).text(245, 232, "O_1", TEXT, 15)
    s.force(105, 210, 105, 280, "m_1g", RED).force(465, 210, 465, 270, "m_2g", RED, -8, 0, "end")
    s.force(225, 210, 225, 150, "Mg", YELLOW)
    s.force(185, 125, 185, 95, "Mg", YELLOW, -8, 6, "end").force(185, 159, 185, 205, "Mg", RED, -8, -14, "end")
    s.force(185, 70, 185, 102, "", YELLOW).force(225, 70, 225, 112, "Mg", YELLOW).force(205, 70, 205, 35, "2Mg", GREEN, 24, 12)
    return s.svg()


@fig
def st_table():
    s = S(760, 250, "A board overhanging a table by a third, and a beam on a platform overhanging by 0.2, with all forces")
    s.text(190, 26, "a third overhangs", MUTED, 15).text(565, 26, "0.2 of the beam overhangs", MUTED, 15)
    s.rect(50, 130, 190, 14, MUTED).line(70, 144, 70, 225, TEXT, 4).line(215, 144, 215, 225, TEXT, 4)
    s.rect(120, 114, 180, 14).dot(240, 128, YELLOW).text(262, 150, "edge", MUTED, 13, "start")
    s.dot(210, 121, RED, 5).force(210, 121, 210, 195, "mg", RED, -7, 0, "end")
    s.force(240, 128, 240, 50, "N", GREEN).force(300, 121, 300, 190, "F", YELLOW)
    s.ground(420, 650, 150).rect(450, 132, 250, 16).dot(450, 148, YELLOW, 5).text(450, 185, "O", YELLOW)
    s.force(575, 140, 575, 215, "mg", RED).force(700, 132, 700, 55, "F", GREEN)
    s.force(450, 148, 450, 85, "N", GREEN)
    return s.svg()


@fig
def st_sand():
    s = S(580, 290, "Board on two supports at the moment of lift-off, with all forces")
    s.rect(80, 100, 390, 14).support(210, 114).support(470, 114).text(185, 160, "O", TEXT)
    s.line(80, 114, 80, 180, TEXT).rect(55, 180, 50, 40, ORANGE).text(80, 206, "m(t)", ORANGE, 15)
    s.force(80, 114, 80, 160, "mg", ORANGE).force(80, 180, 80, 135, "", ORANGE).force(80, 220, 80, 270, "mg", RED)
    s.dot(275, 107, RED, 5).force(275, 107, 275, 195, "Mg", RED)
    s.force(210, 114, 210, 40, "N_O = (M+m)g", GREEN, 8, 6)
    s.text(145, 90, "L/3", TEXT, 16).text(243, 90, "L/6", MUTED, 15).text(470, 85, "N → 0", GREEN, 16)
    return s.svg()


# ---------- 10. Импульс ----------
@fig
def mom_system():
    s = S(640, 270, "A system of particles with internal and external forces")
    s.path("M120,60 C300,0 520,40 530,150 C540,250 300,260 180,215 C80,180 40,95 120,60z", MUTED, 1.6, CELL, .45, "8 6")
    a, b, c = (200, 110), (360, 160), (320, 70)
    s.arrow(a[0], a[1], a[0] + 62, a[1] + 19, GREEN).arrow(b[0], b[1], b[0] - 62, b[1] - 19, GREEN)
    for x, y in (a, b, c, (440, 100), (230, 190)):
        s.circle(x, y, 11)
    s.arrow(200, 110, 70, 135, YELLOW).arrow(440, 100, 590, 60, YELLOW)
    s.text(185, 92, "1", TEXT).text(380, 185, "2", TEXT).text(255, 142, "F₁₂", GREEN, 15).text(315, 128, "F₂₁", GREEN, 15)
    s.text(70, 165, "F₁ ext", YELLOW, 15).text(580, 95, "Fᵢ ext", YELLOW, 15)
    return s.svg()


@fig
def mom_center():
    s = S(640, 220, "Centre of mass of loads on a light rod as the balance point")
    s.rect(60, 100, 500, 12)
    xs = [(110, 12), (180, 14), (250, 17), (330, 14), (400, 12), (480, 11)]
    for i, (x, r) in enumerate(xs, 1):
        s.circle(x, 100 - r, r).text(x, 55, f"m{'₁₂₃₄₅₆'[i-1]}", BLUE, 15)
    xc = sum(x * r * r for x, r in xs) / sum(r * r for x, r in xs)
    s.support(xc, 112).arrow(xc, 112, xc, 190, RED).text(xc + 40, 188, "Mg", RED).text(xc - 30, 160, "x_C", YELLOW, 18)
    s.arrow(60, 205, 600, 205, MUTED, 2).text(600, 192, "x", MUTED, 15, "middle", True)
    return s.svg()
