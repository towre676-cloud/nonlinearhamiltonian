import json
from pathlib import Path
P=Path(__file__).resolve().parent
entries=[]
def add(n,date,evidence,field,title,origin,receipt,excerpt,question,summary,defs,name,statement,proof,setup,calc,conclusion,limits,extension,refs=()):
 id=f'Y24-07-{n:03d}'
 entries.append(dict(id=id,title=title,status='Revised classical development with scoped worked result',summary=summary,definitions=defs,result=dict(name=name,statement=statement,proof=proof),example=dict(setup=setup,calculation=calc,conclusion=conclusion),limits=limits,extension=extension,references=[dict(label=a,url=b) for a,b in refs],original=dict(date=date,month='2024-07',evidence=evidence,field=field,concept=title,origin=origin,question=question,math=statement,finish='Check the stated proof and reproduce the worked example under its explicit hypotheses.',kind='Developed mathematical revision',refs=[],source_excerpt=excerpt,retrieval_receipt=receipt,original_question=None,attribution_note='The historical evidence is an assistant-only retrieval summary or a truncated topic fragment. This source excerpt quotes that summary, not a verified original transcript. The revised question, proof and example are newly authored here; no absent user prompt or original theorem is reconstructed.')))

add(1,'2024-07-02','A','Measure theory','An undefined Ψ measure needs an actual transport law',
 'The assistant listed Ψ-measure and ergodic theory without recovered axioms.','root_followups.json#0','Ψ-measure/ergodic theory for synaptic plasticity',
 'Which measure and transformation are defined, and is Ψ a new structure or a conjugate presentation of an old one?',
 'The surviving label does not define a mathematical theory. A precise replacement is to ask what a measurable coordinate transport preserves. This yields an exact invariant-measure and ergodicity statement, while preventing a decorative prefix from being mistaken for additional mathematical power. The example is deliberately finite so that every invariant set and orbit can be checked directly.',
 ['Let (X,Σ,μ) be a probability space, T:X→X a measurable measure-preserving map, and ψ:X→Y a measurable bijection with measurable inverse. Define ν=ψ_*μ and S=ψTψ⁻¹. Ergodicity means every measurable set invariant modulo null sets has probability zero or one.'],
 'Measurable conjugacy preserves invariant measure and ergodicity',
 'S preserves ν. Moreover T is ergodic exactly when S is ergodic. Integrals satisfy ∫_Y f dν=∫_X f∘ψ dμ whenever the integral is defined.',
 'For a measurable A⊆Y, ν(S⁻¹A)=μ(ψ⁻¹S⁻¹A)=μ(T⁻¹ψ⁻¹A)=μ(ψ⁻¹A)=ν(A). Invariant sets correspond by ψ⁻¹, and their probabilities are unchanged, proving both directions of the ergodicity assertion. The integral formula follows first for indicator functions, then finite simple functions and finally integrable functions by the usual approximation argument. Nothing in the transport creates a new invariant or a new probability law unless some structural requirement is changed.',
 'Use X={0,1,2,3}, uniform measure, T(j)=j+1 modulo4, and the relabeling ψ=(0↔2).',
 'The only subsets invariant under the four-cycle are the empty set and the whole set, so T is ergodic. Its conjugate S has the same single orbit with labels permuted. A point indicator has integral1/4 in both presentations. Yet T is not mixing: the probability of returning to the same singleton is periodic rather than approaching the product of probabilities.',
 'Invariance, ergodicity and mixing are distinct conditions. A reversible relabeling preserves them rather than improving them.',
 'No definition of Ψ-numbers or a new Ψ-measure was recovered. The theorem concerns a specified classical measurable conjugacy and does not validate the historical applied interpretation.',
 'If Ψ is intended to discard information or change the measure, specify that map and compute which invariants survive; compare the result with the reversible case rather than assuming equivalence.')

add(2,'2024-07-02','A','Information theory','Ψ mutual information and capacity need a channel',
 'The assistant named Ψ-mutual information and Ψ-capacity without a recovered definition.','root_followups.json#0','Ψ-mutual information and Ψ-capacity',
 'What channel law and input constraint define the information quantity, and can a relabeling change it?',
 'A channel capacity is an optimization over input distributions for a declared conditional law. It cannot be obtained by attaching a new symbol to mutual information. The binary symmetric channel provides a complete example in which the optimum can be proved exactly, and a reversible relabeling theorem states what a renamed representation can and cannot change.',
 ['For finite random variables, I(X;Y)=Σp(x,y)log₂[p(x,y)/(p_X(x)p_Y(y))]. For a channel W(y|x), capacity is sup_{p_X}I(X;Y), without an additional cost constraint here. Let h₂(ε)=−εlog₂ε−(1−ε)log₂(1−ε), with endpoint values defined by continuity.'],
 'Capacity of a binary symmetric channel',
 'For Y=X⊕N, with N independent Bernoulli(ε), the capacity is1−h₂(ε) bits per use and is attained by a uniform input. Bijections of the input or output alphabet preserve mutual information and capacity when the channel is transported consistently.',
 'Independence gives H(Y|X)=H(N)=h₂(ε), regardless of the input distribution. Since a binary variable has entropy at most one, I(X;Y)=H(Y)−h₂(ε)≤1−h₂(ε). A uniform input makes Y uniform and attains equality. For a bijection, each joint probability and its two marginals are merely assigned a new index; the defining information sum is unchanged. The optimization domains are also put in bijection, proving the capacity statement.',
 'Take ε=1/4 and compare the endpoint cases.',
 'The capacity is1−h₂(1/4)≈0.1887218755 bits/use. At ε=0 the channel is noiseless and has capacity one; at ε=1/2 its output is independent of its input and capacity is zero. A known deterministic bit flip ε=1 also has capacity one, since the receiver can invert it. Thus an error probability is not by itself an information-loss measure without its channel convention.',
 'The useful object is the conditional distribution and its optimization, with every change of coordinates handled explicitly.',
 'The historical Ψ-capacity formula was not recovered. This elementary channel theorem does not establish that any observed system obeys a memoryless binary channel or that a particular code attains its asymptotic capacity.',
 'Add an explicit input cost or memory law, derive the new optimization domain, and determine whether symmetry still proves the maximizing input distribution.',
 [('Shannon A Mathematical Theory of Communication','https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf')])

