import json
from fractions import Fraction
from pathlib import Path
import partner_lab as P
E=P.E;checks=[]
def check(name,condition):
    assert condition,name;checks.append({'name':name,'status':'passed'})
check('Exact parser rational coefficients',P.parse('q^2/3-2*p')=={(2,0):Fraction(1,3),(0,1):Fraction(-2)})
for text in ["__import__('os').system('x')",'q/p','q**(-1)','unknown','1/0']:
    try:P.parse(text);raise AssertionError('Accepted '+text)
    except (ValueError,ZeroDivisionError):pass
    check('Rejects unsupported expression '+text,True)
check('Zero numerator',P.parse('0')=={})
check('Monomial finite all-degree example',P.classify(3,5)['finite_basis_exponents']==[[0,0],[0,1],[0,2],[1,0],[1,1],[1,17],[2,0],[3,5]])
check('Univariate exact space',P.classify(0,5)['exact_basis'].endswith('c<=2'))
check('Coordinate exchange explicit',P.classify(5,1)['exchange_c_d'] is True)
check('Balanced active dimensions',P.classify(3,3)['active_quotient_dimension']==6 and P.classify(4,4)['active_quotient_dimension']==4)
check('Sextic exceptional partner',E.exact_partner(P.parse('q^3*p^3'),P.parse('q*p^11')))
check('Higher monomial partner',E.exact_partner(P.parse('q^3*p^5'),P.parse('q*p^17')))
check('Perturbed core full-space invariance',P.core_demo()['answer']=='span{1,H}')
for n,dim in [(2,3),(3,2),(4,2),(6,3),(10,3)]:check('Homogeneous quartic kernel degree'+str(n),len(E.homogeneous_kernel(P.parse('q^4+p^4'),n))==dim)
print(json.dumps({'status':'passed','check_count':len(checks),'checks':checks}))
