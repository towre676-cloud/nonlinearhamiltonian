"""Readable spacing for Unicode mathematical prose; historical excerpts untouched."""
import json,re,pathlib
P=pathlib.Path(__file__).resolve().parent
pairs=[('thefirst','the first'),('thelast','the last'),('thetwo','the two'),('thethree','the three'),('thefour','the four'),('thefinite','the finite'),('theinfinite','the infinite'),('theconstant','the constant'),('thepositive','the positive'),('thenegative','the negative'),('thelinear','the linear'),('thenonlinear','the nonlinear'),('thesame','the same'),('theclaimed','the claimed'),('therecovered','the recovered'),('thestated','the stated'),('theactual','the actual'),('theinitial','the initial'),('thecorrect','the correct'),('thehistorical','the historical'),('theordinary','the ordinary'),('theproposed','the proposed'),('ispositive','is positive'),('iszero','is zero'),('isone','is one'),('isnonzero','is nonzero'),('isfalse','is false'),('istrue','is true'),('isfinite','is finite'),('isnegative','is negative'),('isreal','is real'),('isconstant','is constant'),('giveszero','gives zero'),('givesone','gives one'),('firsttwo','first two'),('lasttwo','last two'),('fullcycle','full cycle'),('finiteband','finite band'),('highercumulants','higher cumulants'),('perlayer','per layer'),('everypositive','every positive'),('everynonzero','every nonzero'),('eachcoordinate','each coordinate'),('eachfactor','each factor'),('allterms','all terms'),('allother','all other'),('allpositive','all positive'),('allnegative','all negative'),('allhigher','all higher'),('allthree','all three'),('bothsides','both sides'),('withthe','with the'),('fromthe','from the'),('forthe','for the'),('andthe','and the'),('ofthe','of the'),('tothe','to the'),('inthe','in the'),('onthe','on the'),('bythe','by the'),('eachterm','each term'),('thattail','that tail'),('isnot','is not'),('thetarget','the target'),('zeroat','zero at'),('unitcircle','unit circle'),('operatornorm','operator norm'),('operatorlimit','operator limit'),('traceclass','trace class'),('rankone','rank one'),('ranktwo','rank two'),('timeinverse','time inverse'),('fullrank','full rank'),('current-spectrumdeflation','current-spectrum deflation'),('unit-singularsubspace','unit-singular subspace'),('zerofor','zero for'),('onefor','one for'),('oneand','one and'),('nonzeroand','nonzero and')]
def clean(s):
 s=re.sub(r'(?<=[a-z])(?=[A-Z])',' ',s)
 s=re.sub(r'([A-Z]{2,})([a-z]{3,})',r'\1 \2',s)
 s=re.sub(r'(?<=[A-Za-z])(?=[Α-ω])|(?<=[Α-ω])(?=[A-Za-z])',' ',s)
 for a,b in pairs:s=s.replace(a,b)
 s=re.sub(r'([,;])(?=[A-Za-zΑ-ω])',r'\1 ',s)
 s=re.sub(r'\.(?=[A-Z][a-z])','. ',s)
 return re.sub(' +',' ',s)
E=json.loads((P/'entries.json').read_text())
for e in E:
 for k in ('title','status','summary','limits','extension'):e[k]=clean(e[k])
 e['definitions']=[clean(v) for v in e['definitions']]
 for group in ('result','example'):
  for k,v in e[group].items():e[group][k]=clean(v)
 for k in ('question','math','finish'):e['original'][k]=clean(e['original'][k])
(P/'entries.json').write_text(json.dumps(E,ensure_ascii=False,indent=2)+'\n')