add(3,'2024-07-02','A','Categories and coding','Functorial relabeling does not automatically preserve code distance',
 'Ψ-category theory, cryptography and coding were listed together without definitions.','root_receipts.json#0','Ψ-category theory, Ψ-cryptography/coding',
 'Which structure does the proposed transformation preserve: composition, probability, metric distance, or computational difficulty?',
 'A genuine categorical transport can preserve every composition law while changing the usual Hamming distance of a code. This small counterexample separates structural equivalence from a coding guarantee. It also explains why naming a category cannot supply a cryptographic hardness assumption: additional metric or computational structure must be part of the objects and morphisms.',
 ['A binary length-n code is a subset C⊆{0,1}ⁿ. Its minimum distance is the least Hamming distance between distinct codewords. A category has identity maps and associative composition; a transport by bijections ψ_X sends f:X→Y to ψ_Y f ψ_X⁻¹.'],
 'Composition transport and the missing metric condition',
 'The transported maps preserve identity and composition. An ambient Hamming isometry is sufficient to preserve every code’s pairwise distances and minimum distance; transporting the metric also preserves all distances. Preserving every ambient pairwise distance is exactly the isometry condition. A non-isometric map may nevertheless preserve a particular code or its minimum distance.',
 'For composable f and g, (ψ_Zgψ_Y⁻¹)(ψ_Yfψ_X⁻¹)=ψ_Z(gf)ψ_X⁻¹. Transporting an identity gives an identity. Define d_ψ(ψx,ψy)=d_H(x,y); this pulled-back metric preserves distances tautologically. Keeping the old coordinate Hamming metric instead imposes the nontrivial condition d_H(ψx,ψy)=d_H(x,y). Composition preservation alone says nothing about that equality. Consequently a theorem about one category of sets cannot silently be interpreted as an equivalence of metric-code objects.',
 'Take the repetition code C={000,111} and let ψ swap111 with001 while fixing000 and the other words.',
 'C has minimum distance three and hence can uniquely correct one bit error by nearest-codeword decoding. The image code is {000,001}, whose minimum distance is one and which has no one-error guarantee. The map ψ is still a bijection and transports every set map functorially. By contrast, permuting coordinates or flipping a fixed subset of bits preserves all Hamming distances.',
 'The example proves exactly which extra hypothesis is missing: distance preservation, not more elaborate notation.',
 'No Ψ code or concrete security construction was recovered. The coding guarantee is combinatorial and does not imply resistance to an adversary, while a public bijection need not make inversion computationally difficult.',
 'Specify a category of metric codes with isometric morphisms, then separately formulate any claimed hard inversion problem and test whether the transport changes its algorithmic complexity.')

add(4,'2024-07-03','A','Dimensional arithmetic','A purchasing-power ratio is a stipulated unit conversion',
 'A historical assistant divided5.75 by0.56 and interpreted the result as a purchasing-power equivalent.','root_followups.json#0','5.75/0.56≈10.27',
 'Which ratio is dimensionless, which direction is the conversion, and what uncertainty belongs to the divisor?',
 'The arithmetic can be corrected and bounded without treating historical economic inputs as current measurements or advice. The central mathematical issue is the meaning of a ratio and the conditioning of division. If a price-level ratio is defined in one direction, reversing it changes division into multiplication. A numerical result alone cannot determine which economic interpretation was intended.',
 ['Take a stipulated positive quantity w=5.75 and a stipulated dimensionless conversion ratio r=0.56. Define an index-adjusted quantity q=w/r only after choosing that convention. The reciprocal convention would instead use wr. The values are historical inputs, not current data.'],
 'Exact quotient and interval propagation',
 'The quotient is575/56≈10.26785714. If the divisor is only known to lie in[r₋,r₊]⊂(0,∞), then w/r lies exactly in[w/r₊,w/r₋]. Its local relative sensitivity to r is−1.',
 'Convert5.75=23/4 and0.56=14/25 to fractions; their quotient is(23/4)(25/14)=575/56. For fixed w>0 the function r↦w/r is strictly decreasing, so the interval endpoints reverse. Differentiation gives dq/dr=−w/r² and dlogq/dlogr=−1. If both numerator and denominator vary in positive intervals, monotonicity in each variable gives the sharp rectangle bound[w₋/r₊,w₊/r₋]. These are deterministic uncertainty statements, not assumptions about a sampling distribution.',
 'Suppose the ratio is only specified to lie between0.54 and0.58 while w remains fixed.',
 'Then the quotient lies between575/58≈9.91379310 and575/54≈10.64814815. Reporting10.27 without this roughly0.37-scale uncertainty could suggest a precision not supported by the stipulated input. Using the reverse conversion giveswr=3.22, demonstrating why the ratio definition must precede calculation.',
 'A transparent conversion states units, ratio direction, date of inputs and uncertainty separately. Here only the mathematical quotient is certified.',
 'A real purchasing-power index needs an explicit basket, reference location, date and aggregation rule. None of those specifications can be recovered from this one arithmetic fragment, and the result is not a present-day compensation comparison.',
 'For a defined weighted basket, propagate component-price intervals through the index and prove which comparisons remain invariant under a change of reference basket.')

