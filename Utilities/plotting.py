"""
Matplotlib defaults and export helpers for this repo.

Figures are sized from a nominal LaTeX text width (390 pt) with an optional
golden-ratio height. Vector export is PDF + EPS; TeX text is opt-in via env.
"""

import os
import matplotlib as mpl
import numpy as np

# External LaTeX (text.usetex=True) needs a working `latex` on PATH.
# Set PINNS_USE_LATEX=1 if TeX is installed and you want publication text.
_use_tex = os.environ.get("PINNS_USE_LATEX", "").strip().lower() in ("1", "true", "yes")

_LATEX_TEXTWIDTH_PT = 390.0
_PT_PER_IN = 72.27


def scaled_figure_size(width_scale: float, n_panels_vertical: int = 1):
    """Return [width, height] in inches for a single column scaled by *width_scale*."""
    width_in = _LATEX_TEXTWIDTH_PT * (1.0 / _PT_PER_IN) * width_scale
    golden = (np.sqrt(5.0) - 1.0) / 2.0
    height_in = n_panels_vertical * width_in * golden
    return [width_in, height_in]


_common_rc = {
    "font.family": "serif",
    "axes.labelsize": 10,
    "font.size": 10,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.figsize": scaled_figure_size(1.0),
}

if _use_tex:
    mpl.rcParams.update(
        {
            **_common_rc,
            "pgf.texsystem": "pdflatex",
            "text.usetex": True,
            "font.serif": [],
            "font.sans-serif": [],
            "font.monospace": [],
            "pgf.preamble": r"\usepackage[utf8x]{inputenc}\n\usepackage[T1]{fontenc}",
        }
    )
else:
    mpl.rcParams.update(
        {
            **_common_rc,
            "text.usetex": False,
        }
    )

import matplotlib.pyplot as plt


def _ensure_tex_disabled_when_unconfigured() -> None:
    if not _use_tex:
        mpl.rcParams["text.usetex"] = False


def open_single_axis_figure(width_scale: float, n_panels_vertical: int = 1):
    """Create a figure with one subplot; respects optional-TeX rc settings."""
    _ensure_tex_disabled_when_unconfigured()
    fig = plt.figure(figsize=scaled_figure_size(width_scale, n_panels_vertical))
    ax = fig.add_subplot(111)
    return fig, ax


def export_vector_figure(base_path: str, crop: bool = True, figure=None):
    """Write *base_path*.pdf and *base_path*.eps. Pass *figure* to avoid ``gcf()`` surprises."""
    _ensure_tex_disabled_when_unconfigured()
    fig = plt.gcf() if figure is None else figure
    pdf = f"{base_path}.pdf"
    eps = f"{base_path}.eps"
    if crop:
        fig.savefig(pdf, bbox_inches="tight", pad_inches=0)
        fig.savefig(eps, bbox_inches="tight", pad_inches=0)
    else:
        fig.savefig(pdf)
        fig.savefig(eps)
