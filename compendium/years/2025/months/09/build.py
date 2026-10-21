from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
entries=[]
def source(date,needle,ev):
    for p in sorted(HERE.glob('root*.json')):
        for i,r in enumerate(json.loads(p.read_text())):
            for c in r.get('result',{}).get('content',[]):
                for line in c.get('text','').splitlines():
                    if date in line and needle.lower() in line.lower() and (ev=='T' or (ev+'@'+date) in line):return line,f'{p.name} record {i}'
    raise ValueError((date,needle))
def E(date,needle,ev,field,title,question,summary,defs,statement,proof,setup,calculation,conclusion,limits,extension,refs=()):
    excerpt,receipt=source(date,needle,ev)
    entries.append(dict(id=f'Y25-09-{len(entries)+1:03d}',title=title,status='Classical mathematics with newly authored proof or worked finite certificate',summary=summary,definitions=defs,result=dict(name=title,statement=statement,proof=proof),example=dict(setup=setup,calculation=calculation,conclusion=conclusion),limits=limits,extension=extension,references=[dict(label=l,url=u) for l,u in refs],original=dict(date=date,month='2025-09',evidence=ev,field=field,concept=title,origin='Recovered dated mathematical subject; attribution limits are preserved.',question=question,math=statement,finish='Worked result, explicit example, stated limits and a precise extension',kind='Revised mathematical treatment',refs=[u for _,u in refs],source_excerpt=excerpt,retrieval_receipt=receipt,original_question=None,attribution_note='The historical source identifies a topic or summarizes an exchange. U labels user subject matter, not authorship of adjacent assistant formulas. A labels an assistant passage. All revised questions and mathematical developments are newly authored; no verbatim original prompt is claimed.')))

E('2025-09-01','Banach','A','Fixed-point theory','A compositional contraction certificate with an exact fixed point',
 'Which complete invariant domain and Lipschitz bounds certify the entire composition, and what error does its residual rigorously control?',
 'The contraction-verifier project has a substantial mathematical core: a product of verified operator bounds can certify a unique fixed point and provide an a posteriori error bar. The certificate must apply to the actual composed map, rather than to labels assigned to its stages.',
 ['A map T on a complete metric space is a contraction if d(Tx,Ty)≤q d(x,y) for one uniform q<1 and T maps that space into itself.', 'For T=A∘R∘Γ∘S, Lipschitz constants multiply. On Rᵈ, S_t=I+t11ᵀ has Euclidean norm max(1,|1+td|).'],
 'A self-map with contraction constant q has a unique fixed point x*. For every x, d(x,x*)≤d(x,Tx)/(1−q). For d=2,t=1/4 and T(x)=(1/4)S_t x+(1,0), the exact constant is3/8 and x*=(22/15,2/15).',
 'Starting at x₀, the successive increments satisfy d(x_(n+1),x_n)≤qⁿd(x₁,x₀). Their geometric sum makes the iterates Cauchy; completeness gives a limit, and Lipschitz continuity makes it fixed. Two fixed points have distance at most q times their distance, forcing equality. The triangle inequality gives d(x,x*)≤d(x,Tx)+q d(x,x*), proving the residual bound. For S_t, the all-ones direction has eigenvalue1+td and its orthogonal complement eigenvalue1; symmetry turns their maximum absolute value into the operator norm. The worked affine map has matrix[[5/16,1/16],[1/16,5/16]], with eigenvalues3/8,1/4. Solving(I−M)x=(1,0) gives the stated rational fixed point.',
 'Certify the zero initial state without first using the closed-form answer.',
 'Its residual norm is one, so the general bound gives ||x*||₂≤8/5. Direct substitution of(22/15,2/15) verifies the fixed-point equation exactly. After n iterations the initial increment bound gives error at most(8/5)(3/8)ⁿ. An SVD-based certificate can be replaced here by exact eigenvalues, avoiding uncertainty about numerical singular-value tolerances.',
 'The verifier now has an executable theorem: a named operator, a proved contraction margin, an exact solution and a certified iteration error.',
 'A computed ε or a sampled Jacobian does not certify a global bound. Completeness, domain invariance and all stage bounds remain necessary; a nonnormal matrix can have spectral radius below one while its chosen norm exceeds one.',
 'For a block-coupled system, construct a nonnegative matrix of cross-Lipschitz bounds and choose positive weights making its weighted maximum norm less than one.',
 [('Mathlib Banach contraction theorem','https://leanprover-community.github.io/mathlib4_docs/Mathlib/Topology/MetricSpace/Contracting.html')])

E('2025-09-29','cos','A','Nonlinear iteration','The cosine iteration has a rigorous tail certificate',
 'Which uniform interval bound validates the cosine fixed point and the proposed summable-tail condition?',
 'The τ-Reflection fragment proposed τ_(k+1)=cosτ_k, a tail norm and a local derivative indicator. This example supports a complete theorem, but a derivative at one iterate must be replaced by a bound on a forward-invariant interval.',
 ['Let x_(n+1)=cos x_n for a real initial value. After the first iteration x₁∈[−1,1].', 'On I=[−1,1], cos maps I into[cos1,1]⊂I and has Lipschitz constant q=sin1<1. Define the increment tail R_N=Σ_(k=N)^∞|x_(k+1)−x_k|.'],
 'There is one real solution r=cos r, every real initial condition converges to r, and R_N≤|x_(N+1)−x_N|/(1−sin1) for N≥1. In particular the increment tail is absolutely summable. The sequence x_n² need not decrease.',
 'The mean-value theorem bounds |cos x−cos y| by(sin1)|x−y| on I. The interval is complete and invariant, so the contraction theorem gives its unique fixed point and convergence after the first step. Any real fixed point already lies in[−1,1], so this is also global uniqueness on R. Consecutive increments decrease at least geometrically with factor q; summing proves the tail estimate. The pointwise number |sin x_N| can be smaller than the supremum derivative on a containing interval, so it alone is not a uniform certificate. Starting at zero gives x₀²=0 and x₁²=1, disproving a blanket decreasing-energy interpretation of H_n=x_n².',
 'Construct a narrow certified interval and estimate a concrete tail.',
 'Alternating Taylor bounds for cosine show cos(739/1000)>739/1000 and cos(740/1000)<740/1000. Since cos x−x is strictly decreasing on this positive interval, the unique fixed point lies between these rationals. The same Taylor bounds can be implemented with rational arithmetic. Once two consecutive iterates are known within error δ, the tail formula gives a bound using their difference enlarged by2δ, divided by1−sin1; this makes rounding uncertainty explicit.',
 'The proposed convergence statistic now follows from a uniform contraction theorem and an explicit geometric tail, rather than from a threshold written into a metadata record.',
 'A sheaf carrying fields named tailL1,rho and eps does not thereby satisfy a descent or fixed-point theorem. The result concerns this scalar iteration and does not construct a categorical embedding.',
 'Use interval arithmetic to propagate an invariant rational interval and replace the conservative sin1 bound by the maximum derivative on that interval, producing sharper certified stopping rules.',
 [('Mathlib contraction theorem','https://leanprover-community.github.io/mathlib4_docs/Mathlib/Topology/MetricSpace/Contracting.html')])