add(5,'2024-07-14','A','Control theory','PID gains require a plant and a stability calculation',
 'The assistant gave gains1.2,0.5,0.1 in an applied control example.','root_receipts.json#0','PID parameters K_p=1.2, K_i=0.5, K_d=0.1',
 'For a stated scalar plant, what characteristic polynomial do these gains produce, and which inequalities guarantee stability?',
 'Three controller gains are not a stability theorem. A benign normalized scalar plant provides an exact calculation that can be completed without inferring anything about the original apparatus. This revision also distinguishes an ideal derivative term from a realizable filtered derivative and keeps time units visible.',
 ['Use the normalized plant G(s)=1/(τs+1), τ>0, and ideal controller C(s)=K_p+K_i/s+K_ds in a negative-feedback loop. Closed-loop poles are zeros of1+G(s)C(s), after the transfer expression is reduced. K_p is dimensionless here, K_i has inverse-time units and K_d has time units.'],
 'A complete second-order stability condition',
 'The characteristic polynomial is(τ+K_d)s²+(1+K_p)s+K_i. When τ+K_d>0, it has strictly left-half-plane roots exactly when1+K_p>0 and K_i>0.',
 'Multiply1+GC bys(τs+1) to obtain the polynomial. Divide by its positive leading coefficient. For a real monic quadratic s²+as+b, its roots either are real, in which case negative sum and positive product make both negative, or are a conjugate pair with real part−a/2. Thus a>0,b>0 is sufficient. Necessity follows from negative root sum and positive root product for two real negative roots or a left-half-plane conjugate pair. Marginal cases need separate treatment.',
 'Setτ=1 and use the historical gains K_p=6/5,K_i=1/2,K_d=1/10 as stipulated rational inputs.',
 'Multiplying by ten gives11s²+22s+5. Its roots are−1±√66/11, both negative since√66<11. The closed-loop transfer has numerator s²+12s+5 and denominator11s²+22s+5, so its high-frequency limit is1/11; this ideal derivative model has feedthrough rather than automatically suppressing high-frequency signals.',
 'The chosen model is stable by an exact calculation. The gains themselves do not certify any other plant.',
 'Delays, actuator constraints, sensor noise and derivative filtering change the model. In particular a derivative filter adds state and changes the characteristic polynomial. No operational instructions for the historical device follow from this abstract example.',
 'Add a specified first-order derivative filter and classify the resulting cubic’s stability region with a Routh–Hurwitz certificate.',
 [('Åström and Murray Feedback Systems','https://fbsbook.org/')])

add(6,'2024-07-14','A','Logarithmic scales','A logarithmic threshold needs a reference and a squared-amplitude convention',
 'The assistant used a decibel threshold in the same applied control discussion.','root_receipts.json#0','sound trigger threshold 80 dB',
 'Is the logarithm applied to power or amplitude, and which reference quantity makes the argument dimensionless?',
 'The mathematics of a logarithmic scale can be stated independently of a trigger or hardware implementation. The decisive distinction is between a power-like quantity and an amplitude whose square produces that quantity. Forgetting this distinction produces a factor-of-two error in the logarithm and a much larger multiplicative error after exponentiation.',
 ['For positive power-like P and reference P₀, define L=10log₁₀(P/P₀). If P/P₀=(A/A₀)² under a fixed matched relation, then L=20log₁₀|A/A₀|. The ratio inside either logarithm is dimensionless.'],
 'Multiplicative ratios become additive level differences',
 'A level difference ΔL corresponds to power ratio10^(ΔL/10), or amplitude ratio10^(ΔL/20) when the squared-amplitude hypothesis holds. Adding independent equal powers adds10log₁₀2 to the level, not twice the level.',
 'Subtract the two logarithmic definitions and use logx−logy=log(x/y); exponentiation in base ten gives the ratio formulas. For equal powers P+P=2P, the difference from the original level is10log₁₀(2P/P)=10log₁₀2. The amplitude formula follows from log(a²)=2loga for a>0. If amplitudes are coherent and are added before squaring, their phase relation changes the resulting power, so the independent-power addition rule cannot be reused.',
 'Compare a ten-unit level increase and a doubling of independent power in a purely normalized example.',
 'A ten-unit increase multiplies power by ten and amplitude by√10. A power doubling increases the level by approximately3.0102999566. Two equal in-phase amplitudes instead double amplitude and quadruple power, giving approximately6.0205999133. Opposite phases can cancel, illustrating why one must specify what is being added.',
 'A level is a dimensionless logarithmic representation of a declared ratio. It cannot be interpreted without its reference and relation between amplitude and power.',
 'The old threshold’s reference, calibration and measurement protocol were not recovered. This derivation supplies no acoustic-exposure assessment or control-device calibration and does not infer a physical intensity from an isolated level number.',
 'For a stochastic sum of components with specified cross-correlations, derive the expected squared amplitude and compare coherent, uncorrelated and anticorrelated limits.')

