from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parent
receipts=json.loads((ROOT/'root_coverage.json').read_text())
source=receipts[0]['result']['structuredContent']['messages'][0]['content'].splitlines()
entries=[]
def ref(label,url):return dict(label=label,url=url)
def add(n,needle,title,question,summary,definitions,name,statement,proof,setup,calculation,conclusion,limits,extension,references):
    line=next(x for x in source if needle in x)
    m=re.search(r'([UA])@(2025-08-\d\dT[0-9:]+Z)',line);assert m
    evidence,date=m.groups()
    entries.append(dict(id=f'Y25-08-{n:03}',title=title,status='Developed classical result with a scoped worked example',summary=summary,
        definitions=definitions,result=dict(name=name,statement=statement,proof=proof),
        example=dict(setup=setup,calculation=calculation,conclusion=conclusion),limits=limits,extension=extension,references=references,
        original=dict(date=date,month='2025-08',evidence=evidence,field='Analysis, arithmetic and geometry',concept=title,
          origin='Dated mathematical fragment recovered from the August2025 coverage sweep',question=question,math=statement,
          finish='Proof or derivation and worked example',kind='Revised mathematical treatment',refs=[r['url'] for r in references],
          source_excerpt=line,retrieval_receipt='root_coverage.json record0',original_question=None,
          attribution_note='The source line is retained exactly. The question, proposition and example are newly developed here; a verbatim historical prompt is not claimed.')))

add(901,'U@2025-08-02T05:10:45Z','An exact KP line soliton from a traveling-wave reduction',
 'Which tanh ansatz solves a precisely normalized KP equation, and how do amplitude, width and transverse slope determine speed?',
 'The source proposed a symbolic tanh solver. A complete solution begins by fixing the PDE normalization and deriving the algebraic constraints. The single-soliton family provides an exact benchmark for a symbolic solver and a numerical residual.',
 ['Use (u_t+6uu_x+u_xxx)_x+3s u_yy=0 with s=+1 or -1.',
  'Let X=x+ell*y-c*t, k>0, and impose decay of U(X), U-prime and U-double-prime at both infinities.'],
 'Exact traveling-wave and tau-function identity',
 'u(x,y,t)=2k² sech²(kX) solves KP when c=4k²+3s*ell². It also equals2 partial_x² log(1+exp(2kX)).',
 'Substitution gives [-cU-prime+6UU-prime+U-triple-prime]-prime+3s*ell² U-double-prime=0. Integrate twice using the stated decay to obtain U-double-prime+(3s*ell²-c)U+3U²=0. For f=sech²(kX), direct differentiation yields f-double-prime=4k²f-6k²f². Setting U=2k²f therefore gives U-double-prime=4k²U-3U²; the reduced ODE vanishes exactly at the stated speed. Differentiating log(1+exp(2kX)) twice gives k²sech²(kX), proving the tau representation. The tanh form is U=2k²[1-tanh²(kX)], so degree balancing M=2 becomes a verified consequence in this example.',
 'Choose k=1/2, ell=1 and s=+1.',
 'The amplitude is1/2, speed c=4 and profile U(X)=(1/2)sech²(X/2). At X=0, U=1/2 and U-double-prime=-1/4, so U-double-prime- U+3U²=-1/4-1/2+3/4=0. Its line-integrated mass is integral U dX=4k=2.',
 'All solution parameters and the PDE residual are determined analytically.',
 'A KP solution alone establishes neither a tsunami source model nor accuracy near shorelines, breaking waves or varying bathymetry. Those require additional equations and data.',
 'Extend the symbolic procedure to a two-exponential tau function and derive the interaction coefficient from the bilinear KP identity; verify the one-soliton limit before numerical comparisons.',
 [ref('Hirota, Exact Solution of the Korteweg-de Vries Equation for Multiple Collisions of Solitons','https://doi.org/10.1103/PhysRevLett.27.1192')])

