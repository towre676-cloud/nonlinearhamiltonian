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
    entries.append(dict(id=f'Y25-10-{len(entries)+1:03d}',title=title,status='Classical mathematics with newly authored proof or worked finite certificate',summary=summary,definitions=defs,result=dict(name=title,statement=statement,proof=proof),example=dict(setup=setup,calculation=calculation,conclusion=conclusion),limits=limits,extension=extension,references=[dict(label=l,url=u) for l,u in refs],original=dict(date=date,month='2025-10',evidence=ev,field=field,concept=title,origin='Recovered dated mathematical subject; attribution limits are preserved.',question=question,math=statement,finish='Worked result, explicit example, stated limits and a precise extension',kind='Revised mathematical treatment',refs=[u for _,u in refs],source_excerpt=excerpt,retrieval_receipt=receipt,original_question=None,attribution_note='The source is a retrieved topic/exchange summary, not necessarily a verbatim transcript. U identifies user subject matter and does not attribute adjacent assistant equations to the user. Revised questions, proofs and examples are newly authored.')))

E('2025-10-01','affine RG','U','Differential equations','The RG leaf has an exact first integral, and its two-loop extension introduces a logarithm',
 'Which differential equation defines the leaf, and what field of functions contains its two-loop solution?',
 'The RG capsule has a clear mathematical core: a first-order ODE with a rational invariant. The historical differential form and the invariant require a sign check. The two-loop equation can also be integrated explicitly, although its inverse is generally not rational in the parameters.',
 ['Let μ′=bμ² with μ(0)=μ₀≠0. A prime denotes differentiation with respect to ℓ.', 'For a two-loop model use μ′=μ²(b+cμ), on a connected interval avoiding μ=0 and b+cμ=0.'],
 'The one-loop solution is μ(ℓ)=μ₀/(1−bμ₀ℓ), with invariant μ⁻¹+bℓ=μ₀⁻¹. Its annihilating one-form is dμ/μ²−b dℓ. For b≠0, an antiderivative of1/[μ²(b+cμ)] is F(μ)=−1/(bμ)+(c/b²)log|(b+cμ)/μ|.',
 'Differentiate μ⁻¹+bℓ: its derivative is−μ′/μ²+b=0. This also shows that the historical plus-sign form dμ/μ²+b dℓ would instead vanish on μ′=−bμ², so the form and invariant cannot share the same sign without correction. For the two-loop integrand, partial fractions give1/[μ²(b+cμ)]=1/(bμ²)−c/(b²μ)+c²/[b²(b+cμ)]. Integrating yields F; thus F(μ(ℓ))−F(μ₀)=ℓ until a singularity or branch boundary is reached. The logarithm is essential unless c=0 or another degeneracy removes it.',
 'Use the recovered rational capsule parameters μ₀=3/7 and b=5/2 in the one-loop equation.',
 'The solution is μ(ℓ)=6/(14−15ℓ), with pole at14/15. At ℓ=1/5 it equals6/11, and1/μ+bℓ=11/6+1/2=7/3=1/μ₀. This exact rational check validates the leaf on its nonsingular interval. For the two-loop inversion, Newton iteration is meaningful only after choosing a real branch and checking that F′ stays nonzero there.',
 'The capsule now carries a verifiable invariant, a corrected differential form and an explicit scope for the implicit logarithmic extension.',
 'No arithmetic motive, physical RG law or global continuation is obtained merely by hashing these parameters. The pole excludes part of the nominal time axis, and a solution branch must not be continued through it by an algebraic cancellation.',
 'Bracket a branch of the two-loop implicit equation and prove a Newton or interval-Newton convergence certificate using explicit derivative bounds.',
 [('NIST DLMF logarithms','https://dlmf.nist.gov/4.2')])

E('2025-10-01','Gramian','U','Linear algebra and symmetry','Whitening and signed-permutation invariance impose different equations',
 'Which Gramian is positive definite, and which additional condition makes a quadratic form invariant under the whole B₅ group?',
 'The October framework combined normalized Gramians, whitening and a B₅ chamber index. These operations have precise independent meanings. Whitening produces an orthonormal metric, while invariance under all coordinate sign flips and permutations forces a quadratic form to be scalar.',
 ['Let Σ be a real symmetric positive-definite5×5 matrix and W=Σ^(−1/2), the positive spectral inverse square root.', 'The signed-permutation group B₅ consists of matrices P with one±1 in each row and column. Its order is2⁵5!=3840.'],
 'WᵀΣW=I. A real symmetric matrix κ satisfies PᵀκP=κ for every P∈B₅ if and only if κ=cI. Thus whitening alone does not prove that the original Gramian was B₅ invariant.',
 'By the spectral theorem write Σ=QDQᵀ with Q orthogonal and positive diagonal D. Then W=QD^(−1/2)Qᵀ, and multiplication gives the identity. For the group claim, flip the sign of coordinate i. An off-diagonal entry κ_ij with j≠i changes sign under conjugation, so invariance forces it to be zero. Permutations then exchange diagonal entries, forcing them all equal. Conversely a scalar multiple of the identity is fixed by every orthogonal signed permutation. Counting the group requires an arbitrary permutation and five independent signs, giving the stated order.',
 'Take Σ=diag(1,4,9,16,25).',
 'Its whitening matrix is diag(1,1/2,1/3,1/4,1/5), and direct rational multiplication yields I. But swapping the first two coordinates changes Σ, so the original metric lacks B₅ symmetry. A generic vector with distinct nonzero absolute coordinates has3840 distinct signed-permutation images; ties or zeros introduce stabilizers and shorten its orbit. A claimed chamber index therefore needs a tie convention and an admissibility test.',
 'The geometry separates normalization, symmetry and orbit counting, making each claim independently checkable.',
 'A singular Gramian has no inverse square root on the full space; a pseudoinverse instead whitens only its range. The number3840 is not the totient value384 or the dimension248 of E₈.',
 'For a measured Gramian, quantify the symmetry defect max_P||PᵀΣP−Σ|| and compare it with the exact group average, which is(trΣ/5)I.',
 [('Humphreys Reflection Groups and Coxeter Groups, publisher record','https://doi.org/10.1017/CBO9780511623646')])

E('2025-10-01','Hensel','A','p-adic analysis','Newton lifting supplies an exact p-adic certificate rather than a digest comparison',
 'Which congruence, derivative unit and precision doubling justify the proposed p-adic realization?',
 'The Rust scaffold named Newton/Hensel and p-adic logarithms. A small exact lift gives those words mathematical substance. It also clarifies why reducing a cryptographic digest modulo p is unrelated to comparing p-adic realizations of an arithmetic object.',
 ['For f∈Z_p[X], a simple root modulo p is a residue a₀ with f(a₀)≡0 modp and f′(a₀) not divisible by p.', 'A Newton step a′=a−f(a)/f′(a) is defined in Z_p when f′(a) is a unit. Congruence precision is measured by v_p.'],
 'If v_p(f(a))≥m≥1 and f′(a) is a unit, the Newton step has v_p(f(a′))≥2m and a′≡a modp^m. Repetition converges to the unique root in a+pZ_p. For f=X²−2,p=7, the residue3 lifts to a genuine7-adic square root.',
 'Taylor expansion gives f(a+h)=f(a)+f′(a)h+h²g for integral g. Choose h=−f(a)/f′(a), whose valuation is at least m; the first two terms cancel and the remainder has valuation at least2m. The derivative remains a unit because a′≡a modp. The successive corrections have valuations tending to infinity, so completeness of Z_p gives a root. If two roots x,y share a modulo p, then f(x)−f(y)=(x−y)u with u a unit, by the same derivative argument; hence x=y.',
 'Lift the square root by ordinary congruence arithmetic.',
 'Modulo7 the root is3. Write a=3+7k. The congruence a²−2≡7+42k mod49 requires1+6k≡0 mod7, giving k=1 and a=10 mod49. Write a=10+49k; modulo343 its defect is98+980k, yielding2+20k≡0 mod7 and k=2, so a=108 mod343. Indeed108²−2=11662=34·343. Each check is an exact integer divisibility statement.',
 'The p-adic value is specified by compatible congruences and a uniqueness theorem, not a floating decimal or a hash residue.',
 'The ordinary p-adic logarithm needs a stated convergence domain such as1+pZ_p for odd p. Comparing real and p-adic periods additionally requires actual comparison maps; no such map is supplied by the lift alone.',
 'Implement precision-doubling lifts together with exact polynomial residual valuations and prove compatibility of all emitted congruence certificates.',
 [('Milne Algebraic Number Theory','https://www.jmilne.org/math/CourseNotes/ANT.pdf')])

E('2025-10-03','Cone','A','Homological algebra','The mapping cone turns an echo equivalence into an acyclicity test',
 'Which chain map is being compared, and does its cone have zero homology in every degree?',
 'The corrected Morphic Echo proposal replaced informal equality with a chain map and its cone. This is a precise mathematical improvement: quasi-isomorphism has an exact obstruction complex, and the identity map admits an explicit contracting homotopy.',
 ['Use cochain complexes with d increasing degree. For a cochain map f:C→D, Cone(f)ⁿ=Dⁿ⊕C^(n+1), with differential d(y,x)=(d_Dy+fx,−d_Cx).', 'A quasi-isomorphism induces an isomorphism on every cohomology group. A complex is contractible if dh+hd is its identity for some degree−1 map h.'],
 'Cone(id_C) is contractible by h(y,x)=(0,y). More generally Cone(f) is acyclic if and only if f is a quasi-isomorphism.',
 'The cone differential squares to zero because d_Df=fd_C: its first component has the two cross terms cancel, while the second is d_C²x. For f=id, dh(y,x)=(y,−dy) and hd(y,x)=(0,dy+x); their sum is(y,x). Contractibility forces cohomology to vanish because every closed v equals d(hv). For general f, the short exact sequence0→D→Cone(f)→C[1]→0 gives a long exact cohomology sequence whose connecting map is H(f). Exactness shows that vanishing cone cohomology is equivalent to H(f) being injective and surjective in every degree. This classical exact-sequence input is stated explicitly.',
 'Let C and D both be Q concentrated in degree zero, with f multiplication by2.',
 'The cone is Q in degree−1 mapped by2 to Q in degree zero, so its kernel and cokernel are both zero. Thus multiplication by2 is a quasi-isomorphism over Q. Over Z the same cone has cokernel Z/2, so it is not acyclic. The coefficient ring changes the certificate even though the displayed matrix is unchanged.',
 'An echo claim becomes a concrete complex, a coefficient choice and an exact homology calculation.',
 'A hash comparison does not establish a chain-map equation. Acyclicity and contractibility are also distinct for general complexes over arbitrary rings; only the identity-cone case here is given an explicit contraction.',
 'For bounded free integer complexes, certify d²=0 and the chain-map identities first, then use Smith forms to compute the cone homology including torsion.',
 [('Stacks Project cones of complexes','https://stacks.math.columbia.edu/tag/0149')])