add(7,'2024-07-20','A','Algebra and dimensions','Ideal power identities as a typed algebraic system',
 'The historical passage contained resistance, voltage, current and power formulas; applied body-current content is excluded.','root_followups.json#1','R=V²/P; I=V/R',
 'What assumptions make the power identities equivalent, and which quantities are determined by a chosen pair of positive inputs?',
 'The useful mathematical content is a small nonlinear change of variables, not an implementation design. In a stated ideal resistive model, two positive parameters determine the others, and dimensional consistency can be audited. The application-specific numerical instructions and estimates in the old exchange are not carried forward.',
 ['Take positive normalized variables R,V,I,P satisfying V=IR and P=VI. The assumptions exclude time variation, reactive components and sign changes. In dimensional form, resistance has units voltage/current and power has units voltage×current.'],
 'Equivalent positive parametrizations',
 'For positive V and P, the unique positive solution is I=P/V and R=V²/P. Conversely any positive I and R give V=IR and P=I²R. These are equivalent coordinates on the positive solution set.',
 'Substitute V=IR into P=VI to obtain P=I²R. Solving the positive equations in the other direction gives I=P/V and R=V/I=V²/P. Positivity ensures division and rules out ambiguity from taking square roots: if P,R are given, I=√(P/R) and V=√(PR) select positive branches. Every displayed expression has matching dimensions. A ratio with an incompatible unit cannot be made valid by a numerical coincidence.',
 'Use a benign dimensionless algebra example V=2 and P=1.',
 'Then I=1/2 and R=4. Reconstructing gives IR=2, VI=1 and I²R=1. If V and P are instead uncertain positive intervals, R=V²/P is increasing in V and decreasing in P, giving the sharp bound[V₋²/P₊,V₊²/P₋]. This interval statement identifies how input uncertainty propagates without assuming a probability distribution.',
 'The mathematical certificate is a consistent parametrization and an interval bound, not a recommendation about a physical circuit.',
 'The ideal scalar identities do not characterize a time-varying impedance, frequency-dependent losses, a human body or a safe operating range. All such applied claims and operational calculations from the source are excluded from this mathematical development.',
 'For a specified complex impedance, distinguish real average power from apparent power and prove the relevant inequality using a defined inner product.')

add(8,'2024-07-20','A','Partition theory','Euler’s product yields an exact partition recurrence',
 'Modular forms and Euler’s pentagonal theorem were named in an application list.','root_followups.json#1','partition theory (Euler’s pentagonal number theorem)',
 'Which generating series counts partitions, and what exact coefficient recurrence follows from Euler’s identity?',
 'A precise generating-function calculation is a much stronger result than a broad application list. It specifies the ring, the counted objects and a recurrence that can be replayed with integers. The all-orders product identity is classical; the newly supplied work is its derivation of the recurrence and an independent finite replay.',
 ['Work in the formal ring Z[[q]], where each coefficient of an infinite product depends on finitely many factors. Let p(n) count unrestricted partitions, with p(0)=1 and p(n)=0 for n<0. Its generating series is P(q)=∏_{m≥1}(1−q^m)⁻¹.'],
 'Pentagonal recurrence with formal-series scope',
 'Euler’s classical identity ∏_{m≥1}(1−q^m)=Σ_{k∈Z}(−1)^kq^{k(3k−1)/2} implies p(n)=Σ_{k≥1}(−1)^(k−1)[p(n−k(3k−1)/2)+p(n−k(3k+1)/2)]. Each coefficient equation is finite.',
 'For each part size m, the series1+q^m+q^{2m}+… records its possible multiplicities. Multiplying gives one monomial for each partition and proves the formula for P. Multiply Euler’s identity by P to obtain one. For n>0, its nth coefficient is zero; isolate the k=0 term p(n), pair positive and negative k, and move the remaining terms to the other side. Formal finiteness follows because the pentagonal exponents grow quadratically. This argument derives the recurrence from the stated classical theorem, rather than pretending a finite coefficient test proves the entire Euler identity.',
 'Compute p(n) both by adding allowed part sizes and by the recurrence.',
 'The first values for n=0,…,10 are1,1,2,3,5,7,11,15,22,30,42. At n=5 the recurrence is p(4)+p(3)−p(0)=5+3−1=7. The verifier independently counts by finite generating-product dynamic programming and checks agreement through a declared cutoff.',
 'The result identifies an exact counting object and a replayable certificate. The modular-form connection requires additional transformation laws and is not established merely by writing a q-series.',
 'This is an unrestricted-partition identity. Distinct, bounded or colored partitions require different products. No proposed physical or economic cyclic interpretation follows from the coefficient equality.',
 'Choose a constrained partition language, derive its own product or transfer recurrence and determine whether any modular transformation theorem actually applies.',
 [('NIST DLMF Unrestricted Partitions','https://dlmf.nist.gov/27.14')])

