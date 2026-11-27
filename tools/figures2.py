"""Чертежи к задачам и примерам из тетради (дополнение к figures.py)."""
import math

from figures import BLUE, CELL, GREEN, MUTED, ORANGE, RED, TEXT, VIOLET, YELLOW, F, S, fig


def box(s, cx, y, label, c=BLUE, w=46, h=36):
    s.rect(cx - w / 2, y, w, h, c)
    return s.text(cx, y + h / 2 + 6, label, c, 16)


def curve(s, X, Y, f, a, b, c=BLUE, w=3, n=120):
    pts = [(a + (b - a) * i / n) for i in range(n + 1)]
    return s.path("M" + " L".join(f"{X(t):.1f},{Y(f(t)):.1f}" for t in pts), c, w)


# ================= 1. Векторы =================
@fig
def vec_scalar():
    s = S(700, 170, "Multiplying a vector by a number: stretching and reversing")
    s.arrow(40, 110, 150, 70, BLUE).text(90, 75, "a", BLUE, 19, it=True)
    s.arrow(220, 130, 440, 50, GREEN).text(310, 70, "2a", GREEN, 19, it=True)
    s.arrow(620, 60, 510, 100, RED).text(560, 65, "−1·a", RED, 19, it=True)
    s.text(95, 150, "original", MUTED, 15).text(330, 155, "λ &gt; 0: same way", MUTED, 15).text(570, 135, "λ &lt; 0: reversed", MUTED, 15)
    return s.svg()


@fig
def vec_order():
    s = S(560, 340, "The vector sum on grid paper does not depend on order: 6 squares right and 8 up")
    k, ox, oy = 30, 90, 300
    for i in range(13):
        s.line(ox + i * k, 20, ox + i * k, oy + 20, '#9aa4b2" stroke-opacity="0.28', 1)
    for j in range(10):
        s.line(ox - 20, oy - j * k, ox + 12 * k, oy - j * k, '#9aa4b2" stroke-opacity="0.28', 1)
    P = lambda x, y: (ox + x * k, oy - y * k)
    s.arrow(*P(0, 0), *P(4, 2), BLUE).arrow(*P(4, 2), *P(6, 8), GREEN)
    s.arrow(*P(0, 0), *P(2, 6), GREEN, 2, "7 5").arrow(*P(2, 6), *P(6, 8), BLUE, 2, "7 5")
    s.arrow(*P(0, 0), *P(6, 8), YELLOW)
    s.text(185, 285, "a", BLUE, 19, it=True).text(260, 170, "b", GREEN, 19, it=True).text(100, 190, "b", GREEN, 19, it=True)
    s.text(400, 80, "a + b = b + a", YELLOW, 18).text(430, 110, "6 right, 8 up", MUTED, 15)
    return s.svg()


@fig
def vec_combo():
    s = S(700, 300, "Building the sum of five vectors a and three vectors b, and also minus a minus two b")
    x, y = 50, 250
    for _ in range(5):
        s.arrow(x, y, x + 34, y - 36, BLUE)
        x, y = x + 34, y - 36
    for _ in range(3):
        s.arrow(x, y, x + 62, y + 28, GREEN)
        x, y = x + 62, y + 28
    s.arrow(50, 250, x, y, YELLOW, 2, "8 6").text(265, 232, "5a + 3b", YELLOW, 18)
    s.arrow(650, 220, 616, 256, BLUE).arrow(616, 256, 554, 228, GREEN).arrow(554, 228, 492, 200, GREEN)
    s.arrow(650, 220, 492, 200, YELLOW, 2, "8 6").text(580, 180, "−a − 2b", YELLOW, 18)
    s.text(662, 255, "−a", BLUE, 16).text(560, 262, "−b", GREEN, 16).text(80, 190, "a", BLUE, 18, it=True).text(325, 70, "b", GREEN, 18, it=True)
    return s.svg()


@fig
def vec_signs():
    s = S(720, 260, "Six vectors with different projection signs")
    s.axes(50, 220, 60, 60, "x", "y")
    data = [("a", 150, 150, 215, 80, "+ +"), ("b", 310, 150, 255, 85, "− +"), ("c", 370, 160, 370, 70, "0 +"),
            ("d", 430, 80, 490, 150, "+ −"), ("e", 590, 80, 535, 150, "− −"), ("f", 610, 115, 695, 115, "+ 0")]
    for n, x1, y1, x2, y2, sg in data:
        s.arrow(x1, y1, x2, y2, BLUE)
        cx = (x1 + x2) / 2
        s.text(cx - 14, (y1 + y2) / 2 - 8, n, YELLOW, 19, it=True).text(cx, 195, sg, GREEN, 18)
    s.text(420, 235, "signs of projections: (a_x, a_y)", MUTED, 15)
    return s.svg()


@fig
def vec_polygon():
    s = S(520, 270, "A closed chain of five vectors has zero sum")
    p = [(380, 190), (460, 90), (300, 60), (150, 110), (230, 225)]
    cols = [BLUE, GREEN, ORANGE, VIOLET, RED]
    lab = [(448, 150), (385, 62), (215, 70), (165, 180), (305, 232)]
    for i in range(5):
        (x1, y1), (x2, y2) = p[i], p[(i + 1) % 5]
        s.arrow(x1, y1, x2, y2, cols[i])
        s.text(*lab[i], f"v_{i+1}", cols[i], 17)
    s.text(300, 150, "Σ v = 0", YELLOW, 21).dot(380, 190, YELLOW, 5)
    return s.svg()


# ================= 2. Кинематика =================
@fig
def kin_tangent():
    s = S(640, 300, "Instantaneous speed as the tangent slope, average speed as the secant slope")
    s.axes(70, 250, 520, 220, "t", "S")
    X = lambda t: 70 + t * 100
    f = lambda t: 30 * t + 15 * math.sin(1.6 * t)
    Y = lambda v: 250 - v * 1.25
    curve(s, X, Y, f, 0, 4.8)
    t = 2.0
    d = 30 + 15 * 1.6 * math.cos(1.6 * t)
    s.line(X(t - 1), Y(f(t) - d), X(t + 1.6), Y(f(t) + 1.6 * d), GREEN, 2.4).dot(X(t), Y(f(t)), GREEN, 5)
    s.line(X(0), Y(0), X(4.5), Y(f(4.5)), YELLOW, 1.8, "8 6")
    s.text(430, 225, "green is the tangent: v", GREEN, 16).text(430, 200, "yellow is the secant: ⟨v⟩", YELLOW, 16)
    return s.svg()


@fig
def kin_dx():
    s = S(640, 250, "A displacement graph may go negative")
    s.axes(70, 130, 520, 110, "t", "d_x", 100)
    X = lambda t: 70 + t * 80
    curve(s, X, lambda v: 130 - v, lambda t: 80 * math.sin(t) * (1 - t / 14), 0, 5.8)
    s.text(X(1.5), 30, "d_x &gt; 0", GREEN, 16).text(X(4.6), 232, "d_x &lt; 0", RED, 16).text(X(4.1), 55, "slope &lt; 0 ⇒ v_x &lt; 0", MUTED, 16)
    return s.svg()


@fig
def kin_convert():
    s = S(760, 500, "From the position graph we get distance, speed and velocity component")
    x = lambda t: 9 * t - 4.2 * t * t + .55 * t ** 3
    v = lambda t: 9 - 8.4 * t + 1.65 * t * t
    T, n = 5.2, 400
    ts = [T * i / n for i in range(n + 1)]
    path = [0]
    for i in range(1, n + 1):
        path.append(path[-1] + abs(x(ts[i]) - x(ts[i - 1])))
    panels = [("x", [x(t) for t in ts], 50, 190, 130, 60, BLUE, "position x(t)"),
              ("d", path, 430, 190, 140, 0, GREEN, "distance d(t): only grows"),
              ("|v|", [abs(v(t)) for t in ts], 50, 440, 140, 0, ORANGE, "speed v(t)"),
              ("v_x", [v(t) for t in ts], 430, 370, 90, 80, YELLOW, "velocity component v_x(t)")]
    for name, vals, x0, y0, up, below, c, title in panels:
        hi = max(max(vals), 1e-9)
        lo = max(-min(vals), 1e-9)
        k = min(up / hi, (below / lo) if below else up / hi)
        s.axes(x0, y0, 290, up + 15, "t", name, below)
        s.path("M" + " L".join(f"{x0+t*52:.1f},{y0-u*k:.1f}" for t, u in zip(ts, vals)), c, 3)
        s.text(x0 + 165, 245 if y0 < 200 else 482, title, c, 15)
    roots = [(8.4 - math.sqrt(8.4 ** 2 - 4 * 1.65 * 9)) / 3.3, (8.4 + math.sqrt(8.4 ** 2 - 4 * 1.65 * 9)) / 3.3]
    for t in roots:
        for x0, y1, y2 in ((50, 50, 190), (430, 50, 190), (50, 290, 440), (430, 290, 440)):
            s.line(x0 + t * 52, y1, x0 + t * 52, y2, MUTED, 1, "3 6")
    return s.svg()