E('2025-09-20','cocycle','U','Abelian groups and invariants','Transport defects satisfy a cocycle law and a sharp norm bound',
 'What are the source and target groups of each defect, and which compatibility makes the claimed scalar invariant survive transport?',
 'The user supplied unusually concrete formalization goals: free abelian leaf groups, cokernel defects, a composition law and a linear τ functional. A finite-rank model proves the cocycle and stability statements directly and exposes the compatibility required of τ.',
 ['Represent a finite free abelian leaf group by Zⁿ. For transport F:Zⁿ→Zᵐ, source state a and target state b, define Δ_f=b−Fa∈Zᵐ.', 'For a later transport G:Zᵐ→Zᵏ with target c, define Δ_g=c−Gb. A scalar functional is τ_w(x)=wᵀx for integer weights w.'],
 'Δ_(g∘f)=GΔ_f+Δ_g. If source and target weights satisfy w_mᵀF=w_nᵀ, then |τ_(w_m)(b)−τ_(w_n)(a)|≤||w_m||∞||Δ_f||₁. The constant ||w_m||∞ is the best uniform coefficient for this inequality.',
 'Expand G(b−Fa)+(c−Gb)=c−GFa; the intermediate state cancels exactly. The compatibility rewrites the scalar difference as w_mᵀ(b−Fa)=w_mᵀΔ_f. The triangle inequality gives |Σw_iΔ_i|≤Σ|w_i||Δ_i|≤max|w_i|Σ|Δ_i|. To prove sharpness, choose Δ to be a unit coordinate vector at an index maximizing |w_i|, with its sign chosen accordingly; equality holds. Zero defect therefore certifies conservation under the explicit weight compatibility, while a nonzero defect can still be invisible to a chosen functional.',
 'Take F=[[1,1],[0,1]], a=(1,2), b=(4,1), and target weight w=(2,−1).',
 'The transported state is Fa=(3,2), so Δ=(1,−1), with norm₁=2. The source weight is Fᵀw=(2,1), giving τ_target(b)=7 and τ_source(a)=4, a difference3 bounded by2·2=4. A subsequent map G=[1,1] sends this defect to zero: the two coordinate discrepancies cancel under that observation. Thus a conserved coarse scalar need not imply that the full transport defect vanished.',
 'This supplies a meaningful formal invariant and a quantitative error certificate, including an exact explanation of observational blindness.',
 'A cokernel class is a further quotient, not the same object as the raw vector. A functional descends to cokerF only when it annihilates imF, a different condition from the transport compatibility above. Hash equality supplies neither condition.',
 'For a transport network, impose compatible weights at all vertices and derive a pathwise bound by propagating each local defect through downstream operators; optimize weights to minimize the resulting certificate.',
 [('Stacks Project cokernels and exact sequences','https://stacks.math.columbia.edu/tag/010I')])

E('2025-09-20','cokernel','U','Integral linear algebra','Cokernel certificates detect torsion that real residuals can miss',
 'Which exact integer quotient encodes the obstruction, and how does its Smith form differ from a small floating residual?',
 'The free-abelian formalization naturally leads to integer cokernels. Their torsion is a concrete and computable obstruction. Passing to real vectors can erase it entirely, so an approximate linear solve is not a replacement for the integral certificate.',
 ['For an integer matrix F:Zⁿ→Zᵐ, its cokernel is Zᵐ/imF. Smith normal form uses unimodular integer row and column changes to diagonal entries d₁|d₂|⋯.', 'For F=diag(2,3), its image is2Z×3Z; a class is zero exactly when the first coordinate is even and the second is divisible by three.'],
 'coker diag(2,3) is Z/2⊕Z/3≅Z/6. Its order is six although F is invertible over Q and R. Every homomorphism from this finite cokernel to the additive group Z is zero.',
 'The quotient map sends(a,b) to(a mod2,b mod3), and its kernel is exactly the image of F. The Chinese remainder map from Z/6 to this quotient, k↦(k mod2,k mod3), is bijective: injectivity follows because divisibility by both2 and3 implies divisibility by6, and both sets have six elements. Consequently the Smith invariant factors are1,6, consistent with determinant6 and gcd of all entries1. A homomorphism h from a finite group to Z sends every element x of finite order r to an integer with rh(x)=0; torsion-freeness of Z forces h(x)=0. Thus an integer-valued τ on this cokernel cannot detect its nonzero torsion classes.',
 'Test the obstruction vector d=(1,1).',
 'It has order six because kd lies in the image exactly when2|k and3|k. The equation Fx=d has the rational solution x=(1/2,1/3), and therefore a real solver reports residual zero. Nevertheless there is no integer solution. Six times the class vanishes, and smaller positive multiples do not. Reduction modulo2 and modulo3 provides a finite exact witness of the obstruction; no numerical tolerance enters the conclusion.',
 'The cokernel is an actual arithmetic invariant, and the example shows exactly which information a real-valued norm or integer scalar functional loses.',
 'A raw defect vector, its norm, its rational solvability and its integral quotient class answer different questions. A vanishing scalar summary does not imply a vanishing class without a separating family of tests.',
 'Construct explicit unimodular transformation matrices U,V with UFV in Smith form, so the certificate includes the change of coordinates and not merely a diagonal list claimed by a program.',
 [('Morris Newman Integral Matrices, publisher record','https://www.sciencedirect.com/book/9780125175501/integral-matrices')])

E('2025-09-09','soliton_conserved','A','Formal invariants','A trace invariant follows from local rewrite equations by induction',
 'Which precise transition relation preserves which algebraic quantity, and what statement must the formal proof actually establish?',
 'The Lean scaffold named transport and soliton conservation but retained an admitted proof. There is a straightforward positive theorem available: homomorphisms annihilating each allowed rewrite are conserved along every finite trace. It is independent of whether the states are called solitons.',
 ['Let states be x∈Zⁿ and allowed rewrite increments r₁,…,r_k. A transition has x′=x+r_j for some j.', 'For integer weights w, let τ(x)=wᵀx. A finite trace is a list of states linked by allowed transitions.'],
 'If wᵀr_j=0 for every allowed rewrite, τ has the same value at both ends of every finite trace. Conversely, conservation for all one-step traces forces all these equations. Thus exact linear conservation laws are the integer solutions of Rᵀw=0, where R contains the rewrite columns.',
 'For a one-step trace τ(x+r_j)−τ(x)=wᵀr_j=0. Induct on trace length: the empty trace has identical endpoints; appending one allowed transition preserves the already conserved value. Conversely, apply the claimed conservation law to the one-step trace0→r_j. This yields wᵀr_j=0 for every j. The argument identifies the exact proposition to encode: every transition and every finite closure of that relation preserves τ. A theorem of type True or a runtime message saying VERIFIED does not establish this quantified statement.',
 'Use three leaf types with rewrite r=(1,−2,1).',
 'Both w=(1,1,1) and v=(1,2,3) annihilate r. Starting at x=(0,4,0), one rewrite gives(1,2,1) and two give(2,0,2). Total count remains4, while the weighted quantity remains8. Solving w₁−2w₂+w₃=0 gives w₁=2w₂−w₃, so every integer conservation law is an integer combination of(2,1,0) and(−1,0,1). If nonnegative states are required, transitions leaving that domain must be forbidden; the same proof still applies to the remaining traces.',
 'The formalization target is a complete induction theorem with a computable family of all linear invariants, not merely an artifact hash.',
 'This theorem establishes no nonlinear PDE soliton, physical energy or collision resistance. It also does not certify that the historical admitted Lean scaffold was successfully completed.',
 'Compute the integer nullspace for a larger declared rewrite system and prove that its chosen basis generates all linear conservation laws; then formalize the trace induction against that exact basis.',
 [('Mathlib free abelian groups','https://leanprover-community.github.io/mathlib4_docs/Mathlib/GroupTheory/FreeAbelianGroup.html')])