add(9,'2024-07-21','T','Differential geometry','An eleven-dimensional space does not determine an operator',
 'The source fragment mentioned an eleven-dimensional variety X and then truncated at an operator symbol.','root_receipts.json#0','Cognitive-mathematical framework included 11D variety X, D^',
 'What field, regularity and operator type are intended, and which identities follow from the chosen definitions?',
 'Dimension alone does not specify a manifold, variety, metric, probability law or differential operator. The fragment therefore cannot justify reconstructing its missing D. A self-contained replacement develops the exterior derivative on a stated eleven-dimensional affine coordinate space and proves exactly the structural identity it supplies.',
 ['Take ordinary smooth real functions on R¹¹ with coordinates x₁,…,x₁₁. A k-form is a sum of coefficient functions times alternating products dx_{i₁}∧…∧dx_{i_k}. The fiber dimension is C(11,k). Define d(f dx_I)=Σ_j(∂_j f)dx_j∧dx_I.'],
 'The de Rham differential has square zero',
 'For twice continuously differentiable coefficients, d²=0. The sequence has fiber dimensions1,11,55,165,330,462,462,330,165,55,11,1 in degrees0 through11.',
 'Expand d² on a coordinate form. Every pair j≠l contributes two terms with equal mixed derivatives and opposite wedge signs; repeated indices vanish because dx_j∧dx_j=0. Commutation of mixed derivatives then cancels all terms. Counting increasing k-tuples gives C(11,k), and binomial symmetry gives matching dimensions in degrees k and11−k. The total exterior-algebra fiber dimension is2¹¹, while alternating the dimensions gives(1−1)¹¹=0. These algebraic counts do not identify the global cohomology of an arbitrary eleven-dimensional space.',
 'Use f=x₁x₂ and the one-form α=x₁dx₂.',
 'Here df=x₂dx₁+x₁dx₂ and d(df)=dx₂∧dx₁+dx₁∧dx₂=0. Also dα=dx₁∧dx₂ and d(dα)=0. A metric-dependent Laplacian or Dirac operator would require additional data and would not be interchangeable with this degree-raising differential.',
 'The example supplies a real operator, its type and a proved identity while preserving the gap in the historical record.',
 'The original operator expression is truncated, its geometric field and structure are unspecified, and no evidence establishes that an empirical system has this dimension or this de Rham model.',
 'If a complete operator is recovered, state its domain, codomain, grading and analytic domain, then compare its actual identities with the differential constructed here.')

add(10,'2024-07-21','A','Partial differential equations','A coupled diffusion model needs an energy balance',
 'The assistant proposed coupled fields with diffusion, a correction M and a gradient term.','root_followups.json#1','∂φ/∂t=D∇²φ+γ(ψ−φ)',
 'Which specified coupled PDE has a well-posed dissipative structure, and what modes remain conserved?',
 'The recovered partial formula leaves the other field’s evolution and the correction undefined. A symmetric linear pair provides a fully solvable mathematical comparison. Its energy identity and Fourier eigenvalues determine precisely when perturbations decay, without assigning unproved meanings to the field labels.',
 ['On a periodic interval let u_t=D u_xx−γ(u−v) and v_t=D v_xx+γ(u−v), with D>0 and γ>0. Assume sufficiently smooth real solutions. Define total field s=u+v, difference r=u−v, and energy E=∫(u²+v²)/2 dx.'],
 'Exact mode decomposition and dissipation',
 'The fields satisfy s_t=D s_xx and r_t=D r_xx−2γr. The total spatial integral of s is conserved, while E′=−D∫(u_x²+v_x²)dx−γ∫(u−v)²dx≤0.',
 'Add and subtract the equations to obtain the decoupled systems. For energy, multiply each equation by its own field, integrate, and integrate the second derivatives by parts; periodic boundary terms cancel. The coupling contribution is−γu(u−v)+γv(u−v)=−γ(u−v)². Integrating the s-equation proves conservation. On a Fourier mode e^{ikx}, s has exponent−Dk² and r has exponent−Dk²−2γ. Therefore the only undamped mode is a constant common value of u and v, fixed by the total mean.',
 'Take a2π-periodic domain, D=γ=1, u(x,0)=cosx and v(x,0)=0.',
 'Initially s=r=cosx. Thus u(x,t)=(e^(−t)+e^(−3t))cosx/2 and v(x,t)=(e^(−t)−e^(−3t))cosx/2. Every displayed coefficient solves the corresponding two-dimensional linear ODE exactly. Both fields converge to zero here because their common conserved mean is zero.',
 'The theorem shows what a concrete diffusion-coupling choice guarantees. It does not establish that an arbitrary added correction M preserves any energy or stability.',
 'Nonlinear terms, unequal diffusivities and nonperiodic boundaries can change the balance. A gradient term must come from a specified potential and metric before a dissipation argument is available. The original model was not validated by this replacement.',
 'Add a named potential F(u,v), derive the modified energy and identify conditions for boundedness or loss of convexity before studying bifurcations.')