E('2025-10-03','Čech','A','Descent','Transition functions satisfy a cocycle equation, and gauge changes preserve it',
 'Are the overlap functions genuine descent data, and which gauge-invariant obstruction is actually computed?',
 'The corrected curvature proposal used c_ijk=g_ijg_jkg_ki. For abelian transition functions this supplies a finite, exact descent condition. It should be distinguished from a differential curvature two-form and from the hash attached to a record.',
 ['On a three-patch cover use positive real transition functions g_ij, with g_ji=g_ij⁻¹. Compatible line-bundle descent requires g₁₂g₂₃g₃₁=1 on the triple overlap.', 'A change of local trivialization by positive h_i sends g_ij to g′_ij=h_i⁻¹g_ijh_j. For constant positive functions, logarithms turn multiplication into addition.'],
 'The triple product c=g₁₂g₂₃g₃₁ is invariant under these abelian gauge changes. It equals one exactly when the logarithmic edge values sum to zero around the triangle. A nonunit product cannot be repaired by changing local trivializations.',
 'Multiply the three transformed functions: h₁⁻¹g₁₂h₂·h₂⁻¹g₂₃h₃·h₃⁻¹g₃₁h₁=h₁⁻¹ch₁=c. Taking logarithms gives logc=logg₁₂+logg₂₃+logg₃₁. On a filled triangle, a closed additive edge cochain is exact: choose local potentials v₁=0,v₂=logg₁₂,v₃=logg₁₂+logg₂₃; the third edge equation holds precisely when the sum vanishes. This is a finite descent calculation with every overlap specified.',
 'Set g₁₂=2,g₂₃=3 and first choose g₃₁=1/6.',
 'The product is one, and local weights(1,2,6) exhibit g_ij=h_j/h_i around the cycle. Replacing the final value by1/5 gives c=6/5. No gauge choices h_i can change that value to one. In logarithmic coordinates the defect is log(6/5), a real cocycle-failure measurement, while an integer coefficient model would require a different group and differential.',
 'The descent condition and its invariant failure have explicit algebraic meaning, so a proposed curvature detector has a precise target.',
 'For nonabelian transition groups the product transforms by conjugation rather than remaining literally fixed. A connection curvature and an anomaly class require further differential or cohomological data; this three-number example does not establish those identifications.',
 'Build a larger cover with specified intersection groups and verify every coboundary identity, then determine which gauge-invariant obstruction classes survive refinement.',
 [('Stacks Project descent data','https://stacks.math.columbia.edu/tag/023U')])

E('2025-10-03','pushout','A','Category theory','A pushout glues compatible maps by a universal property',
 'Which maps are being glued, and what uniquely characterizes the proposed sealing object?',
 'The sealing proposal invoked a pushout and verifier replay. A finite vector-space pushout provides an actual mathematical model: it glues two interfaces along their shared part. Its universal property expresses compatibility independently of file names, hashes or motives.',
 ['For maps i:A→B and j:A→C over Q, define P=(B⊕C)/{(i(a),−j(a)):a∈A}.', 'The canonical maps β:B→P and γ:C→P send b to[(b,0)] and c to[(0,c)]. They satisfy βi=γj.'],
 'For every pair u:B→V,v:C→V with ui=vj, there is one linear map w:P→V with wβ=u,wγ=v. Thus P is a pushout. If i and j are injective, dimP=dimB+dimC−dimA.',
 'Define a map on the direct sum by(b,c)↦u(b)+v(c). On a relation vector(i(a),−j(a)) its value is ui(a)−vj(a)=0, so it descends to the quotient. Its composites have the prescribed values. Every quotient class is a sum of an image from B and one from C, so these composites determine w uniquely. For injective i and j, the relation subspace is an injected copy of A; subtracting its dimension gives the formula.',
 'Take A=Q,B=C=Q² and let both maps send a to(a,0).',
 'The pushout has dimension three, with coordinates that can be written[(b₁,b₂;c₁,c₂)]↦(b₁+c₁,b₂,c₂). Its kernel consists exactly of(a,0;−a,0), the relation subspace. Compatible maps u(b)=b₁+2b₂ and v(c)=c₁+3c₂ glue to w(x,y,z)=x+2y+3z. Changing one map’s shared-coordinate coefficient would break compatibility and prevent that factorization.',
 'The construction gives sealing an exact interface-gluing interpretation and a finite certificate of compatibility.',
 'A software manifest must specify a category and actual maps before its merge is a pushout. Universal constructions do not automatically supply arithmetic motives, semantic correctness or replay equality. Those require independent definitions and verification.',
 'Specify a category of typed finite execution records and prove that the proposed merge satisfies this universal property, including how conflicting shared fields are rejected.',
 [('Stacks Project pushouts of modules','https://stacks.math.columbia.edu/tag/0D12')])

E('2025-10-05','Sel','A','Arithmetic exact sequences','A rank-two Mordell–Weil group forces a4-Selmer group of at least sixteen elements',
 'Which claims are actual group cardinalities, and do they satisfy the Kummer exact sequence before any BSD conclusion is attempted?',
 'The389a1 passage reported rank two and both2- and4-Selmer cardinality four. If interpreted literally, these quantities conflict with elementary consequences of the Kummer exact sequence. The positive result is a compact exact-sequence audit that arithmetic receipts must pass.',
 ['For an elliptic curve E/Q and n≥2, the Kummer sequence gives0→E(Q)/nE(Q)→Sel_n(E/Q)→Sha(E/Q)[n]→0.', 'By the Mordell–Weil structure theorem write E(Q)≅Zʳ⊕T with finite torsion T. Consequently |E(Q)/nE(Q)|=nʳ|T/nT|.'],
 'If rankE(Q)=2, then |Sel₄|≥16. If additionally |Sel₂|=4, then Sha[2]=0 and the entire2-primary torsion subgroup Sha[2^∞] is zero. These are conditional deductions from genuine certified rank and Selmer groups, not validation of the historical computations.',
 'The injection in the exact sequence gives |Sel_n|≥|E/nE|≥nʳ, proving the lower bound. At n=2,r=2, the lower bound is four. Equality forces both |T/2T|=1 and |Sha[2]|=1 because their product with four equals four. If an abelian group has a nonzero element of order2^k, multiplying it by2^(k−1) produces a nonzero element of order two. Therefore absence of2-torsion eliminates every finite2-power-order element. No finiteness assumption on all of Sha is needed for this last elementary implication.',
 'Check the free-rank model Z² at the two levels.',
 'Its quotient modulo2 has four elements, represented by coordinate pairs in{0,1}². Its quotient modulo4 has sixteen, represented by{0,1,2,3}². The reduction map modulo4→modulo2 has four-element fibers. An identity-looking2×2 Smith matrix between unspecified lattices cannot replace these quotient cardinalities or prove that a purported4-Selmer group has only four elements.',
 'The exact sequence supplies both a contradiction test and a valid route from a minimal2-Selmer group to a2-primary Sha conclusion when its premises are genuinely proved.',
 'The historical rank, regulator and analytic intervals have not been independently certified here. A number labeled Sel₄ might denote another invariant; that ambiguity must be resolved before interpreting its value.',
 'Produce explicit descent maps, local solubility certificates and quotient presentations, then verify the Kummer injection and all group orders with exact integer algebra.',
 [('Milne Elliptic Curves, Selmer exact sequence','https://www.jmilne.org/math/Books/EC2.pdf')])

E('2025-10-05','regulator','A','Lattices and heights','A regulator is a Gram determinant tied to a generator basis',
 'Which height pairing and independent generators define the regulator, and what changes under a finite-index basis replacement?',
 'The reported narrow regulator interval is meaningful only after fixing the points, height convention and error bounds. A positive-definite lattice model gives the exact change-of-basis law and shows why determinant data alone cannot certify that the chosen points generate the full lattice.',
 ['For independent generators P₁,…,P_r with symmetric height-pairing matrix G, the regulator is detG in the declared normalization.', 'Replacing the generator column by an integer matrix M changes the Gram matrix to G′=MᵀGM. A unimodular matrix has determinant±1.'],
 'detG′=(detM)²detG. A unimodular change preserves the regulator, while a finite-index sublattice of index m multiplies it by m². Linear dependence makes the Gram determinant zero.',
 'The determinant identity follows directly from multiplicativity of determinants and detMᵀ=detM. For a full-rank integer coordinate matrix, the index of the generated sublattice is |detM|, as can be proved by Smith form. Thus its squared covolume scales by the square of the index. Positive definiteness makes independent-vector Gram determinants positive. If the vectors are dependent, their coordinate matrix has a nontrivial kernel and so does their Gram matrix, forcing determinant zero.',
 'Take G=[[2,1],[1,3]], whose determinant is five.',
 'The unimodular matrix M=[[1,1],[0,1]] gives G′=[[2,3],[3,7]], still with determinant five. Replacing the second generator by twice itself gives diag(1,2)ᵀGdiag(1,2)=[[2,2],[2,12]], whose determinant is twenty, four times five. The latter pair spans an index-two sublattice. A numerical determinant near twenty would therefore not by itself identify the full-lattice regulator.',
 'The regulator becomes an invariant with explicit basis and saturation conditions rather than a decimal detached from its generators.',
 'An elliptic canonical-height computation additionally needs normalization, rigorous truncation bounds and a proof of independence. A Smith matrix from another complex does not certify those inputs. None of the historical decimal intervals is assumed verified here.',
 'Given candidate points, certify the height matrix by intervals, bound its smallest eigenvalue away from zero, and prove saturation at each relevant prime before calling its determinant the full Mordell–Weil regulator.',
 [('Milne Elliptic Curves, heights and Mordell–Weil groups','https://www.jmilne.org/math/Books/EC2.pdf')])

E('2025-10-09','sqrt5','A','Special values and units','A real quadratic L-derivative is exactly the logarithm of a unit',
 'Which character, conductor and regulator normalization make the proposed Stark comparison an actual exact identity?',
 'The Stark reframing supplied Q(√5), its golden unit and L′(0,χ). There is an elegant complete classical model: use the primitive even quadratic Dirichlet character modulo five. Hurwitz-zeta and gamma identities then evaluate its derivative exactly, without invoking an unproved general regulator theorem.',
 ['Let χ₅(1)=χ₅(4)=1,χ₅(2)=χ₅(3)=−1 and χ₅(5k)=0. Put φ=(1+√5)/2.', 'For Re(s)>1, L(s,χ₅)=5^(−s)Σ_(a=1)^4χ₅(a)ζ(s,a/5), then extend analytically using Hurwitz zeta.'],
 'L(0,χ₅)=0 and L′(0,χ₅)=logφ. The element φ is an algebraic unit of norm−1, satisfying φ²−φ−1=0. This is a precisely normalized regulator-sized logarithm, not a proof of every proposed Stark realization.',
 'Use the classical identities ζ(0,x)=1/2−x and ζ′(0,x)=logΓ(x)−(1/2)log(2π). The weighted constant and linear sums vanish, giving L(0)=0; thus differentiating5^(−s) contributes no extra term. The character sum is zero, so the log(2π) terms also cancel. Therefore L′(0)=log[Γ(1/5)Γ(4/5)/(Γ(2/5)Γ(3/5))]. Euler’s reflection formula turns the ratio into sin(2π/5)/sin(π/5)=2cos(π/5)=φ. The special-function identities are the explicit classical inputs; the cancellation and unit comparison are derived here. The conjugate unit is(1−√5)/2=−φ⁻¹, giving norm−1.',
 'Separate this character from unspecified ray-class data over Q(√5).',
 'The displayed χ₅ is a character over Q of conductor five. It cuts out the real quadratic field, but is not by itself a complete choice of ray-class character over that field. Its derivative exponentiates to φ in the stated real embedding; the other embedding has negative value, and absolute logarithms or totally positive-unit conventions can introduce a factor two. Squaring φ gives a norm-one unit and doubles the logarithm.',
 'The recovered idea has an actual special-value identity and an exact algebraic unit certificate.',
 'No general toric motivic class, mixed-signature Eisenstein cocycle or p-adic comparison is constructed. The universal claim of unconditional validity for all totally real or CM situations is not adopted.',
 'Specify a genuine ray-class character, its infinity type and vanishing order, then compare a rigorously evaluated L-leading term with a candidate unit using a stated regulator map and norm relations.',
 [('NIST DLMF Hurwitz zeta special values','https://dlmf.nist.gov/25.11'),('NIST DLMF gamma reflection','https://dlmf.nist.gov/5.5')])