add(902,'U@2025-08-04T15:37:10Z','Finite-field Hilbert90 as an exact descent calculation',
 'Can a norm-one element be written explicitly as v/Frobenius(v), and which part of this computation constitutes descent?',
 'The source requested a concrete Hilbert90 example rather than an unspecified obstruction. A quadratic finite field makes the cocycle, norm and coboundary entirely visible.',
 ['Let F49=F7[a]/(a²-3);3 is not a square in F7.',
  'The nontrivial Galois automorphism is sigma(a)=a^7=-a. A multiplicative1-cocycle for this cyclic group is specified by u with u*sigma(u)=1.'],
 'Explicit finite-field Hilbert90',
 'Every norm-one u in F49-star is v/sigma(v). The element u=5-a is obtained from v=1+a.',
 'The multiplicative group F49-star is cyclic of order48. Its norm is x maps to x^8, whose image has order6 and whose kernel has order8. The homomorphism v maps to v/sigma(v)=v^(-6) has kernel F7-star of order6, hence image of order8. Every image element has norm1 by cancellation, so image and norm kernel coincide. For the explicit example, (1+a)/(1-a)=(1+a)²/(1-a²)=(4+2a)/5=5+6a=5-a in F7. Its norm is(5-a)(5+a)=25-3=22=1 modulo7. Thus the cocycle is a coboundary with an explicit witness.',
 'Represent field elements by pairs(r,s), meaning r+s*a, with multiplication(r,s)(t,v)=(rt+3sv,rv+st) modulo7.',
 'Enumeration gives48 nonzero elements,8 norm-one elements and8 distinct ratios v/sigma(v). The displayed ratio and norm both hold exactly in this pair arithmetic.',
 'The descent claim is certified by finite algebra, and its witness can be independently replayed.',
 'Hilbert90 eliminates this particular multiplicative cocycle obstruction. It does not solve arbitrary discrete logarithms or identify every arithmetic obstruction with a finite-field cocycle.',
 'Generalize the enumerator to F(q^n), compare the norm kernel with the image of v/sigma(v), and then separate linear-algebra cost from a discrete-logarithm representation of the same elements.',
 [ref('Milne, Class Field Theory, Hilbert90 and cyclic extensions','https://www.jmilne.org/math/CourseNotes/cft.html')])

add(903,'U@2025-08-04T15:22:05Z','A nonprincipal ideal gives an actual Picard obstruction',
 'What exact ideal-class obstruction survives after finite-field multiplicative cocycles have vanished?',
 'The proposed torsor-descent framework becomes concrete over the integers of Q(sqrt(-5)). An ideal can have a principal square while itself remaining nonprincipal; that is a genuine Picard-group phenomenon.',
 ['Let O=Z[a], a²=-5, the ring of integers of Q(sqrt(-5)). Let I=(2,1+a).',
  'For the fppf topology the Kummer sequence gives0→O-star/(O-star)²→H¹(Spec O,mu2)→Pic(O)[2]→0.'],
 'An explicit nonzero class of order2',
 'I has norm2, satisfies I²=(2), and is not principal. Its ideal class is a nonzero element of Pic(O)[2].',
 'Reduction modulo I sends a to1 in F2 and identifies O/I with F2, so the ideal norm is2. The square I² is generated by4,2+2a and-4+2a. All are divisible by2, and(2+2a)-(-4+2a)-4=2; hence I²=(2). If I were generated by r+s*a, its norm would be |r²+5s²|=2, impossible for integers r,s. Thus[I] is nonzero and2[I]=0. The fppf Kummer exact sequence places this obstruction in the image of a mu2 torsor. More explicitly, the isomorphism I-tensor-I→O given by multiplication followed by division by2 supplies a square trivialization of the invertible module I.',
 'Compare the norm equation for a generator with the explicit generators of the squared ideal.',
 'For s=0, r²=2 has no integral solution; for |s|>=1 the norm is at least5. Nevertheless the displayed integral combination of generators of I² equals2 exactly.',
 'The obstruction and its order are proved without an unprovided Selmer computation.',
 'At the prime2 the mu2 torsor need not be étale; the fppf topology is essential here. No claim about the complexity of general torsor descent follows.',
 'Compute the local trivializations of O direct-sum I with multiplication(v,w)→vw/2, then verify the transition cocycle and its Kummer boundary explicitly.',
 [ref('The Stacks Project, Kummer theory','https://stacks.math.columbia.edu/tag/03PK'),ref('Milne, Algebraic Number Theory','https://www.jmilne.org/math/CourseNotes/ant.html')])