@fig
def kin_ex42():
    s = S(760, 500, "Problem 4.2: graphs of position, distance, average speed and speed versus position")
    s.axes(60, 200, 270, 165, "t, s", "x, m")
    X = lambda t: 60 + t * 60
    Y = lambda v: 200 - v * 25
    s.path(f"M{X(0)},{Y(0)} L{X(1)},{Y(4)} L{X(2)},{Y(4)} L{X(3)},{Y(2)}", BLUE)
    s.axes(450, 200, 270, 165, "t, s", "S, m")
    X2 = lambda t: 450 + t * 60
    s.path(f"M{X2(0)},{Y(0)} L{X2(1)},{Y(4)} L{X2(2)},{Y(4)} L{X2(3)},{Y(6)}", GREEN)
    s.axes(60, 440, 270, 165, "t, s", "⟨v⟩")
    Y3 = lambda v: 440 - v * 30
    s.line(X(0), Y3(4), X(1), Y3(4), YELLOW, 3)
    curve(s, X, Y3, lambda t: 4 / t, 1, 2, YELLOW)
    s.line(X(2), Y3(2), X(3), Y3(2), YELLOW, 3)
    s.axes(450, 440, 270, 165, "x, m", "v, m/s")
    X4 = lambda v: 450 + v * 55
    s.arrow(X4(0), Y3(4), X4(4), Y3(4), ORANGE).arrow(X4(4), Y3(2), X4(2), Y3(2), RED)
    s.text(X4(2), Y3(4) - 12, "forward, 4 m/s", ORANGE, 15).text(X4(3), Y3(2) + 24, "back, 2 m/s", RED, 15)
    for x0, y0, nx, step, ys, ky in ((60, 200, 3, 60, (2, 4), 25), (450, 200, 3, 60, (4, 6), 25), (60, 440, 3, 60, (2, 4), 30), (450, 440, 4, 55, (2, 4), 30)):
        for i in range(1, nx + 1):
            s.text(x0 + i * step, y0 + 20, str(i), MUTED, 13)
        for v in ys:
            s.text(x0 - 10, y0 - v * ky + 5, str(v), MUTED, 13, "end")
    return s.svg()


@fig
def kin_vx_uniform():
    s = S(640, 200, "Uniform motion: the graph of speed versus position is horizontal")
    s.arrow(40, 160, 600, 160, MUTED, 2).arrow(320, 175, 320, 20, MUTED, 2)
    for i in range(-4, 5):
        s.text(320 + i * 60, 182, str(i), MUTED, 13)
    s.line(80, 60, 560, 60, ORANGE, 3).text(332, 52, "4", MUTED, 14, "start").text(450, 45, "v = const", ORANGE, 16)
    s.text(600, 145, "x", MUTED, 16, it=True).text(300, 30, "v", MUTED, 16, it=True)
    return s.svg()


# ================= 3. Ускорение =================
@fig
def acc_axis():
    s = S(640, 130, "One-dimensional motion: initial position, velocity and acceleration")
    s.arrow(40, 80, 600, 80, MUTED, 2).line(80, 68, 80, 92, TEXT).text(80, 116, "0", MUTED).text(600, 108, "x", MUTED, 16, it=True)
    s.dot(220, 80, BLUE, 7).text(220, 116, "x_0", BLUE).arrow(220, 62, 330, 62, GREEN).text(280, 45, "v_0", GREEN).arrow(370, 62, 450, 62, ORANGE).text(410, 45, "a", ORANGE, 18, it=True)
    return s.svg()


@fig
def acc_cases():
    s = S(760, 260, "Position graphs at positive acceleration and different signs of initial velocity")
    s.axes(60, 190, 270, 160, "t", "x")
    curve(s, lambda t: 60 + t * 80, lambda v: 190 - v * 14, lambda t: 1.2 * t + t * t, 0, 2.7, BLUE)
    s.text(190, 240, "v_0 &gt; 0, a &gt; 0", BLUE, 16)
    s.axes(440, 160, 270, 130, "t", "x", 70)
    curve(s, lambda t: 440 + t * 70, lambda v: 160 - v * 17, lambda t: -4 * t + 1.6 * t * t, 0, 3.4, ORANGE)
    s.line(527, 160, 527, 203, MUTED, 1.4, "5 5").text(590, 245, "v_0 &lt; 0, a &gt; 0: turns back", ORANGE, 16)
    return s.svg()


@fig
def acc_brake():
    s = S(700, 175, "Braking over 100 metres: 10 metres per second at the midpoint, zero at the end")
    s.ground(40, 660, 120)
    for x, t, c in ((90, "v_0 = ?", GREEN), (340, "10 m/s", YELLOW), (590, "0", RED)):
        s.line(x, 70, x, 120, MUTED, 1.5, "5 5").text(x, 55, t, c, 18).dot(x, 120, c, 6)
    s.arrow(215, 90, 150, 90, ORANGE).text(190, 80, "a", ORANGE, 17, it=True)
    s.line(90, 145, 590, 145, TEXT, 1.5).text(340, 167, "S = 100 m", TEXT, 16)
    return s.svg()


@fig
def acc_v2():
    s = S(560, 260, "Speed squared grows linearly with displacement")
    s.axes(80, 220, 430, 190, "d", "v²")
    s.line(80, 190, 470, 50, BLUE, 3).dot(80, 190, GREEN, 5).text(62, 196, "v_0²", GREEN, 16, "end")
    s.text(340, 150, "v² = v_0² + 2ad", TEXT, 19).text(310, 195, "slope equals 2a", MUTED, 15)
    return s.svg()


@fig
def acc_slope():
    s = S(640, 280, "A rolling ball covers segments 1, 3 and 5 in equal times")
    s.line(60, 50, 600, 230, TEXT, 3).circle(75, 40, 15, ORANGE)
    P = lambda u: (75 + u * 54, 55 + u * 18)
    for a, b, c, lab in ((0, 1, BLUE, "S_1"), (1, 4, GREEN, "3S_1"), (4, 9, YELLOW, "5S_1")):
        (x1, y1), (x2, y2) = P(a), P(b)
        s.line(x1, y1 + 18, x2, y2 + 18, c, 5).dot(x2, y2, c, 5)
        s.text((x1 + x2) / 2 - 20, (y1 + y2) / 2 + 52, lab, c, 17)
    return s.svg()


@fig
def acc_two():
    s = S(600, 290, "Two-stage acceleration: area under the graph")
    s.axes(80, 240, 470, 210, "t", "v")
    s.path("M80,240 L250,110 L250,240 z", BLUE, 1.5, BLUE, .25).path("M250,240 L250,110 L470,110 L470,240 z", GREEN, 1.5, GREEN, .22)
    s.path("M250,110 L470,50 L470,110 z", ORANGE, 1.5, ORANGE, .3).path("M80,240 L250,110 L470,50", TEXT, 3)
    s.text(195, 215, "a_1t_1²/2", BLUE, 16).text(360, 185, "a_1t_1·t_2", GREEN, 16).text(415, 100, "a_2t_2²/2", ORANGE, 14)
    s.text(250, 265, "t_1", MUTED).text(470, 265, "t_1 + t_2", MUTED).text(62, 115, "v_1", MUTED)
    return s.svg()


@fig
def acc_lab():
    s = S(640, 240, "Setup: a body on an incline 125 centimetres long")
    s.path("M80,200 L560,200 L560,60 z", MUTED, 2, CELL)
    s.circle(525, 52, 16, ORANGE).arrow(480, 66, 400, 90, GREEN).text(440, 62, "a", GREEN, 18, it=True)
    s.text(300, 112, "L = 125 cm", TEXT, 17).text(590, 135, "h", BLUE, 19, it=True)
    s.path("M150,200 A70,70 0 0 0 147,180", YELLOW, 2).text(172, 192, "φ", YELLOW, 18)
    return s.svg()


# ================= 4. Масса и плотность =================
def iso(s, x, y, a, c=BLUE):
    d = a * .45
    s.path(f"M{x},{y} h{a} v{a} h{-a}z", c, 2, CELL)
    s.path(f"M{x},{y} l{d},{-d} h{a} l{-d},{d}z", c, 2, CELL)
    return s.path(f"M{x+a},{y} l{d},{-d} v{a} l{-d},{d}z", c, 2, CELL)


@fig
def dens_volumes():
    s = S(720, 240, "Cylinder, cone and sphere with volume formulas")
    s.path("M80,60 v110 a50,16 0 0 0 100,0 v-110", BLUE, 2.5, CELL).path("M80,60 a50,16 0 1 0 100,0 a50,16 0 1 0 -100,0", BLUE, 2.5, CELL)
    s.line(130, 60, 180, 60, YELLOW).text(155, 55, "R", YELLOW, 15).text(65, 120, "H", GREEN).text(130, 220, "V = πR²H", TEXT, 18)
    s.path("M310,170 L360,40 L410,170", GREEN, 2.5, CELL).path("M310,170 a50,16 0 1 0 100,0 a50,16 0 1 0 -100,0", GREEN, 2.5)
    s.line(360, 170, 410, 170, YELLOW).text(385, 164, "R", YELLOW, 15).line(360, 40, 360, 170, MUTED, 1.4, "5 5").text(345, 120, "H", GREEN)
    s.text(360, 220, "V = πR²H / 3", TEXT, 18)
    s.circle(590, 110, 65, ORANGE).path("M525,110 a65,18 0 0 0 130,0", ORANGE, 1.5).line(590, 110, 655, 110, YELLOW).text(622, 100, "R", YELLOW, 15)
    s.text(590, 220, "V = 4πR³ / 3", TEXT, 18)
    return s.svg()


