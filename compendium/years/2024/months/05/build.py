from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
entries=[]
def evidence(date,needle):
    fallback=None
    for p in sorted(HERE.glob('root*.json')):
        for i,r in enumerate(json.loads(p.read_text())):
            obj=r.get('result',{})
            text='\n'.join(x.get('text','') for x in obj.get('content',[]) if x.get('type')=='text')
            for line in text.splitlines():
                if date and date in line:
                    hit=(line,f'{p.name}[{i}]')
                    if needle.lower() in line.lower():return hit
                    fallback=fallback or hit
    if fallback:return fallback
    raise ValueError((date,needle))
def E(date,needle,field,title,question,summary,defs,statement,proof,setup,calc,conclusion,limits,extension,refs=()):
    id=f'Y24-05-{len(entries)+1:03d}'
    excerpt,receipt=evidence(date,needle)
    entries.append(dict(id=id,title=title,status='Classical or elementary result developed here with explicit scope',summary=summary,definitions=defs,result=dict(name=title,statement=statement,proof=proof),example=dict(setup=setup,calculation=calc,conclusion=conclusion),limits=limits,extension=extension,references=[dict(label=a,url=b) for a,b in refs],original=dict(date=date,month='2024-05',evidence='A',field=field,concept=title,origin='An assistant-only mathematical passage was recovered; the original user prompt was not returned.',question=question,math=statement,finish=conclusion,kind='Developed calculation',refs=[],source_excerpt=excerpt,retrieval_receipt=receipt,original_question=None,attribution_note='The historical evidence is assistant-authored. The revised question, proof and example are editorial developments, not quotations or claims about the user’s original wording.')))

E('2024-05-06','formulas','Measure theory','Finite mixtures and typed kernel pairings',
 'What objects do the delta symbols represent, and what integrability or positivity conditions make the proposed kernel expression meaningful?',
 'The recovered passage combined weighted delta symbols with a two-variable kernel integral. A precise replacement distinguishes probability measures, functions and operators. Finite atomic measures already give exact calculations, and a positive-semidefinite kernel turns them into a useful geometric comparison without imposing any application interpretation.',
 ['Let X={p,c}. Define μ_A=(4/5)δ_p+(1/5)δ_c and μ_B=(1/2)δ_p+(1/2)δ_c as probability measures.', 'For a kernel K:X×X→R, define B_K(μ,ν)=Σx,y K(x,y)μ{x}ν{y}. For L² functions use ⟨f,T_Kg⟩=∫overline(f(x))K(x,y)g(y)dxdy when the integral is justified.'],
 'If the finite kernel matrix is symmetric positive semidefinite, B_K is a positive-semidefinite bilinear pairing and B_K(μ_A−μ_B,μ_A−μ_B)≥0. A two-variable kernel on general measure spaces is a bounded L² operator when it is square-integrable, with operator norm at most its L² kernel norm.',
 'For the finite claim, identify a signed measure with its vector of masses, so B_K(v,v)=vᵀKv. The assumed matrix property gives the sign. For the integral claim, Cauchy–Schwarz in y gives |T_Kg(x)|²≤(∫|K(x,y)|²dy)||g||². Integrate in x to obtain ||T_Kg||²≤||K||²_L²||g||². A second Cauchy–Schwarz estimate bounds the pairing by ||f||||K||_L²||g||. Complex functions require the displayed conjugation; without it one has a bilinear rather than the usual sesquilinear Hilbert pairing.',
 'Take the kernel matrix K=[[1,ρ],[ρ,1]], with −1≤ρ≤1.',
 'Its eigenvalues are 1+ρ and 1−ρ. The mass difference is v=(3/10,−3/10), giving vᵀKv=(9/50)(1−ρ). At ρ=0 the squared distinction is 9/50; at ρ=1 it is zero although μ_A≠μ_B. The constant kernel sees only total mass, which is one for both. This is a fully explicit example of a positive kernel that is not sufficiently discriminating for the chosen measures.',
 'Kernel positivity makes the quadratic expression nonnegative; distinguishing different inputs requires a separate injectivity property. A weighted delta expression is not automatically an ordinary pointwise function.',
 'The two-point symbols here are abstract labels, not dietary or behavioral variables. Generalized delta distributions need not lie in L², so the atomic calculation and the function-space operator theorem must not be conflated.',
 'For a specified finite candidate family, compute the kernel nullspace and identify exactly which signed mass differences are invisible.',
 [('NIST DLMF integral operators and numerical quadrature background','https://dlmf.nist.gov/3.5')])