E('2025-10-16','spectral-zeta','A','Spectral analysis','Heat residues follow from a Mellin transform and need not be integer indices',
 'Which operator, heat expansion and Mellin normalization define the proposed residue?',
 'The Global Residue Index proposal combined spectral residues, complex residues and integer indices. A circle Laplacian gives a complete countercheck and a positive calculation: its heat leading term determines a zeta residue that varies continuously with the circle length.',
 ['On a circle of circumference L, remove the zero mode from −d²/dx². The nonzero eigenvalues are(2πn/L)²,n∈Z minus{0}.', 'Let K(t)=Σ_(n≠0)e^(−tλ_n) and ζ_A(s)=Σ_(n≠0)λ_n^(−s). For Re(s)>1/2, Γ(s)ζ_A(s)=∫₀∞t^(s−1)K(t)dt.'],
 'ζ_A(s)=2(L/(2π))^(2s)ζ_R(2s), so its residue at s=1/2 is L/(2π). Equivalently K(t) has leading term L/(√(4πt)), whose Mellin pole divided by Γ(1/2) gives the same residue. It is not generally an integer.',
 'The spectral series factors immediately into a scale and2Σn^(−2s). The Riemann zeta function has residue one at argument one, so ζ_R(2s) has residue1/2 at s=1/2; multiplication gives L/(2π). For the Mellin identity, integrate each positive heat term using the substitution u=tλ_n, giving Γ(s)λ_n^(−s); absolute convergence permits summation. Splitting the heat integral at one shows that a term a t^(−1/2) contributes a/(s−1/2) to Γ(s)ζ_A(s). With a=L/(2√π), division by√π gives L/(2π). This explains the normalization rather than equating different residues by terminology.',
 'Take circles of lengths2π andπ.',
 'Their zeta residues are respectively one and one-half, while the topology is the same. Scaling the length by c multiplies the residue by c. An integer Fredholm index cannot track this continuous noninteger variation without a different definition or an additional normalization theorem. Complex contour residues likewise depend on the particular meromorphic function whose coefficient is being taken.',
 'The spectral residue is fully computed and its relationship to a heat coefficient is proved.',
 'The heat expansion and meromorphic continuation for general elliptic operators require analytic hypotheses. This example does not identify the proposed logarithmic, categorical and topological indices, nor prove GRIT.',
 'Choose one elliptic family and state its supertrace, zero-mode subtraction and twisting class; compare the resulting integer index with separately normalized zeta residues before seeking an equality.',
 [('Vassilevich Heat kernel expansion: user’s manual','https://arxiv.org/abs/hep-th/0306138')])

E('2025-10-09','Index','A','Index theory in finite dimension','A heat supertrace equals an Euler index because nonzero modes pair',
 'Which grading and differential make the claimed protected index independent of heat time?',
 'The index tables have a rigorous finite analogue that explains the mechanism behind protection: a differential pairs nonzero even and odd modes, so their heat contributions cancel. An ordinary heat trace does not have this cancellation.',
 ['Take a two-term finite-dimensional real or complex Hilbert complex C⁰→ᵈC¹. Let D=d+d* on C⁰⊕C¹, graded even/odd.', 'The heat supertrace is Str(e^(−tD²))=Tr_(C⁰)e^(−td*d)−Tr_(C¹)e^(−tdd*).'],
 'For every t≥0 in this finite-dimensional complex, Str(e^(−tD²))=dimkerd−dimcokerd=dimC⁰−dimC¹. More generally a finite complex has heat supertrace equal to its alternating cohomology dimension.',
 'The positive spectra of d*d and dd* agree including multiplicities: if d*d v=λv with λ>0, then dv≠0 and dd*(dv)=λdv, with inverse correspondence λ⁻¹d* on the eigenspaces. Hence e^(−tλ) cancels between the two graded traces. The remaining zero modes are kerd in degree zero and ker d*=cokerd in degree one. Rank-nullity gives their dimension difference dimC⁰−dimC¹. The same pairing on each degree proves the finite-complex statement, equivalently by decomposing into harmonic spaces and two-term exact pairs.',
 'Use d=[[1,−1],[0,0]] between two copies of R².',
 'Both d*d and dd* have eigenvalues0,2. Each ordinary heat trace is1+e^(−2t), so the total ungraded trace is2+2e^(−2t), which changes with time. Their supertrace is zero for every t. The cohomology dimensions are one in each degree, also giving1−1=0. This explicitly demonstrates why the grading and the differential identity are part of the index theorem’s mechanism.',
 'A protected quantity can be constructed and checked, but its protection comes from a proved pairing of modes.',
 'The finite theorem is not the Atiyah–Singer theorem for a differential operator on a manifold. Twists, boundary conditions and APS corrections require their own hypotheses. A generic residue trace has no reason to share this cancellation.',
 'Construct a finite discretization that preserves d²=0 and grading exactly, then prove that its supertrace index matches a chosen topological cochain complex before taking any continuum limit.',
 [('Atiyah and Singer The index of elliptic operators I','https://doi.org/10.2307/1970715')])

E('2025-10-12','PF ODE','U','Ordinary differential equations','A Picard–Fuchs basis comparison is determined by values and derivatives at one regular point',
 'Do both proposed period constructions solve the same normalized ODE, and what initial data fix their constant change of basis?',
 'The period comparison returned genuinely mismatched certified leaves. A constant scale or symplectic mixing is a hypothesis to prove, not a consequence of the word period. The recovered second-order equation gives an exact local uniqueness test and a useful series certificate.',
 ['Consider(1−u²)a″−a/4=0 on a simply connected domain avoiding±1. A fundamental solution matrix records two solutions and their first derivatives.', 'For scalar solutions y₁,y₂, their Wronskian is W=y₁y₂′−y₁′y₂.'],
 'The Wronskian is constant. Any two fundamental matrices for the same equation differ by a constant invertible matrix. At u=0 the normalized solutions have expansions y₁=1+u²/8+3u⁴/128+⋯ and y₂=u+u³/24+5u⁵/384+⋯.',
 'Rewrite the equation as a″=a/[4(1−u²)]. Differentiating W gives y₁y₂″−y₁″y₂=0. Both solution matrices satisfy the same first-order system F′=AF; hence(F⁻¹G)′=−F⁻¹AF F⁻¹G+F⁻¹AG=0. The constant is determined by the value-and-derivative matrices at any regular point. For a=Σc_nuⁿ, coefficient comparison yields c_(n+2)=[n(n−1)+1/4]c_n/[(n+2)(n+1)]. Substituting initial data(1,0) and(0,1) gives the displayed rational coefficients and W(0)=1.',
 'Compare a claimed second basis with z₁=2y₁+y₂ and z₂=y₁+y₂.',
 'The change matrix is[[2,1],[1,1]], determinant one, so it preserves the two-dimensional standard alternating form. Its value-and-derivative data at zero are exactly that matrix. A mere scale/sign fit is a smaller class than all such changes; conversely six matching sampled values do not prove equality unless the ODE and initial data are already certified. A hash mismatch may reflect normalization or a genuinely different function; the differential test distinguishes them.',
 'The comparison becomes a finite initial-data and differential-equation certificate with a declared normalization.',
 'The equation alone does not identify a specific Seiberg–Witten differential, period cycle or global monodromy basis. In rank one, WDVV commutator conditions are scalar and cannot replace these missing differential constraints.',
 'Certify each numerical solution’s residual and initial-data enclosure, then use a Grönwall estimate for the first-order system to bound their discrepancy across a regular comparison domain.',
 [('Isidro et al Picard–Fuchs equations for Seiberg–Witten models','https://arxiv.org/abs/hep-th/9703186')])

E('2025-10-09','heat equation','A','Theta functions','A theta heat equation and an elliptic transformation can be proved term by term',
 'Which q and theta conventions make the proposed heat equation and Jacobi covariance agree?',
 'The October tables included Jacobi forms, heat equations and modular period comparisons. The elementary theta series supplies a completely normalized case. It also shows why an index or coefficient bound cannot be copied between conventions without checking its transformation law.',
 ['For Imτ>0, set θ(τ,z)=Σ_(n∈Z)exp(πin²τ+2πinz). This uses q=exp(πiτ).', 'On compact subsets with Imτ bounded below, Gaussian decay dominates every fixed derivative in τ or z, allowing termwise differentiation.'],
 '∂_τθ=(1/(4πi))∂²_zθ. Also θ(τ,z+1)=θ(τ,z) and θ(τ,z+τ)=exp(−πiτ−2πiz)θ(τ,z). The last factor is the half-index convention for this theta function.',
 'Differentiating one term with respect to τ multiplies it byπin². Differentiating twice in z multiplies it by−4π²n²; division by4πi givesπin², proving the heat equation. Shifting z by one contributes exp(2πin)=1. For the τ shift, n²+2n=(n+1)²−1; reindexing n+1 extracts exp(−πiτ−2πiz) and leaves the original series. The convergent Gaussian bounds justify both the differentiations and the index shift, so these are identities of holomorphic functions on their stated domain.',
 'Inspect the first nonconstant modes and a prospective finite-coefficient certificate.',
 'At fixed τ the n=±1 terms are2qcos(2πz). Their z-second derivative divided by4πi is2πi qcos(2πz), exactly their τ derivative. But agreement of finitely many Fourier modes does not identify an unrestricted function: adding q^N changes none of the lower coefficients. A genuine Sturm-type certificate needs a specified finite-dimensional modular or Jacobi space, its weight, level, index and a correct theorem bounding vanishing.',
 'The exact transformation and heat identities are a solid base for a normalized modular-gauge comparison.',
 'No Jacobi bound B=2 or cutoff K=2 is inferred from this theta function. Scalar modular, half-index theta and index-four Jacobi forms have different spaces and coefficient conventions. Nekrasov/PF matching requires its own normalization data.',
 'Specify a finite-dimensional target space and construct a coefficient matrix of a proved basis; exact rank then determines how many coefficients suffice to identify an element within that space.',
 [('NIST DLMF theta definitions and transformations','https://dlmf.nist.gov/20.2')])

