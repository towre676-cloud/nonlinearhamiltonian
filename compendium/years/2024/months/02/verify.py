"""Portable exact checks of February 2024 reconstructed examples.

This verifies declared mathematical examples, not historical completeness or
the empirical validity of a concentration or storage model.
"""
from fractions import Fraction as F
from pathlib import Path
import json,math

HERE=Path(__file__).resolve().parent
checks=[]
def check(id,name,condition,detail):
 assert condition,name
 checks.append(dict(id=id,name=name,status='passed',detail=detail))

# Base-dimension exponents in the order length, amount, mass.
add_units=lambda *args:tuple(sum(z) for z in zip(*args))
concentration=(-3,1,0);area=(2,0,0);depth=(1,0,0);molar_mass=(0,-1,1)
check('Y24-02-001','The missing length dimension',add_units(concentration,area)==(-1,1,0) and add_units(concentration,area,depth,molar_mass)==(0,0,1),
 'Concentration×area is amount/length; including depth and molar mass gives mass.')
litres_per_km3=1000**3*1000
check('Y24-02-001','Exact cubic conversion',litres_per_km3==10**12,'1km³=10^9m³=10^12L; a factor of 10^6L/km³ is not the SI conversion.')
C=F(1,10**6);A=F(10)*1000**2;M=F('55.845')
mass_kg_per_m=C*A*1000*M/1000
check('Y24-02-001','Exact depth-dependent mass coefficient',mass_kg_per_m==F('558.45'),{'kg_per_metre_depth':str(mass_kg_per_m),'scope':'The stated concentration, area and molar mass are stipulated inputs.'})
h=F(5,2);volume_litres=A*h*1000;amount=C*volume_litres;mass_kg=M*amount/1000
check('Y24-02-001','Worked slab calculation',volume_litres==25000000000 and amount==25000 and mass_kg==F('1396.125'),{'new_example_depth_metres':str(h),'volume_litres':str(volume_litres),'moles':str(amount),'kilograms':str(mass_kg)})
check('Y24-02-001','What added depth reproduces the old final number',mass_kg_per_m*F(1,1000)*1000==F('558.45'),'A newly chosen depth of 0.001m yields 558.45g; this depth is not claimed to have appeared in the historical conversation.')

A0=F('30.37');B0=F('9.8');ratio=A0/B0
low=F('30.365')/F('9.85');high=F('30.375')/F('9.75')
check('Y24-02-002','Stipulated area ratio',ratio==F(3037,980) and A0*10**6/(B0*10**6)==ratio,{'exact_ratio':str(ratio),'decimal':float(ratio),'scope':'Arithmetic on historical approximate inputs, not contemporary geographic measurements.'})
check('Y24-02-002','Conditional rounding enclosure',low==F(6073,1970) and high==F(81,26) and 3<low<=ratio<=high<4,{'enclosure':[str(low),str(high)],'integer_area_bound':3,'scope':'An explicitly added deterministic rounding model, not a confidence interval.'})
check('Y24-02-002','Area versus width packing counterexample',F(20)*F(1,2)>math.pi and 2>F(1,2),'The target rectangle has surplus area but insufficient width for a radius-one disk. Rotating a disk does not change its width.')
check('Y24-02-002','Union area differs from summed overlap',F(6)+F(5)-F(2)==9,'Two constructed zones of areas six and five with overlap two have union area nine, not eleven.')

Q=F(3600);I=F(2);R=F(1,10);duration=Q/I
E0=3*Q+Q/2
loss=R*I*I*duration
start_voltage=4-R*I;end_voltage=3-R*I
delivered=(start_voltage+end_voltage)*I*duration/2
check('Y24-02-003','Independent integral storage balance',duration==1800 and E0==12600 and loss==720 and delivered==11880 and E0==loss+delivered,
 {'seconds':str(duration),'stored_joules':str(E0),'loss_joules':str(loss),'delivered_joules':str(delivered),'method':'Storage is integrated in charge; delivered power is independently integrated as an affine function of time.'})
check('Y24-02-003','Charge and energy unit conversions',Q/3600==1 and E0/3600==F(7,2) and loss/3600==F(1,5) and delivered/3600==F(33,10),
 {'capacity_ampere_hours':1,'stored_watt_hours':str(E0/3600),'loss_watt_hours':str(loss/3600),'delivered_watt_hours':str(delivered/3600)})
for q in [F(0),Q/4,Q/2,Q]:
 voc=3+q/Q
 for current in [F(0),F(3,2),F(2)]:
  e_dot=-voc*current;pout=(voc-R*current)*current;heat=R*current**2
  assert e_dot+pout+heat==0
check('Y24-02-003','Pointwise balance samples',True,'Exact rational evaluation accompanies the chain-rule proof. The chosen storage model is an editorial reconstruction of a qualitative historical fragment.')

entries=json.loads((HERE/'entries.json').read_text())
assert len(entries)>=3
for e in entries:
 o=e['original']
 assert o['month']=='2024-02' and o['date'].startswith('2024-02-')
 assert o['evidence']=='A' and o['original_question'] is None
 assert 'A@'+o['date'] in o['source_excerpt']
 assert o['question'].startswith('Reconstruction:')
checks.append(dict(id='MONTH-2024-02',name='Attribution and receipt audit',status='passed',detail='Every current entry has a dated assistant fragment, a reconstructed question and a null original user prompt. Mathematical checks do not establish full-month retrieval.'))
(HERE/'checks.json').write_text(json.dumps({'month':'2024-02','checks':checks,'count':len(checks),'status':'passed'},ensure_ascii=False,indent=2))
print(json.dumps({'month':'2024-02','checks':len(checks),'status':'passed'}))