E('2024-05-06','w=','Complex analysis','Winding number from a lifted angle',
 'When is the contour integral an integer, and why does it survive a deformation that avoids the origin?',
 'The recovered contour expression becomes a topological invariant only for a closed nonvanishing loop with enough regularity to integrate. Its integer value comes from the endpoint change of a lifted angle, not from a numerical convention for complex logarithms.',
 ['Let z:[0,1]→C∖{0} be a piecewise continuously differentiable closed loop.', 'Choose a continuous argument lift α(t) on the interval so z(t)=r(t)exp(iα(t)), r(t)>0. Define w(z)=(1/(2πi))∫₀¹z′(t)/z(t)dt.'],
 'The integral equals [α(1)−α(0)]/(2π), an integer. Winding adds under concatenation and is unchanged under a continuous homotopy through loops avoiding zero.',
 'On each smooth segment, z′/z=r′/r+iα′. The real contribution is log r(1)−log r(0)=0 because the loop closes. The remaining term is the argument difference divided by 2π. Equal endpoints imply exp(i(α(1)−α(0)))=1, so the difference is an integer multiple of 2π. Concatenation joins lifts after adding a constant multiple of 2π and therefore adds endpoint differences. During a homotopy avoiding zero, lifted endpoint differences vary continuously but remain integer multiples of 2π; their integer cannot change. This proof also identifies the precise excluded event: crossing zero destroys the nonvanishing lift.',
 'For integer k consider z_k(t)=2exp(2πikt). Contrast it with a loop translated through the origin.',
 'Here z′_k/z_k=2πik, so w(z_k)=k exactly. A reverse traversal changes k to −k. The circles z_a(t)=a+exp(2πit), for real a, have winding one when |a|<1 and zero when |a|>1; at a=±1 the curve passes through zero and the integral is undefined. Consequently no invariant-preserving homotopy through nonvanishing loops can connect the k=1 and k=0 cases.',
 'The algebraic contour formula and the topological loop classification agree once their domains are specified.',
 'An open curve has no integer winding without an added closing convention. A self-intersecting curve is allowed, but the result is winding about the chosen point rather than simply an unsigned count of visible circles.',
 'For a polygonal loop and an uncertainty disk around each vertex, certify whether all admissible edges avoid zero and retain one common winding.',
 [('Hatcher Algebraic Topology fundamental group of the circle','https://pi.math.cornell.edu/~hatcher/AT/at1-tc.html')])

E('2024-05-06','Euler','Calculus of variations','An Euler–Lagrange equation with a coercive minimization certificate',
 'What function space and boundary condition make the variational equation valid, and does a stationary point actually minimize the functional?',
 'The recovered Euler–Lagrange expression was formally appropriate but lacked a problem for which stationarity, boundary terms and minimization could be checked. A strictly convex quadratic functional supplies all three and separates a first variation from an optimality theorem.',
 ['On (0,1), prescribe u∈H₀¹(0,1) and J(u)=(1/2)∫₀¹[(u′)²+u²]dx−∫₀¹f u dx, with f∈L².', 'The weak Euler–Lagrange equation is ∫(u′v′+uv)dx=∫fv dx for every v∈H₀¹. If u is twice differentiable, it reads −u″+u=f.'],
 'Any weak solution is the unique global minimizer. For every admissible perturbation v, J(u+v)−J(u)=(1/2)∫[(v′)²+v²]dx≥0, with equality only for v=0.',
 'Expand J(u+εv). Differentiating at ε=0 gives the weak equation. Integration by parts produces −u″+u=f when the regularity and fixed endpoint conditions justify it; the endpoint contribution vanishes because v is zero there. For the exact difference formula, expand J(u+v) and use the weak equation to cancel its cross term ∫(u′v′+uv−fv). The remaining positive quadratic term proves minimization and uniqueness without confusing them with stationarity. Existence follows from the standard coercive Hilbert-space variational theorem, since the bilinear form is an inner product equivalent to the H¹ norm on this space and the forcing functional is bounded.',
 'Take f(x)=(π²+1)sin(πx).',
 'The function u(x)=sin(πx) has the required zero endpoints and satisfies −u″+u=f. Its energy is J(u)=−(π²+1)/4 because ∫sin²πx=∫cos²πx=1/2. Perturbing by v=a sin(2πx) increases J by a²(4π²+1)/4, an exact positive gap. This gives both an analytic optimizer and a quantitative perturbation certificate.',
 'The stationary equation is now backed by a convexity argument and an exact gap formula.',
 'Nonconvex integrands can have saddle stationary points and multiple minimizers. Free endpoints create natural boundary conditions instead of eliminating all boundary terms. The chosen example is a mathematical boundary-value problem, not a model validated by its notation.',
 'Discretize this same functional using piecewise-linear finite elements and compare the discrete energy gap with the continuous certificate.',
 [('Evans partial differential equations course notes and variational methods','https://math.berkeley.edu/~evans/')])

