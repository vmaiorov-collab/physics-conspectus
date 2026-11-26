# Конспекты по физике (механика)

Сайт: **https://vmaiorov-collab.github.io/physics-conspectus/**

Десять тем по рукописным записям занятий: векторы, кинематика, равноускоренное движение, масса и плотность,
законы Ньютона, блоки, закон Гука, трение, статика, импульс и центр масс.

Каждый конспект — один HTML-файл (формулы KaTeX и SVG-чертежи встроены), открывается без интернета.
Оформление — как в [conspectus](https://github.com/vmaiorov-collab/conspectus).

## Сборка

```bash
python3 tools/build.py
```

Тексты лежат в `content/`, чертежи (SVG, генерируются кодом) — в `tools/figures.py` и `tools/figures2.py`.