E('2025-10-10','Yukawa','U','Spectral linear algebra','An index does not determine Yukawa singular values',
 'Which invariant is protected, and which additional metric data determine the unprotected singular values?',
 'The October program tried to link masses or Yukawa data to a protected index pushforward. Finite linear algebra gives a decisive constraint on any such bridge: an index can remain fixed while every nonzero singular value varies. A theorem relating them would need extra structure beyond index equality.',
 ['For a linear map Y:Cⁿ→Cᵐ, its finite Fredholm index is dimkerY−dimcokerY=n−m.', 'The singular values are square roots of the eigenvalues of Y*Y and depend on the chosen Hermitian metrics. They are not determined by the index.'],
 'For Y_t:C→C² defined by z↦(tz,0), the index is−1 for every complex t, while its sole singular value is|t|. At t=0 the kernel and cokernel dimensions both jump, but their difference remains−1.',
 'If t≠0, the map is injective and its range has dimension one, so ker dimension is zero and coker dimension one. At zero, the kernel has dimension one and the cokernel dimension two. Both give index−1. Meanwhile Y_t*Y_t is the1×1 matrix|t|², proving the singular-value formula. The index equality also follows from rank-nullity for any finite map, regardless of its entries. Thus an index theorem at this level cannot recover a continuous scale such as|t| without another equation that restricts t.',
 'Compare t=1 with t=100 and with zero.',
 'All three maps have the same index. Their singular values are1,100,0, and their operator norms have those same values. A proposed formula multiplying the singular value by a separately specified scale can consequently vary by a factor100 while every index datum remains unchanged. This is an exact family, not a numerical near-counterexample. Gauge or basis changes that are unitary preserve singular values, whereas arbitrary invertible basis changes need not.',
 'The distinction identifies the genuine mathematical burden of connecting a protected invariant to metric observables.',
 'No physical mass convention is adopted from the recovered factor v/2, and no biological or particle prediction follows. A topological index may constrain zero modes or differences of dimensions without setting nonzero spectral scales.',
 'State a metric or variational principle that restricts Y inside a fixed index class, then prove quantitative bounds on its singular values; only those added hypotheses can support a scale prediction.',
 [('NIST DLMF matrix spectral notation','https://dlmf.nist.gov/1.2')])

E('2025-10-10','Tor','A','Derived algebra','A Tor group requires modules and a resolution before it can model an obstruction',
 'Which ring and modules define the claimed derived interaction, and what does its first Tor group actually calculate?',
 'The Higgs/torsor synthesis invoked Tor₁ without a specified resolution. A small exact model demonstrates what a derived tensor product detects: failure of a relation to remain injective after tensoring. This is meaningful homological mathematics but does not automatically identify a physical field.',
 ['Let R=k[x] over a field k and M=R/(x). A free resolution is0→R→ˣR→M→0.', 'Tor_i^R(M,N) is the i-th homology of a free resolution of M tensored with N. Ordinary tensor product is its degree-zero part.'],
 'Tor₀^R(M,M)≅k and Tor₁^R(M,M)≅k, while higher Tor groups vanish for this resolution. By contrast Tor₁^R(R,M)=0 because R is free.',
 'Multiplication by x on R is injective, since the polynomial ring over a field is a domain; its cokernel is M, proving exactness of the resolution. Tensor with M. On M the element x acts as zero, so the resulting two-term complex is M→⁰M. Its kernel in degree one is M and its cokernel in degree zero is M, with no other terms. The one-term free resolution of R instead has no degree-one term, giving zero first Tor. The difference is structural: the relation x becomes zero after imposing x=0, leaving a degree-one class.',
 'Replace the second module by N=R/(x−1).',
 'Multiplication by x acts as multiplication by one on N, so the tensored resolution is N→¹N, an isomorphism. Both its kernel and cokernel vanish. Thus Tor₁(M,N)=0 and M⊗N=0. The supports x=0 and x=1 do not meet, in contrast to the self-intersection example. This calculation supplies an explicit input-dependent obstruction, not a universal nonzero derived field.',
 'The categorical language now has an exact ring, modules, maps and homology certificate.',
 'Nothing here identifies Tor₁ with a Higgs bundle, a particle mass or a determinant pushforward. Those interpretations would require a specified functor and a theorem preserving the relevant structures, not just matching notation.',
 'For a declared intersection of algebraic subschemes, compute a Koszul resolution and determine when higher Tor measures nontransversality, then state precisely which geometric obstruction it represents.',
 [('Stacks Project Tor and resolutions','https://stacks.math.columbia.edu/tag/00M0')])

E('2025-10-14','E₈','U','Root systems','The E₈ roots, its Lie dimension and the totient384 are different exact counts',
 'Which finite set or vector space is being counted by each dimension in the framework?',
 'The pre-geometric framework combined E₈, rank384 and φ(1680). These numbers can all be checked, but they count different mathematical objects. An explicit root construction gives a positive algebraic certificate without claiming that the resulting counts establish a spacetime model.',
 ['In R⁸ take roots of two kinds: vectors with two entries±1 and six zeros, and vectors with all entries±1/2 with an even number of minus signs.', 'Euler’s totient φ(n) counts invertible residues modulo n. The signed-permutation group B₅ has order3840, separately.'],
 'The displayed E₈ root set has112+128=240 norm-squared-two roots spanning R⁸. The associated complex simple Lie algebra has dimension8+240=248. Also φ(1680)=384, since1680=2⁴·3·5·7.',
 'There are choose(8,2) ways to choose the nonzero coordinates of an integer root and four sign choices, yielding112. There are2⁸ half-sign patterns, half with even parity, yielding128. Every vector has norm squared two. Integer roots e_i−e_j span the coordinate-sum-zero subspace, and e₁+e₂ is outside it, proving full rank eight. For a complex simple Lie algebra the root decomposition consists of an eight-dimensional Cartan subalgebra and one-dimensional spaces for each root, giving248; that structural root-decomposition fact is the classical input. The totient formula gives1680(1−1/2)(1−1/3)(1−1/5)(1−1/7)=384.',
 'Compare root count, Lie rank, Lie dimension and an independently chosen categorical rank.',
 'They are240,8,248 and, if separately constructed, a possible number384 of simple objects. No equality forces a category with384 simples or global dimension1680. Reflection closure of the displayed root set is additionally checked exactly by the verifier: for norm-two α, s_α(β)=β−(α·β)α must remain in the set for every ordered pair. This verifies root-system structure beyond merely counting short vectors.',
 'The numbers become concrete algebraic invariants with distinct definitions, and the root structure receives an exact finite certificate.',
 'These calculations do not construct F-symbols, scattering amplitudes, an emergent metric or a physical coupling. Matching numerical counts across domains supplies no functor or equivalence by itself.',
 'Specify a genuine category or representation construction from the root data and prove its rank, dimensions and fusion rules rather than using the totient as a substitute for that construction.',
 [('American Institute of Mathematics explicit E₈ roots','https://admin.aimath.org/E8/e8.html')])

E('2025-10-14','Ext','A','Semisimple algebra','Semisimplicity kills ordinary extension classes',
 'Which cohomology theory measures the proposed categorical deformation, and does ordinary Ext vanish under the stated semisimplicity assumption?',
 'The October audit correctly questioned using positive-degree Ext in a semisimple setting. The exact reason is elementary: every short exact sequence splits, and every object is projective. A deformation theory must therefore identify another complex or weaken semisimplicity.',
 ['An abelian category is semisimple here when every short exact sequence splits. In finite-dimensional vector spaces, every subspace has a complement.', 'Ext¹(C,A) classifies short exact sequences0→A→B→C→0 up to equivalence; higher Ext can be computed from projective resolutions when available.'],
 'In a semisimple abelian category with the usual Ext construction, Extⁿ(C,A)=0 for n>0. For finite-dimensional vector spaces, a split extension is explicitly B≅A⊕C.',
 'Choose a section s:C→B of the surjection p:B→C. Then(a,c)↦i(a)+s(c) is an isomorphism A⊕C→B: injectivity follows after applying p, and surjectivity follows by subtracting s(p(b)) from b. Hence every extension represents the zero class in Ext¹. More generally, given an epimorphism and a map from any object, a splitting of the epimorphism lifts that map; therefore every object is projective. A resolution concentrated in degree zero computes all higher Ext as zero. This is a theorem about this specific derived functor, not every cohomology assigned to a tensor category.',
 'Compare vector spaces with modules over the dual numbers k[ε]/(ε²).',
 'In the latter category the sequence0→k→k[ε]/(ε²)→k→0, where the first map sends1 to ε, does not split as a module sequence. A hypothetical lift of1 from the quotient would be1+cε, but multiplication by ε sends it to ε≠0, whereas ε acts as zero on k. Thus nontrivial extensions arise once the semisimple hypothesis is removed.',
 'The framework must select an obstruction theory that survives its own assumptions, rather than assigning nonzero Ext classes where they are forced to vanish.',
 'Davydov–Yetter, Hochschild and other deformation cohomologies have their own definitions; this argument does not identify them or claim they all vanish. A software field called cohomology does not fix which functor is intended.',
 'Specify the tensor-deformation cochain complex and prove that its differential squares to zero, then compute a low-degree example before interpreting it as geometric curvature.',
 [('Etingof Gelaki Nikshych Ostrik Tensor Categories','https://doi.org/10.1090/surv/205')])

E('2025-10-14','F-symbols','U','Braided tensor categories','A four-object pointed model has fully checkable F, R and S data',
 'What actual coherence and nondegeneracy equations does the proposed modular data satisfy?',
 'The speculative categorical framework lacked a genuine source for its F,R,S arrays. A small pointed braided model shows what a complete finite certificate looks like. Its fusion, associator, braiding and modular matrix can all be verified from bilinearity.',
 ['Let A=F₂² label four simple objects, with fusion a⊗b=a+b, unit zero and all dimensions one. Use associator F=1.', 'Define R(a,b)=(−1)^(a₁b₂), quadratic twist q(a)=R(a,a), and b(a,b)=R(a,b)R(b,a). Set S_(a,b)=b(a,b)/2.'],
 'The pentagon and hexagon equations hold; S is real orthogonal with S²=I, and its Verlinde coefficients are N_(a,b)^c=1 when c=a+b and zero otherwise. The global squared dimension is four.',
 'A constant associator one satisfies every pentagon product identically. The two hexagon equations reduce to multiplicativity of R in each argument, which follows from bilinearity of a₁b₂ over F₂. The symmetric bicharacter is(−1)^(a₁b₂+a₂b₁); its pairing is nondegenerate because any nonzero a has a b giving exponent one. Finite-character orthogonality givesΣ_x b(a,x)b(c,x)=4δ_(a,c), proving S²=I. Since S_(0,x)=1/2, the Verlinde sum becomes(1/4)Σ_x b(a+b+c,x), which is one precisely when a+b+c=0. Finally q(a+b)=q(a)q(b)b(a,b), checking the twist compatibility.',
 'List the twist values and compare their data requirements with a proposed384-object model.',
 'In order00,10,01,11 the twists are1,1,1,−1, and every S entry is±1/2. Four one-dimensional simples giveΣd_a²=4. The verifier checks all64 fusion triples, all pairings and all finite hexagon instances exactly. A larger claimed rank does not determine any of these arrays; it increases the number of coherence equations that need a source or proof.',
 'This finite model demonstrates constructive categorical mathematics instead of using numerical dimensions as proxies for coherence.',
 'The example is a pointed modular category related to the toric-code data; it is not the proposed E₈/384 category, a semiconductor scattering model or a physical realization. Those require separately specified functors and dynamics.',
 'Starting from a genuine larger fusion rule, solve or derive its coherence data and verify a modular nondegeneracy certificate before computing RT-type invariants.',
 [('Etingof et al Tensor Categories','https://doi.org/10.1090/surv/205')])