@fig
def dens_rods():
    s = S(680, 180, "Rods of equal mass and cross-section: aluminium is almost 2.9 times longer than iron")
    for y, w, c, n in ((50, 170, ORANGE, "iron"), (125, 491, BLUE, "aluminium: 2.9 times longer")):
        s.rect(80, y - 18, w, 36, c).circle(80 + w, y, 18, c)
        s.text(80 + w / 2, y + 6, n, c, 16)
    s.text(450, 55, "both have mass m", MUTED, 16)
    return s.svg()


@fig
def dens_jar():
    s = S(680, 220, "A full jar minus an empty jar gives the mass of jam")
    for x, full, lab in ((110, True, "3.9 kg"), (340, False, "400 g")):
        s.rect(x - 50, 60, 100, 100, BLUE).rect(x - 56, 44, 112, 18, MUTED)
        if full:
            s.path(f"M{x-48},82 q12,-8 24,0 t24,0 t24,0 t24,0 V158 H{x-48}z", RED, 1.5, RED, .35)
        s.text(x, 195, lab, TEXT, 18)
    s.text(225, 115, "−", YELLOW, 30).text(455, 115, "=", YELLOW, 30)
    s.path("M510,90 q12,-8 24,0 t24,0 t24,0 t24,0 t24,0 V160 H510z", RED, 2, RED, .35)
    s.text(570, 195, "3.5 kg of jam (3 L)", RED, 17)
    return s.svg()


@fig
def dens_truck():
    s = S(560, 220, "A truck body 2 by 1.5 by 1.8 metres is unloaded at 20 kilograms per minute")
    s.path("M80,80 h200 v100 h-200z", BLUE, 2.5, CELL).path("M80,80 l60,-45 h200 l-60,45 z", BLUE, 2.5, CELL).path("M280,80 l60,-45 v100 l-60,45 z", BLUE, 2.5, CELL)
    s.text(180, 202, "2 m", TEXT).text(345, 178, "1.5 m", TEXT, 16).text(48, 135, "1.8 m", TEXT, 16)
    s.arrow(360, 100, 440, 100, ORANGE).text(455, 80, "20 kg/min", ORANGE, 17).text(455, 135, "216 min", YELLOW, 19)
    return s.svg()


@fig
def dens_hollow():
    s = S(520, 250, "A hollow cube with a 6 centimetre edge and 2 millimetre walls")
    iso(s, 110, 90, 120)
    s.path("M124,104 h92 v92 h-92z", ORANGE, 2, "none", 1, "6 5")
    s.text(170, 232, "6 cm", TEXT).text(170, 155, "cavity 5.6", ORANGE, 14).text(400, 120, "216 cm² = 6a²", MUTED, 16).text(400, 155, "wall 2 mm", ORANGE, 16)
    return s.svg()


@fig
def dens_corner():
    s = S(520, 260, "A cube with a half-edge cube cut from its corner")
    P = lambda x, y, z: (130 + x * 140 + z * 62, 230 - y * 140 - z * 62)

    def face(pts, c=BLUE):
        s.path("M" + " L".join(f"{a:.0f},{b:.0f}" for a, b in (P(*p) for p in pts)) + "z", c, 2.2, CELL)
    h = .5
    face([(0, 0, 0), (1, 0, 0), (1, h, 0), (h, h, 0), (h, 1, 0), (0, 1, 0)])
    face([(1, 0, 0), (1, 0, 1), (1, 1, 1), (1, 1, h), (1, h, h), (1, h, 0)])
    face([(0, 1, 0), (h, 1, 0), (h, 1, h), (1, 1, h), (1, 1, 1), (0, 1, 1)])
    face([(h, h, 0), (1, h, 0), (1, h, h), (h, h, h)], ORANGE)
    face([(h, h, 0), (h, 1, 0), (h, 1, h), (h, h, h)], ORANGE)
    face([(h, h, h), (1, h, h), (1, 1, h), (h, 1, h)], ORANGE)
    s.text(200, 252, "a", TEXT, 18, it=True).text(425, 120, "cut out: a/2", ORANGE, 16).text(430, 160, "m = ⅞ρa³", YELLOW, 19)
    return s.svg()


@fig
def dens_holes():
    s = S(520, 270, "A three by three by three cube with through holes: seven small cubes removed")
    a = 60
    x, y = 110, 90
    iso(s, x, y, 180)
    for i in (1, 2):
        s.line(x + i * a, y, x + i * a, y + 180, BLUE, 1.5).line(x, y + i * a, x + 180, y + i * a, BLUE, 1.5)
        s.line(x + i * a, y, x + i * a + 81, y - 81, BLUE, 1.5)
        s.line(x + i * 27, y - i * 27, x + 180 + i * 27, y - i * 27, BLUE, 1.5)
    s.rect(x + a, y + a, a, a, ORANGE, '#9aa4b2" fill-opacity="0.65', 0)
    s.text(430, 130, "27 − 7 = 20", YELLOW, 20).text(430, 165, "M = 20m", TEXT, 19)
    return s.svg()


@fig
def dens_scale():
    s = S(640, 235, "A one to five scale model has 125 times less volume")
    iso(s, 80, 150, 32, ORANGE)
    iso(s, 330, 65, 125, MUTED)
    s.text(100, 215, "birch, 100 g", ORANGE, 16).text(400, 220, "iron, 150 kg", TEXT, 16)
    s.arrow(160, 160, 300, 125, YELLOW).text(215, 110, "lengths ×5", YELLOW, 16).text(225, 185, "volume ×125", YELLOW, 16)
    return s.svg()


@fig
def dens_heat():
    s = S(560, 225, "Heating makes every size grow by two percent and volume by six percent")
    iso(s, 80, 85, 90)
    iso(s, 330, 75, 104, RED)
    s.arrow(230, 125, 300, 125, YELLOW).text(125, 207, "a, ρ", BLUE, 18).text(385, 207, "1.02a, ρ/1.06", RED, 18)
    return s.svg()


@fig
def dens_coin():
    s = S(640, 195, "Cross-section of a coin: thicker at the rim than in the middle")
    s.path("M120,70 H160 L175,85 H465 L480,70 H520 V130 H480 L465,115 H175 L160,130 H120 Z", ORANGE, 2.5, CELL)
    s.line(120, 160, 520, 160, TEXT, 1.5).text(320, 183, "D = 25.75 mm", TEXT, 16)
    s.line(545, 70, 545, 130, GREEN, 2).text(590, 105, "h = 2.2", GREEN, 16)
    s.text(320, 50, "middle is thinner than the rim", MUTED, 15)
    return s.svg()


@fig
def dens_gold():
    s = S(560, 220, "A gold cube with an edge of about forty centimetres next to a person")
    s.ground(60, 500, 190)
    s.circle(140, 45, 18, MUTED).path("M140,63 V130 M140,80 L110,115 M140,80 L170,115 M140,130 L118,188 M140,130 L162,188", MUTED, 3)
    iso(s, 300, 140, 50, YELLOW)
    s.text(440, 100, "≈ 1216 kg", YELLOW, 19).text(440, 130, "edge ≈ 40 cm", TEXT, 16)
    return s.svg()


# ================= 5. Законы Ньютона =================
@fig
def newt_wagon():
    s = S(640, 220, "Inside a uniformly moving carriage the motion cannot be detected")
    s.ground(40, 600, 180).rect(150, 60, 260, 100, BLUE).circle(200, 166, 14).circle(360, 166, 14)
    s.circle(260, 95, 11, MUTED).path("M260,106 V135 M260,135 L248,158 M260,135 L272,158 M245,118 H275", MUTED, 2.5)
    s.line(380, 60, 380, 20, TEXT).path("M380,20 L415,30 L380,40z", RED, 2, RED, .5)
    s.arrow(430, 110, 540, 110, GREEN).text(500, 95, "v = const", GREEN, 17)
    return s.svg()


@fig
def newt_frame():
    s = S(640, 250, "Reference frame: reference body, coordinate system and clock")
    s.axes(150, 180, 170, 140, "x", "y")
    s.arrow(150, 180, 90, 215, MUTED, 2).circle(150, 180, 14, ORANGE).text(110, 238, "1. reference body", ORANGE, 15, "start")
    s.text(260, 90, "2. coordinates", TEXT, 16)
    s.circle(500, 100, 55, BLUE).line(500, 100, 500, 62, TEXT, 3).line(500, 100, 528, 112, TEXT, 3).dot(500, 100)
    s.text(500, 190, "3. clock (time)", BLUE, 16)
    return s.svg()


