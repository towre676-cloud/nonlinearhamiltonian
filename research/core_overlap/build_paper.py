#!/usr/bin/env python3
"""Assemble the scoped proof paper; --pdf requires pandoc and XeLaTeX."""
from pathlib import Path
import argparse
import re
import subprocess

ROOT = Path(__file__).resolve().parent
CHAPTERS = ['README.md', 'pure_perfect_power.md', 'pure_quadratic_composition.md',
            'analytic_shear_square.md', 'shear_composition_complete.md',
            'shear_oscillator.md', 'constant_quadratic_classification.md',
            'quadratic_frontier.md', 'quadratic_shear_residual.md',
            'affine_shear_potentials.md',
            'deformation_obstructions.md', 'audit_sector_dynamics.md',
            'audit_balanced_transverse.md', 'depth_finite_determination.md',
            'analytic_bridge.md', 'analytic_potential_classification.md',
            'canonical_bridge.md', 'audit_balanced.md',
            'review_assessment.md', 'review_near_followup.md',
            'extension_proof_review.md', 'SOURCES.md']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf', action='store_true')
    args = parser.parse_args()
    front = '''---
title: "Exact Nonlinear Sectors"
subtitle: "Composition classifications, oscillator cores, analytic potentials and deformation obstructions"
author: "Nonlinear Hamiltonian research programme"
date: "22 October 2026 - internally reviewed research draft"
fontsize: 10pt
colorlinks: true
linkcolor: NavyBlue
urlcolor: NavyBlue
toc-depth: 1
---

'''
    parts = [front]
    for index, name in enumerate(CHAPTERS):
        text = (ROOT / name).read_text()
        if name == 'canonical_bridge.md':
            text = text.split('The companion `canonical_verify.py`')[0].rstrip()+'\n'
        if name == 'depth_finite_determination.md':
            text = text.split('The proof, rather than the grid, establishes')[0].rstrip()+'\n'
        if name == 'audit_sector_dynamics.md':
            text = text.replace('## Minimal derivative closures for targets',
                                '\\Needspace{14\\baselineskip}\n\n## Minimal derivative closures for targets')
        text = text.replace('\u2011', '-').replace('\u2212', '-')
        text = text.replace('e91e14da9d59e799ad9ed0331f59b2b500e478e8', 'e91e14d')
        # amsmath permits tags on aligned displays, outside the environment.
        def align(match):
            body = match.group(1)
            tags = re.findall(r'\\tag\{[^}]+\}', body)
            body = re.sub(r'\\tag\{[^}]+\}', '', body)
            return r'\begin{aligned}' + body + r'\end{aligned}' + ''.join(tags)
        text = re.sub(r'\\begin\{split\}(.*?)\\end\{split\}', align, text, flags=re.S)
        text = re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', align, text, flags=re.S)
        if index:
            parts.append('\\clearpage\n\n')
        parts.append(text.strip() + '\n\n')
    paper = '\n'.join(line.rstrip() for line in ''.join(parts).splitlines()).rstrip()+'\n'
    (ROOT / 'PAPER.md').write_text(paper)
    if args.pdf:
        out = ROOT / 'output/pdf/Exact_Core_Overlap_Research.pdf'
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['pandoc', 'PAPER.md',
                        '--from=markdown+tex_math_single_backslash+tex_math_dollars',
                        '--pdf-engine=xelatex', '--toc', '--number-sections',
                        '-V', 'geometry:margin=22mm', '-V', 'mainfont=DejaVu Serif',
                        '-V', 'sansfont=DejaVu Sans', '-V', 'monofont=DejaVu Sans Mono',
                        '--include-in-header=paper_header.tex', '-o', str(out)],
                       cwd=ROOT, check=True)
        print(out)


if __name__ == '__main__':
    main()