add(904,'U@2025-08-05T06:22:34Z','Clutching produces a computable cohomological obstruction',
 'Which explicit obstruction distinguishes bundles with identical base dimension and structure group?',
 'A proposed universal degree delta=d+s leaves the actual obstruction group and class unspecified. Circle bundles on the same two-sphere give a complete small model in which every integer obstruction can occur.',
 ['Cover S² by northern and southern discs; on their equatorial overlap glue complex lines by g_m(exp(i*phi))=exp(i*m*phi), m an integer.',
  'Use the convention c1=[F/(2pi)]; reversing the clutching convention reverses both signs. In polar coordinates take A_N=(m/2)(1-cos theta)dphi and A_S=-(m/2)(1+cos theta)dphi.'],
 'Clutching degree and curvature certificate',
 'The resulting line bundle has first Chern number m and is trivial exactly when m=0. Fixed dimensions therefore do not determine its obstruction.',
 'On the overlap A_N-A_S=m*dphi, matching the logarithmic derivative of the transition function under the stated convention. Both local curvatures equal F=(m/2)sin(theta)dtheta-wedge-dphi. Its normalized integral is(2pi)^(-1) integral F=m. Changing a local trivialization on a disc multiplies the equatorial transition by a loop that extends across that disc and has winding0, so it cannot change m. Conversely, a degree-zero map S¹→U(1) is null-homotopic; its extension across a hemisphere removes the transition and trivializes the bundle. Thus the integer is both an obstruction and a complete invariant in this clutching problem.',
 'Keep the base S² and group U(1) fixed and choose m=0,1,2.',
 'The curvature integrals are0,2pi,4pi. All three models have identical base and group dimensions, while only the first bundle is trivial.',
 'A meaningful obstruction requires coefficients, degree and a class, all visible in this example.',
 'This calculation does not classify loop groups, gerbes or higher stacks. Their obstruction theories need their own coefficient objects and descent data.',
 'Construct a gerbe on a three-sphere from explicit triple-overlap data and determine the corresponding integral degree-three class, keeping the cocycle identities separate from dimensional labels.',
 [ref('Hatcher, Vector Bundles and K-Theory','https://pi.math.cornell.edu/~hatcher/VBKT/VB.pdf')])

add(905,'U@2025-08-02T00:45:27Z','An Eisenstein correction has an exact modular transformation law',
 'Which combination involving E2(9*tau) is genuinely modular, and why does its anomalous term cancel?',
 'The CP-moonshine manuscript used E2(9*tau) as an analytic lift. A scalar weight-two example gives an exact covariance benchmark before introducing unknown triplet representations or fitted physics parameters.',
 ['Use E2(tau)=1-24 sum(n>=1)sigma1(n)q^n with q=exp(2pi*i*tau).',
  'For N>1 define F_N(tau)=E2(tau)-N*E2(N*tau). For gamma in Gamma0(N), c is divisible by N.'],
 'Cancellation of the quasimodular anomaly',
 'F_N transforms with weight2 on Gamma0(N). Its holomorphic modular-form extension at the cusps is the standard weight-two Eisenstein construction.',
 'The classical formula is E2(gamma*tau)=(c*tau+d)²E2(tau)+[6/(pi*i)]c(c*tau+d). Since c is divisible by N, the integral matrix gamma_N=(a,Nb;c/N,d) lies in SL2(Z) and satisfies N*gamma*tau=gamma_N*(N*tau). Applying the same transformation to E2(N*gamma*tau) gives anomaly[6/(pi*i)](c/N)(c*tau+d). Multiplication by N makes this anomaly identical to the first one, so their difference vanishes. Holomorphy at cusps follows from the standard Eisenstein-series construction; the displayed calculation proves the covariance directly. It also shows why E2(N*tau) alone does not have the claimed homogeneous weight-two law.',
 'Take N=9 and compute the constant and q^9 coefficients.',
 'The constant is1-9=-8. Since sigma1(9)=13, the q^9 coefficient is-24*13+216*1=-96; the q coefficient is-24. The nonzero constant term means this example is not a cusp form.',
 'The normalization and exact covariance are fixed independently of numerical success percentages.',
 'No unprovided Delta(27) representation, mock completion or shadow integral has been certified. Finite sampled transformation tests cannot establish a global modular identity.',
 'Specify exact S and T matrices and prove their group relations, then derive the completed vector-valued transformation law with a stated shadow and convergence domain.',
 [ref('Mathlib, exact transformation formulas for the weight-two Eisenstein series','https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/ModularForms/EisensteinSeries/E2/Transform.html')])