E('2025-09-17','11a1','A','Elliptic curves','Genuine local arithmetic replaces a synthetic Hecke trace',
 'Which elliptic curve and good-reduction counts produce the coefficient sequence, and which exact recurrences extend it?',
 'The September repair explicitly moved from smoothing arbitrary floats to the curve conventionally labeled11a1. This is a strong constructive turn: its finite-field equation independently determines local traces, and the unramified Euler factor determines prime-power coefficients without fitting them.',
 ['Take E:y²+y=x³−x²−10x−20. For a good prime p, define a_p=p+1−#E(F_p), including the point at infinity.', 'The local generating function isΣ_(r≥0)a_(p^r)t^r=(1−a_pt+pt²)⁻¹, with a₁=1. At coprime indices use a_(mn)=a_ma_n.'],
 'Exact enumeration gives #E(F₂)=5,#E(F₃)=5,#E(F₅)=5,#E(F₇)=10, hence a₂=−2,a₃=−1,a₅=1,a₇=−2. The Euler factor implies a_(p^r)=a_pa_(p^(r−1))−pa_(p^(r−2)) for r≥2.',
 'For each listed prime enumerate x and y and test the polynomial equation modulo p, then add one point at infinity; this is a finite arithmetic certificate rather than a fitted trace. Multiplying the generating series by1−a_pt+pt² and comparing its constant, linear and higher coefficients proves the recurrence. The input primes are good: direct Weierstrass discriminant calculation gives−11⁵, so only11 is excluded from these particular factors. Hasse’s inequality can check the resulting counts, but it does not select the counts by itself. A construction assigning arbitrary data within that bound still needs a curve or another arithmetic source.',
 'Generate the next coefficients from the exact p=2 trace.',
 'The recurrence gives a₄=(−2)²−2=2, a₈=(−2)·2−2(−2)=0, and a₁₆=(−2)·0−2·2=−4. Coprime multiplicativity gives a₆=a₂a₃=2 and a₁₀=a₂a₅=−2. The generating factor begins1−2t+2t²+0t³−4t⁴+⋯. This coefficient sequence is a consequence of the declared factor; the modular interpretation of the curve is a separate classical theorem.',
 'The local input is now reproducible from an actual equation, and the extension to prime powers has an exact algebraic justification.',
 'These finite calculations establish no BSD formula, analytic rank or zero certification. Bad-prime factors require their own reduction analysis. The historical repair passage was truncated after the proposed special-value computations.',
 'Construct a rigorously bounded modular-form special-value computation using a stated functional equation and tail estimate, keeping the local arithmetic and analytic continuation certificates separate.',
 [('LMFDB elliptic curve11.a1','https://www.lmfdb.org/EllipticCurve/Q/11/a/1'),('John Cremona Algorithms for Modular Elliptic Curves','https://johncremona.github.io/book/fulltext/')] )

E('2025-09-15','Sym','A','Euler factors','The symmetric-square factor needs all three eigenvalue products',
 'Which normalization of the local parameters defines Sym², and what information is lost by squaring only the trace?',
 'The detector used factors of the form(1−a_p²p^(−s))⁻¹. That is not the symmetric-square factor of a two-dimensional unramified arithmetic parameter. Writing its three eigenvalues explicitly yields a complete finite correction and an exact worked factor.',
 ['Use arithmetic parameters α,β satisfying α+β=a and αβ=p. On the symmetric square, the eigenvalues areα²,αβ,β².', 'Let t=p^(−s). This unnormalized convention keeps the middle eigenvalue p. Dividing α,β by√p instead gives the unitary normalization and changes the variable scaling.'],
 'The unramified symmetric-square denominator is(1−α²t)(1−pt)(1−β²t)=1−(a²−p)t+p(a²−p)t²−p³t³. For the exact p=2,a=−2 input, it equals1−2t+4t²−8t³.',
 'The trace of the three-dimensional representation is α²+αβ+β²=(α+β)²−αβ=a²−p. The pairwise eigenvalue products sum to p(α²+β²)+p²=p(a²−2p)+p²=p(a²−p). Their product is(αβ)³=p³. Expanding the three linear factors proves the cubic formula without choosing roots numerically. For p=2,a=−2, the roots of X²+2X+2 are−1±i, whose squares are∓2i. Their quadratic contribution is1+4t², and the middle factor is1−2t, giving the displayed product.',
 'Compare the local coefficient sequences of the corrected and historical factors.',
 'Inverting1−2t+4t²−8t³ gives coefficients1,2,0,0,16,…; direct recurrence or multiplication checks these exactly. The rank-one surrogate(1−4t)⁻¹ instead gives1,4,16,64,256,…, already disagreeing at the first local coefficient. The distinction is representation-theoretic: the trace of Sym² is a²−p, not the square a² of the original trace. A finite Euler product over selected primes additionally has only the analytic properties of that finite rational expression.',
 'The functorial-lift theme acquires an actual local representation calculation rather than a mean-square heuristic.',
 'This is an unramified local factor calculation. It does not construct ramified factors, analytic continuation, a global functional equation or the automorphy of a symmetric-square lift. Those are separate deep inputs.',
 'Starting from genuine curve traces, include correct ramified local data and a known global functional equation, then prove a truncation bound before interpreting any critical-line scan.',
 [('Deligne Formes modulaires et représentations l-adiques','https://www.numdam.org/item/SB_1968-1969__11__139_0/')])