E('2024-05-24','superalgebra','Superalgebra','A consistent gl(1|1) replacement for unspecified graded brackets',
 'Which generators are even or odd, and do the proposed brackets satisfy the graded Jacobi identity?',
 'The recovered framework listed operators Q_i,M_j,O_k and extended commutators without specifying parity or a representation. A two-by-two matrix superalgebra is a complete small replacement: its relations can be computed and its graded Jacobi identity follows from associativity.',
 ['Give C^(1|1) one even basis vector and one odd basis vector. Diagonal matrices are even and off-diagonal matrices odd.', 'For homogeneous matrices X,Y, define [X,Y]_s=XY−(−1)^(|X||Y|)YX. Set Q+=E₁₂, Q−=E₂₁, N=E₁₁ and I=E₁₁+E₂₂.'],
 'The relations are [Q+,Q−]_s=I, [N,Q+]_s=Q+, [N,Q−]_s=−Q−, [Q+,Q+]_s=[Q−,Q−]_s=0, and I is central. All graded Jacobi identities hold.',
 'Matrix multiplication gives Q+Q−=E₁₁ and Q−Q+=E₂₂. Both generators are odd, so their superbracket adds rather than subtracts these products. Their squares vanish, and multiplication by N yields the stated weights. For the general graded Jacobi identity, expand (−1)^(|X||Z|)[X,[Y,Z]_s]_s plus its two cyclic counterparts. Every associative triple product occurs twice with opposite signs after collecting parity factors. Thus cancellation is algebraic and does not require a separate physical hypothesis about the operators. The representation makes this sign convention testable; using an ordinary commutator for the two odd matrices would instead yield E₁₁−E₂₂.',
 'Take X=Q+, Y=Q− and Z=N.',
 'The inner bracket [Q+,Q−]_s is I and hence its bracket with N vanishes. The other Jacobi terms involve [N,Q+]=Q+ and [N,Q−]=−Q− and cancel exactly. The identity matrix is not forced to vanish merely because an ordinary commutator of finite matrices has trace zero: the odd-odd superbracket is an anticommutator and can have nonzero ordinary trace.',
 'A graded algebra is determined by its parity and identities, not by attaching quantum or neural labels to unspecified operators.',
 'This gives gl(1|1), not a representation of every proposed collection of operators in the old framework. Dynamics, state spaces, adjoints and observables would need additional definitions. Algebraic consistency alone establishes no physical application.',
 'For any newly proposed finite generator relations, solve the graded Jacobi polynomial constraints before searching for representations or assigning interpretations.',
 [('Supercommutator conventions in gl(1|1) current algebra research','https://scoap3-prod-backend.s3.cern.ch/media/files/69571/10.1016/j.nuclphysb.2022.115790.pdf')])

E('2024-05-24','Z(M','Arithmetic geometry','Point-counting zeta functions and one elliptic local factor',
 'Does Z(M,t) count symmetric powers, rational points over extensions or a cohomological determinant, and under which finite-field hypotheses do these descriptions agree?',
 'The recovered zeta and Euler-product formulas did not identify a base field or the cohomology behind their determinants. Finite-field examples recover genuine arithmetic content while keeping a Hasse–Weil zeta function distinct from an individual cohomological L-factor.',
 ['For X/F_q put N_r=#X(F_(q^r)) and Z(X,t)=exp(Σr≥1 N_r t^r/r), interpreted as a formal series.', 'For a smooth elliptic curve E/F_q, write a_q=q+1−#E(F_q). Its standard degree-two numerator is P_q(t)=1−a_q t+q t²; the full zeta function is P_q(t)/[(1−t)(1−qt)].'],
 'For the affine and projective lines, Z(A¹,t)=1/(1−qt) and Z(P¹,t)=1/[(1−t)(1−qt)]. For E:y²=x³+x+1 over F₅, direct enumeration gives N₁=9 and N₂=27, consistent with a₅=−3 and P₅(t)=1+3t+5t².',
 'For the line, N_r=q^r; substitute into the exponential and use −log(1−u)=Σu^r/r. The projective line has one additional point, adding the factor 1/(1−t). Also Symⁿ(A¹) is affine n-space because an unordered multiset of n roots is encoded by the coefficients of its monic polynomial. This explains the symmetric-power coefficient qⁿ in that example. For the elliptic curve, count each right-hand-side value and its square roots, then add the point at infinity. The standard elliptic zeta theorem supplies the degree-two form; comparing the first coefficients gives N₁=q+1−a and N₂=q²+1−(a²−2q). The finite counts verify this instance but are not a proof of that theorem for every curve.',
 'Count the specified elliptic curve first over F₅, then over F₂₅=F₅[u]/(u²−2).',
 'Over F₅ the numbers of affine y solutions for x=0,1,2,3,4 are 2,0,2,2,2, so N₁=9. Exact finite-field enumeration over F₂₅ gives 26 affine points plus infinity. Since a²−2q=9−10=−1, the predicted extension count is 25+1−(−1)=27. The inverse local elliptic L-factor is 1/(1+3·5^(−s)+5·5^(−2s)); it is not the full point-counting zeta function with its extra degree-zero and degree-two factors.',
 'The arithmetic determinant must identify the object and degree it represents. Concrete point counts can check a proposed factor and expose a mismatched numerator or denominator.',
 'The historical symbol M was not defined in the recovered passage. No motive, global Euler product, functional equation or quantum-neural interpretation is reconstructed from that missing definition.',
 'For further small primes, check good reduction and enumerate the same curve to build explicitly declared local factors, recording that global analytic continuation requires a separate theorem.',
 [('J S Milne Lectures on Etale Cohomology','https://www.jmilne.org/math/CourseNotes/LEC210.pdf'),('J S Milne Elliptic Curves','https://www.jmilne.org/math/Books/EC2.pdf')])