add(906,'A@2025-08-08T23:35:01Z','A Mellin split gives a reproducible central L-value formula',
 'What exact functional-equation identity can replace an unstable central-value quadrature?',
 'The historical approximate-functional-equation outputs disagree even in sign. For a weight-two form, splitting the Mellin integral at the Fricke fixed point gives a rapidly convergent center formula whose normalization can be checked directly.',
 ['Let f(tau)=sum(n>=1)a_n exp(2pi*i*n*tau) be a weight-two cusp form of level N.',
  'Assume f(i/(N*t))=epsilon*N*t²*f(i*t), epsilon=+1 or -1, and |a_n|<=2n. Put c=2pi/sqrt(N).'],
 'Exact central-value series with an explicit tail',
 'L(1,f)=(1+epsilon)sum(n>=1)(a_n/n)exp(-c*n). Truncation after M terms has absolute tail at most2|1+epsilon|exp[-c(M+1)]/(1-exp(-c)).',
 'The Mellin identity gives L(1,f)=2pi integral(0,infinity)f(i*t)dt. Set A=1/sqrt(N) and substitute t=1/(N*u) in the lower integral. The Fricke identity turns it into epsilon integral(A,infinity)f(i*u)du. Thus the full integral equals(1+epsilon) times the upper integral. Termwise integration is justified by absolute exponential convergence on t>=A and gives the stated series. The coefficient bound yields |a_n/n|<=2, so a geometric series bounds the omitted tail. In particular epsilon=-1 forces the center value to vanish. For an elliptic newform, the bound follows from |a_n|<=d(n)sqrt(n) and the elementary inequality d(n)<=2sqrt(n).',
 'For N=11 use f=eta(tau)²eta(11*tau)², whose Fricke sign is epsilon=+1.',
 'The q product q*product(1-q^n)²(1-q^(11n))² yields exact integer coefficients. Twenty terms give approximately0.2538418608559107, with analytic tail below3e-17 under the coefficient bound. The numerical approximation has its own rounding error; the tail formula is independent of quadrature-node choices.',
 'The local normalization, functional equation and truncation error are exposed rather than hidden in a generic AFE routine.',
 'The theorem assumes genuine modular coefficients and the stated Fricke law. Applying it to arbitrary surrogate traces would not construct a modular L-function.',
 'Implement interval exponential evaluation and retain the exact Fourier coefficients plus the analytic tail to produce a completely rounded central-value enclosure.',
 [ref('LMFDB, weight-two level11 modular forms','https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/11/2/a/'),ref('Milne, Modular Functions and Modular Forms','https://www.jmilne.org/math/CourseNotes/MF.pdf')])