E('2025-10-14','Pareto','A','Optimization','A Pareto frontier contains points that no linear selector can choose',
 'Which objectives define dominance, and what information is lost when a two-objective frontier is replaced by H−λd?',
 'The dashboard selected high entropy and low maximal displacement, then inserted its selection into a coupling predictor. The optimization itself has a precise finite theory. Weighted scalarization can miss nondominated points, and an inserted normalization factor can cancel algebraically.',
 ['For pairs(d,H), smaller d and larger H are preferred. A point is dominated if another has no larger d and no smaller H, with at least one strict improvement.', 'For λ≥0 a linear selector maximizes H−λd. The recorded predictor has form A=(D²/d²)(248/r)(r/e^H), with d>0,r≠0.'],
 'Every strict optimizer of a positive weighted selector is nondominated, but not every nondominated point optimizes such a selector. The predictor simplifies to A=248D²d^(−2)e^(−H), independent of r.',
 'If a selected point were dominated, the dominating point would improve or preserve each weighted objective and strictly improve at least one with positive weight, contradicting strict optimality. For failure of the converse, use(0,0),(1,2/5),(2,2). All three are nondominated. For the middle point to beat the first requires λ<2/5; to beat the last requires λ>8/5. No λ satisfies both. The predictor cancellation follows by multiplication, and logarithmic differentiation gives dlogA=−2dlogd−dH when D is fixed. This separates actual sensitivity from a redundant displayed rank parameter.',
 'Use the three-point frontier to audit the dashboard rule.',
 'At λ=1, the endpoint scores are zero and zero, while the middle score is−3/5. The middle remains a valid tradeoff despite never winning any nonnegative linear weight. If d is multiplied by two at fixed H, the simplified predictor falls by a factor four; increasing H bylog2 halves it. These exact sensitivities do not constitute a fitted physical law.',
 'The selection rule and predictor now have explicit limitations and algebraic invariants that can be checked independently of presentation.',
 'The stored H may not be Shannon entropy unless its definition says so. No value of a physical fine-structure constant or causal relation follows from choosing a point on this frontier.',
 'Enumerate the whole nondominated finite set and use a declared constraint d≤d₀ to select among unsupported points; propagate uncertainty through the simplified predictor rather than its redundant factorization.',
 [('Boyd and Vandenberghe Convex Optimization, author text','https://web.stanford.edu/~boyd/cvxbook/')])

E('2025-10-21','Sieve','A','Finite harmonic analysis','Character orthogonality gives an exact frame bound before a large-sieve claim',
 'Which character family and sampling operator determine the best quadratic bound?',
 'The proposed q-large-sieve optimizer asserted an arithmetic inequality and automatic stability. A finite character transform supplies a rigorous foundation: its quadratic bound is an operator-norm statement. Orthogonality proves an exact special case and reveals the missing dependence on the chosen family.',
 ['For the cyclic group C_m use characters χ_k(r)=exp(2πikr/m), k,r=0,…,m−1.', 'For complex coefficients a_r, define S_k=Σ_r a_rχ_k(r). More generally a family has analysis matrix A with entries character values and bound ||Aa||²≤C||a||².'],
 'Σ_k|S_k|²=mΣ_r|a_r|². The optimal general constant is the largest eigenvalue of A*A. Repeating a character changes the frame bound, so the number and multiplicity of characters cannot be omitted.',
 'Expand the squared modulus: Σ_kΣ_(r,s)a_r conjugate(a_s)exp(2πik(r−s)/m). The inner geometric sum is m when r=s and zero otherwise, proving Parseval. For a general matrix, the Rayleigh quotient a*A*Aa/(a*a) is maximized at its largest eigenvalue by the Hermitian spectral theorem. If a character row is repeated, its rank-one contribution is added again to A*A and can increase that eigenvalue. The same finite algebra governs multiplicative characters after identifying a finite cyclic unit group; primitive-character restrictions or sums over multiple moduli change the family and require another bound.',
 'Take m=4 and coefficients(1,2,0,−1).',
 'Their squared norm is six, so the transformed squared norm is exactly twenty-four. At m=4 the transform uses only1,−1,i,−i and can be checked with exact integer pairs. A gradient vector in the same space satisfies this identity, but that identity alone specifies no learning rate, objective smoothness or decrease theorem.',
 'The arithmetic transform has an exact finite certificate, and the claimed inequality becomes a concrete spectral question.',
 'This does not prove the recovered multi-modulus weighted large-sieve inequality, its q^(ω(n)) factors or any datacenter speedup. A frame inequality does not automatically establish optimization stability.',
 'Specify the precise character matrix and weights, compute or bound its Gram spectrum, then combine that bound with a separate smooth-objective convergence theorem.',
 [('NIST DLMF discrete Fourier transform','https://dlmf.nist.gov/1.8')])

E('2025-10-21','projects gradients','A','Convex optimization','Projecting the updated state has a descent proof; clipping the gradient is a different operation',
 'Which projection is used, and which smoothness and feasibility hypotheses imply the claimed stability?',
 'The proposed update projected a gradient into a budget set. A standard projected-gradient theorem applies instead to projection of the proposed new state. Distinguishing the two operations yields both a rigorous descent certificate and a one-dimensional counterexample to automatic constraint preservation.',
 ['Let C⊂Rⁿ be nonempty closed and convex, x∈C, and f have L-Lipschitz gradient. Set x⁺=Π_C(x−η∇f(x)).', 'Euclidean projection is characterized by⟨z−Π_Cz,y−Π_Cz⟩≤0 for all y∈C.'],
 'f(x⁺)≤f(x)−(1/η−L/2)||x⁺−x||². Hence0<η<2/L gives descent unless the step is zero. The alternative x−ηΠ_C(∇f(x)) need not stay in C.',
 'Use the projection characterization with z=x−ηg, g=∇f(x), and y=x. Writing s=x⁺−x gives⟨g,s⟩≤−||s||²/η. The smoothness inequality f(x+s)≤f(x)+⟨g,s⟩+(L/2)||s||² then proves the descent bound. The projection characterization itself follows by differentiating the squared distance along each segment from the minimizer to y. Convexity of C makes those segments feasible and strict convexity of squared distance gives uniqueness of the projection.',
 'Compare the two updates on C=[−1,1], f(x)=(x−2)²/2 and x=1.',
 'The gradient is−1. Projecting the new state givesΠ_C(1+η)=1, the constrained minimizer. Projecting the gradient into C leaves−1, so the alternative gives1+η, outside the feasible set for everyη>0. For an interior example x=0 andη=1/2, the correct update gives1 and decreases f from two to one-half, consistent with the theorem L=1.',
 'A complete stability statement now rests on a specific update and explicit constants, rather than on the arithmetic name of the constraint.',
 'Nonconvex feasible sets can have multivalued projections, and a changing or stochastic objective needs additional analysis. No reported training acceleration or memory reduction is verified by this finite theorem.',
 'For a specified ellipsoidal budget, derive the exact projection through its scalar Lagrange-multiplier equation and certify that the numerical solver’s error preserves the descent margin.',
 [('Boyd and Vandenberghe Convex Optimization','https://web.stanford.edu/~boyd/cvxbook/')])

E('2025-10-23','lambda','A','Finite prime sums','A finite prime oscillatory sum has exact calculus but no automatic zero correspondence',
 'Which analytic identities follow from the actual finite sum, and what additional theorem would connect it to zeta zeros?',
 'The Ribbon–Lakeland draft supplied an explicit prime sum and derivative but also interpreted a nonvanishing defect as flatness. The finite formula can be analyzed exactly. That analysis should precede any operator or RH interpretation.',
 ['For X≥2 set λ_X(t)=Σ_(p≤X)(logp)/(1+p)[2cos(tlogp)−2]+t/2.', 'The sum is finite, so it is a real entire function of real t extended holomorphically to complex t. It is not by definition an operator eigenvalue or a regularized determinant.'],
 'λ_X(0)=0, λ_X′(0)=1/2 and λ_X″(0)=−2Σ_(p≤X)(logp)³/(1+p)<0. Its derivative is1/2−2Σ_(p≤X)(logp)²sin(tlogp)/(1+p). These identities do not force zeros at any prescribed ordinates.',
 'Differentiate each finite summand using the chain rule. The first derivative introduces a second logarithmic factor, and the second introduces a third with cosine. At zero the sine terms vanish and every cosine equals one, giving the stated values. Taylor expansion then gives λ_X(t)=t/2−Ct²+O(t⁴), where C=Σ(logp)³/(1+p)>0. The nonzero derivative at zero makes that particular zero simple. A point selected independently need not make the prime sum or its proposed flatness defect vanish.',
 'Keep only p=2, giving a fully explicit one-prime model.',
 'λ₂(t)=(2log2/3)(cos(tlog2)−1)+t/2. At t=2π/log2 the cosine returns to one, so λ₂(t)=π/log2, not zero. Its periodic prime part and linear drift therefore do not jointly vanish merely because the phase returns. Increasing X changes the function; it is not a proved convergence approximation until a tail theorem is supplied.',
 'The exact calculus is a valid mathematical result, while the arithmetic correspondence remains a separate burden.',
 'A self-adjoint operator already has real point spectrum, so that property alone cannot be equivalent to RH without a proved correspondence encoding all nontrivial zeros. Finite PASS bounds or target-seeded matrices do not supply that theorem. A flatness defect near5.7 is not zero.',
 'Define one operator with domain and a target-independent construction, prove its spectral counting law, and only then seek an analytic identity linking its determinant or trace to an arithmetic function.',
 [('NIST DLMF Riemann zeta zeros','https://dlmf.nist.gov/25.10')])

E('2025-10-31','parity integral','U','Trigonometric integrals','The sine quotient has an exact parity integral and a finite quadrature certificate',
 'Why does the integral distinguish odd and even positive integers, and when is a discrete midpoint rule exact?',
 'The parity integral is one of the clearest exact mathematics problems recovered in October. Its apparent endpoint singularities are removable for integer a, and a finite trigonometric expansion proves both the integral and a useful sampling theorem.',
 ['For a positive integer a define I(a)=∫₀^(aπ)sinx/sin(x/a)dx, interpreted by continuous endpoint limits.', 'Substitute x=aθ to get I(a)=a∫₀πU_(a−1)(cosθ)dθ, where U_(a−1)(cosθ)=sin(aθ)/sinθ.'],
 'I(a)=aπ for odd a and zero for even a. For odd a=2m+1, the N-point midpoint rule in θ is exact whenever m<N. For even a its symmetric midpoint sum is zero for every N.',
 'For odd a=2m+1, the quotient equals1+2Σ_(k=1)^mcos(2kθ); for even a=2m it equals2Σ_(k=1)^mcos((2k−1)θ). Both follow from a finite geometric sum of complex exponentials. Integrating each nonconstant integer cosine over[0,π] gives zero, leavingπ only in the odd case. The expansion also removes the endpoint singularities. At midpoint nodes θ_j=(j+1/2)π/N, the sum of cos(2kθ_j) vanishes when1≤k<N, by a geometric sum. Every odd-frequency cosine sum vanishes by pairing θ_j withπ−θ_j, proving the even case.',
 'Take a=5 and N=3.',
 'The quotient is1+2cos2θ+2cos4θ. Both cosine sums vanish at the three midpoint nodes, so the midpoint integral equalsπ and I(5)=5π exactly. If each sampled quotient value has absolute error at mostδ, the propagated integration error is at most aπδ, because the positive quadrature weights sum to aπ. This is a mathematical error bound; hardware specifications alone do not imply a particular δ.',
 'The exact parity identity and its discrete certificate follow from the same finite Fourier structure.',
 'The theorem concerns positive integer a. Noninteger values may introduce interior poles and require a different integration prescription. No energy conversion, superconductivity or self-calibration claim follows from the integral identity.',
 'Derive an end-to-end interval certificate combining removable-endpoint evaluation, sample errors and quantized weights, retaining the exact Fourier cutoff that makes the ideal midpoint rule exact.',
 [('NIST DLMF Chebyshev trigonometric formulas','https://dlmf.nist.gov/18.5')])