E('2025-09-15','FFT','A','Numerical analysis','FFT derivatives are exact for an interpolant, not for an unknown function',
 'Which frequency band and aliasing bound justify the derivative estimate used by the zero detector?',
 'The historical pipeline proposed DFT derivatives for a critical-line zero hunt. Fourier differentiation can be exact and useful, provided its object is identified: it differentiates the trigonometric interpolant selected by the sample grid. Finite samples alone cannot bound derivatives of an unrestricted analytic function.',
 ['Sample a2π-periodic function at x_j=2πj/N, j=0,…,N−1. The DFT assigns coefficients to one representative of each frequency class modulo N.', 'A band-limited trigonometric polynomial with frequencies |k|<N/2 has derivative coefficients ikc_k. Modes k and k+N have identical samples.'],
 'DFT differentiation exactly recovers derivatives of the declared band-limited polynomial. Without a frequency or analytic-tail bound, no finite sample grid gives a uniform derivative-error bound: h(x)=cos(Nx)−1 vanishes on the grid but h″(0)=−N².',
 'Discrete orthogonality gives N⁻¹Σ_jexp(i(k−ℓ)x_j)=1 when N divides k−ℓ and0 otherwise, by the finite geometric-sum formula. If all frequencies lie in a single nonaliasing band, this recovers each coefficient exactly. Differentiating the finite Fourier expansion multiplies its coefficient by ik, so the derivative is exact for that expansion. For the counterexample, Nx_j=2πj makes every value of h zero, while differentiating twice gives h″(x)=−N²cos(Nx). Multiplying h by any positive constant enlarges the derivative discrepancy without changing any sample. Analyticity alone therefore does not remove finite-grid nonidentifiability.',
 'Use N=8 and the known polynomial f(x)=sin x+2cos2x.',
 'Its nonzero frequencies are±1,±2, all inside the nonaliasing band. The DFT differentiates it to cos x−4sin2x and gives f′(0)=1 exactly in symbolic arithmetic. Adding3(cos8x−1) changes none of the eight samples or the first derivative at zero, but changes the second derivative at zero by−192. A double-zero diagnostic relying on both numerical derivatives needs an error estimate that excludes precisely this kind of invisible high-frequency component.',
 'The Fourier method becomes a rigorous tool when accompanied by its bandwidth or tail certificate.',
 'A grid derivative and a bootstrap interval do not by themselves certify the derivative of a global L-function. Floating-point error is additional to aliasing and must be handled separately.',
 'Assume an explicit coefficient bound |c_k|≤Ce^(−a|k|), derive a tail bound forΣk²|c_k| outside the sampled band, and combine it with rounding bounds to certify derivative signs.',
 [('Lloyd Trefethen Spectral Methods in MATLAB, author resources','https://people.maths.ox.ac.uk/trefethen/spectral.html')])

E('2025-09-15','double-zero','A','Complex analysis','A contour count can certify two zeros without certifying a double zero',
 'Does the certificate count nearby zeros with multiplicity, or prove exact multiplicity at a specified point?',
 'The double-zero search correctly described its status as heuristic. The distinction can be made mathematically sharp: a contour comparison robustly certifies a total count, whereas a double zero requires exact vanishing of the value and first derivative at the same point.',
 ['A holomorphic function has a zero of multiplicity two at z₀ exactly when f(z₀)=f′(z₀)=0 and f″(z₀)≠0.', 'Rouché’s theorem says that |h|<|g| on a simple closed contour implies g and g+h have the same total zero count inside, including multiplicities, provided they are holomorphic on the enclosed region.'],
 'For f_ε(z)=(z−1)²+ε and0<|ε|<r², the circle |z−1|=r encloses exactly two zeros, but both are simple. Its midpoint has f′_ε(1)=0 and f″_ε(1)=2, although it is not a zero.',
 'On the contour, |(z−1)²|=r²>|ε|, so Rouché compares f_ε with(z−1)² and gives total count two. Alternatively its roots are1±√(−ε), both strictly inside the circle. When ε≠0 they are distinct, and the derivative2(z−1) is nonzero at either root, proving simplicity. At ε=0 the roots merge and the first two vanishing equations hold exactly. The strict contour gap r²−|ε| is robust under additional perturbations smaller than that gap, while exact equality f(1)=0 is not stable under arbitrary small constant perturbations.',
 'Take ε=1/100 and r=1/2.',
 'The roots are1±i/10. On the contour the unperturbed modulus is1/4 and the perturbation is1/100, leaving margin6/25. A certified evaluation error below that margin preserves the total count, but not a claim that either root is repeated. The midpoint values are f(1)=1/100,f′(1)=0,f″(1)=2. A tolerance treating the first value as zero can therefore misclassify two nearby simple zeros as one double zero.',
 'A useful certificate states exactly whether it establishes existence, total multiplicity, isolation or an exact repeated root.',
 'A full Turing count for an arithmetic L-function has additional hypotheses and global input; this elementary Rouché example does not supply that machinery. Empty candidate lists establish no nonexistence theorem.',
 'Combine a rigorous analytic approximation with an explicit contour error bound, then isolate each zero in disjoint disks and apply a derivative lower bound to certify simplicity.',
 [('NIST DLMF zeros and contour methods','https://dlmf.nist.gov/25.10')])

E('2025-09-15','Iwasawa','U','p-adic power series','A μ-invariant is a valuation, not a real-valued twist statistic',
 'Which p-adic power series defines μ and λ, and which algebraic operations preserve those invariants?',
 'The September sampler used cosine aggregates and bootstrap intervals under an Iwasawa label. A genuine elementary analogue starts with a power series over Z_p. Its invariants come from coefficient valuations and reduction modulo p, and can be proved invariant under multiplication by a unit.',
 ['For nonzero F(T)=Σa_nTⁿ∈Z_p[[T]], define μ(F)=min_n v_p(a_n) and λ(F)=min{n:v_p(a_n)=μ(F)}.', 'Write F=p^μF₀, where at least one coefficient of F₀ is a unit. A power-series unit U has constant coefficient in Z_p×.'],
 'For nonzero F,G, μ(FG)=μ(F)+μ(G) and λ(FG)=λ(F)+λ(G). In particular multiplication by a unit preserves both invariants. These statements follow directly from the integral-domain property of F_p[[T]].',
 'Divide F and G by their lowest p-powers, obtaining primitive series F₀,G₀ whose reductions modulo p are nonzero. Their product remains nonzero because a formal series ring over a field is a domain: the first nonzero coefficients multiply to the first nonzero coefficient of the product. Thus no extra p divides every coefficient of F₀G₀, proving the μ identity. The orders in T of the two nonzero reductions are λ(F),λ(G); their product has the sum of those orders. A unit has μ=λ=0, so multiplication by it preserves both values. The argument uses the complete power series, not a real distributional interpretation.',
 'Use p=3 and F(T)=9(3+T²+3T³).',
 'The coefficient valuations are at least two, with the first valuation-two coefficient at degree two; hence μ=2 and λ=2. Multiplying by1+T gives9(3+3T+T²+4T³+3T⁴). After division by9 and reduction modulo3 this is T²+T³=T²(1+T), retaining the same invariants. Conversely, a finite truncation before degree two would incorrectly suggest all known coefficients have valuation at least three; unseen coefficients must be controlled before certifying the infinite-series minimum.',
 'The arithmetic meaning is now explicit and supplies exact certificates for a declared algebraic object.',
 'This elementary definition does not prove that a sampled series is the characteristic series of an Iwasawa module or a p-adic L-function. Real cosine twists, confidence intervals and numerical regularity alone do not establish that connection.',
 'Construct a genuine measure on Z_p, prove integrality of its Amice transform, and bound all unseen coefficients sufficiently to certify its μ invariant from a finite computation.',
 [('Coates Schneider Sujatha Modules over Iwasawa algebras','https://arxiv.org/abs/math/0110342')])