add(907,'U@2025-08-04T02:41:44Z','Filtered Frobenius membership needs a precision certificate',
 'What can a finite p-adic residual prove about a proposed filtered Frobenius splitting condition?',
 'The proposed Generator5 returns a vanishing code from phi(v)-p^(-1)v in Fil1. Even before a genuine syntomic realization is supplied, a filtered-vector-space example explains which finite-precision conclusions are valid.',
 ['Let V=Q5², Fil1=span(e2), phi=diag(1,5), and pi:V→V/Fil1 be first-coordinate projection.',
  'Define the integral-scaled obstruction R(v)=pi[(5phi-I)v]. Membership phi(v)-v/5 in Fil1 is equivalent to R(v)=0.'],
 'Exact obstruction and finite-precision distinction',
 'For v=(x,y), R(v)=4x. Exact splitting is equivalent to x=0; a zero residue modulo5^N proves only x=0 modulo5^N.',
 'The first coordinate of(5phi-I)v is4x, while the second is24y and disappears in the quotient. Since4 is a5-adic unit, multiplication by4 preserves the5-adic valuation. Therefore an observed residual of valuation k<N certifies a nonzero obstruction, while a residual represented by0 modulo5^N only bounds its valuation below by N. It cannot distinguish exact0 from5^N times a nonzero unit. This conclusion uses the exact filtered matrix and the declared input precision; it does not depend on an empirical threshold. The denominator p^(-1) must also be accounted for when converting a residual precision back to the original equation.',
 'Choose v=(25,1).',
 'R(v)=100 has5-adic valuation2. It is0 modulo25 but100 modulo125, so the precision-two verdict cannot establish vanishing and the precision-three verdict disproves it.',
 'The example produces an explicit precision-stable nonvanishing decision once sufficient digits are available.',
 'This is a stipulated filtered linear-algebra model, not a computed syntomic cohomology group or a Selmer certificate for an elliptic curve.',
 'For an actual filtered(phi,N) module, compute quotient matrices over a valuation ring, certify their elementary divisors and propagate input precision through each denominator and inverse.',
 [ref('Milne, Class Field Theory, local fields and valuations','https://www.jmilne.org/math/CourseNotes/cft.html')])

add(908,'U@2025-08-03T03:56:33Z','The classical Heegner hypothesis is a local test',
 'Does the proposed pair E:y²=x³-x and K=Q(i) satisfy the classical split-prime Heegner hypothesis?',
 'A formal q-deformation must begin with a correctly specified classical construction. The conductor and quadratic field already decide whether the standard X0(N) Heegner-point setup applies.',
 ['Use the classical Heegner hypothesis: every rational prime dividing the conductor N splits in the imaginary quadratic field K.',
  'For the source curve N=32. Q(i) has discriminant-4; a prime dividing the discriminant is ramified rather than split.'],
 'Failure at2 and a split-prime alternative',
 'The source pair fails the classical split-prime hypothesis because2 ramifies in Q(i). In Q(sqrt(-7)),2 splits, so the prime condition for level32 is satisfied.',
 'In Z[i],2=-i(1+i)², proving ramification directly. In the ring of integers Z[(1+sqrt(-7))/2], the generator theta satisfies theta²-theta+2=0. Modulo2 its polynomial is X(X-1), with two distinct roots. Dedekind factorization, or the corresponding two distinct norm-two ideals, therefore gives splitting of2. These calculations check the exact local premise of the classical modular-curve construction. They do not supply the height formula, prove a point has infinite order or define a q-deformation. A generalized Heegner construction allowing ramification would require its own different hypotheses.',
 'Compare discriminants-4 and-7 at the unique prime dividing32.',
 'The first has discriminant divisible by2 and a repeated factor; the second has discriminant congruent1 modulo8 and distinct factors over F2. No numerical period calculation is required for this decision.',
 'The starting field can be chosen to meet a precise classical condition before any formal deformation is attempted.',
 'A satisfied Heegner hypothesis alone does not imply a nonzero L-derivative or a non-torsion point. Formal power-series coordinates are not automatically points on the original elliptic curve.',
 'Specify the modular parametrization and CM ideal, compute a genuine classical Heegner point, verify its curve equation, and only then formulate an algebraic deformation with a proved specialization map.',
 [ref('Gross and Zagier, Heegner points and derivatives of L-series','https://doi.org/10.1007/BF01388809')])