E('2025-10-31','Psi','U','Exact integration','The logarithmic sine integral separates into an elementary term and Catalan’s constant',
 'What is the exact value of the recovered logarithmic integral, including its integrable endpoint singularity?',
 'The exact input is Ψ=∫₀^(π/4)log[(1+x²)sin¹⁰x]dx. Separating its logarithms produces a complete evaluation with a familiar special constant, and prevents later large integer factors from obscuring the original expression.',
 ['Let a=π/4 and G=Σ_(n≥0)(−1)^n/(2n+1)², Catalan’s constant.', 'On0<x≤a, log[(1+x²)sin¹⁰x]=log(1+x²)+10logsinx. Near zero the singularity is10logx plus a bounded function, hence integrable.'],
 'Ψ=a log(1+a²)−2a+2arctana−10a log2−5G, with a=π/4.',
 'An elementary primitive is∫log(1+x²)dx=xlog(1+x²)−2x+2arctanx, verified by differentiation. For the sine term use the Abel-regularized Fourier expansion log(2sinx)=−Σ_(n≥1)cos(2nx)/n on(0,π). Integrating its convergent radial regularizations from0 to a and taking the limit gives∫₀ᵃlogsinx dx=−a log2−(1/2)Σ_(n≥1)sin(2na)/n². At a=π/4, the sine values cycle1,0,−1,0, so this sum is G. Multiplying by ten and adding the elementary part gives the formula. Absolute convergence of the integrated1/n² series makes its final evaluation unambiguous.',
 'Give a rigorous series error bar without numerical integration through the logarithmic endpoint.',
 'Truncating G after N odd-denominator terms has alternating-series error at most1/(2N+1)². Its contribution to Ψ is at most5/(2N+1)². Bounds forπ, logarithms and arctangent can then be propagated separately. The exact expression has no intrinsic16384 factor; any such factor in a rearranged later formula must come from an explicitly shown algebraic normalization.',
 'The problem receives a closed form, an endpoint-convergence argument and a direct numerical certification route.',
 'The derivation concerns the recovered Ψ alone. It does not reconstruct the separate unrecovered golden-ratio integral or an unspecified rational antiderivative from the broad assistant list.',
 'Extend the same calculation to∫₀ᵃlog[(1+x²)sin^(2m)x]dx for rational multiples a/π, expressing the trigonometric part through explicitly normalized Clausen or Dirichlet L-values.',
 [('NIST DLMF Clausen function and trigonometric integrals','https://dlmf.nist.gov/25.12')])

E('2025-10-31','1152','U','Laplace integrals','The recovered fourth-power logarithmic integral has an exact elementary evaluation',
 'Can the claimed closed form be derived from the exact input, with both endpoint limits controlled?',
 'The recovered input is I=∫₀¹[(sin(log√t−π/4)+cos(π/4−log√t))/(logπ·log(t²))]⁴dt. Its numerator simplifies before any integration. A Laplace transform and three integrations by parts then verify the reported closed form exactly.',
 ['Set v=−(1/2)logt>0. The numerator becomes−√2sinv, and dt=−2e^(−2v)dv.', 'Define K(a)=∫₀∞e^(−av)sin⁴v/v⁴ dv for a>0. The sine quotient tends to one at zero and exponential decay controls infinity.'],
 'I=[18π+90log2−33log20−12arctan(1/2)]/[1152(logπ)⁴].',
 'The substitution gives I=K(2)/[32(logπ)⁴]. Use8sin⁴v=3−4cos2v+cos4v and set H(v)=e^(−av)(3−4cos2v+cos4v). H and its first three derivatives vanish at zero, while they decay at infinity. Three integrations by parts give∫H/v⁴=(1/6)∫H‴/v. Applying the elementary Frullani identity∫₀∞(e^(−λv)−e^(−μv))/v dv=log(μ/λ), valid for positive real parts with continuous logarithm, yields K(a)=(1/48)Re[3a³loga−4(a−2i)³log(a−2i)+(a−4i)³log(a−4i)]. All divergent individual terms cancel because the combined derivatives vanish at zero.',
 'Evaluate this formula at a=2.',
 '(2−2i)³=−16−16i and(2−4i)³=−88+16i. Their logarithms have real parts(log8)/2,(log20)/2 and arguments−π/4,−arctan2. Collecting real parts gives K(2)=π/2+(5/2)log2−(11/12)log20−(1/3)arctan(1/2), using arctan2=π/2−arctan(1/2). Division by32(logπ)⁴ gives precisely the displayed numerator and denominator.',
 'This is a genuine verified historical closed form, supported by a complete analytic derivation rather than by accepting an assistant decimal.',
 'The real logarithms and fourth power matter. The original expression has removable behavior at t=1; numerical routines evaluating it literally can create0/0 unless that limit is handled.',
 'Derive the analogous transform for other even powers sin^(2m)v/v^(2m), proving endpoint cancellation before using logarithmic or complex-power expressions.',
 [('NIST DLMF logarithms and integral representations','https://dlmf.nist.gov/4.2')])

E('2025-10-31','operatorname{Tr}','A','Cyclotomic fields','Cyclotomic trace orthogonality fixes the coefficient p, not p+1',
 'Which embeddings define the trace, and are the coefficients integral character multiplicities or arbitrary rational weights?',
 'The retrieved cyclotomic expression used a coefficient p+1 and reported30/13 in a character setting. Summing the actual embeddings gives an exact trace identity and a useful integrality test, while leaving the unrecovered original coefficient data unspecified.',
 ['Let p be prime, ζ=exp(2πi/p), and X=Σ_(k=0)^(p−1)a_kζ^k. For the trace formula first allow a_k∈Q.', 'The embeddings of Q(ζ) send ζ toζ^r for r=1,…,p−1. Put A=Σa_k and C₀=Σ_(k+ℓ≡0 modp)a_ka_ℓ.'],
 'Tr_(Q(ζ)/Q)(X²)=pC₀−A². If all a_k are integers, this trace is an integer. The same integrality holds for every algebraic-integer X, including ordinary finite-group character values contained in this field.',
 'The embedding sumΣ_(r=1)^(p−1)ζ^(rm) is p−1 if p divides m and−1 otherwise: include the r=0 term and use a geometric series. Expand X² and apply this sum to every pair(k,ℓ). Congruence-zero pairs contribute(p−1)C₀, and the other pairs contribute−(A²−C₀), giving pC₀−A². For integral coefficients the formula is visibly integral. More generally the field trace of an algebraic integer is a rational algebraic integer, hence an ordinary integer. Thus a noninteger30/13 cannot be that trace without changing the object or its normalization.',
 'Take p=5 and X=ζ+ζ⁻¹.',
 'Here A=2 and C₀=2, so the trace is5·2−4=6. Directly X²=ζ²+2+ζ⁻², whose trace is−1+8−1=6. Replacing p by p+1 would give eight and therefore fails this exact test. Repeated coefficients or a different rational normalization must be stated before applying an integrality conclusion.',
 'The trace is now an explicit finite embedding sum with a sharp algebraic consistency check.',
 'The actual A₅ coefficient list and embedding into Q(ζ₁₃) were not recovered. This entry does not invent them or identify an arbitrary rationally normalized sum with an ordinary character trace.',
 'Recover a genuine character expansion, verify its field of values and integral lattice, then compute all Galois traces and compare them with representation-theoretic multiplicity formulas.',
 [('Milne Fields and Galois Theory','https://www.jmilne.org/math/CourseNotes/FT.pdf')])

E('2025-10-21','trace-class','A','Operator ideals','Trace class is contained in Hilbert–Schmidt, and strong convergence alone preserves neither',
 'Which operator topology is certified, and are the claimed trace-class and Hilbert–Schmidt properties mutually consistent?',
 'The operator report asserted a compact trace-class but non-Hilbert–Schmidt limit. Under the standard definitions this is impossible. The useful development is an exact hierarchy of operator ideals and a set of examples distinguishing singular-value summability from strong convergence.',
 ['For a compact operator A on a Hilbert space, let s_n(A)≥0 be its singular values. Trace class meansΣs_n<∞; Hilbert–Schmidt meansΣs_n²<∞.', 'Strong convergence A_N→A means A_Nx→Ax for every fixed vector x, without requiring convergence in operator norm.'],
 'Every trace-class operator is Hilbert–Schmidt, with||A||_HS≤||A||₁. Compactness does not imply either summability condition. A strong limit of finite-rank operators need not even be compact.',
 'For any finite nonnegative sequence,Σs_n²≤(Σs_n)²; monotone limits give the norm inequality when the trace norm is finite. For diagonal operators on ℓ², compactness is equivalent to diagonal entries tending to zero, and the two ideal conditions reduce to the displayed scalar series. Thus diag(1/n) is Hilbert–Schmidt but not trace class, while diag(1/√n) is compact but not Hilbert–Schmidt. Coordinate projections P_N have finite rank and converge strongly to identity because the ℓ² tail of every fixed vector tends to zero. Identity is not compact on an infinite-dimensional space, since its image of the orthonormal unit vectors has no norm-convergent subsequence.',
 'Certify the genuinely trace-class diagonal A=diag(1/n²).',
 'Its finite-rank truncation has trace-norm errorΣ_(n>N)n⁻²≤1/N and Hilbert–Schmidt squared errorΣ_(n>N)n⁻⁴≤1/(3N³), by integral comparison. These are actual convergence bounds in specified norms. A persistent empirical ratio near0.8 is neither one of these bounds nor a proof of strong convergence.',
 'The hierarchy rejects an inconsistent claim while supplying concrete norm certificates a spectral approximation could genuinely satisfy.',
 'Singular values, not signed eigenvalue sums, define these ideals for general operators. A fitted exponent on finitely many residuals proves no asymptotic summability theorem.',
 'Derive a target-independent singular-value envelope for the proposed prime kernel, then integrate its tail to certify the strongest operator ideal and topology the construction actually supports.',
 [('Barry Simon Trace Ideals and Their Applications','https://doi.org/10.1090/surv/120')])