E('2025-09-20','cross-ratio','U','Moduli and elliptic curves','A cross-ratio produces an auditable map into elliptic-curve moduli',
 'Which projective invariants determine the curve family, and which distinct parameter values map to the same moduli point?',
 'The historical account eventually identified an auditable pushforward distribution on elliptic-curve moduli as the defensible mathematical object. This is more precise than treating a change of input source as a new Langlands correspondence. The Legendre family provides an exact finite model of that pushforward.',
 ['For four ordered distinct points on P¹, a Möbius transformation places three at0,1,∞; the fourth is a cross-ratio λ∉{0,1}.', 'The Legendre curve is E_λ:y²=x(x−1)(x−λ), with j(λ)=256(1−λ+λ²)³/[λ²(1−λ)²].'],
 'The j-value is unchanged by λ↦1−λ and λ↦1/λ, hence by the six usual cross-ratio transforms. For λ=3 these six distinct values are3,−2,1/3,−1/2,3/2,2/3, all with j=21952/9. A probability law on λ therefore has a well-defined pushforward to j, with collisions that can be counted exactly.',
 'Möbius invariance follows by cancellation in the cross-ratio formula after substituting(az+b)/(cz+d). For j, replacing λ by1−λ preserves the quadratic1−λ+λ² and the denominator factors. Replacing λ by1/λ multiplies the numerator byλ⁻⁶ and the denominator byλ⁻⁶, leaving the ratio unchanged. These two transformations generate the six-point orbit, so all its values share j. Substitution at λ=3 gives256·7³/(9·4)=21952/9. For any measure ν, define the pushforward by j_*ν(B)=ν(j⁻¹(B)); this directly makes the collision structure part of the induced distribution.',
 'Assign equal probability to the six listed rational parameters.',
 'Their parameter distribution has six atoms, but its j-pushforward is a single atom at21952/9. Thus apparent parameter diversity can collapse entirely after passage to moduli. The j-invariant classifies elliptic curves over an algebraic closure, but equality of j over Q allows distinct quadratic twists, so an arithmetic distribution must retain twist data when appropriate. Conductor, rational isogeny and reduction traces are additional arithmetic statistics rather than consequences of the j histogram alone.',
 'The meaningful output is a transparent, testable map with explicit fibers and sampling choices.',
 'No new Galois representation or modularity theorem follows from the provenance of λ. The example does not infer sensitive geometric or biological properties from the arithmetic; it treats only abstract input parameters.',
 'Define a finite rational parameter sample, retain twist classes and compute exact good-prime trace vectors; quantify separately collisions in j, isomorphism class and rational isogeny class.',
 [('Milne Elliptic Curves, author text','https://www.jmilne.org/math/Books/EC2.html')])

E('2025-09-21','Legendre','A','Finite fields','A Legendre-symbol certificate has a precise and limited arithmetic meaning',
 'Which finite-field symbol is evaluated, and what additional data would be required to interpret it as a Hilbert or local geometric invariant?',
 'The historical face-plumbing module attached Maslov and Tamagawa names to a Legendre-symbol proxy. The useful mathematical component is exact quadratic residuosity. Its input, proof and finite certificate can be stated independently of those unsupported interpretations.',
 ['For an odd prime p and p∤a, the Legendre symbol(a/p) is1 if a is a nonzero square modulo p and−1 otherwise.', 'Euler’s criterion is a^((p−1)/2)≡(a/p) mod p. It concerns the multiplicative group of F_p, not a general integer-valued Maslov index or elliptic Tamagawa number.'],
 'For p=163 and a=6 the Legendre symbol is1. An explicit square root modulo163 certifies this directly. More generally, the set of nonzero squares is a subgroup of index two, and the Legendre symbol is a multiplicative homomorphism F_p×→{±1}.',
 'The squaring map on F_p× has kernel{1,−1}, because x²=1 factors as(x−1)(x+1) and the field has odd characteristic. Its image therefore has(p−1)/2 elements and is a subgroup. The quotient has order two, proving multiplicativity of its sign character. To prove Euler’s criterion, use cyclicity of F_p×: for a generator g, a=g^k and a^((p−1)/2)=(-1)^k, which is1 exactly for even k, namely the squares. For the stated numerical case, a direct modular square root and modular exponentiation supply mutually consistent finite certificates.',
 'Distinguish a quadratic residue result from an unrestricted local-symbol claim.',
 'The roots are13 and150:13²=169≡6 mod163 and150≡−13. The verifier independently enumerates them and checks6⁸¹≡1 mod163. In an odd-p Hilbert symbol formula, a unit u paired with the uniformizer p gives(u,p)_p=(u/p); this explains one genuine relationship. But a general Hilbert symbol(a,b)_p depends on two square classes and their valuations. A single Legendre value cannot supply those missing arguments, and neither label produces the component group of an elliptic curve’s Néron model.',
 'The returned sign can be certified exactly, while its semantic interpretation remains a separate theorem requiring separately defined objects.',
 'The historical build failed before completing the claimed formal pipeline; emitted JSON alone does not validate a formal proof. No anatomical or physical conclusion is drawn from this arithmetic example.',
 'Specify a genuine quadratic extension of Q_p and verify norm-solvability or the full odd-prime Hilbert-symbol formula against exact valuation and residue data.',
 [('Milne Class Field Theory','https://www.jmilne.org/math/CourseNotes/CFT.pdf')])

E('2025-09-19','fractional','U','Resource algebra','Fractional ownership is a partial algebra, not duplicable permission',
 'Which partial composition law enforces the claimed ownership budget, and which logical rules are still needed for a race-freedom theorem?',
 'The second-descent passage included rational fractional ownership and race-freedom goals. The underlying algebra can be proved completely in a small model. It explains why full ownership cannot be duplicated, while keeping the separate operational and logical assumptions visible.',
 ['Let resource shares be rationals q∈[0,1]. Define q⊕r=q+r only when q+r≤1; zero is the identity.', 'A compatible family of shares is one whose sum is at most one. A full share is1. The associated separation-style composition is partial, so an undefined sum is not another resource.'],
 'This operation is a partial commutative monoid with cancellation. A full share has no compatible positive remainder and cannot be composed with a second full share. Any positive rational share can be split into smaller compatible rational shares.',
 'Commutativity and the zero law follow from rational addition. A three-share composite exists exactly when q+r+s≤1; in that case either parenthesization exists and has the same sum, proving the appropriate partial associativity law. If q⊕r=q⊕s, cancellation in Q gives r=s. If1⊕r is defined with r≥0, the defining inequality1+r≤1 forces r=0. Thus1⊕1 is undefined. For any rational0<q≤1 and rational0<t<1, the shares tq and(1−t)q are positive, compatible and sum to q. These facts precisely encode a conserved ownership budget.',
 'Split one permission into three equal readers and recombine it.',
 'The three shares1/3,1/3,1/3 have total one, and any two compose to2/3. Adding a fourth positive third is undefined because4/3 exceeds one. Similarly1/3 and2/3 compose to a full share, whereas retaining either part after consuming the recombined full resource would require an additional rule that duplicates the budget. The algebra is exact over rational numbers and its validity requires no numerical tolerance.',
 'The ownership idea has a concrete conservation law that can support a formal program logic.',
 'A data-race-freedom theorem additionally requires a language semantics and rules connecting read/write actions to these resources. The partial algebra alone proves no compiler, garbage collector, constant-time bound or bootloader property. It also does not identify the exact historical Iris modality denoted by◇.',
 'Specify a small concurrent language, give reads fractional permission and writes full permission, and prove that two enabled writes or a write/read conflict cannot hold compatible resource assertions.',
 [('Jung et al Iris from the ground up','https://iris-project.org/pdfs/2018-iris-ground-up.pdf')])

