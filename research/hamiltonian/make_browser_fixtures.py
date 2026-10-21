from pathlib import Path
import sys,json,itertools
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'independent'));import engine as E
cases=list(itertools.product(range(7),range(7),range(8),range(8)))+[(1,5,5,3),(3,3,1,11),(3,5,1,17),(1,3,23,7)]
out=[]
for a,b,c,d in cases:
    H=E.monomial(a,b);G=E.monomial(c,d);s=E.moyal(H,G);terms=[]
    for k,p in sorted(s.items()):
        for (q,r),coef in p.items():terms.append({'hbar':k,'q':q,'p':r,'coefficient':str(coef)})
    out.append({'params':[a,b,c,d],'terms':terms,'exact':not E.defects(H,G),'active':bool(E.poisson(H,G))})
(ROOT/'tmp/browser_fixtures.json').write_text(json.dumps(out,separators=(',',':')))
print(len(out))