E('2025-10-29','gradient flows','U','Conservative PDEs','Cahn–Hilliard flow conserves mass and dissipates a declared energy',
 'Which free energy and boundary conditions make the proposed fourth-order equation a gradient flow?',
 'The recovered dissipative equation has a genuine variational structure when its mobility and boundary terms are specified. The resulting mass and energy identities are strong mathematical content, but do not imply a universal controller or transfer the model to unrelated applications.',
 ['On a periodic domain set E[ψ]=∫[f(ψ)+(K/2)|∇ψ|²]dx, with K≥0 and smooth f. Its variational derivative is μ=f′(ψ)−KΔψ.', 'Let ψ_t=∇·(M∇μ) with smooth nonnegative mobility M; assume enough regularity to differentiate E and integrate by parts.'],
 'The total mass∫ψ is constant and dE/dt=−∫M|∇μ|²≤0. For constant M and f(ψ)=aψ²/2, a Fourier mode k evolves at rate−M|k|²(a+K|k|²).',
 'Integrating the divergence over a periodic domain gives zero, proving mass conservation. Differentiating the energy and integrating its gradient term by parts gives dE/dt=∫μψ_t. Substituting the PDE and integrating once more gives the negative mobility-weighted gradient norm. Derivatives of M create no extra term in this divergence-form integration identity. For the quadratic potential and Fourier mode e^(ik·x), Δ contributes−|k|², so μ=(a+K|k|²)ψ_mode and its evolution has the stated rate. When a<0, low-frequency modes can grow despite global energy dissipation.',
 'On a2π-periodic line take a=K=M=1 and ψ(x,t)=m+εe^(−2t)cosx.',
 'Its mean is m and μ=m+2εe^(−2t)cosx. The PDE gives ψ_t=−2εe^(−2t)cosx exactly. Its energy isπm²+πε²e^(−4t), whose derivative is−4πε²e^(−4t). The dissipation integral∫|μ_x|² has exactly that positive value. This checks both conservation and decay without discretization.',
 'The gradient-flow claim now has a complete energy certificate and an explicit solution.',
 'Boundary fluxes, negative mobility or insufficient regularity change the proof. The identity does not make holonomy equal to thermodynamic loss, and a feedback law requires a separately defined state and stability analysis.',
 'Discretize with a symmetric graph Laplacian and a discrete variational derivative, then prove exact mass conservation and a time-step energy inequality before comparing implementations.',
 [('Cahn and Hilliard Free Energy of a Nonuniform System I','https://doi.org/10.1063/1.1744102')])

E('2025-10-19','[d,','U','Differential forms','Fiber integration commutes with d on closed product fibers in a fixed convention',
 'What are the degrees and signs of the operators in the proposed pushforward-curvature identity?',
 'The recovered identity[d,π₊]ω=∫Ω_L∧ω requires a type check before a geometric interpretation. With ordinary exterior derivative and a curvature two-form, its sides have different degrees. A closed-product-fiber calculation supplies the correct elementary comparison.',
 ['Let π:B×F→B with F a closed oriented m-manifold. Write horizontal forms before vertical forms and defineπ! by integrating the vertical top-degree coefficient.', 'Thenπ! lowers form degree by m, d raises it by one, and wedge multiplication by a curvature two-form raises it by two.'],
 'In this convention d_Bπ!ω=π!dω for smooth product forms on closed fibers. The commutator has degree1−m, whereasπ!(Ω_L∧ω) has degree2−m; the proposed equality therefore cannot hold as an identity of ordinary graded forms without changing an operator or adding extra structure.',
 'For a product α∧β with α horizontal and β vertical of top degree, d contributes d_Bα∧β plus a vertical derivative that has no higher vertical degree; integrating gives(d_Bα)∫β, the derivative ofπ!ω. Terms of vertical degree m−1 can contributeπ!d_Fβ, but their integral is zero by Stokes because F has no boundary. All other vertical degrees integrate to zero. Linearity and a local coefficient expansion prove the statement. The degree comparison follows simply by adding the operator degree shifts, independently of any dynamics.',
 'Use B=R,F=S¹ and ω=(x²+sinθ)dθ.',
 'Integration givesπ!ω=2πx². Its derivative is4πx dx. Meanwhile dω=2x dx∧dθ, whose fiber integral is also4πx dx. There is no extra curvature term. If the fiber had a boundary, Stokes would supply an explicitly signed boundary contribution instead, not an arbitrary line-bundle curvature insertion.',
 'The pushforward idea becomes a well-typed theorem with a direct example and a clear location for genuine boundary corrections.',
 'Other orientation conventions move signs, and covariant or superconnection pushforwards are different constructions. The calculation does not rule out correctly defined index-theoretic curvature formulas; it rules out copying this displayed degree-mismatched formula literally.',
 'Specify the connection and graded complex for a twisted pushforward, then derive its commutator formula with every degree and boundary term shown.',
 [('Bott and Tu Differential Forms in Algebraic Topology','https://doi.org/10.1007/978-1-4757-3951-0')])

E('2025-10-19','Bloch','U','Polylogarithms','The Bloch–Wigner correction has coefficient one, and a scalar residue leaves a level curve',
 'Which logarithm branches and normalization preserve the dilogarithm symmetry, and can one real residue identify a complex point?',
 'The recovered formula used half the standard logarithmic correction in the Bloch–Wigner function. The normalized function has a useful exact functional relation. Adding it to log|z| gives a legitimate real observable, but generally only one constraint on a two-dimensional variable.',
 ['On compatible branches away from0 and1 use D(z)=ImLi₂(z)+log|z|Arg(1−z), extended as the standard single-valued Bloch–Wigner function.', 'Define R(z)=log|z|+D(z). At a real0<x<1, Li₂(x) is real and D(x)=0.'],
 'The normalized function satisfies D(1−z)=−D(z). A coefficient1/2 in its correction fails this relation in general. Near any real x∈(0,1), the equation R(z)=logx defines a local real one-dimensional level curve, rather than uniquely determining z.',
 'Spence’s identity Li₂(z)+Li₂(1−z)=π²/6−logzlog(1−z) has imaginary part equal to minus[log|z|Arg(1−z)+log|1−z|Argz]. Adding the two full correction terms cancels it, proving antisymmetry on compatible branches and then by continuation. Half corrections leave half the uncanceled expression. Along the real interval R(x)=logx, so its derivative in the real direction is1/x≠0. The real implicit-function theorem therefore gives a smooth one-dimensional local level set of R in the complex plane.',
 'Take z=i and compare it with1−i.',
 'The series ImLi₂(i)=Σ_(n≥1)sin(nπ/2)/n² equals Catalan’s constant G, and log|i|=0, so D(i)=G. Antisymmetry gives D(1−i)=−G. For the half-normalized formula, the sum of the two values instead equals−πlog2/8, since log|1−i|=(log2)/2 and Arg(i)=π/2. This exact nonzero defect exposes the normalization error.',
 'The regulator-sized function has a correct identity, while its observation map has a precise local nonidentifiability statement.',
 'The result does not construct a motivic regulator, a hyperbolic3-manifold or the proposed physical curvature. Global branch behavior and integral lattice normalizations require their own definitions.',
 'Add an independently defined second real observable and compute the2×2 Jacobian; a nonzero determinant would give local identifiability of z, whereas one scalar residue cannot.',
 [('Zagier The dilogarithm function','https://people.mpim-bonn.mpg.de/zagier/files/doi/10.1007/978-3-540-30308-4_1/fulltext.pdf')])

E('2025-10-30','Casimir','U','Representation theory','Finite-group symmetry permits frequency ratios but does not usually force one',
 'Which representation and equivariant operator make30/13 a necessity rather than a chosen pair of coefficients?',
 'The October acoustic-Casimir program attached30/13 to A₅ symmetry. A genuine symmetry constraint can be proved, but it normally leaves independent scalar parameters on distinct blocks. An explicit equivariant oscillator family shows why the ratio needs an additional operator construction.',
 ['Letρ be the orthogonal permutation representation of A₅ on R⁵. On V⊕V use the same group action in both blocks.', 'For positive a,b let K=diag(a²I₅,b²I₅). The conservative oscillator is x″+Kx=0, with frequencies a and b.'],
 'K commutes with everyρ(g)⊕ρ(g) for every positive pair a,b. Hence A₅ equivariance alone allows every positive frequency ratio b/a, including30/13. It does not select that ratio.',
 'Each block of K is a scalar matrix, which commutes with every linear map on that block. Direct block multiplication therefore proves equivariance without needing a character table. The oscillator separates into five copies of x″+a²x=0 and five of y″+b²y=0, so their frequencies are exactly a,b. Since the same representation and symmetry hold as a,b vary continuously, no single ratio is forced by this symmetry condition. Schur’s lemma can make an operator scalar on an irreducible block, but it does not fix its scalar without specifying the actual central element or dynamical law.',
 'Choose a=13,b=30 and then change only b to31.',
 'Both stiffness matrices have integer entries and exactly the same A₅ action. Their frequency ratios are respectively30/13 and31/13. An experimental ratio matching the former cannot distinguish a symmetry necessity from a fitted parameter unless the stiffness operator is independently derived. If a prescribed group-algebra element supplies the operator, its character values and normalization can then be calculated as extra data.',
 'The next mathematical task is an operator derivation, rather than a numerical coincidence between a ratio and a group label.',
 'This example does not model a particular resonator or accept the reported Q, loss or decay measurements. Perfectoid descent and Stark regulators provide no automatic map to this real stiffness matrix.',
 'Specify an A₅-equivariant geometric differential operator and boundary conditions, decompose its representation and prove an exact relation between the relevant eigenvalues; that would make a ratio theorem substantive.',
 [('Milne Group Theory, representations and Schur lemma','https://www.jmilne.org/math/CourseNotes/GT.pdf')])

E('2025-10-30','damping','U','Linear differential equations','Damping ratio, decay and Q must use the same oscillator convention',
 'Which ODE defines the reported damping quantities, and do their numerical values satisfy its exact relations?',
 'The acoustic discussion reported dampingζ≈0.697 alongside an enormous Q. A conditional oscillator calculation checks consistency without treating any historical physical measurement as established. Different experimental definitions require an explicit conversion rather than a shared label.',
 ['Use x″+2ζω₀x′+ω₀²x=0, withω₀>0 and0<ζ<1. Define the model quality parameter Q=1/(2ζ).', 'The damped angular frequency isω_d=ω₀√(1−ζ²), and a solution’s amplitude envelope decays as exp(−ζω₀t).'],
 'The amplitude multiplier after one damped period is exp[−2πζ/√(1−ζ²)]. For ζ=697/1000, the model Q is500/697, not1.43×10⁹. These conclusions are exact consequences of the declared ODE.',
 'The characteristic equation has roots−ζω₀±iω₀√(1−ζ²), giving the exponential envelope and oscillatory factor. One damped period is2π/ω_d; substituting it in the envelope gives the multiplier. The Q value follows from the stated conventional parameter definition. For the mechanical energy E=(x′²+ω₀²x²)/2, differentiating and using the ODE gives E′=−2ζω₀x′²≤0, which is the actual dissipative identity. The envelope and energy are related but not identical pointwise functions.',
 'Evaluate the dimensionless relations at the reported damping scale.',
 'Here1−ζ²=514191/10⁶, so the period multiplier is exp(−1394π/√514191), approximately0.0022. A value0.738 could describe a different time interval or observable, but it is not this full-period amplitude multiplier. Conversely a model Q near10⁹ requiresζ near5×10⁻¹⁰ under the same definition. The discrepancy cannot be resolved by changingω₀, which cancels from both relations.',
 'A small exact ODE audit identifies which reported quantities could belong to one common mathematical model.',
 'No claim is made about an actual device’s measured Q, bandwidth or physical damping mechanism. At stronger damping, alternative experimental Q definitions need care; the definition used here is explicit.',
 'Define the measured transfer function and derive its bandwidth and ringdown parameters from one model, propagating uncertainty before comparing them with arithmetic constants.',
 [('NIST DLMF elementary differential equations','https://dlmf.nist.gov/1.13')])