E('2024-05-24','Schr','Mathematical physics','Schrödinger continuity and guidance on a nonvanishing region',
 'Which equation conserves probability, and what additional condition allows a phase-gradient velocity to be defined?',
 'The recovered framework combined a generalized Schrödinger equation with a guidance equation. A valid mathematical connection is obtained directly from the ordinary Schrödinger PDE, with domains and zeros kept visible rather than introducing unsupported cross-domain terms.',
 ['Let iℏψ_t=−(ℏ²/(2m))Δψ+Vψ, where V is real and m>0. Define ρ=|ψ|² and j=(ℏ/m)Im(overline(ψ)∇ψ).', 'On a region where ψ≠0 and a phase lift exists, write ψ=√ρ exp(iS/ℏ); then j=ρ∇S/m.'],
 'The continuity equation is ρ_t+div j=0. On the nonvanishing phase-lift region the real part also gives S_t+|∇S|²/(2m)+V−(ℏ²/(2m))Δ√ρ/√ρ=0. The velocity j/ρ is well defined there, but need not extend through a node.',
 'Multiply the Schrödinger equation by overline(ψ), multiply its conjugate by ψ and subtract. The real potential terms cancel. Using div(overline(ψ)∇ψ−ψ∇overline(ψ))=overline(ψ)Δψ−ψΔoverline(ψ) yields continuity. Substitute the polar expression and separate real and imaginary parts to obtain the displayed equations; the division by √ρ is exactly why zeros must be excluded. Total mass is conserved only after the divergence integral has zero boundary flux, for example on a periodic domain or under suitable decay.',
 'Use the circle of circumference 2π, integer k and normalized state ψ(x,t)=exp(i[kx−ℏk²t/(2m)])/√(2π).',
 'Here ρ=1/(2π), j=ℏk/(2πm) and j/ρ=ℏk/m. The quantum-potential term vanishes because √ρ is constant. The phase solves S_t+S_x²/(2m)=0, and every trajectory of the stated guidance ODE moves at the same constant velocity. Integer k makes the wavefunction periodic even though a global real phase S changes by 2πℏk around the circle.',
 'Probability conservation, phase topology and a velocity field are separate but compatible pieces of a fully specified calculation.',
 'The polar reformulation is local near zeros and may require multiple phase charts. It does not validate modifications of the PDE or physical interpretations of a guidance law beyond the stated model.',
 'For a chosen nodal wavefunction, determine the connected nonvanishing regions and analyze whether the current transports mass between their boundaries.',
 [('David Tong Lectures on Quantum Field Theory and quantum-mechanical preliminaries','https://www.damtp.cam.ac.uk/user/tong/qft.html')])

E('2024-05-25','Gross','Nonlinear PDE','A nonlinear wave equation derived from its energy',
 'Which nonlinear wave equation follows from an explicit energy, and what quantities can be proved conserved?',
 'The Gross–Pitaevskii name appeared among many unrelated field theories. Its useful mathematical content can be developed as a Hamiltonian complex-field equation with a prescribed quartic energy and boundary conditions.',
 ['On a periodic interval, set E(ψ)=∫[(ℏ²/(2m))|ψ_x|²+V|ψ|²+(g/2)|ψ|⁴]dx, with real time-independent V,g.', 'The Hamiltonian field equation is iℏψ_t=δE/δoverline(ψ)=−(ℏ²/(2m))ψ_xx+Vψ+g|ψ|²ψ.'],
 'For sufficiently regular periodic solutions, mass N=∫|ψ|²dx and E are constant. For constant V=V₀ and density ρ₀, the spatially constant state ψ(t)=√ρ₀ exp(−i(V₀+gρ₀)t/ℏ) solves the equation exactly.',
 'Vary ψ and its conjugate independently in the real energy. Integration by parts yields the displayed functional derivative, with periodic endpoints eliminating boundary terms. The continuity calculation from the linear equation still works because V+g|ψ|² is real; therefore N is conserved. For energy, differentiating E along the solution gives twice the real part of the pairing of δE/δoverline(ψ) with the conjugate time derivative. Substituting ψ_t=(1/(iℏ))δE/δoverline(ψ) makes the pairing purely imaginary, so its real part vanishes. Substitution of the constant state leaves only its phase derivative and reproduces V₀+gρ₀.',
 'Choose ℏ=m=1, V₀=0, g=2, ρ₀=3 on an interval of length L.',
 'The exact state is √3 exp(−6it). Its mass is 3L and its energy is 9L. The nonlinear term changes the phase rate without changing the density. For a spatially varying perturbation, these two scalar invariants constrain but do not determine the subsequent evolution; proving stability requires a separate perturbation estimate.',
 'A nonlinear PDE can be mathematically coherent without deriving any of the other theories listed next to it. The energy functional and symplectic equation, rather than its name, provide the connection.',
 'The conservation proof presupposes the required regularity or a justified approximation argument. Focusing nonlinearities can introduce further well-posedness and blowup questions; no global solution theorem is claimed here.',
 'Compute the linearized spectrum around the constant state for a stated periodic length and sign of g, distinguishing a conserved solution from a stable one.',
 [('Lieb Seiringer and Yngvason rigorous Gross–Pitaevskii energy derivation','https://doi.org/10.1103/PhysRevA.61.043602')])