E('2025-09-19','bisimulation','U','Transition systems','Bisimulation preserves observable traces under a stated transition relation',
 'Which transitions and observations are matched, and are latency steps observable or intentionally hidden?',
 'The latency-parametric garbage-collection passage named bisimulation without returning complete operational semantics. A finite labeled model develops the exact mathematical claim available from that idea and distinguishes strong step matching from an unproved constant-time assertion.',
 ['A labeled transition system has states S and relations x→ᵃx′ for labels a. A relation R is a strong bisimulation if every transition on either side can be matched with the same label and related target.', 'A finite observable trace is a label word obtained along a path. Declaring an internal label τ invisible leads to a different, weak-bisimulation definition.'],
 'Related states in a strong bisimulation have identical sets of finite labeled traces. The relation pairing a two-state alternating machine with a one-state a-loop is a bisimulation, although their concrete state counts differ.',
 'Prove trace preservation by induction on word length. The empty word is possible from every state. If xRy and x has a path beginning with label a, the forth condition supplies a matching a-transition from y to a related state; apply induction to the remaining word. The back condition gives the reverse inclusion. For the example let x₀→ᵃx₁ and x₁→ᵃx₀, and y→ᵃy. The relation{(x₀,y),(x₁,y)} matches the unique a-transition from each state in both directions, so it is a bisimulation. Every finite trace in either model is a power aⁿ.',
 'Add a silent preparatory step to only one implementation.',
 'If x₀→ᵗᵃᵘx₁→ᵃx₀ while y has only an a-loop, the previous relation is not a strong bisimulation because y cannot match the τ label. A weak relation may intentionally erase that internal step, but then it has proved equivalence only after that abstraction. If τ consumes measurable time, erasing it cannot by itself prove equal latency, constant running time or an18-cycle bound.',
 'The semantic matching relation is a constructive abstraction theorem once its labels and observability policy are explicit.',
 'No historical garbage-collector transition relation or timing model was recovered. The example therefore supplies a newly defined finite theorem rather than claiming that the original implementation had been verified. A modal symbol must likewise be interpreted before any formula such as◇false→⊥ can be assessed.',
 'Use a cost-labeled transition relation and prove a cost-preserving simulation, or an explicit bounded-cost refinement, so latency conclusions follow from the actual matched data.',
 [('Milner Communication and Concurrency, author bibliography','https://www.cl.cam.ac.uk/~rm135/')])

E('2025-09-14','sqrt','A','Nonlinear interval maps','The square-root smoothing map has dynamics but is not a linear Hecke operator',
 'What does the actual surrogate map do, and which exact endpoint tests can reject a claimed commutation law?',
 'The recovered micro-space map is concrete enough to analyze after normalizing its unit interval. Its positive mathematical content is a concave dynamical map; assigning it a Hecke label does not make it a linear arithmetic correspondence.',
 ['Normalize x∈[0,M] by u=x/M. The real-valued smoothing becomes h(u)=(u+√u)/2 on[0,1].', 'Let θ(u)=clamp(su+t,0,1), where clamp(v,0,1)=min(1,max(0,v)). Exact reciprocity in this finite model means h∘θ=θ∘h on the stated domain.'],
 'h is increasing and concave, has exactly the fixed points0 and1, and every orbit starting in(0,1] converges to1. It is not linear and is not globally Lipschitz on[0,1]. Any commuting θ must send each of0,1 to one of0,1.',
 'For0<u<1, √u>u, so u<h(u)<1. Iterates are increasing and bounded, hence have a limit; continuity makes it a fixed point. Solving h(u)=u gives√u=u and therefore u∈{0,1}; a positive starting value excludes zero. Concavity follows from h″(u)=−1/(8u^(3/2))<0 in the interior. The ratio[h(u)−h(0)]/u=(1+u^(−1/2))/2 is unbounded as u→0, ruling out a global Lipschitz constant. If h and θ commute and e is an endpoint fixed by h, then h(θ(e))=θ(h(e))=θ(e), so θ(e) must itself be an endpoint.',
 'Apply the endpoint test to a newly specified affine-clipped example s=3/10,t=−1/10.',
 'Here θ(0)=0 but θ(1)=1/5. Thus h(θ(1))=(1/5+1/√5)/2 differs from θ(h(1))=1/5. The commutator already fails at the endpoint, independently of a dense grid or an optimizer. Nonlinearity can be checked from h(1/4)=3/8, whereas linear homogeneity would require h(1/4)=(1/4)h(1)=1/4.',
 'The surrogate has a fully understood interval dynamics and simple necessary reciprocity tests. Those are meaningful mathematical results without an arithmetic reinterpretation.',
 'The recorded micro-witness numbers are not independently certified: the exact integer rounding, scale, scan grid and definition of Δ were not all recovered. The new example does not claim to reproduce their run.',
 'Classify affine maps preserving[0,1] that commute with h. The endpoint condition reduces the nonconstant unclipped case to identity or reflection; one interior test excludes reflection, leaving only identity and the two endpoint constants.',
 [('NIST DLMF elementary-function definitions','https://dlmf.nist.gov/4.2')])

E('2025-09-15','witness','A','Certified computation','Integer micro-arithmetic needs a proved rounding envelope',
 'Which real map does the integer routine approximate, and how do its local rounding errors propagate through a commutator?',
 'The laboratory reported micro-unit reciprocity witnesses. Exact integer arithmetic removes floating roundoff but does not remove approximation error: flooring a square root changes the mathematical map. A transparent quantization model gives an explicit certificate and explains why a one-unit local error can be amplified near zero.',
 ['Fix an integer M≥1 and integer0≤x≤M. Define h_M(x)=floor((x+floor√(xM))/2), and h(u)=(u+√u)/2.', 'For normalized quantities use the error |h_M(x)/M−h(x/M)|. On[δ,1], h has Lipschitz bound L_δ=1/2+1/(4√δ), while on the full interval it is only Hölder controlled near zero.'],
 'For every integer x in the domain,0≤h(x/M)−h_M(x)/M<1/M. Globally, |h(u)−h(v)|≤(|u−v|+√|u−v|)/2. Consequently an input uncertainty of one micro-unit can produce an output uncertainty of order M^(−1/2), rather than order M⁻¹.',
 'Write r=√(xM) and k=floor r, so0≤r−k<1. Replacing r by k changes the numerator half by less than1/2. Since x+k is an integer, its division by two loses either0 or1/2 under flooring. The total unnormalized loss is strictly below one; division by M proves the bound. For0≤v≤u, √u−√v=(u−v)/(√u+√v)≤√(u−v), proving the global inequality. On a domain bounded below by δ, the derivative formula gives the stated uniform Lipschitz coefficient. This separates a local exact rounding lemma from its potentially nonuniform propagation.',
 'Take M=10⁶ and compare normalized inputs0 and1/M.',
 'The integer square root of M is1000, so h_M(1)=floor1001/2=500. Thus the normalized output difference is500/M=1/2000 even though the input difference is1/10⁶, an amplification factor500. The real output is1001/(2·10⁶), and its difference from the integer output is exactly1/(2·10⁶), within the proved envelope.',
 'A legitimate micro-unit certificate must state both the integer equality and the real-map error bound; the example makes the missing scale dependence explicit.',
 'This independently specified quantizer is not asserted to be the exact historical Bash implementation. A claimed Δ of two units cannot be interpreted without the grid, flooring conventions and domain where error propagates.',
 'For a specified clipped θ quantizer, prove a commutator-error envelope using the Hölder bound globally or L_δ on a verified positive subdomain, then compare the observed integer defect with that envelope.',
 [('NIST DLMF square-root function','https://dlmf.nist.gov/4.2')])