@fig
def newt_first_second():
    s = S(720, 200, "First law: no force, constant velocity. Second law: a force produces acceleration")
    s.ground(40, 330, 130).rect(80, 85, 60, 45).arrow(150, 108, 260, 108, GREEN).text(205, 90, "v = const", GREEN, 16)
    s.text(180, 175, "ΣF = 0", TEXT, 19)
    s.ground(390, 690, 130).rect(430, 75, 80, 55, BLUE).text(470, 108, "m", BLUE)
    s.arrow(510, 102, 620, 102, YELLOW).text(590, 90, "F", YELLOW, 19, it=True).arrow(430, 55, 500, 55, ORANGE).text(515, 52, "a", ORANGE, 18, it=True)
    s.text(540, 175, "F = ma", TEXT, 19)
    return s.svg()


@fig
def newt_nature():
    s = S(760, 290, "Four kinds of interaction")
    s.text(380, 35, "nature of the interaction", TEXT, 19)
    for x, n, c in ((90, "gravitational", BLUE), (290, "electromagnetic", GREEN), (490, "weak", ORANGE), (660, "strong", RED)):
        s.arrow(380 + (x - 380) * .3, 48, x, 92, c, 2).text(x, 115, n, c, 16)
    s.circle(65, 190, 34, BLUE).circle(155, 190, 10, BLUE).arrow(102, 190, 122, 190, YELLOW).arrow(142, 190, 124, 190, YELLOW)
    s.text(95, 255, "weight force mg", MUTED, 15)
    for i, t in enumerate(("friction F_fr", "normal force N", "tension T", "elastic force F_el")):
        s.text(290, 160 + 30 * i, t, TEXT, 16)
    s.text(490, 190, "particle decays", MUTED, 15)
    s.circle(660, 190, 38, RED).circle(647, 178, 13, ORANGE).text(647, 183, "p", ORANGE, 14).circle(675, 185, 13, MUTED).text(675, 190, "n", MUTED, 14).circle(655, 205, 13, ORANGE).text(655, 210, "p", ORANGE, 14)
    s.text(660, 255, "nuclear forces", MUTED, 15)
    return s.svg()


@fig
def newt_planet():
    s = S(640, 250, "The planet pulls the body, and the body pulls the planet with an equal force")
    s.circle(200, 140, 90, BLUE).rect(188, 32, 24, 18, ORANGE)
    s.arrow(200, 41, 200, 90, RED).arrow(200, 140, 200, 98, GREEN).text(232, 80, "mg", RED, 16).text(232, 125, "mg", GREEN, 16)
    s.text(470, 100, "g_Earth ≈ 9.81 N/kg", TEXT, 18).text(470, 140, "g_Moon ≈ 1.6 N/kg", MUTED, 18)
    return s.svg()


@fig
def newt_string():
    s = S(720, 200, "A taut string pulls the body, a slack string exerts no force")
    s.ground(40, 330, 140).rect(70, 90, 70, 50).line(140, 112, 290, 70, TEXT).arrow(140, 112, 220, 89, YELLOW).text(205, 75, "T", YELLOW, 19)
    s.text(180, 180, "taut: T along the string", TEXT, 16)
    s.ground(390, 690, 140).rect(420, 90, 70, 50).path("M490,112 C530,160 570,60 640,100", TEXT, 2).text(540, 180, "slack: T = 0", TEXT, 16)
    return s.svg()


# ================= 6. Блоки =================
@fig
def tens_wall():
    s = S(640, 120, "A string fixed to a wall is pulled at the other end with force F")
    s.wall(25, 100, 80).line(80, 65, 450, 65, TEXT).dot(450, 65).arrow(450, 65, 560, 65, YELLOW).arrow(450, 65, 360, 65, GREEN, 4)
    s.text(525, 45, "F", YELLOW, 19, it=True).text(395, 45, "T = F", GREEN, 18)
    return s.svg()


@fig
def tens_heavy():
    s = S(680, 280, "Tension in a heavy string grows with height")
    s.ground(60, 220, 30, True).line(140, 30, 140, 185, TEXT, 3).rect(110, 185, 60, 50).text(140, 216, "m", BLUE)
    s.dot(140, 110, YELLOW, 5).arrow(140, 110, 140, 65, YELLOW).text(175, 75, "T(x)", YELLOW, 17)
    s.line(85, 110, 85, 185, MUTED, 1.5).text(68, 155, "x", MUTED, 18, it=True).text(190, 140, "M, L", MUTED, 16).arrow(140, 235, 140, 275, RED).text(170, 268, "mg", RED, 15)
    s.axes(390, 230, 230, 170, "x", "T")
    s.line(390, 180, 590, 90, GREEN, 3).text(372, 185, "mg", MUTED, 14, "end").line(590, 230, 590, 90, MUTED, 1.2, "5 5").text(590, 252, "L", MUTED)
    s.text(500, 40, "T = mg + (Mg/L)·x", TEXT, 17).text(605, 80, "(M+m)g", MUTED, 14)
    return s.svg()


@fig
def tens_frictionless():
    s = S(440, 220, "With a frictionless pulley the tension is equal on both sides")
    s.pulley(250, 80, 40).line(222, 52, 90, 160, TEXT).line(290, 80, 290, 180, TEXT)
    s.arrow(160, 103, 95, 156, YELLOW).arrow(290, 110, 290, 185, YELLOW)
    s.text(105, 125, "T_1", YELLOW, 18).text(318, 160, "T_2", YELLOW, 18).text(200, 205, "T_1 = T_2", TEXT, 19)
    return s.svg()


def zigzag(label, kinds, end, loads=None, tens=None, start=None, platform=None, h=480, d=84):
    """Одна нить: вертикальные участки, соединённые подвижными ('m') и неподвижными ('f') блоками.

    start: None — левый конец на потолке, иначе подпись груза на левом конце.
    end: 'c' потолок, 'p' платформа, 'F' свободный конец с силой, иначе подпись груза.
    Нарисованы все силы: натяжения T, силы крюков 2T и силы тяжести.
    """
    r = d / 2
    n = len(kinds)
    x0 = 70
    xs = [x0 + i * d for i in range(n + 1)]
    W = max(560, int(xs[-1] + 230))
    s = S(W, h, label)
    top, hi, lo, bot = 30, 105, 235, 340
    ly = lo + 118  # верх грузов
    s.ground(40, xs[-1] + 40, top, True)
    ys = [hi if k == "f" else lo for k in kinds]
    forces = []  # рисуются последними, поверх нити и блоков

    def load_(x, name, c):
        box(s, x, ly, name, c)
        forces.append((x, ly, x, ly - 28, "T" if c == ORANGE else "2T", YELLOW))
        forces.append((x, ly + 36, x, ly + 84, name + "g", RED))

    if start:
        s.line(xs[0], ys[0], xs[0], ly, TEXT)
        load_(xs[0], start, ORANGE)
    else:
        s.line(xs[0], top, xs[0], ys[0], TEXT)
    for i in range(1, n):
        s.line(xs[i], ys[i - 1], xs[i], ys[i], TEXT)
    mi = 0
    for i, k in enumerate(kinds):
        cx = xs[i] + r
        sweep = 1 if k == "f" else 0
        s.pulley(cx, ys[i], r - 2)
        s.path(f"M{xs[i]},{ys[i]} A{r},{r} 0 0 {sweep} {xs[i+1]},{ys[i]}", TEXT, 2)
        down = 1 if k == "f" else -1
        for x in (xs[i], xs[i + 1]):  # натяжение двух ветвей, действующее на блок
            forces.append((x, ys[i], x, ys[i] + 40 * down, "T", YELLOW))
        if k == "f":
            s.line(cx, top, cx, ys[i], TEXT, 2)
            forces.append((cx, hi, cx, hi - 55, "2T", GREEN))
        else:
            forces.append((cx, lo, cx, lo + 60, "2T", GREEN))
            if platform:
                s.line(cx, ys[i], cx, bot, TEXT, 2)
                forces.append((cx, bot, cx, bot - 28, "2T", YELLOW))
            elif loads:
                s.line(cx, ys[i], cx, ly, TEXT, 2)
                load_(cx, loads[mi], GREEN)
                mi += 1
    last = ys[-1]
    if end == "c":
        s.line(xs[n], last, xs[n], top, TEXT)
    elif end == "p":
        s.line(xs[n], last, xs[n], bot, TEXT)
        forces.append((xs[n], bot, xs[n], bot - 28, "T", YELLOW))
    elif end == "F":
        s.line(xs[n], last, xs[n], 290, TEXT)
        forces.append((xs[n], 270, xs[n], 330, "F = T", YELLOW))
    else:
        s.line(xs[n], last, xs[n], ly, TEXT)
        load_(xs[n], end, ORANGE)
    if platform:
        right = xs[n] + 24 if end == "p" else xs[n] - 28
        left = xs[0] - 10
        mid = (left + right) / 2
        s.rect(left, bot, right - left, 42).text(mid, bot + 20, platform, BLUE, 16)
        weight = "mg" if platform.startswith("m =") else platform + "g"
        forces.append((mid, bot + 30, mid, bot + 90, weight, RED))
    for x1, y1, x2, y2, t, c in forces:
        s.force(x1, y1, x2, y2, t, c, 7, 0)
    for i, t in enumerate(tens or []):
        s.text(W - 95, 120 + 34 * i, t, YELLOW if i == 0 else TEXT, 18)
    return s.svg()