E('2024-05-25','path integral','Mathematical physics','Finite Gaussian and Grassmann integrals before formal path integrals',
 'Which finite-dimensional integral is defined, and what limit would be required before writing a functional integration symbol?',
 'The recovered passage used ∫DA Dψ exp(iS) beside several theories. The symbol alone does not give a measure or a convergence prescription. Finite Gaussian and Grassmann models supply exact reference calculations and explain why bosonic and fermionic quadratic contributions have different determinant powers.',
 ['For a real symmetric positive-definite n×n matrix A, define Z(A,J)=∫Rⁿ exp(−xᵀAx/2+Jᵀx)dx.', 'For independent Grassmann generators ψ_i and overline(ψ)_i, fix an ordered Berezin integration convention so ∫exp(−overline(ψ)Aψ)dψd overline(ψ)=det A.'],
 'The real Gaussian integral equals (2π)^(n/2)(det A)^(−1/2)exp(JᵀA⁻¹J/2). The corresponding finite fermionic quadratic integral is a determinant, with its sign tied to the chosen measure order.',
 'Complete the square: xᵀAx−2Jᵀx=(x−A⁻¹J)ᵀA(x−A⁻¹J)−JᵀA⁻¹J. An orthogonal diagonalization reduces the remaining integral to n one-variable Gaussians, each √(2π/λ_i), proving the formula. For the Grassmann expression, nilpotence truncates the exponential. Only the term containing every ψ and overline(ψ) survives integration; antisymmetrizing its coefficient sums over permutations with their signs, which is precisely the determinant once the ordering convention is fixed. This is algebraic integration, not Lebesgue integration over an ordinary vector of complex numbers.',
 'Take A=diag(2,8) and J=(2,0).',
 'The bosonic integral is (π/2)exp(1), since det A=16 and JᵀA⁻¹J/2=1. Its normalized mean is A⁻¹J=(1,0) and covariance A⁻¹=diag(1/2,1/8). The two-generator-pair Grassmann calculation instead yields 16 in the stated convention. Neither expression is an unregulated oscillatory infinite-dimensional integral.',
 'A defined finite model identifies the determinant, normalization and state space that a formal field integral must eventually reproduce.',
 'An infinite-dimensional translation-invariant Lebesgue measure is not supplied by the notation DA. Analytic continuation, regularization, gauge fixing and continuum convergence require separate arguments. No construction of QCD, loop gravity or M-theory is claimed.',
 'Choose a finite lattice quadratic action and prove convergence of selected normalized correlation functions as the lattice is refined, with boundary conditions and dimension specified.',
 [('David Tong Quantum Field Theory path integrals','https://www.damtp.cam.ac.uk/user/tong/qft.html')])

E('2024-05-25','AdS','Mathematical modeling','Source derivatives and dimensional claims in a proposed unification',
 'Which statements are identities of a defined generating function, which are model assumptions, and which merely have the right dimensions?',
 'The historical catalogue placed generating-function equalities, wave equations in different dimensions and a timescale ℏ/E beside one another. A rigorous revision separates what can be derived from a finite partition function from assumptions that require additional structure.',
 ['For a finite probability space with real statistic X and baseline weights p_i>0, set Z(J)=Σi p_i exp(JX_i) and W(J)=log Z(J).', 'A dimensional timescale τ=ℏ/E is defined only for a specified positive energy E; a differential operator □_d additionally needs a d-dimensional metric and a field domain.'],
 'W′(J) is the mean of X under the tilted distribution and W″(J) is its nonnegative variance. For a two-point X=±1 with equal weights, W=log cosh J and W″=sech²J. Dimensional agreement of ℏ/E with time does not select an evolution law.',
 'Differentiate the finite sum: Z′/Z=Σp_i exp(JX_i)X_i/Z. Differentiating again gives Z″/Z−(Z′/Z)², which is exactly the tilted second moment minus its mean square. The normalized tilted weights are positive and sum to one, making the variance nonnegative. For the two-point example Z=cosh J, and elementary differentiation gives tanh J and sech²J. Separately, ℏ has dimensions energy times time, so ℏ/E has time dimensions. That dimensional fact is compatible with numerous distinct laws and cannot choose one. For example both deterministic waiting time τ and an exponential waiting distribution of mean τ share the same scale while having different variances.',
 'Compare the response model X=±1 with two proposed waiting-time models at an arbitrary E>0.',
 'The response has mean tanh J and susceptibility sech²J, both calculated from a defined partition function. The deterministic waiting model has variance zero; the exponential model with rate E/ℏ has variance (ℏ/E)². Their mean times agree although their distributions do not. Likewise a wave equation □₁₁ψ=0 does not become a definition of an interacting eleven-dimensional theory merely because the dimension is named.',
 'A source-functional identity can be tested through its derivatives. A dimensional timescale and an undefined equality between theories require independent premises.',
 'This finite calculation does not prove an AdS/CFT correspondence, a collapse hypothesis, a multiverse functional or a proposed gravitational correction. Those were speculative assistant associations in the recovered record.',
 'For any proposed equality of partition functions, state both sides as defined objects and compare normalized derivatives or coefficients before claiming an equivalence of theories.',
 [('David Tong Statistical Field Theory generating functions','https://www.damtp.cam.ac.uk/user/tong/sft.html')])