E('2025-09-19','Chebyshev','U','Orthogonal polynomials and local recurrences','Chebyshev polynomials give exact normalized Hecke recurrences',
 'Which recurrence connects genuine local coefficients to a bounded spectral parameter, and what stability bound follows from it?',
 'The platform suggestions named both Chebyshev recurrence and Hecke data. Their precise connection is classical and productive: the unramified degree-two local recurrence becomes the second-kind Chebyshev recurrence after normalization. This provides a testable algebraic bridge rather than a new correspondence claim.',
 ['Set U₀(x)=1,U₁(x)=2x and U_r(x)=2xU_(r−1)(x)−U_(r−2)(x).', 'For arithmetic parameters a,p, define b₀=1,b₁=a and b_r=a b_(r−1)−p b_(r−2). Put x=a/(2√p).'],
 'b_r=p^(r/2)U_r(x). If |a|≤2√p, then |b_r|≤(r+1)p^(r/2). For |x|<1, U_r(cosθ)=sin((r+1)θ)/sinθ, with continuous endpoint values U_r(±1)=(±1)^r(r+1).',
 'Substitute b_r=p^(r/2)c_r into its recurrence to obtain c_r=(a/√p)c_(r−1)−c_(r−2)=2xc_(r−1)−c_(r−2), with the same initial data as U_r. Induction proves the identity. The sine addition formula proves the trigonometric recurrence and initial values, giving the expression in the interior. For a bound that remains stable at the endpoints, use the equivalent sum U_r(cosθ)=e^(irθ)+e^(i(r−2)θ)+⋯+e^(−irθ), a sum of r+1 unit complex numbers. The triangle inequality gives r+1 uniformly, and evaluation at θ=0,π gives the endpoint values.',
 'Use the genuine p=2,a=−2 input from11a1.',
 'The first U-polynomials are1,2x,4x²−1,8x³−4x. At x=−1/√2, multiplying by the prescribed powers of√2 gives b₀=1,b₁=−2,b₂=2,b₃=0,b₄=−4, matching exact arithmetic recurrence. The bound for r=4 is|−4|≤5·4=20. It is a coarse certified bound, not a prediction that every coefficient reaches the maximum.',
 'The relationship provides exact normalization checks and endpoint-safe coefficient bounds across the arithmetic and spectral descriptions.',
 'The Hasse-type input |a|≤2√p must come from a proved arithmetic source. An arbitrary float converted into x is not thereby a Hecke eigenvalue. This recurrence does not prove global automorphy or endoscopy.',
 'Use recurrence-based interval arithmetic to evaluate long prime-power coefficient blocks and compare its certified error growth with unstable evaluation of the sine quotient near x=±1.',
 [('NIST DLMF Chebyshev polynomials','https://dlmf.nist.gov/18.5')])

E('2025-09-10','geometric','A','Sampling and exponential decay','A geometric checkpoint clock estimates a decay rate without being a soliton',
 'What mathematical quantity does the checkpoint schedule estimate, and which formula remains invariant when the time spacing changes?',
 'The geometric τ-clock was eventually described as a sampling cadence rather than a PDE mechanism. That modest interpretation still has a complete mathematical development: exponential decay can be recovered from unequally spaced samples, and a geometric schedule has a transparent resolution-versus-horizon tradeoff.',
 ['Choose times t_k=t₀q^k with t₀>0,q>1, and a positive signal E(t)=C exp(−αt), C>0.', 'For consecutive samples define α_hat_k=−[log E(t_k)−log E(t_(k−1))]/[t_k−t_(k−1)].'],
 'For exact exponential data α_hat_k=α for every k, regardless of q. The number of positive checkpoints through horizon T≥t₀ is1+floor(log(T/t₀)/logq). If each log measurement has absolute error at mostδ, then |α_hat_k−α|≤2δ/(t_k−t_(k−1)).',
 'Take logarithms: logE(t)=logC−αt. Subtracting two samples cancels logC and gives−α times their time difference, proving the rate identity. The checkpoint count follows by solving t₀q^k≤T for integers k≥0. If the measured logarithms are logE(t_k)+e_k with |e_k|≤δ, the estimated slope differs by−(e_k−e_(k−1))/(t_k−t_(k−1)); the triangle inequality gives the error bound. Thus larger gaps reduce this particular absolute log-noise amplification, while they also discard information about changes within those gaps.',
 'Let t₀=1,q=2,C=3,α=1/2 and T=16.',
 'The checkpoints are1,2,4,8,16, exactly five. Their log values are log3−1/2,log3−1,log3−2,log3−4,log3−8. Every consecutive secant gives1/2. With log-error boundδ=1/100, the first rate uncertainty is at most1/50, and the last is at most1/400. A nonexponential signal could share all five values yet differ between them, so this schedule alone does not identify a differential equation.',
 'The clock has an exact estimation law and an explicit sampling cost, without importing unsupported soliton terminology.',
 'The historical caching speedup was workflow-dependent and is not a mathematical performance guarantee. The theorem concerns exact or bounded-error log samples, not hash validity or physical energy.',
 'Assume a bounded second derivative of logE and derive an interpolation-error certificate between checkpoints, then choose q to balance sample count, noise amplification and missed curvature.',
 [('NIST DLMF logarithm and exponential functions','https://dlmf.nist.gov/4.2')])