add(11,'2024-07-21','A','Motivic invariants and entropy','A product of motivic measure and entropy needs a scalar realization',
 'The assistant proposed a complexity index CCI(X,t)=μ_mot(X)E(t).','root_followups.json#1','CCI(X,t)=μ_mot(X)×E(t)',
 'In which ring does the motivic value live, which realization makes the product numerical, and is the result even nonnegative?',
 'A motivic class and a real entropy need not belong to the same scalar system. Choosing a realization makes a product meaningful, but can immediately expose failures of a proposed complexity interpretation. This is a mathematical diagnostic of the formula; the historical empirical interpretation is not assumed or validated.',
 ['For complex algebraic varieties, the Grothendieck ring K₀(Var_C) imposes[X]=[Z]+[X∖Z] for a closed subvariety Z and multiplication[X][Y]=[X×Y]. A motivic measure is a specified ring homomorphism from this ring. Compactly supported Euler characteristic χ_c is an integer-valued realization. For a finite distribution p, H(p)=−Σp_i logp_i.'],
 'A numerical realization can vanish or be negative on nontrivial objects',
 'The scalar functional J(X,p)=χ_c(X)H(p) is well defined. It is not intrinsically a nonnegative or separating complexity index: a smooth elliptic curve has χ_c=0, and a smooth projective curve of genus g≥2 has χ_c=2−2g<0.',
 'For a smooth projective complex curve, Betti numbers are(1,2g,1), giving Euler characteristic1−2g+1. Since H(p)≥0, multiplying by this Euler characteristic gives zero for genus one and negative values for higher genus whenever the entropy is positive. Additivity and multiplicativity of χ_c explain why it is a valid motivic realization, but those algebraic properties do not imply positivity or sensitivity to the geometric distinctions a proposed index hopes to capture. A different realization changes the numerical question and must be declared.',
 'Let p=(1/2,1/2), so H=log2, and compare projective curves of genus0,1,2.',
 'The resulting J values are2log2,0 and−2log2. All three curves are geometrically substantial, so zero cannot mean absence of structure, and the negative value cannot be silently read as a nonnegative complexity score. A formal class μ_mot(X) without a scalar realization would not even produce these real numbers.',
 'The product is an authored functional only after its codomain is fixed. Its desired interpretation requires additional axioms and tests.',
 'The source does not supply an actual motivic-measure definition, scalar realization, entropy estimator or validation. This example neither reconstructs those missing choices nor establishes a measurement of cognition.',
 'State desired positivity, additivity, normalization and separation requirements, then test whether any proposed realization can satisfy them simultaneously on an explicit family of varieties.',
 [('Stacks Project varieties and cohomology background','https://stacks.math.columbia.edu/'),('Deligne Théorie de Hodge II','https://www.numdam.org/item/PMIHES_1971__40__5_0/')])

add(12,'2024-07-21','A','D modules and Hodge theory','A flat connection is not automatically a mixed Hodge module',
 'The assistant named mixed-Hodge and D-module functors without recovered construction data.','root_followups.json#1','mixed-Hodge/D-module functors',
 'Which connection, rational structure and filtrations support a claimed Hodge-theoretic object?',
 'A concrete rank-one connection demonstrates both the available analytic calculation and the additional structure that remains missing. It prevents a named functor from being treated as an automatic attachment to an arbitrary differential equation. The Hodge-module theory is classical and deep; this entry develops a small conditional example and does not claim to reconstruct the absent functor.',
 ['On C* consider the differential equation x y′=αy for α∈C, equivalently a rank-one connection with local horizontal sections proportional to x^α. A loop around zero changes a chosen logarithm by2πi. Quasi-unipotent monodromy means that some positive power of the monodromy operator is unipotent.'],
 'Exact monodromy and a necessary structural test',
 'The rank-one monodromy is multiplication by exp(2πiα). It is quasi-unipotent exactly when this scalar is a root of unity, equivalently α is rational modulo integers with zero imaginary part. A filtered regular-holonomic D-module alone does not automatically specify a mixed Hodge module.',
 'On a simply connected sector choose logx and solve y=exp(αlogx). Analytic continuation around one positive loop multiplies y by exp(2πiα). In rank one, unipotent means scalar one, so quasi-unipotence is the existence of m≥1 with exp(2πimα)=1. This requires mα to be an integer. Hodge-module data additionally include a compatible rational perverse-sheaf structure, weight and Hodge filtrations, and conditions involving nearby cycles and admissibility; none are provided merely by solving the differential equation. Where a chosen admissible theory requires quasi-unipotence, the scalar calculation is a direct necessary test.',
 'Compare α=1/2 and α=√2.',
 'The first monodromy is−1 and becomes trivial after two turns, compatible with a double-cover origin for the local system. The second never becomes one under a finite positive power. Both connections are regular singular at zero, so regular singularity alone does not enforce the extra quasi-unipotence condition. Compatibility with a full Hodge structure remains a separate construction even in the first case.',
 'The example separates an explicitly computed local system from the much stronger filtered and rational structure required by the intended theory.',
 'No universal functor from arbitrary proposed operators to mixed Hodge modules is established. The rank-one quasi-unipotence calculation is not a sufficient characterization of mixed Hodge modules, and the exact target category must be stated.',
 'Construct an actual geometric family and its Gauss–Manin connection, then identify its rational local system, filtrations and boundary monodromy rather than adding those labels after the fact.',
 [('Morihiko Saito On the definition of mixed Hodge modules','https://arxiv.org/abs/1307.2140')])