E('2024-05-27','morphism','Category theory','Intertwining maps define a category of dynamical systems',
 'Which triples or maps are genuine morphisms, and does composition preserve the chosen dynamical structure?',
 'The recovered category names IndCog and CogEco were accompanied by morphism triples and functors but no complete axioms. A category of finite linear systems gives a mathematically finished replacement and a precise test for any proposed map between models.',
 ['An object is a pair (V,A), where V is a finite-dimensional real vector space and A:V→V is linear.', 'A morphism L:(V,A)→(W,B) is a linear map satisfying LA=BL. Composition is ordinary composition of linear maps and identities are identity maps.'],
 'These objects and intertwiners form a category. Every intertwiner transports the flow: Lexp(tA)=exp(tB)L. The forgetful assignment (V,A)↦V is a functor, but an arbitrary linear map need not be a morphism.',
 'The identity commutes with A. If LA=BL and MB=CM, then (ML)A=M(LA)=M(BL)=(MB)L=C(ML), so composition preserves the intertwining condition. Associativity is inherited from linear composition. Induction gives LAⁿ=BⁿL, and the absolutely convergent matrix exponential series gives the flow identity term by term. Thus a map that preserves the generator also preserves every time map. Conversely differentiating a flow-intertwining identity at t=0 recovers LA=BL.',
 'Let A=diag(−1,−2) on R², B=[−1] on R and L=[1,0].',
 'The equality LA=BL holds, and observing the first coordinate produces ẏ=−y for every initial state. The second mode is lost, but the observed dynamics closes exactly. By contrast M=[1,1] does not intertwine A with B: MA=[−1,−2] while BM=[−1,−1]. Its output derivative depends on hidden state and does not obey the same closed scalar equation. A purported functor using M would therefore need a different target object or extra state.',
 'The category formalism now expresses a concrete compatibility theorem rather than a vocabulary overlay.',
 'The recovered morphism triples were not defined sufficiently to reconstruct the original category. This replacement is explicitly newly specified mathematics, not a claim that the old named framework had already satisfied these axioms.',
 'For coupled block systems, require a componentwise morphism to intertwine the off-diagonal coupling blocks as well; solve those matrix equations exactly.',
 [])

E('2024-05-27','steady','Dynamical systems','Coupled equilibria with a complete two-variable stability test',
 'Which coupling strengths preserve a unique stable equilibrium, and how does a steady-state equation differ from a stability result?',
 'The May category-and-environment passages included coupled PDE or ODE variables and steady-state equations. A two-variable linear family develops the mathematical distinction completely and gives a parameter boundary that can be certified.',
 ['Let ẋ=−a x+b y+u and ẏ=c x−d y+v, with a,d>0 and real b,c,u,v.', 'Set A=[[-a,b],[c,−d]], D=ad−bc and forcing h=(u,v). A fixed point solves A z+h=0.'],
 'If D≠0 the fixed point is unique. It is exponentially stable exactly when D>0, because the trace is −(a+d)<0. If D<0 it is a saddle. At D=0, equilibrium existence and nonuniqueness depend on forcing compatibility.',
 'The characteristic polynomial is λ²+(a+d)λ+D. For a real two-by-two matrix, both roots have negative real part precisely when their sum is negative and product positive. Here the sum is always −(a+d), so positivity of D is the remaining condition. If D<0, the real roots have opposite signs. At D=0 one eigenvalue is zero, and solving the singular linear equations requires h to lie in the image of −A; if it does, adding any null vector gives another fixed point. These statements follow directly from the quadratic polynomial and linear algebra, not from the word equilibrium.',
 'Take a=d=1 and b=c=r with forcing u=1,v=0.',
 'For |r|<1, D=1−r²>0 and the fixed point is (1/(1−r²),r/(1−r²)); the eigenvalues are −1±r. At r=1 the equations require −x+y+1=0 and x−y=0, which are inconsistent, so no fixed point exists. With zero forcing instead, r=1 has the entire line x=y of equilibria. For r>1, the unique forced fixed point is unstable even though its algebraic formula still exists.',
 'A static equation, a unique solution and an attracting state are three distinct claims with separate conditions.',
 'This is a linear finite example. A coupled PDE additionally needs function spaces, boundary conditions and an operator-domain analysis; nonlinear local stability does not automatically imply global behavior.',
 'Apply the same block-intertwining criterion to this family and classify which scalar observations have exact closed dynamics across the parameter boundary.',
 [])

