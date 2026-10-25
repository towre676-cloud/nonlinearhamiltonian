#!/usr/bin/env python3
"""Render the proved all-degree filtration dimensions from Theorem QF.

Matplotlib is needed only to rebuild this publication figure. The mathematical
replay bundle and its certificate checkers use the Python standard library.
"""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    out = Path(__file__).resolve().parent / 'output/figures/Sharp_Depth_Transitions.png'
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                         'axes.spines.top': False, 'axes.spines.right': False})
    fig, ax = plt.subplots(figsize=(8.8, 4.8), layout='constrained')
    depths = [2, 3, 4, 5, 6]
    rows = [('Quadratic or lower potential', [6, 6, 6, 6, 6], '#1769aa', 'o'),
            ('Cubic potential', [6, 5, 4, 3, 2], '#c24d2b', 's'),
            ('Potential degree at least four', [6, 4, 2, 2, 2], '#387b54', 'D')]
    for label, values, color, marker in rows:
        ax.plot(depths, values, color=color, marker=marker, linewidth=2.3,
                markersize=6, label=label)
    ax.set(xlabel='Hamiltonian bracket depth R',
           ylabel='Dimension of the joint third-gate kernel',
           xticks=depths, yticks=[2, 3, 4, 5, 6], ylim=(1.7, 6.35),
           title='Sharp stopping depths for exact nonlinear sectors')
    ax.grid(axis='y', color='#d8dee7', linewidth=.7)
    ax.legend(loc='upper right', bbox_to_anchor=(1, -.20), frameon=False,
              ncols=1, fontsize=10)
    fig.savefig(out, dpi=220, facecolor='white')
    print(out)


if __name__ == '__main__':
    main()