add(13,'2024-07-21','A','Homology','Reduced homology and intersection cohomology remove different phenomena',
 'Reduced-homology refinements and intersection cohomology appeared in adjacent July21 frameworks.','root_followups.json#1','reduced-homology refinements; intersection cohomology',
 'Which chain complex or singular-space invariant is intended, and which information is changed by the refinement?',
 'Reduced homology removes the universal connected-component class; intersection cohomology modifies allowable behavior at singular strata. They do not perform the same correction and cannot be substituted for one another. Two elementary spaces exhibit the different mechanisms without claiming a general singularity classification.',
 ['For a nonempty finite simplicial complex, reduced homology adds the augmentation C₀→F summing vertex coefficients. For a connected space, H₀≅F but reduced H₀=0. Middle-perversity intersection cohomology is a different theory for appropriately stratified singular spaces, with its own allowable-chain conditions.'],
 'A graph calculation and a singular-curve comparison',
 'An unfilled triangle has ordinary Betti numbers(1,1), reduced Betti numbers(0,1), and a filled triangle has ordinary Betti numbers(1,0). For an irreducible rational nodal projective curve, ordinary Betti numbers are(1,1,1), while its intersection cohomology agrees with the normalization P¹ and has Betti numbers(1,0,1).',
 'The triangle graph has three vertices and three edges. Its boundary matrix has rank two because the graph is connected, so dimH₁=3−2=1 and dimH₀=3−2=1. The augmentation removes the latter class. Filling the triangle adds a two-simplex whose nonzero boundary spans the cycle, killing H₁ without disconnecting the space. For the nodal curve, identifying two distinct points of its normalization P¹ produces the extra ordinary loop. The normalization description of its intersection complex prevents treating that singular identification as a new permissible middle-dimensional class; thus its intersection cohomology is the cohomology of P¹. This last identification is a standard singular-curve theorem, not a finite matrix proof of general intersection theory.',
 'Compare a connected loop, a filled loop and the nodal rational curve.',
 'Reducing the triangle’s degree-zero homology leaves its genuine one-cycle intact. Filling it changes the topology and removes that cycle. Passing to intersection cohomology of the singular curve instead changes how the singular stratum contributes, while retaining the top-dimensional orientation class.',
 'Every claimed refinement must name its input space, coefficient field, chain theory and the information it is meant to retain.',
 'The historical framework did not define a simplicial filtration or a stratification. These examples do not convert an unspecified dataset into a topological invariant or infer a physical meaning for a Betti number.',
 'Construct the relevant finite complex or normalization map explicitly, compute both invariants and document which classes are lost and why.',
 [('Goresky and MacPherson Morse theory and intersection homology theory','https://www.math.ias.edu/~goresky/pdf/MorseIH.pdf')])

add(14,'2024-07-21','A','Contact geometry','Legendrian structure begins with a contact form and a tangent condition',
 'Legendrian invariants were named without a recovered contact manifold or knot.','root_followups.json#1','Legendrian invariants',
 'Which contact structure and embedded curve define the Legendrian problem, and which invariants are actually preserved?',
 'The word Legendrian supplies a strong differential constraint only after the ambient contact structure is fixed. A simple calculation in standard three-dimensional contact space makes that constraint explicit, while the standard front formulas show how genuine knot invariants require additional global data. This is a classical construction, not evidence for a Legendrian model of an unspecified application.',
 ['Use R³ with contact form α=dz−y dx; its contact planes are kerα and α∧dα is nowhere zero. A parametrized curve γ(t)=(x(t),y(t),z(t)) is Legendrian when α(γ′)=z′−yx′=0. A contactomorphism may preserve the plane field by multiplying α by a nowhere-zero function.'],
 'A local Legendrian curve and a contact scaling',
 'The curve γ(t)=(t,t,t²/2) is Legendrian. For any a≠0, S_a(x,y,z)=(ax,ay,a²z) satisfies S_a*α=a²α and preserves the contact planes. Where x′≠0, a front projection to(x,z) determines y=dz/dx.',
 'Differentiating the curve gives z′=t and yx′=t, so the tangent condition holds exactly. Pull back dz−y dx under S_a to obtain a²dz−(ay)(a dx)=a²α. Since the scalar is nonzero, its kernel is unchanged. The front-slope formula is simply the tangent equation divided by x′. At points where x′=0 this division is unavailable, and generic fronts use semicubical cusps rather than an arbitrary smooth graph; that singularity data is part of the invariant formulas.',
 'For a standard generic Legendrian unknot front with two cusps and no crossings, fix the usual front convention.',
 'The Thurston–Bennequin number is writhe minus half the cusp count, giving tb=0−2/2=−1. With one upward and one downward oriented cusp, the corresponding rotation count is zero. These are invariants of a specified closed Legendrian knot under the stated conventions; the open polynomial curve above has no such closed-knot invariant assigned by this calculation.',
 'A tangent identity, a contactomorphism and a global knot invariant are three separate mathematical claims, each with its own data.',
 'The old record supplies none of the ambient form, embedding or front diagram. The local example does not classify Legendrian knots, and tb together with rotation is not a complete invariant in general.',
 'Provide an explicit front diagram, verify its Legendrian lift and compute how the declared invariants change under stabilization or contact isotopy.',
 [('John Etnyre Legendrian and Transversal Knots','https://arxiv.org/abs/math/0306256')])