E('2024-05-27','SDE','Stochastic analysis','A specified noisy dynamics and its stationary covariance',
 'What stochastic process is meant by a disturbance term, and which drift and diffusion assumptions produce a stationary distribution?',
 'A recovered passage contained a social SDE and a noisy state ODE without a probability law or stability conditions. The Ornstein–Uhlenbeck model gives a complete mathematical replacement whose moments and equilibrium can be derived exactly, without retaining the unsupported application interpretation.',
 ['Let dX_t=−aX_tdt+σdW_t, where a>0, σ≥0 and W is standard Brownian motion. Assume X₀ is independent of future Brownian increments and has finite second moment.', 'The Itô stochastic integral satisfies E∫f dW=0 and E|∫f dW|²=∫|f|² for deterministic square-integrable f.'],
 'The solution is X_t=e^(−at)X₀+σ∫₀^t e^(−a(t−s))dW_s. Its mean is e^(−at)EX₀ and its variance is e^(−2at)Var(X₀)+(σ²/(2a))(1−e^(−2at)). The centered Gaussian N(0,σ²/(2a)) is invariant.',
 'Multiply the SDE by the deterministic integrating factor e^(at); the product rule has no quadratic-variation cross term with that factor, giving the explicit solution. Independence and zero mean of the stochastic integral give the mean formula and eliminate the covariance cross term. Itô isometry evaluates the noise variance as σ²∫₀^t e^(−2a(t−s))ds. A deterministic initial state leads to a Gaussian integral, and starting with the stated independent Gaussian makes the displayed variance constant. This proves stationarity of its one-time distributions; the transition law supplies the full Markov invariant distribution.',
 'Choose a=2, σ=3 and X₀=1 deterministically.',
 'The mean is e^(−2t) and variance (9/4)(1−e^(−4t)), approaching 9/4. Noise does not vanish merely because the mean approaches zero. In several dimensions, the stable linear SDE dX=AXdt+B dW has stationary covariance P satisfying AP+PAᵀ+BBᵀ=0 when A is Hurwitz; this follows by differentiating P(t)=∫₀^t e^(As)BBᵀe^(Aᵀs)ds and taking its convergent limit.',
 'A stochastic equilibrium is a distribution, not necessarily a fixed sample path. The noise amplitude and stable drift determine its width.',
 'Brownian noise is an explicit modeling assumption, not a consequence of an unexplained ε(t). This derivation does not claim that a social or cognitive process follows an OU law.',
 'For a rational stable drift and diffusion matrix, solve the Lyapunov covariance equation exactly and determine which covariance directions are invisible under a chosen observation map.',
 [])

E('2024-05-27','Kleisli','Category theory and topology','Finite probability kernels compose but do not determine topology',
 'Can the proposed monadic maps be defined as composable probability kernels, and what extra data are needed before topological invariants make sense?',
 'The recovered framework placed Kleisli categories, a binary operation, Betti numbers and fundamental groups together. There are valid mathematical structures here, but they require distinct inputs. A finite probability-kernel category is explicit, while a point cloud or transition table does not itself select a unique topological complex.',
 ['A finite probability kernel P:X→Y is a row-stochastic matrix, Pxy≥0 and ΣyPxy=1. Composition is (PQ)xz=ΣyPxyQyz.', 'A simplicial complex requires specified simplices closed under faces. Its homology is computed from boundary maps, not from stochastic normalization alone.'],
 'Finite probability kernels form a category with identity matrices and associative composition. The distribution pushforward μ↦μP respects that composition. The same three vertices can support a disconnected complex, a triangle boundary or a filled triangle, with different Betti numbers despite the same vertex set.',
 'A product of nonnegative matrices is nonnegative, and summing a product row gives ΣyPxyΣzQyz=1. Finite-sum associativity proves (PQ)R=P(QR); the identity matrix gives the deterministic identity kernel. Also (μP)Q=μ(PQ), supplying the stated functorial behavior. For topology, three isolated vertices have β₀=3. Adding the three cycle edges makes a connected one-dimensional complex with β₁=1; adding its triangular face makes that cycle a boundary and β₁=0. No choice among these complexes follows from having merely named three states.',
 'Use P=[[1/2,1/2],[1,0]] and Q=[[1,0],[1/4,3/4]].',
 'Then PQ=[[5/8,3/8],[1,0]], whereas QP=[[1/2,1/2],[7/8,1/8]], so the composition operation is associative but not commutative. If a threshold rule turns transitions into graph edges, changing that threshold can change connectivity; filling selected cycles is another independent modeling choice. Thus neither a monad label nor an algebra operation selects the homology without a construction rule.',
 'Category composition and topological invariants can coexist in a specified model, but neither is supplied by the other’s vocabulary.',
 'This gives the finite-distribution Kleisli example, not every possible monad or the unrecovered details of the historical CogEco framework. No original mathematical prompt or complete axioms were returned.',
 'Specify a functor from the kernel data to a filtered complex and test whether its maps preserve the declared filtration; only then compare persistent topological invariants.',
 [('Hatcher Algebraic Topology homology construction','https://pi.math.cornell.edu/~hatcher/AT/ATchapters.html')])