F["pul_1a"] = lambda: zigzag("Platform on two movable pulleys: four segments of string", "mfm", "c", platform="m = 20 kg", tens=["4T = mg", "T = 50 N", "hook: 2T = 100 N"])
F["pul_1b"] = lambda: zigzag("Platform held by five segments of string", "mfmf", "p", platform="m = 20 kg", tens=["5T = mg", "T = 40 N", "hook: 2T = 80 N"])
F["pul_2a"] = lambda: zigzag("Load m1 on two movable pulleys, load m2 at the end of the string", "mfmf", "m_2", platform="m_1", tens=["m_2g = T", "m_1g = 4T", "m_1/m_2 = 4"])
F["pul_3a"] = lambda: zigzag("Load 2m at the string end, loads m and M on movable pulleys", "fmfm", "c", loads=["m", "M"], start="2m", tens=["T = 2mg", "mg = 2T", "Mg = 2T"])
F["pul_3b"] = lambda: zigzag("Load M at the string end, loads m and 2m on movable pulleys", "fmfm", "c", loads=["m", "2m"], start="M", tens=["T = Mg", "mg = 2T", "2mg = 2T"])
F["pul_eq1"] = lambda: zigzag("The free end is pulled with force F; the load hangs on two movable pulleys", "mfmf", "F", platform="m", tens=["4F = mg", "F = 100 N", "m = 40 kg"])
F["pul_eq3"] = lambda: zigzag("Platform on a movable pulley and on the end of the same string", "mf", "p", platform="m = 30 kg", tens=["2T + T = mg", "T = 100 N"])


def cascade(label, stages, end, labs, formula, load="m_1", axle=None):
    """Цепочка подвижных блоков: правая ветвь каждого держит ось следующего. Нарисованы все силы."""
    s = S(640, 660, label)
    top = 30
    s.ground(40, 440, top, True)
    rad = [34, 48, 62][:stages]
    cx, y = 100, 470
    pos = []
    for r in rad:
        pos.append((cx, y, r))
        cx, y = cx + r, y - 130
    for i, (x, py, r) in enumerate(pos):
        s.pulley(x, py, r - 2)
        s.line(x - r, top, x - r, py, TEXT, 2).path(f"M{x-r},{py} A{r},{r} 0 0 0 {x+r},{py}", TEXT, 2)
        if i + 1 < stages:
            s.line(x + r, py, x + r, pos[i + 1][1], TEXT, 2)
    x, py, r = pos[0]
    s.line(x, py, x, 555, TEXT)
    box(s, x, 555, load, BLUE, 64, 38)
    xe, ye, re_ = pos[-1]
    xe += re_
    if end == "c":
        s.line(xe, ye, xe, top, TEXT, 2)
    elif end == "T":
        s.line(xe, ye, xe, 45, TEXT, 2)
    else:
        R = 30
        s.pulley(xe + R, 90, R - 2)
        s.line(xe, ye, xe, 90, TEXT, 2).path(f"M{xe},90 A{R},{R} 0 0 1 {xe+2*R},90", TEXT, 2)
        s.line(xe + R, top, xe + R, 90, TEXT).line(xe + 2 * R, 90, xe + 2 * R, 260, TEXT)
        box(s, xe + 2 * R, 260, end, GREEN)
        t = labs[-1]
        s.force(xe, 90, xe, 135, t).force(xe + 2 * R, 90, xe + 2 * R, 135, t)
        s.force(xe + R, 90, xe + R, 42, "2" + t, GREEN)
        s.force(xe + 2 * R, 260, xe + 2 * R, 215, t).force(xe + 2 * R, 296, xe + 2 * R, 350, end + "g", RED)
    axle = axle or ["2" + labs[0]] + labs[:-1]
    for i, (x, py, r) in enumerate(pos):
        s.force(x - r, py, x - r, py - 40, labs[i], YELLOW, 7, 4, "start", 18)
        s.force(x + r, py, x + r, py - 40, labs[i], YELLOW, 8, 4, "start", 18)
        s.force(x, py, x, py + (62 if i == 0 else 72), axle[i], GREEN, 8, 0, "start", 17)
    x, py, r = pos[0]
    s.force(x, 555, x, 536, "", GREEN)
    s.force(x, 593, x, 640, ("mg" if load.endswith("kg") or load == "m" else load + "g"), RED)
    if end == "T":
        s.text(xe + 12, 56, "T (pull)", YELLOW, 15, "start")
        s.arrow(xe, 90, xe, 45, YELLOW)
    for i, t in enumerate(formula):
        s.text(490, 420 + 34 * i, t, TEXT, 19)
    return s.svg()


F["pul_1c"] = lambda: cascade("Two movable pulleys one after another", 2, "c", ["T_2", "T_1"], ["2T_2 = mg, T_2 = 100 N", "T_1 = T_2/2 = 50 N"], "20 kg")
F["pul_2b"] = lambda: cascade("Cascade of two movable pulleys with load m2", 2, "m_2", ["T_1", "T_2"], ["m_1g = 2T_1 = 4T_2", "m_1/m_2 = 4"])
F["pul_cascade"] = lambda: cascade("Cascade of three movable pulleys with load m2", 3, "m_2", ["T_1", "T_2", "T_3"], ["m_1g = 8T_3 = 8m_2g", "m_1/m_2 = 8"])
F["pul_eq2"] = lambda: cascade("Cascade of two movable pulleys, string end pulled with force T", 2, "T", ["W/2", "W/4"], ["T = W/4", "W = 80 N, m = 8 kg"], "m", ["W", "W/2"])


@fig
def pul_eq4():
    s = S(760, 380, "Horizontal pulley chain with all forces: the pull T halves at every stage")
    s.wall(20, 240, 660, False)
    for x, y in ((130, 70), (280, 100), (430, 130)):
        s.pulley(x, y, 28)
    s.pulley(560, 182, 20)
    s.line(130, 40, 660, 40, TEXT, 2).path("M130,40 A30,30 0 0 0 130,100", TEXT, 2).line(130, 100, 280, 100, TEXT, 2)
    s.line(280, 70, 660, 70, TEXT, 2).path("M280,70 A30,30 0 0 0 280,130", TEXT, 2).line(280, 130, 430, 130, TEXT, 2)
    s.line(430, 100, 660, 100, TEXT, 2).path("M430,100 A30,30 0 0 0 430,160", TEXT, 2).line(430, 160, 560, 160, TEXT, 2)
    s.path("M560,160 A22,22 0 0 1 582,182", TEXT, 2).line(582, 182, 582, 250, TEXT).line(560, 182, 660, 182, MUTED, 2)
    box(s, 582, 250, "m")
    s.force(130, 70, 50, 70, "T", YELLOW, -2, -10, "middle")
    for x, y1, y2, t, c in ((130, 40, 100, "T/2", YELLOW), (280, 70, 130, "T/4", GREEN), (430, 100, 160, "T/8", ORANGE)):
        s.force(x, y1, x + 62, y1, t, c, -14, -7, "middle").force(x, y2, x + 62, y2, t, c, -14, 17, "middle")
    s.force(280, 100, 218, 100, "T/2", YELLOW, 10, -8, "middle").force(430, 130, 368, 130, "T/4", GREEN, 10, -8, "middle")
    s.force(560, 160, 505, 160, "T/8", ORANGE, 8, -8, "middle").force(582, 182, 582, 225, "T/8", ORANGE)
    s.force(560, 182, 602, 140, "axle", GREEN, 6, 0)
    s.force(582, 250, 582, 222, "", ORANGE).force(582, 286, 582, 336, "mg", RED)
    s.text(200, 300, "mg = T/8", TEXT, 19).text(220, 330, "T = 8 kN ⇒ mg = 1 kN", MUTED, 17)
    return s.svg()