# Incorporate the later, more precise recovered July21 assistant fragments.
e=entries[8]
e['original'].update(evidence='A',origin='The July21 assistant called X an eleven-dimensional cognitive superspace and placed a symbol ψ in D^bMHM(X). No actual X, object, or operator construction was recovered.',retrieval_receipt='root_specifics.json#0',source_excerpt='11-dimensional cognitive superspace; ψ∈D^bMHM(X); rat_X:D^bMHM(X)→D^b_cs(X;Q)')
e['summary']='The fuller recovered fragment names an eleven-dimensional space and a derived category, rather than defining the space or a concrete differential operator. Dimension alone does not specify a manifold, variety, metric or probability law. A self-contained comparison develops the exterior derivative on ordinary R¹¹, proves its structural identity, and explicitly distinguishes this classical object from an unspecified derived Hodge-module object.'
e['limits']='The later fragment supplies the labels X and D^bMHM(X), but no actual variety, mixed Hodge module or geometric construction. An object of a derived category need not be an ordinary scalar field or a differential operator. The smooth real de Rham example is a newly chosen comparison, not an identification of the original symbols or an empirical dimensional claim.'
e=entries[11]
e['original'].update(retrieval_receipt='root_specifics.json#0',source_excerpt='rat_X:D^bMHM(X)→D^b_cs(X;Q), Dmod_X→D^b_coh(D_X), linked by DR_X')
e['summary']+=' In the classical setting, the rational realization rat and the underlying regular-holonomic D-module are compatible after complexification with the de Rham functor, using the chosen perverse normalization. Merely naming D^b_coh(D_X) is too broad to assert this regular-holonomic correspondence for every coherent D-module.'
e['limits']+=' The source’s actual rat/DR labels are thus recognized, while the appropriate regularity, rational structure and cohomological shifts must still be specified; arbitrary coherent D-modules are not automatically in the Riemann–Hilbert equivalence.'
e=entries[12]
e['original'].update(retrieval_receipt='root_specifics.json#0',source_excerpt='CH*(L)=Ker ∂_n/Im ∂_(n+1); IH^k(X)=H^k(p_*IC•Q_X)')
e['limits']+=' Writing ker∂/im∂ is the generic homology recipe only after ∂²=0 is proved; it does not define a Legendrian-specific differential. Intersection cohomology requires a specified intersection complex, derived global pushforward and shift convention: for a pure complex d-dimensional variety with perverse normalization IC restricting to Q[d], IH^k(X)=H^(k−d)(RΓ(X,IC)). Omitting that convention shifts the groups.'
e=entries[13]
e['original'].update(retrieval_receipt='root_specifics.json#0',source_excerpt='Legendrian ξ_std=ker(dz−y dx)')

add(15,'2024-07-21','A','Aggregation and identifiability','Spatial averages can erase the diffusion parameter',
 'The assistant defined global functionals by integrating two spatial fields, alongside a diffusion-coupling system.','root_specifics.json#0','ψ_f(t)=∫N(x,t)dx, φ_f(t)=∫V(x,t)dx; ∂φ/∂t=D∇²φ+γ(ψ−φ)+K(t)',
 'Which parameters remain identifiable after a spatial field is replaced by its integral, and which modes does that observation erase?',
 'An integral observation can be mathematically exact yet lose every trace of a parameter. This issue can be resolved for a periodic linear diffusion-coupling model, using a closed equation for its averages and a nonconstant Fourier mode. The construction is a controlled comparison with the recovered field integrals; it does not assume that the historical labels denote measured quantities or a validated model.',
 ['Let u,v be smooth2π-periodic fields with u_t=D u_xx−γ(u−v) and v_t=D v_xx+γ(u−v), where D,γ>0. Define means U=(2π)⁻¹∫u dx and V=(2π)⁻¹∫v dx. Structural identifiability here means whether an ideal complete observation function uniquely distinguishes a stipulated parameter within this model.'],
 'A mean-only observation cannot identify a diffusion coefficient',
 'The exact mean equations are U′=−γ(U−V), V′=γ(U−V), independent of D. With the initial fields fixed, every D>0 gives the same mean observations. A nonconstant observed Fourier mode instead contains its decay rate Dk² and can distinguish D when its initial amplitude and coupling are known.',
 'The integral of each periodic second derivative is zero. Integrating the PDE therefore closes the two equations without a spatial approximation. Their sum is constant and their difference solves (U−V)′=−2γ(U−V). Hence U=(U₀+V₀+(U₀−V₀)e^(−2γt))/2, with the opposite sign for V. None of these expressions contains D. For s=u+v, however, the kth Fourier coefficient obeys s_k′=−Dk²s_k. If k≠0 and s_k(0)≠0 is known, observing its ratio at a positive time gives D=−log|s_k(t)/s_k(0)|/(k²t). Thus identifiability depends on both the forward equation and the observation operator.',
 'Compare D=1 and D=2 with γ=1, u(x,0)=1+cosx and v(x,0)=1−cosx.',
 'Both models have U(t)=V(t)=1 for every t. Their difference field is r=2e^(−(D+2)t)cosx, so it decays as e^(−3t) or e^(−4t). Mean-only data cannot separate the two exact solutions; a spatial contrast can. In this particular example the total nonconstant mode s is zero, so the corresponding contrast r must be observed instead.',
 'A scalar aggregate needs a proved information-retention claim before it can support parameter inference. Precise forward modeling does not undo loss introduced by the observation map.',
 'The conclusion assumes this stated periodic linear system and fixed initial fields. Boundary flux, forcing or a different observation may reveal D. Conversely unknown initial conditions or coefficients may create additional ambiguities. It is not an assertion about any actual empirical system.',
 'Given a finite collection of weighted spatial integrals, compute which Fourier eigenspaces lie in their common kernel and choose a further mathematical observation that removes a stated parameter ambiguity.')

assert len(entries)==15
P.joinpath('entries.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2))
print(json.dumps({'month':'2024-07','entries':len(entries),'words':sum(len(json.dumps(e,ensure_ascii=False).split()) for e in entries)}))