extra={
1:' At the other endpoint ρ=−1, the squared distinction is9/25, but the total-mass vector(1,1) lies in the kernel. Thus positive semidefiniteness permits null directions at either endpoint; strict positive definiteness requires−1<ρ<1.',
2:' For two nonvanishing differentiable loops z and u, the logarithmic derivative of their pointwise product is (zu)′/(zu)=z′/z+u′/u. Integration therefore proves w(zu)=w(z)+w(u). This product law is distinct from, and compatible with, the concatenation law.',
3:' The boundary condition is part of the certificate: all admissible variations have zero endpoint values, so the integration-by-parts boundary term vanishes exactly. For prescribed nonzero endpoints, choose one fixed admissible lift h and optimize over h+H₀¹ instead. The same positive quadratic remainder then proves uniqueness on that affine admissible set.',
5:' The recovered symmetric-power series has a precise point-counting interpretation: an effective zero-cycle is a nonnegative sum of closed points. A closed point of degree d contributes the geometric series(1−t^d)⁻¹. Multiplying over closed points gives the generating series of their multisets; taking its logarithm yieldsΣ_r N_r t^r/r, because a degree-d point contributes d rational points exactly over extension degrees divisible by d. This connects the symmetric-power generating function, Euler product and exponential point counts under the declared finite-field interpretation.',
4:' The supertrace is tr on the even coordinate minus tr on the odd coordinate. Here str(I)=1−1=0 although tr(I)=2. This distinction explains why the supercommutator identity is compatible with a vanishing supertrace; applying the ordinary trace rule for commutators would discard the grading.',
6:' Nodes show why division needs a domain restriction. For a real standing-wave profile cos x, the current is zero, but its density vanishes at odd multiples ofπ/2. The ratio j/ρ is well defined and zero between nodes, while the formula itself is undefined at each node. A removable interpretation must be justified separately.',
7:' The same constant solution formula holds for negative g, but conservation alone still proves no stability theorem. The energy then has a negative quartic contribution, whereas its kinetic term remains nonnegative. Which perturbations increase or decrease the constrained energy depends on the domain, mass constraint and Fourier mode, not merely on the phase solution.',
8:' Differentiating logZ with respect to J gives A⁻¹J and differentiating once more gives A⁻¹, recovering the mean and covariance without any additional integrations. Positive definiteness is essential: a zero eigenvalue gives a divergent integral along its direction, and a negative eigenvalue makes the real exponential grow quadratically. The fermionic determinant has no such positivity interpretation.',
10:' The kernel of an intertwiner is invariant: if Lv=0 then LAv=BLv=0. Hence a surjective intertwiner produces an autonomous quotient dynamics on V/kerL. A proposed coarse variable failing this invariance cannot close under the chosen linear dynamics without adding hidden coordinates or changing the target evolution.',
11:' The stable fixed point also becomes sensitive near the boundary. As r approaches1 from below, both coordinates grow like1/[2(1−r)]. The slow eigenvalue−1+r tends to zero at the same time. Algebraic solvability away from the singular value therefore supplies neither a uniform response bound nor a uniform decay rate.',
12:' For a concrete multidimensional case, A=diag(−1,−2) and B=I give P=diag(1/2,1/4). Substitution yields AP+PAᵀ=−I exactly. The covariance is anisotropic although the two driving noises have equal intensity; different relaxation rates produce different stationary variances.',
13:' On a triangle boundary, the edge-to-vertex boundary map has rank2, leaving one independent one-cycle. Filling that triangle adds a face whose boundary is precisely the cycle, so the first Betti number drops from1 to0. This extra boundary map is data not contained in a stochastic transition matrix.'}
for k,text in extra.items():entries[k-1]['example']['calculation']+=text
for e in entries:
    e['word_count_approx']=len(json.dumps({k:v for k,v in e.items() if k not in ['original','references']},ensure_ascii=False).split())
    assert e['word_count_approx']>=300,(e['id'],e['word_count_approx'])
(HERE/'entries.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2))
print(json.dumps({'entries':len(entries),'words':sum(e['word_count_approx'] for e in entries)}))