E('2025-10-23','prime-log','U','Harmonic analysis','Prime-log tones have exact beat differences but no common nonzero period',
 'Which frequencies and decay law define the waveform, and what can its beats prove mathematically?',
 'The prime audio construction is a well-defined finite signal. Its useful mathematics concerns irrational frequency ratios, difference frequencies and an exponential envelope. None of these properties alone gives a zeta-zero or spectral-operator theorem.',
 ['Take the undamped two-tone signal y(t)=cos(2πf₀log2·t)+cos(2πf₀log3·t), with f₀>0.', 'The proposed damped version is x(t)=e^(−ct)y(t), c>0. A common period must reproduce both phases for all t.'],
 'log2/log3 is irrational, so the two-tone function has no positive common period. Its product formula has difference frequency f₀log(3/2), while the damped envelope has half-life(log2)/c.',
 'A rational equality log2/log3=m/n would imply2ⁿ=3ᵐ after exponentiation, impossible by unique prime factorization for nonzero positive integers m,n. A period of a finite sum of distinct exponential frequencies must make each phase factor one: linear independence follows by differentiating enough times and solving the Vandermonde system. Thus the two frequencies would have rational ratio if they shared a period. The cosine addition formula rewrites y as2cos[πf₀log6·t]cos[πf₀log(3/2)·t], displaying the difference modulation. Solving e^(−ct)=1/2 gives the half-life.',
 'Use c=1/100 as in the recovered waveform.',
 'Its envelope half-life is100log2. Increasing prime depth adds more logarithmic frequencies, but does not change this imposed envelope. A claimed beat period5.7 needs an actual f₀ and a definition of whether signed modulation or absolute amplitude is measured; the exact difference-frequency formula supplies that conversion. Rescaling f₀ rescales every temporal beat, so an isolated beat number is not an arithmetic invariant.',
 'The signal is mathematically interpretable and its parameters have separate, verifiable roles.',
 'Finite audio spectra are not eigenvalue certificates for an infinite operator. A fitted log-log exponent or curvature amplitude on one plot does not prove an asymptotic theorem.',
 'Specify an observation window and sampling rate, prove an aliasing bound for its highest retained prime frequency, and estimate which difference frequencies can be resolved within the window.',
 [('NIST DLMF trigonometric identities','https://dlmf.nist.gov/4.21')])

E('2025-10-27','Dirichlet','U','Dirichlet polynomials','Second and fourth mean values expose multiplicative resonances exactly',
 'Which finite mean-value identity distinguishes diagonal energy from genuine fourth-order resonance?',
 'The curvature-cancellation passage named Dirichlet-polynomial large values and fourth-order chaos without returning its full formulas. A newly specified finite polynomial supplies exact second and fourth moment identities, making cancellation and multiplicative coincidences precise.',
 ['Let D(t)=Σ_(n=1)^N a_n n^(−it), with fixed complex coefficients. Define the long average M_T(F)=(1/(2T))∫_(−T)^T F(t)dt.', 'For finite sums, the mean of exp(itω) tends to zero for nonzeroω and equals one forω=0.'],
 'lim_(T→∞)M_T(|D|²)=Σ|a_n|². The fourth mean isΣ_(mn=rs)a_ma_n conjugate(a_ra_s), summed over indices at most N. Multiplicative coincidences, not merely pairwise orthogonality, govern this fourth moment.',
 'Integrating one exponential gives sin(Tω)/(Tω) whenω≠0, proving the mean rule. Expanding the squared modulus produces frequencies log(m/n), whose zero condition is m=n. Expanding the fourth power produces frequencies log(rs/(mn)), whose zero condition is mn=rs. Every sum is finite, so termwise integration and passage to the limit need no uniform infinite-series argument. Nonzero-frequency errors are explicitly bounded by1/(T|ω|), though nearly equal products can make finite-window convergence slow.',
 'Take D(t)=1+2^(−it)+4^(−it).',
 'Writing z=2^(−it), its square is1+2z+3z²+2z³+z⁴. Distinct powers have nonzero frequency differences, so the fourth mean is1²+2²+3²+2²+1²=19. The second mean is three. The central coefficient three records the resonance1·4=2·2=4·1. This is a concrete fourth-order interaction that a diagonal-only approximation would miss.',
 'The source’s cancellation theme has a rigorous finite model with an exact resonance certificate.',
 'This does not establish a new large-values bound, zero-density estimate or generic quintic solution. Such claims require the unrecovered inequalities, parameter ranges and analytic estimates.',
 'For a specified coefficient family, bound its multiplicative energy and the nonzero product-gap errors uniformly as N grows, then compare the resulting theorem with any proposed q-sieve improvement.',
 [('Montgomery Topics in Multiplicative Number Theory, publisher record','https://doi.org/10.1007/BFb0060851')])

E('2025-10-27','EMARDA','A','Affine dynamical systems','The asset recurrence has an exact stability threshold independent of its interpretation',
 'Which parameter combinations determine a stable fixed point, and what additional closure is required for the proposed feedback law?',
 'The recovered EMARDA equations can be treated purely as affine dynamics. Their recurrence and capture-gap inequality have exact solutions. No economic or applied advice is needed to state the stability conditions, and an unspecified feedback observable cannot close the system.',
 ['Write A_(t+1)=qA_t+c, where q=1+ρ−δ and c=αW[1+π(M−1)] are fixed real constants.', 'The recovered gap is γ=(1−λ)M−λ. For a feedback variable α, a law α′=−κ(G−G*) is closed only after G is specified as a function of the state.'],
 'For q≠1, A_t=q^tA₀+c(1−q^t)/(1−q). Its fixed point c/(1−q) is globally attracting exactly when|q|<1. For M>0, γ>0 exactly when λ<M/(M+1).',
 'Subtract the fixed point to obtain A_(t+1)−A*=q(A_t−A*), and iterate. This gives the formula and convergence when|q|<1. For|q|>1 a nonzero initial displacement grows; q=1 gives A_t=A₀+tc, while q=−1 gives an alternating displacement and generally no convergence. For the gap, γ=M−λ(M+1); division by positive M+1 proves its threshold. If one independently sets G=gα+h with g>0 and κ>0, then α−α* decays as exp(−κgt), but that conclusion is unavailable without the specified dependence.',
 'Choose q=3/4,c=2,A₀=0.',
 'The fixed point is eight and A_t=8[1−(3/4)^t]. The first values are0,2,7/2,37/8, each verified by the recurrence. With M=3, the gap is3−4λ and changes sign atλ=3/4. These are exact parameter statements rather than empirical estimates of the named quantities.',
 'The recurrence, threshold and feedback closure have distinct mathematical roles and can each be checked independently.',
 'Parameters are treated as constants in the recurrence theorem; time-varying coefficients require products and new bounds. No prediction about wealth, policy or real systems follows from the algebra alone.',
 'For bounded time-dependent q_t,c_t, derive a uniform contraction and input-to-state bound, then close a specified feedback law and analyze the resulting coupled Jacobian.',
 [('Mathlib geometric sums','https://leanprover-community.github.io/mathlib4_docs/Mathlib/Algebra/GeomSum.html')])

E('2025-10-22','Fractional-Part','T','Multiple integrals and zeta values','Product-variable reduction gives exact zeta integrals and a controlled fractional-part transform',
 'Which exact integrand is known, and what general reduction can be proved without inventing the indexed paper’s missing input?',
 'The sourcebook identifies an October22 four-dimensional fractional-part integral but does not return its full formula or a conversation transcript. The following newly specified examples develop its product-variable theme and retain that attribution limit explicitly.',
 ['For an integrable function F of a product of d independent unit-interval variables, set t=x₁⋯x_d.', 'For s>0 define A(s)=∫₀¹{1/t}t^(s−1)dt, with fractional part{u}=u−flooru. The bounded integrand makes this transform well defined.'],
 '∫_[0,1]^dF(x₁⋯x_d)dx=(1/(d−1)!)∫₀¹F(t)(−logt)^(d−1)dt. In particular∫_[0,1]^4[1−x₁x₂x₃x₄]⁻¹dx=ζ(4)=π⁴/90. For s>1, A(s)=1/(s−1)−ζ(s)/s.',
 'Substitute x_j=e^(−y_j), so the product is e^(−u) with u=Σy_j and the measure contributes e^(−u). The volume density of the nonnegative simplex slice is u^(d−1)/(d−1)!, proved by iterated integration or induction. Substituting t=e^(−u) gives the reduction. For the zeta example, expand1/(1−t)=Σ_(n≥0)tⁿ and use nonnegative termwise integration; each product monomial integrates to1/(n+1)^d. For A, use floor(1/t)=Σ_(n≥1)1_(t≤1/n); its weighted integral isζ(s)/s, while1/t contributes1/(s−1).',
 'Apply the reduction to the newly defined four-dimensional fractional-part example.',
 'Its value is(−1/6)A‴(1), where the apparent pole in the displayed zeta expression cancels at s=1. Differentiation under the bounded fractional-part integral is justified by integrability of|logt|³ near zero. This gives an exact derivative representation without claiming it was the original indexed paper’s equation. The simpler ζ(4) example supplies an independently checkable closed form.',
 'The product-variable method is a real theorem, and the missing source expression stays missing rather than being silently reconstructed.',
 'The sourcebook date is an indexed publication/upload attribution, not a recovered original chat date. The log-cotangent and ArcCoth paper formulas likewise were not returned and are not claimed evaluated here.',
 'Recover a precise fractional-part integrand, apply this reduction, and justify any zeta-derivative continuation with dominated convergence or an explicit cancellation at the relevant point.',
 [('NIST DLMF Riemann zeta integral representations','https://dlmf.nist.gov/25.5')])

extras={6:' The dimension count can therefore be checked without guessing an ambient arithmetic interpretation: four coordinates lose exactly one independent shared-interface relation.',21:' This proof uses feasibility of the old state when testing the projection inequality. Omitting that premise removes the stated descent conclusion.',24:' To justify the Abel limit near zero, one can split the interval at a small positiveε. Uniform convergence applies on the remaining compact interval, while the integral of|logx| over(0,ε) tends to zero. The integrated Fourier series is absolutely summable, so its final Catalan specialization is independent of the approach.',25:' Frullani’s identity follows by differentiating with respect toλ in the half-plane Reλ>0: the derivative of the integral is−1/λ, equal to the derivative of−logλ. Matching the value atλ=μ fixes the constant. In the combined expression all coefficients sum to zero, allowing a common reference exponential to be subtracted before integration. This supplies a convergent identity at every stage rather than assigning values to divergent individual integrals. The original t-integrand has finite limit1/[64(logπ)⁴] as t approaches one, because sinv/v tends to one; the exponential substitution makes both endpoint bounds explicit.',26:' This test uses the complete embedding trace, not a selected subset of conjugates.'}
for k,text in extras.items():entries[k-1]['example']['calculation']+=text

for k,text in {28:' The constant Fourier mode has zero decay rate, exactly matching the mass conservation law.',30:' Thus a small residual value is not equivalent to a unique recovered point in the parameter plane.',32:' The dimensionless period multiplier is independent of the chosen time unit and natural-frequency scale.',34:' More generally, collect the coefficients of D squared by the product mn. The fourth mean is the sum of squared moduli of those grouped coefficients, so collisions add coherently before the final square.',35:' At the boundary q=−1, deviations alternate forever unless the initial state already equals the fixed point.',36:' For d=4 the zeta integrand is integrable even at the all-ones corner, as the convergent nonnegative series proves directly.'}.items():entries[k-1]['example']['calculation']+=text
def finish():
    for e in entries:
        words=len(' '.join([e['summary'],*e['definitions'],*e['result'].values(),*e['example'].values(),e['limits'],e['extension']]).split())
        assert words>=270,(e['id'],words)
    (HERE/'entries.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
    print(len(entries),'entries')
if __name__=='__main__':finish()