@fig
def pul_eq5():
    s = S(900, 700, "Platform m2 on four segments balanced by load m1, with all forces")
    k = 1.7
    P = lambda x, y: (x * k - 20, y * k - 15)

    def ln(x1, y1, x2, y2):
        s.line(*P(x1, y1), *P(x2, y2), TEXT, 2)

    def arc(x1, x2, y, sweep):
        r = (x2 - x1) / 2 * k
        (a, b), (c, d) = P(x1, y), P(x2, y)
        s.path(f"M{a},{b} A{r},{r} 0 0 {sweep} {c},{d}", TEXT, 2)

    s.ground(P(50, 30)[0], P(360, 30)[0], P(50, 30)[1], True)
    for x, y, r in ((100, 75, 38), (162, 285, 20), (206, 210, 20), (228, 150, 20), (258, 85, 28)):
        s.pulley(*P(x, y), r * k)
    ln(100, 30, 100, 75); arc(60, 140, 75, 1); ln(60, 75, 60, 360); ln(140, 75, 140, 285)
    arc(140, 184, 285, 0); ln(184, 285, 184, 210); ln(162, 285, 162, 360)
    arc(184, 228, 210, 1); ln(228, 210, 228, 360); ln(206, 210, 206, 150)
    arc(206, 250, 150, 1); ln(250, 150, 250, 360); ln(228, 150, 228, 85)
    arc(228, 288, 85, 1); ln(288, 85, 288, 170); ln(258, 30, 258, 85)
    box(s, *P(300, 170), "m_1", ORANGE, 60, 44)
    (a, b), (c, d) = P(45, 360), P(275, 360)
    s.rect(a, b, c - a, 48).text(P(105, 360)[0], b + 30, "m_2", BLUE, 19)

    def f(x, y, dy, t, c=YELLOW, left=False):
        a, b = P(x, y)
        s.force(a, b, a, b + dy, t, c, -6 if left else 6, 2, "end" if left else "start", 15)

    f(60, 75, 40, "W/4", left=True); f(140, 75, 40, "W/4"); f(100, 75, -55, "W/2", GREEN, True)
    f(140, 285, -50, "W/4", left=True); f(184, 285, -50, "W/4"); f(162, 285, 55, "W/2", GREEN, True)
    f(184, 210, 34, "W/4", left=True); f(228, 210, 34, "W/4"); f(206, 210, -36, "W/2", GREEN, True)
    f(206, 150, 34, "W/2", left=True); f(250, 150, 34, "W/2"); f(228, 150, -36, "W", GREEN, True)
    f(228, 85, 34, "W", left=True); f(288, 85, 34, "W"); f(258, 85, -55, "2W", GREEN, True)
    f(60, 360, -45, "W/4", left=True); f(162, 360, -45, "W/2", left=True); f(228, 360, -45, "W/4", left=True); f(250, 360, -45, "W/2")
    f(150, 388, 45, "m_2g", RED)
    f(288, 170, -22, "", YELLOW); s.force(P(300, 170)[0], P(300, 170)[1] + 44, P(300, 170)[0], P(300, 170)[1] + 110, "W = m_1g", RED)
    s.text(720, 130, "W = m_1g", TEXT, 20).text(720, 175, "m_2g = W/4 + W/2", TEXT, 19).text(755, 208, "+ W/4 + W/2", TEXT, 19).text(720, 255, "m_1/m_2 = 2/3", YELLOW, 22)
    return s.svg()


@fig
def pul_infinite():
    s = S(680, 480, "An infinite chain of movable pulleys with equal loads, with all forces")
    s.ground(40, 520, 30, True)
    pos = [(110, 385, 28), (138, 250, 38), (176, 115, 46)]
    for i, (x, y, r) in enumerate(pos):
        s.pulley(x, y, r - 2)
        s.line(x - r, 30, x - r, y, TEXT, 2).path(f"M{x-r},{y} A{r},{r} 0 0 0 {x+r},{y}", TEXT, 2)
        if i < 2:
            s.line(x + r, y, x + r, pos[i + 1][1], TEXT, 2)
    s.line(222, 115, 290, 55, TEXT, 2, "6 6").text(312, 55, "…", TEXT, 28)
    for i, (x, y, r) in enumerate(pos, 1):
        s.force(x - r, y, x - r, y - 42, f"T_{i}", YELLOW, -7, 4, "end").force(x + r, y, x + r, y - 42, f"T_{i}")
        s.line(x - 16, y, x, y, RED, 1.5).force(x - 16, y, x - 16, y + r + 38, "Mg", RED, -7, 0, "end")
        if i > 1:
            s.force(x, y, x, y + 46, f"T_{i-1}", GREEN, 8, 0)
    s.text(500, 170, "2Tᵢ = Tᵢ₋₁ + Mg", TEXT, 19)
    s.text(500, 215, "far away Tᵢ → A", TEXT, 18).text(500, 255, "A = (A + Mg)/2", TEXT, 19).text(500, 300, "A = Mg", YELLOW, 22)
    return s.svg()


@fig
def lab_triangle():
    s = S(640, 260, "The triangle of distances is similar to the triangle of forces")
    s.path("M120,40 V200 H260 Z", BLUE, 2.5, CELL).text(98, 125, "y", BLUE, 19, it=True).text(190, 224, "x", BLUE, 19, it=True).text(210, 110, "l", BLUE, 19, it=True)
    s.arrow(420, 40, 420, 200, RED).arrow(420, 200, 560, 200, YELLOW).arrow(560, 200, 420, 40, GREEN)
    s.text(395, 125, "W", RED, 19).text(490, 224, "F", YELLOW, 19).text(515, 110, "T", GREEN, 19)
    s.text(320, 125, "∼", TEXT, 34).text(320, 250, "W / y = F / x", TEXT, 18)
    return s.svg()


@fig
def lab_rulers():
    s = S(720, 290, "Two ways to hold the ruler: to measure x and to measure along the string")
    for ox, title in ((60, "fig. 1: measuring x"), (420, "fig. 2: ruler along the string")):
        s.ground(ox, ox + 190, 40, True).line(ox + 40, 40, ox + 140, 180, TEXT, 2).dot(ox + 140, 180).line(ox + 140, 180, ox + 140, 220, TEXT)
        box(s, ox + 140, 220, "m")
        s.line(ox + 140, 180, ox + 205, 180, TEXT).rect(ox + 205, 167, 55, 26, ORANGE)
        s.text(ox + 130, 278, title, MUTED, 15)
    s.rect(100, 46, 120, 14, YELLOW).rect(206, 60, 14, 118, YELLOW)
    s.path("M450,50 L550,190 L562,181 L462,41 Z", YELLOW, 2, CELL)
    return s.svg()


@fig
def lab_f_graph():
    s = S(560, 270, "The force grows in proportion to the ratio of x to y")
    s.axes(80, 220, 420, 190, "x/y", "F, N")
    X = lambda u: 80 + u * 700
    Y = lambda f: 220 - f * 80
    s.line(X(0), Y(0), X(.55), Y(4 * .55), YELLOW, 1.8, "8 6")
    for x, y, f in ((6.5, 24, 1), (8.5, 23.5, 1.5), (11, 22.5, 2)):
        s.dot(X(x / y), Y(f), BLUE, 6)
    for f in (1, 2):
        s.text(66, Y(f) + 5, str(f), MUTED, 14, "end")
    for u in (.2, .4):
        s.text(X(u), 242, str(u), MUTED, 14)
    s.text(260, 40, "slope of the line is W ≈ 4 N", TEXT, 16)
    return s.svg()


# ================= 7. Гук =================
@fig
def hooke_types():
    s = S(760, 210, "Four kinds of deformation: tension, bending, torsion, shear")
    s.wall(55, 120, 40).rect(40, 70, 90, 36).arrow(130, 88, 175, 88, YELLOW)
    s.path("M215,110 Q285,40 355,110", BLUE, 8).arrow(285, 40, 285, 70, YELLOW)
    s.wall(55, 120, 410).rect(410, 70, 100, 36).path("M520,65 A22,30 0 1 1 505,112", YELLOW, 2.5).arrow(512, 115, 498, 104, YELLOW)
    s.ground(590, 730, 125).path("M605,125 L635,60 H715 L685,125 Z", BLUE, 2.5, CELL).path("M605,125 V60 H685 V125", MUTED, 1.4, "none", 1, "5 5").arrow(640, 45, 720, 45, YELLOW)
    for x, t in ((100, "tension"), (285, "bending"), (460, "torsion"), (660, "shear")):
        s.text(x, 180, t, TEXT, 17)
    return s.svg()


@fig
def hooke_normal():
    s = S(760, 230, "The normal force is perpendicular to the surface; a hanging body stretches the string")
    s.ground(40, 190, 40, True).line(115, 40, 115, 100, TEXT).rect(90, 100, 50, 50).arrow(115, 125, 115, 60, YELLOW).arrow(115, 125, 115, 200, RED).text(140, 75, "T", YELLOW, 18).text(145, 195, "mg", RED, 16)
    s.ground(290, 470, 150).rect(345, 100, 70, 50).arrow(380, 125, 380, 40, GREEN).arrow(380, 125, 380, 205, RED).text(405, 55, "N", GREEN, 19).text(410, 200, "mg", RED, 16)
    s.path("M540,120 Q630,200 720,100", TEXT, 3).circle(612, 131, 24).arrow(612, 131, 596, 62, GREEN).arrow(612, 131, 612, 210, RED).text(575, 70, "N", GREEN, 19).text(645, 205, "mg", RED, 16)
    return s.svg()


@fig
def hooke_rod():
    s = S(620, 140, "A rod of length l extends by delta l under force F")
    s.wall(30, 100, 60).rect(60, 45, 330, 42).rect(390, 45, 60, 42, ORANGE).arrow(450, 66, 560, 66, YELLOW)
    s.text(225, 115, "l", TEXT, 19, it=True).text(420, 115, "Δl", ORANGE, 18).text(535, 45, "F", YELLOW, 19)
    return s.svg()


@fig
def hooke_pieces():
    s = S(720, 330, "A heavy spring cut into pieces: the higher the piece, the larger its load")
    s.ground(60, 180, 30, True)
    y = 30
    for h in (80, 66, 52, 38, 26):
        s.spring(120, y, 120, y + h, 4, 9)
        s.dot(120, y + h, MUTED, 3)
        y += h
    for i, lab in enumerate(("bottom: no load", "2nd: holds m_1g", "3rd: holds 2m_1g")):
        s.text(165, 285 - i * 45, lab, TEXT, 15, "start")
    s.axes(440, 270, 230, 200, "i", "Δl_i")
    for i in range(7):
        s.dot(440 + i * 30 + 10, 270 - i * 26, GREEN, 5)
    s.text(560, 40, "Δl_i = (i−1)·m_1g/k_1", TEXT, 16)
    return s.svg()


