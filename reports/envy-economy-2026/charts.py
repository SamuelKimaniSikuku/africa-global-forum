#!/usr/bin/env python3
"""Rebuild the three research graphs (SVG for the web, PNG for the PDF).

Run with Python, matplotlib and numpy installed. Values are transcribed from
the primary sources below. No interpolation or invented observations.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "img"
PAPER, INK, RED, FOREST, GRID = "#F4EFE6", "#0E0B08", "#C8421A", "#2A3D2A", "#D9CFC1"

# Lei et al. (2026), section 3.4, combined no-intercept outcome model.
# https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2026.1825169/full
# Wellbeing/self-esteem are reverse-coded: positive r = poorer outcomes.
ASSOCIATIONS = [
    ("Social-evaluative\nnegative emotions", .438, .385, .487),
    ("Anxiety", .382, .322, .439),
    ("Depression", .306, .252, .358),
    ("Lower wellbeing", .268, .208, .326),
    ("Lower self-esteem", .263, .210, .314),
]

# OECD/European Commission (2023), main-indicators brochure, p. 12;
# 2021 EU data. COMBINED overqualified OR not employed; tertiary educated.
# https://www.oecd.org/content/dam/oecd/en/publications/support-materials/2023/06/indicators-of-immigrant-integration-2023_70d202c4/indicators-of-immigrant-integration-settling-in-main-indicators-2023-brochure.pdf
EMPLOYMENT = [("Immigrants", 47), ("Native-born adults", 30)]

# Hunt et al. (2018), pp. 761-762. Higher initial symptom subgroup only
# (BDI-II >= 14), NOT means for the full trial of 143 undergraduates.
# https://www.researchgate.net/publication/328838624_No_More_FOMO_Limiting_Social_Media_Decreases_Loneliness_and_Depression
TRIAL = [("Limited use", 23.0, 14.5), ("Usual use", 22.8, 22.83)]

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 13, "text.color": INK,
    "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
    "figure.facecolor": PAPER, "axes.facecolor": PAPER,
    "svg.fonttype": "none", "svg.hashsalt": "agf-envy-2026",
})


def canvas(title, subtitle, h=5.3):
    fig = plt.figure(figsize=(8, h))
    fig.text(.045, .935, title, fontsize=20, weight="bold", va="top")
    fig.text(.045, .847, subtitle, fontsize=12, color="#6B635A", va="top")
    return fig


def clean(ax):
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", length=0, pad=9)
    ax.set_axisbelow(True)


def save(fig, name):
    # Fixed canvas keeps predictable web/PDF dimensions. SVG text stays text.
    fig.savefig(OUT / f"{name}.svg", metadata={"Date": None})
    fig.savefig(OUT / f"{name}.png", dpi=200)
    plt.close(fig)


def associations():
    fig = canvas("Upward comparison and wellbeing", "Correlation r  |  Dots: estimates; lines: 95% confidence intervals", 5.8)
    ax = fig.add_axes([.39, .20, .52, .53])
    for i, (label, value, lo, hi) in enumerate(ASSOCIATIONS):
        ax.errorbar(value, i, xerr=[[value-lo], [hi-value]], fmt="o", ms=8,
                    color=RED, ecolor=RED, elinewidth=2, capsize=5, capthick=1.5)
        ax.annotate(f"{value:.3f}", (hi, i), xytext=(10, 0), textcoords="offset points",
                    va="center", fontsize=12, weight="bold")
    ax.set_yticks(range(5), [x[0] for x in ASSOCIATIONS], fontsize=12)
    ax.set_ylim(4.55, -.65)
    ax.set_xlim(0, .6)
    ax.set_xticks([0, .1, .2, .3, .4, .5, .6])
    ax.xaxis.grid(True, color=GRID, linewidth=.8)
    clean(ax)
    fig.text(.045, .065, "Source: Lei et al. (2026), combined model, section 3.4.\nAssociation, not causation; no African-diaspora estimate.", fontsize=11, color="#6B635A", linespacing=1.5)
    save(fig, "comparison-associations")


def employment():
    fig = canvas("Qualifications meet unequal conditions", "EU adults with tertiary education  |  2021 data", 4.7)
    ax = fig.add_axes([.30, .28, .61, .41])
    ax.barh([0, 1], [47, 30], height=.48, color=[RED, FOREST])
    ax.set_yticks([0, 1], [x[0] for x in EMPLOYMENT], fontsize=12)
    ax.set_ylim(1.7, -.65)
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"])
    ax.xaxis.grid(True, color=GRID, linewidth=.8)
    for i, (_, value) in enumerate(EMPLOYMENT):
        ax.text(value+2, i, f"{value}%", va="center", fontsize=17, weight="bold")
    clean(ax)
    fig.text(.30, .19, "Overqualified or not employed", fontsize=12, weight="bold")
    fig.text(.045, .055, "Source: OECD/European Commission (2023), brochure p. 12.\nAll immigrant origins; labour-market context, not a measure of envy.", fontsize=11, color="#6B635A", linespacing=1.5)
    save(fig, "employment-context")


def trial():
    fig = canvas("A social media trial: reported scores", "Higher-symptom subgroup only  |  Mean BDI-II depression score", 5.6)
    ax = fig.add_axes([.12, .23, .81, .47])
    x = np.arange(2)
    width = .27
    b1 = ax.bar(x-width/2, [23.0, 22.8], width, label="Baseline", color=FOREST)
    b2 = ax.bar(x+width/2, [14.5, 22.83], width, label="Week 4", color=RED)
    ax.bar_label(b1, labels=["23.0", "22.8"], padding=5, fontsize=14, weight="bold")
    ax.bar_label(b2, labels=["14.5", "22.83"], padding=5, fontsize=14, weight="bold")
    ax.set_xticks(x, ["Limited use", "Usual use"], fontsize=14)
    ax.set_ylim(0, 30)
    ax.set_yticks([0, 10, 20, 30])
    ax.yaxis.grid(True, color=GRID, linewidth=.8)
    ax.legend(loc="lower right", bbox_to_anchor=(1, 1.035), ncols=2, frameon=False, fontsize=12)
    clean(ax)
    fig.text(.12, .125, "Lower scores indicate fewer depressive symptoms.", fontsize=12)
    fig.text(.045, .045, "Source: Hunt et al. (2018), pp. 761-762. Baseline BDI-II ≥ 14.\nThese subgroup means are not results for all 143 participants.", fontsize=11, color="#6B635A", linespacing=1.5)
    save(fig, "social-media-trial")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    associations()
    employment()
    trial()
    print("Wrote three SVG graphs and three PDF-resolution PNGs.")