add(909,'U@2025-08-01T16:13:11Z','A calibrated search has a computable multiplicity cost',
 'How does searching many modular-coordinate fits change the interpretation of the best apparent anomaly?',
 'The source moonshine interpretation selected fitted coordinates and reported a significance value. A finite family of tests gives an exact mathematical benchmark for distinguishing one prespecified statistic from a selected maximum.',
 ['Let p1,...,pM be valid null p-values, so Pr(pj<=u)<=u for each j.',
  'Define p_adj=min(1,M*min_j pj). Independence is not assumed for the familywise bound.'],
 'Finite-search familywise control',
 'Pr(p_adj<=alpha)<=alpha. If the p-values are independent uniform variables, Pr(min pj<=u)=1-(1-u)^M exactly.',
 'The event p_adj<=alpha is contained in the union of events pj<=alpha/M. The union bound gives probability at most sum_j alpha/M=alpha, proving the adjusted test. Under independence, the complementary event pj>u for all j has probability(1-u)^M, giving the exact formula. The theorem concerns the whole specified search family: fitting extra parameters, choosing observables after inspection or retaining only successful seeds enlarges that family or requires a different null calibration. A held-out evaluation can avoid reusing the same observations for both selection and confirmation.',
 'As a newly stipulated illustration, take M=1000 independent null tests and u=0.001.',
 'The chance of at least one such small p-value is1-0.999^1000, approximately0.6323. Thus a selected value0.001 does not carry the interpretation of one prespecified test.',
 'The cost of selection can be computed without asserting any physical mechanism or interpreting fitted couplings as predictions.',
 'The exact independence formula is illustrative. The historical search size, data covariance and original analysis are unavailable, so no corrected historical significance is claimed.',
 'Freeze the observables and coordinate map, simulate the complete selection procedure under a stated correlated null, and compare a separately held-out statistic with that calibrated distribution.',
 [])

add(910,'A@2025-08-05T15:20:07Z','Compounding distinguishes price growth from purchasing-power decay',
 'What mathematical relation connects an annual inflation factor, an annual purchasing-power loss and a thirty-year cumulative ratio?',
 'The source challenged an invented annual rate. The mathematical repair is to state a hypothetical rate transparently and distinguish the two reciprocal quantities before inserting any empirical index.',
 ['Let the annual price multiplier be1+pi>0 and the annual purchasing-power multiplier be1-d>0.',
  'Purchasing power is reciprocal to the price index for a fixed nominal amount and a fixed basket.'],
 'Exact reciprocal compounding',
 '(1-d)=1/(1+pi), so d=pi/(1+pi). After T years the price factor is(1+pi)^T and the purchasing-power factor is(1-d)^T.',
 'If one basket costs P0 initially and PT=P0(1+pi)^T later, a fixed nominal amount buys PT/P0 times fewer baskets; its relative purchasing power is P0/PT. Equating the annual reciprocal factor with1-d gives the stated conversion. For variable annual rates pi_t, replace the power by the product of(1+pi_t); averaging rates arithmetically does not in general reproduce that product. The constant equivalent annual rate is exp[T^(-1)sum log(1+pi_t)]-1. These are index identities, not estimates of any country or historical period.',
 'Stipulate d=0.033 for T=30; do not treat it as a measured historical rate.',
 'The purchasing-power factor is0.967^30, approximately0.3654, and the reciprocal price factor is about2.7366. The corresponding price inflation rate is0.033/0.967, approximately3.4126 percent, rather than3.3 percent.',
 'The example separates a mathematical scenario from the missing empirical rate and keeps numerator and denominator conventions consistent.',
 'Actual purchasing power depends on a declared basket, index construction, time window and source series. No current inflation or investment conclusion is inferred from this hypothetical example.',
 'Given a specified historical index series, compute log growth by interval, chain the factors exactly to the available decimal precision, and quantify how alternative basket definitions change the result.',
 [])

(ROOT/'early_entries.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2))
print(json.dumps({'entries':len(entries),'ids':[e['id'] for e in entries]}))