@fig
def hooke_young():
    s = S(760, 190, "Two rods side by side are twice as stiff; stiffness grows with cross-section")
    s.wall(40, 110, 50).rect(50, 60, 190, 28).arrow(240, 74, 300, 74, YELLOW).text(285, 55, "F", YELLOW, 18).text(150, 130, "F/x = k", TEXT, 18)
    s.wall(40, 125, 420).rect(420, 52, 190, 28).rect(420, 86, 190, 28).arrow(610, 83, 700, 83, YELLOW).text(665, 65, "2F", YELLOW, 18).text(520, 145, "2F/x = 2k", TEXT, 18)
    s.text(380, 178, "k ∼ A,  k ∼ 1/l  ⇒  k = E·A/l", GREEN, 18)
    return s.svg()


@fig
def hooke_vessel():
    s = S(660, 340, "A vessel on a spring compresses it: weight and spring force in two cases")
    for x, level, lab, sh, w in ((130, 40, "8 N → 10 cm", 0, "8 N"), (390, 74, "16 N → 20 cm", 34, "16 N")):
        s.ground(x - 70, x + 70, 290)
        s.spring(x, 180 + sh, x, 290, 7, 14).rect(x - 50, 85 + sh, 100, 95, MUTED, "none")
        s.rect(x - 48, 178 + sh - level, 96, level, BLUE)
        s.force(x - 20, 180 + sh, x - 20, 70 + sh, "F = " + w, GREEN, -6, 0, "end")
        s.force(x + 20, 160 + sh, x + 20, 270 + sh * .4, "W = " + w, RED, 8, -4)
        s.text(x, 325, lab, TEXT, 16)
    s.text(580, 140, "k = 80 N/m", YELLOW, 19)
    return s.svg()


@fig
def hooke_load():
    s = S(480, 230, "A spring with a one newton load is stretched by ten centimetres")
    s.ground(80, 200, 30, True).spring(140, 30, 140, 150, 8, 12).rect(110, 150, 60, 46).text(140, 180, "1 N", BLUE)
    s.line(200, 105, 200, 150, ORANGE, 2).text(240, 133, "10 cm", ORANGE, 16).text(370, 110, "k = F/Δl", TEXT, 19).text(370, 150, "= 10 N/m", YELLOW, 19)
    s.force(125, 150, 125, 90, "F = 1 N", GREEN, -8, 4, "end").force(140, 180, 140, 225, "W = 1 N", RED, 8, -6)
    return s.svg()


@fig
def hooke_two_springs():
    s = S(560, 290, "A pulley hanging on springs of stiffness 2k and k is pulled down with force F")
    s.ground(80, 220, 30, True)
    s.pulley(150, 150, 28)
    s.spring(120, 30, 120, 150, 8, 10, GREEN).spring(180, 30, 180, 150, 8, 10, BLUE)
    s.path("M120,150 A30,30 0 0 0 180,150", TEXT, 2).line(150, 150, 150, 215, TEXT).arrow(150, 205, 150, 270, YELLOW)
    s.text(92, 95, "2k", GREEN, 18).text(205, 95, "k", BLUE, 18).text(175, 260, "F", YELLOW, 19)
    s.text(390, 100, "F/2 in each spring", TEXT, 16).text(390, 140, "Δx = (F/4k + F/2k)/2", TEXT, 17).text(390, 185, "k_eq = 8k/3", YELLOW, 20)
    s.force(120, 150, 120, 100, "F/2", ORANGE, -8, 22, "end").force(180, 150, 180, 100, "F/2", ORANGE, 8, 22)
    return s.svg()


@fig
def hooke_pulley_speed():
    s = S(560, 200, "The pulley axle speed is half the sum of the string end speeds")
    s.pulley(300, 100, 38)
    s.line(80, 60, 300, 60, TEXT, 2).path("M300,60 A40,40 0 0 1 300,140", TEXT, 2).line(80, 140, 300, 140, TEXT, 2)
    s.arrow(200, 45, 110, 45, BLUE).text(150, 30, "v_1", BLUE).arrow(110, 160, 200, 160, GREEN).text(160, 185, "v_2", GREEN).arrow(300, 100, 400, 100, YELLOW).text(385, 85, "u", YELLOW, 18)
    s.text(465, 150, "2u = v_1 + v_2", TEXT, 18)
    return s.svg()


# ================= 8. Трение =================
@fig
def fric_rough():
    s = S(640, 265, "Under magnification the touching surfaces are rough and their bumps catch")
    s.ground(40, 320, 160).rect(100, 96, 130, 62)
    s.force(230, 127, 305, 127, "F", YELLOW, -6, -9)
    s.force(165, 154, 70, 154, "F_fr", RED, 4, -10, "middle")
    s.force(165, 127, 165, 45, "N", GREEN).force(165, 127, 165, 215, "mg", ORANGE)
    s.circle(480, 115, 95, MUTED).line(230, 158, 392, 130, MUTED, 1.4, "5 5")
    s.path("M400,95 L420,115 L438,92 L458,122 L478,96 L500,118 L520,90 L540,116 L560,98", BLUE, 3)
    s.path("M398,135 L418,112 L440,138 L460,116 L482,140 L502,114 L522,140 L542,118 L562,132", ORANGE, 3)
    s.text(320, 250, "there is a gap between the bodies", MUTED, 15)
    return s.svg()


@fig
def fric_dir():
    s = S(760, 290, "Direction of friction: kinetic, static and on an incline, with all forces")
    for x0, caption, kinetic in ((125, "kinetic", True), (380, "static", False)):
        s.ground(x0 - 100, x0 + 100, 170).rect(x0 - 38, 118, 76, 50)
        s.force(x0, 143, x0, 65, "N", GREEN).force(x0, 143, x0, 228, "mg", ORANGE)
        s.force(x0, 164, x0 - 85, 164, "F_fr", RED, 8, -10, "middle")
        if kinetic:
            s.arrow(x0 + 20, 105, x0 + 85, 105, BLUE, 2.5, "6 5").text(x0 + 80, 93, "v", BLUE, 18)
        else:
            s.force(x0 + 38, 143, x0 + 100, 143, "F", YELLOW, -8, -9)
        s.text(x0, 268, caption, TEXT, 16)
    # наклонная плоскость: u вдоль склона вверх, n по нормали от поверхности
    ux, uy = .903, -.430
    nx, ny = uy, -ux
    px, py = 635, 170
    P = lambda a, b: (px + a * ux + b * nx, py + a * uy + b * ny)
    s.line(*P(-115, 0), *P(115, 0), TEXT, 2)
    for a in range(-105, 115, 16):
        s.line(*P(a, 0), *P(a - 10, -9), MUTED, 1.4)
    corners = [P(-38, 2), P(38, 2), P(38, 50), P(-38, 50)]
    s.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in corners) + " Z", BLUE, 2, CELL)
    cx, cy = P(0, 26)
    s.force(cx, cy, *P(0, 112), "N", GREEN, -8, 0, "end").force(cx, cy, cx, cy + 88, "mg", ORANGE)
    s.force(*P(0, 6), *P(88, 6), "F_fr", RED, -6, -14, "end")
    s.text(645, 268, "on a slope: static", TEXT, 16)
    return s.svg()


@fig
def fric_roll():
    s = S(640, 220, "A rolling wheel keeps climbing out of the dent it presses")
    s.circle(200, 110, 70).dot(200, 110).line(200, 110, 250, 60, YELLOW).text(240, 100, "R", YELLOW, 17).arrow(200, 110, 330, 110, GREEN).text(315, 95, "v", GREEN, 18)
    s.path("M60,170 H150 Q200,196 250,170 H360", TEXT, 3).path("M150,45 Q185,15 235,30", MUTED, 2).arrow(222, 26, 240, 32, MUTED, 2)
    s.text(490, 90, "F = kN/R", TEXT, 22).text(490, 130, "larger R, smaller force", MUTED, 15)
    return s.svg()


@fig
def fric_visc():
    s = S(720, 250, "Viscous friction: the body pushes the medium aside; force goes as speed or speed squared")
    for y, dy in ((50, -22), (90, -30), (150, 30), (190, 22)):
        s.path(f"M30,{y} C110,{y} 130,{y+dy} 180,{y+dy} C230,{y+dy} 250,{y} 330,{y}", MUTED, 1.8)
    s.circle(180, 120, 30, ORANGE).arrow(180, 120, 265, 120, GREEN).arrow(150, 120, 75, 120, RED).text(262, 108, "v", GREEN, 18).text(90, 108, "F", RED, 18)
    s.axes(430, 210, 240, 175, "v", "F")
    s.line(430, 210, 530, 175, BLUE, 3).path("M530,175 Q600,140 640,50", YELLOW, 3)
    s.text(500, 165, "∼ v", BLUE, 17, "start").text(580, 70, "∼ v²", YELLOW, 17)
    return s.svg()