extras={7:' At t=0 every local factor has constant coefficient one. This normalization is part of the representation: multiplying or averaging arbitrary observed values changes the local factor rather than preserving its arithmetic definition.',17:' The same sum representation proves the endpoint limit without dividing by a vanishing sine. It also shows why a small denominator in the quotient formula is a numerical issue rather than a singularity of the underlying polynomial. For exact rational a and p, the unnormalized recurrence remains integral throughout.',18:' A dimensionless geometric ratio controls the schedule; the decay rate still has reciprocal-time units. Rescaling time by a positive constant rescales the estimated rate inversely, while leaving the geometric checkpoint count through a similarly rescaled horizon unchanged.'}
for k,text in extras.items():entries[k-1]['example']['calculation']+=text
E('2025-09-02','rank','A','Exact linear algebra','A modular minor certifies a rational rank lower bound',
 'Which exact minor proves the rank claim, and what independent data certify the upper bound?',
 'The obstruction pipeline proposed modular rank certificates. Their useful theorem is asymmetric: nonzero reduction gives a reliable lower bound over Q, while a rank drop modulo a prime can be accidental. A full certificate needs both sides.',
 ['For an integer matrix A let rank_QA denote its rational rank and rank_pA its rank after reduction over the prime field F_p.', 'A nonzero r×r minor proves rank at least r; a factorization A=BC with B having r columns proves rank at most r over the chosen field.'],
 'rank_pA≤rank_QA. If a minor is nonzero modulo p and a rational rank-r factorization is verified exactly, the two certificates prove rank_QA=r. Conversely rank_pA=0 does not imply rational rank zero.',
 'If an r×r determinant is nonzero modulo p, its integer determinant is not zero, hence the corresponding rational rows and columns are independent. Equivalently every minor larger than the rational rank is the zero integer and stays zero after reduction. The factorization bound follows because every column of BC lies in the span of the r columns of B. Both checks are finite exact equations. For failure of the converse, the one-entry matrix[p] is nonzero over Q but reduces to zero modulo p.',
 'Use A=[[1,2,3],[2,4,6],[0,1,1]].',
 'The minor from rows1,3 and columns1,2 has determinant one, so every prime certifies rank at least two. The second row is twice the first, proving rank at most two, hence exact rank two. A null vector is(−1,−1,1), checked by matrix multiplication. The certificate therefore includes a field-independent nonzero minor and a rational dependence, rather than an unsupported prime-rank number.',
 'This is an implementable rank proof suitable for an obstruction complex or formal verifier.',
 'The modulus must actually be prime before finite-field Gaussian elimination applies. A historical integer merely labeled p is not accepted as prime without a certificate. Rank also does not determine torsion in integral homology.',
 'Emit pivot minors, exact row relations and Smith data together, separating rational rank from integer torsion and checking every claimed transformation matrix.',
 [('Stacks Project finite presentation and matrix rank','https://stacks.math.columbia.edu/tag/00EX')])

E('2025-09-06','tau_monotonic','A','Order and finite certificates','Adjacent exact inequalities prove full monotonicity of a finite clock',
 'What does monotonicity mean over the exact stored type, and does the proposed proof establish all index pairs?',
 'The clock scaffold left monotonicity admitted while displaying decimal sample times. A finite order theorem is enough to close this mathematical obligation. Exact rational timestamps avoid confusing an intended step with a floating representation.',
 ['A finite sequence t₀,…,t_n is nondecreasing if i≤j implies t_i≤t_j, and strictly increasing if i<j implies t_i<t_j.', 'For the recovered six-value pattern use exact rationals t_k=3k/50 for k=0,…,5.'],
 'A sequence in a transitive ordered set is nondecreasing if and only if every adjacent inequality t_k≤t_(k+1) holds. Over Q, positive adjacent increments imply strict increase, and t_j−t_i is their telescoping sum.',
 'The forward direction follows by choosing j=i+1. For the reverse, induct on j−i. Difference zero is reflexivity; for positive difference use the induction hypothesis from i to j−1 and transitivity with the final adjacent inequality. In Q, telescoping gives t_j−t_i=Σ_(k=i)^(j−1)(t_(k+1)−t_k), which is positive when i<j and every summand is positive. This supplies the exact statement a list-inductive proof should establish, including the empty and singleton cases.',
 'Verify the six timestamps and the minimum gap.',
 'The sequence is0,3/50,3/25,9/50,6/25,3/10. Every adjacent gap is3/50, so t_j−t_i=3(j−i)/50 and the end-to-end difference is3/10. The minimum positive separation is3/50, not the average slope of an unspecified continuous interpolant. If the values are rounded with absolute errorδ<3/100, strict order is retained because each perturbed gap exceeds3/50−2δ>0.',
 'The clock obtains a complete finite-order proof and a quantitative robustness margin.',
 'NaN values in a floating type do not obey the ordinary total-order assumptions used here. A computed sequence does not prove a soliton conservation law, and no successful completion of the historical admitted theorem is claimed.',
 'Encode rational timestamps and certified error intervals, prove the adjacent-gap lower bound by recursion, and derive global monotonicity from that lemma rather than asserting it as an axiom.',
 [('Mathlib order and monotone functions','https://leanprover-community.github.io/mathlib4_docs/Mathlib/Order/Monotone/Basic.html')])

E('2025-09-08','KdV','A','Nonlinear waves','A genuine KdV soliton requires a PDE identity, not a checkpoint metaphor',
 'Which field and equation make the tau function a soliton construction, and can the traveling wave be verified directly?',
 'The September discussion named KdV and Hirota tau functions alongside the software clock. An actual classical soliton supplies a constructive comparison. It has a nonlinear PDE, a traveling profile and a precise logarithmic tau formula; those are additional mathematical data.',
 ['Use KdV u_t+6uu_x+u_xxx=0 on R×R. For k>0 set z=x−4k²t−x₀ and F(z)=2k²sech²(kz).', 'Define the positive tau function τ(x,t)=1+exp(2kz), and u=2∂²_xlogτ.'],
 'The field u=F(z) equals2∂²_xlogτ and solves the declared KdV equation exactly. It travels at speed4k², has amplitude2k² and integral∫_R u dx=4k.',
 'Differentiating log(1+e^(2kz)) twice gives4k²e^(2kz)/(1+e^(2kz))²=k²sech²(kz), proving the tau formula after multiplying by two. The profile identity is F″=4k²F−3F², obtained by differentiating sech² or its equivalent tanh expression. Differentiating that identity gives F‴=4k²F′−6FF′. Since u_t=−4k²F′ and u_x=F′, the three KdV terms cancel exactly. Finally∫sech²(kz)dz=2/k, yielding mass4k.',
 'Take k=1 and x₀=0.',
 'The profile u=2sech²(x−4t) moves right with speed four while retaining amplitude two. Its maximum occurs at x=4t, and its integral remains four by translation. The tau function itself grows exponentially on one spatial side, but its second logarithmic derivative is localized; therefore tau and the physical profile are different objects even in this exact construction.',
 'The soliton terminology is now attached to a verified nonlinear-wave solution, giving a positive mathematical model rather than a software analogy.',
 'This proves one traveling-wave solution, not general inverse-scattering theory, multi-soliton interactions or any relation to hash ledgers. A geometrically spaced list of timestamps lacks the field and PDE needed for this theorem.',
 'Construct the two-soliton Hirota tau expression with its interaction coefficient and verify its PDE identity symbolically, then analyze the asymptotic phase shift as a separately stated result.',
 [('Hirota Exact solution of the Korteweg–de Vries equation for multiple collisions of solitons','https://doi.org/10.1103/PhysRevLett.27.1192')])

# Further retrieved topics may be appended before finalization.
for k,text in {20:' Exact positivity therefore proves strict monotonicity.',21:' The speed and amplitude are not independently adjustable within this family: speed is twice amplitude. The translation parameter changes neither the integral nor this amplitude-speed relation.'}.items():entries[k-1]['example']['calculation']+=text
def finish():
    for e in entries:
        words=len(' '.join([e['summary'],*e['definitions'],*e['result'].values(),*e['example'].values(),e['limits'],e['extension']]).split())
        assert words>=260,(e['id'],words)
    (HERE/'entries.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
    print(len(entries),'entries')
if __name__=='__main__':finish()
