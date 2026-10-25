"""Render the audited result into a short staff-review PDF."""
from pathlib import Path
from xml.sax.saxutils import escape
import json
import reportlab
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak

HERE=Path(__file__).resolve().parent
FONT_DIR=Path(reportlab.__file__).resolve().parent/'fonts'
pdfmetrics.registerFont(TTFont('ReviewSans',str(FONT_DIR/'Vera.ttf')))
pdfmetrics.registerFont(TTFont('ReviewSans-Bold',str(FONT_DIR/'VeraBd.ttf')))
pdfmetrics.registerFontFamily('ReviewSans',normal='ReviewSans',bold='ReviewSans-Bold',italic='ReviewSans',boldItalic='ReviewSans-Bold')


def main():
    data=json.loads((HERE/'results/AUDITED_RESULTS.json').read_text())
    rows={r['method']:r for r in data['rows']}
    baseline=rows[data['best_qualified_existing_method']]
    eligible=[r for r in rows.values()if r['qualified']and r['method'].startswith('fused')]
    best=min(eligible,key=lambda r:r['first_workload_seconds'])
    gain=baseline['first_workload_seconds']/best['first_workload_seconds']
    out=HERE/'output/pdf/BNL_Tracking_Review_20261023.pdf';out.parent.mkdir(parents=True,exist_ok=True)
    styles=getSampleStyleSheet()
    styles['Heading2'].fontName='ReviewSans-Bold'
    styles.add(ParagraphStyle(name='TitleLocal',fontName='ReviewSans-Bold',fontSize=18,leading=23,textColor=colors.HexColor('#12334A'),spaceAfter=12))
    styles.add(ParagraphStyle(name='BodyLocal',fontName='ReviewSans',fontSize=9.5,leading=13,spaceAfter=9))
    styles.add(ParagraphStyle(name='SmallLocal',fontName='ReviewSans',fontSize=7.5,leading=10,spaceAfter=6))
    story=[]
    def p(text,style='BodyLocal'):story.append(Paragraph(text,styles[style]))
    def h(text):p(text,'Heading2')
    p('Guarded fixed-momentum tracking<br/>on a public NSLS-II design model','TitleLocal')
    p('Technical review packet | 23 October 2026, America/New_York | Independent research prototype','SmallLocal')
    p(f'<b>Measured result:</b> {gain:.2f}x lower first-workload time versus the fastest tested existing method that passed the frozen accuracy gate: <b>{baseline["first_workload_seconds"]:.3f} s to {best["first_workload_seconds"]:.3f} s</b>. Tracking alone improves by {baseline["median_tracking_with_fallback_seconds"]/best["median_tracking_with_fallback_seconds"]:.2f}x. The new-method cost includes plugin build, lattice construction, compilation, warm-up and guard-triggered native reruns.')
    h('The workload and the accuracy gate')
    p('The source is BNL-authored NSLS2/PyELEGANT demo/nsls2cb65pm.lte, pinned to commit 11d97113ea7ae05fd0ffe710a88793f2bdc9ed84. It is a historical complex-bend design demonstrator: 3 GeV, 791.958 m, 3,030 elements. RF, radiation, collective effects and magnet errors are off; no mechanical apertures are present. This is not the present operational machine.')
    p('A frozen independent-seed confirmation compared 15 predeclared variants on 64 launches for 256 turns. Survival labels must match wherever native 40- and 80-step references agree. Sixteen core launches must have maximum position error at most 1 micrometre and momentum error at most 1 microradian-equivalent normalized momentum. No threshold was relaxed after seeing results.')
    p(f'The selected {escape(best["method"])} passed all {data["reference_agreement_points"]} reference-agreed labels. Point 48 remains unresolved because the references disagree. Core errors were {best["core_position_max_abs_m"]*1e6:.3f} micrometres and {best["core_momentum_max_abs_normalized"]*1e6:.4f} microradian-equivalent. All 25 guard reruns per repetition are charged. This is empirical qualification on this finite test, not a uniform stability theorem.')
    table=[['Method','Qualified','First workload, s']]
    for name in ['native10','native40','analytic10','fused40_s10','fused40_s2','fused40_s4']:
        r=rows[name];table.append([name,'yes'if r['qualified']else'no',f'{r["first_workload_seconds"]:.3f}'])
    t=Table(table,colWidths=[220,90,150],hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E5EDF2')),('FONTNAME',(0,0),(-1,0),'ReviewSans-Bold'),('FONTNAME',(0,1),(-1,-1),'ReviewSans'),('FONTSIZE',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#7892A2'))]))
    story.append(t);story.append(Spacer(1,9))
    p('The roughly 15.2x ratio versus native40 is not the headline: built-in analytic passes already supply much of that improvement. The additional measured gain over analytic10 is 1.61x. No tenfold industrial tuning advantage is established.','SmallLocal')
    p('Primary context: BNL-230151-2026-TECH reports nearly 30,000 HSR field-error simulations; BNL already develops nonlinear-optics and data-driven optimization methods. This contribution claims a qualified implementation benchmark, not invention of matrix transport or accelerator optimization.','SmallLocal')
    p('Sources: github.com/NSLS2/PyELEGANT; technotes.bnl.gov/Home/ViewTechNote/230151; bnl.gov/nsls2/accelerator/research.php. Full bibliographic and provenance records accompany the package.','SmallLocal')
    story.append(PageBreak())
    h('Why this reduction is mathematically admissible')
    p('At fixed momentum deviation, eligible drifts, pure quadrupoles and linear-field bends are affine in the four transverse coordinates in the selected PyAT paraxial model. We compose the actual discrete integration matrices, retaining thick sextupoles. The selected method preserves 40-step linear bodies and uses four sextupole steps. A fused C pass combines each matrix with an input-domain guard. Guard rejection means uncertainty and triggers a native rerun; it is never silently classified as physical loss.')
    p('Independent C-formula review and 108 element/momentum cases with 100 points each found maximum transverse residual 6.94e-18. A separate fused-kernel check passed 100 accepted points and three guard failures. Prefix bounds use a large amplitude margin. They are not outward IEEE error certificates. Floating regrouping can affect chaotic trajectories, so element-level identities do not replace the held-out test.')
    p('Longitudinal path length is not preserved. A conservative exact-rational magnitude argument bounds omitted linear contributions below 10^60 over 4,096 turns; retained nonlinear finiteness and complete IEEE equivalence remain separate. The method requires no RF or other longitudinal-to-transverse feedback. It is not a six-dimensional tracker replacement.')
    h('Costs, reproduction and limits')
    p(f'Reference generation cost {data["reference_generation_seconds"]:.2f} s; all 15 confirmation methods, setups, repeats and one build cost {data["measured_confirmation_campaign_seconds"]:.2f} s. Earlier exploration is additional. Conditional repayment needs {best["conditional_reference_only_break_even_new_equal_cost_batches"]} future equal-cost batches for references alone, or {best["conditional_confirmation_campaign_break_even_additional_equal_cost_batches"]} additional batches for the measured campaign. This assumes reuse without further validation costs. Identical inputs can be cached. No operating-machine or end-to-end optimizer saving has been measured.')
    p('The LTE requests N_KICKS=40, but the PyAT importer defaults to NumIntSteps=10. Explicit step policies and refinement are therefore recorded. Matching step counts does not prove ELEGANT equivalence; no native-ELEGANT cross-code validation was available. All failed variants and the unresolved reference point are retained.')
    p('A longer post-selection backcheck used 128 launches and 512 turns. The selected compiler met the same gate; a subsequently added analytic20 comparator gave an observed 3.86x first-workload ratio, with only one baseline timing. This is not independent confirmation. Further single-point diagnostics were nonmonotone: one boundary launch survived 40/80 steps, was lost at 160, and survived at 320. Fine-pair agreement is therefore not a proof of physical convergence; these boundary cases remain refinement-sensitive.')
    p('The package includes original licensed model, portable C/header sources, frozen protocols and executed sources, raw arrays, independent audits and offline replay. From research/bnl_tracking, install requirements in an isolated Python environment; use build_kernel.py to build with GCC, check_results.py for offline audit, and replay_confirmation.py for a new live run. Recorded outputs are immutable.')
    h('Requested independent evaluation')
    p('A useful next assessment is a BNL-maintained lattice and accuracy contract, including relevant apertures, momentum offsets, nonlinear errors and long-horizon requirements. Test the native analytic-pass workflow as well as the compiler. Adoption should follow a measured complete-cost advantage under that contract; this packet does not recommend connecting the prototype to machine controls.')
    def footer(c,doc):
        c.setFont('ReviewSans',7.5);c.setFillColor(colors.HexColor('#526471'))
        c.drawString(48,28,'Independent review prototype | public historical model | no operational endorsement')
        c.drawRightString(letter[0]-48,28,str(doc.page))
    SimpleDocTemplate(str(out),title='Guarded fixed-momentum tracking on a public NSLS-II design model',author='Nonlinear Hamiltonian research programme',pagesize=letter,rightMargin=48,leftMargin=48,topMargin=42,bottomMargin=48).build(story,onFirstPage=footer,onLaterPages=footer)
    print(out)


if __name__=='__main__':main()