# ================= 9. Статика =================
@fig
def st_couple():
    s = S(520, 210, "A couple: zero net force, yet the body rotates")
    s.rect(140, 85, 220, 40).arrow(140, 105, 140, 25, YELLOW).arrow(360, 105, 360, 185, YELLOW)
    s.text(115, 45, "F", YELLOW, 19).text(385, 175, "F", YELLOW, 19).path("M225,65 Q260,35 292,62", GREEN, 2.5).arrow(284, 53, 297, 69, GREEN)
    s.text(450, 105, "ΣF = 0", TEXT, 18)
    return s.svg()


@fig
def st_rotation():
    s = S(600, 260, "Three forces turn a disc: two one way and one the other")
    s.circle(180, 130, 80).dot(180, 130, YELLOW, 6)
    s.arrow(120, 78, 185, 25, BLUE).arrow(260, 130, 260, 220, GREEN).arrow(100, 130, 100, 222, ORANGE)
    s.text(195, 25, "F_1", BLUE).text(290, 200, "F_2", GREEN).text(75, 215, "F_3", ORANGE)
    s.text(450, 110, "clockwise M =", TEXT, 18).text(450, 140, "= counterclockwise M", TEXT, 18)
    return s.svg()


@fig
def st_strings():
    s = S(760, 255, "Rod on two strings: at the ends and with the second string shifted")
    s.ground(60, 320, 40, True).line(80, 40, 80, 140, TEXT).line(300, 40, 300, 140, TEXT).rect(70, 140, 240, 16)
    s.arrow(80, 140, 80, 80, YELLOW).arrow(300, 140, 300, 80, YELLOW).arrow(190, 148, 190, 215, RED).text(105, 95, "t_1", YELLOW).text(322, 95, "t_2", YELLOW).text(218, 210, "mg", RED, 16)
    s.ground(430, 700, 40, True).line(450, 40, 450, 140, TEXT).line(610, 40, 610, 140, TEXT).rect(440, 140, 250, 16)
    s.arrow(450, 140, 450, 85, YELLOW).arrow(610, 140, 610, 70, YELLOW).arrow(565, 148, 565, 215, RED).text(475, 95, "t_1", YELLOW).text(632, 85, "t_2", YELLOW).text(595, 210, "mg", RED, 16)
    s.line(450, 60, 610, 60, MUTED, 1.4, "5 5").text(530, 55, "l", MUTED, 17).text(565, 243, "middle: L/2", MUTED, 14)
    return s.svg()


@fig
def st_board_split():
    s = S(640, 240, "A board at a table edge split into parts weighing two thirds and one third")
    s.rect(60, 130, 370, 20, MUTED).rect(210, 108, 330, 22).line(430, 100, 430, 130, MUTED, 1.4, "4 4")
    s.dot(430, 130, YELLOW, 6).text(448, 172, "O", YELLOW)
    s.force(320, 119, 320, 195, "2mg/3", RED, -8, 0, "end").force(485, 119, 485, 190, "mg/3", RED)
    s.force(540, 119, 540, 205, "F", GREEN).force(430, 130, 430, 40, "N", GREEN)
    s.text(375, 95, "L/3", MUTED, 14).text(458, 95, "L/6", MUTED, 14).text(513, 95, "L/6", MUTED, 14)
    return s.svg()


@fig
def st_resultant():
    s = S(640, 230, "The resultant of gravity acts where the total moment is zero")
    s.rect(100, 80, 420, 18).arrow(220, 89, 220, 160, RED).arrow(440, 80, 440, 180, ORANGE).arrow(370, 89, 370, 18, GREEN)
    s.rect(420, 50, 40, 30, ORANGE).text(440, 70, "M", ORANGE, 15)
    s.text(190, 175, "mg", RED).text(475, 175, "Mg", ORANGE).text(345, 30, "N", GREEN, 19)
    s.dot(370, 89, YELLOW, 6).text(295, 120, "l_1", MUTED, 15).text(405, 120, "l_2", MUTED, 15).text(320, 215, "mg·l_1 = Mg·l_2", TEXT, 18)
    return s.svg()


@fig
def st_overhang():
    s = S(640, 270, "A board with a load sticks out past the edge of a table")
    s.ground(40, 400, 150).line(400, 150, 400, 245, TEXT, 2)
    s.rect(110, 130, 440, 20).rect(470, 100, 44, 30, ORANGE).text(492, 120, "M", ORANGE, 15)
    s.arrow(250, 140, 250, 215, RED).text(250, 235, "mg", RED)
    s.arrow(492, 130, 492, 215, ORANGE).text(492, 235, "Mg", ORANGE)
    s.arrow(340, 150, 340, 55, GREEN).text(320, 68, "N", GREEN, 19).dot(400, 150, YELLOW, 5)
    for x1, x2, y, lab in ((250, 400, 35, "l_0"), (340, 400, 100, "y"), (400, 492, 70, "x")):
        s.line(x1, y, x2, y, MUTED, 1.5).line(x1, y - 6, x1, y + 6, MUTED, 1.5).line(x2, y - 6, x2, y + 6, MUTED, 1.5)
        s.text((x1 + x2) / 2, y - 9, lab, MUTED, 16, "middle", True)
    s.line(400, 25, 400, 150, MUTED, 1, "4 5").text(418, 172, "edge", YELLOW, 15, "start")
    return s.svg()


@fig
def kin_messenger():
    s = S(680, 230, "A messenger rides from the rear of a moving column to its front and back")
    for y, lab, forward in ((65, "forward: v − u relative to the column", True), (165, "back: v + u relative to the column", False)):
        s.rect(150, y, 340, 26).arrow(490, y + 13, 580, y + 13, ORANGE).text(600, y + 19, "u", ORANGE, 18, it=True)
        x = 175 if forward else 465
        s.dot(x, y - 14, GREEN, 8).arrow(x, y - 14, x + (90 if forward else -90), y - 14, GREEN)
        s.text(x + (108 if forward else -108), y - 9, "v", GREEN, 18, it=True)
        s.text(320, y + 48, lab, MUTED, 15)
    s.text(320, 83, "L", TEXT, 17, "middle", True).text(320, 183, "L", TEXT, 17, "middle", True)
    return s.svg()


@fig
def acc_three():
    s = S(680, 290, "The same segment covered with acceleration, with braking and uniformly")
    rows = ((70, "t_1 = 30 s", 1, "a"), (160, "t_2 = 60 s", -1, "a"), (250, "t_3 = ?", 0, ""))
    for y, t, d, a in rows:
        s.line(80, y, 520, y, TEXT, 2).line(80, y - 9, 80, y + 9, TEXT, 2).line(520, y - 9, 520, y + 9, TEXT, 2)
        s.dot(80, y, BLUE, 7).arrow(80, y - 18, 170, y - 18, BLUE).text(188, y - 13, "v_0", BLUE, 17)
        if d:
            x = 270 if d > 0 else 345
            s.arrow(x, y - 18, x + 75 * d, y - 18, ORANGE).text(x + 93 * d, y - 13, a, ORANGE, 17, it=True)
        else:
            s.text(310, y - 13, "a = 0", MUTED, 16)
        s.text(595, y + 5, t, YELLOW, 17)
    s.text(300, 280, "L", TEXT, 17, "middle", True)
    return s.svg()


F["pul_3c"] = lambda: zigzag("Load M at the string end and equal loads m on both movable pulleys", "fmfm", "c", loads=["m", "m"], start="M", tens=["T = Mg", "mg = 2T", "m = 2M"])


# ================= 10. Импульс =================
@fig
def mom_carts():
    s = S(640, 195, "Two carts leave rest with momenta equal in magnitude")
    s.ground(40, 600, 150)
    for x, w, n, c in ((190, 70, "m_1", BLUE), (350, 110, "m_2", GREEN)):
        s.rect(x, 75, w, 55, c).text(x + w / 2, 108, n, c).circle(x + 16, 140, 10, c).circle(x + w - 16, 140, 10, c)
    s.arrow(190, 55, 80, 55, BLUE).text(125, 40, "v_1", BLUE).arrow(460, 55, 530, 55, GREEN).text(510, 40, "v_2", GREEN)
    s.text(320, 185, "m_1v_1 = m_2v_2", TEXT, 19)
    return s.svg()


@fig
def mom_triangle():
    s = S(560, 280, "Three equal masses: two are replaced by a double mass midway between them")
    s.circle(130, 60, 18).circle(390, 60, 18).circle(390, 230, 18)
    for x, y in ((130, 66), (390, 66), (390, 236)):
        s.text(x, y, "m", BLUE, 15)
    s.line(148, 60, 372, 60, MUTED, 1.5, "7 6").dot(260, 60, ORANGE, 8).text(260, 40, "2m", ORANGE)
    s.line(260, 60, 390, 230, GREEN, 2, "7 6").dot(303.3, 116.7, YELLOW, 8).text(240, 135, "centre of mass", YELLOW, 17)
    s.text(160, 200, "splits the segment 1 : 2", MUTED, 15)
    return s.svg()
