# Year-by-year discussion

Editorial reconstruction, 21 October 2026. Each featured item below quotes its completed treatment’s title, revised question, summary and result, and links to its full proof and example. Selection is editorial; it is not a recovered verbatim annual chat response.

## 2023

The 2023 collection begins by repairing the mathematical object behind a question: the scalar field, state space, observation map, boundary condition or equivalence relation must be named before a proposed connection can be evaluated. Its 114 revised main questions develop into complete treatments, with fourteen further synthesis bodies. The initial revised table is preserved alongside the expanded volume. The historical header referring to “six connecting arguments” does not count the actual fourteen retained synthesis bodies correctly; the public catalog uses the actual body count.

[Complete 2023 question index](../compendium/readable/years/2023/INDEX.md) · [Full CSV](../tables/treatments_2023.csv).

### Separate the meanings of Q

[2023:M001: full treatment, proof and worked example](../compendium/readable/years/2023/M001.md).

The original notation can be repaired completely at the level of objects. Robinson arithmetic Q is a first-order theory, Q_p is a valued field of characteristic zero, F_p[[q]] is a formal power-series ring of characteristic p, and D_q is an operator depending on a numerical or formal parameter. A proposed connection must name the relevant category and map; the shared letter Q supplies neither.

**Revised question.** Which structure is actually intended: Robinson arithmetic Q, a q-difference calculus, a p-adic field, or a formal power-series ring? What maps, if any, connect the chosen structures?

**Result.** There is a canonical dense embedding Q→Q_p and a compatible reduction system Z_p→Z/p^nZ. There is no unital ring homomorphism Q_p→F_p[[q]], or in the reverse direction. In particular these objects cannot be identified by renaming their parameters.

**Limit.** An arithmetic theory can be interpreted in structures, and equal-characteristic local fields can resemble mixed-characteristic fields in selected respects. The characteristic obstruction does not rule out every model-theoretic or categorical comparison; it rules out the specified unital ring identifications.

### Minimal universal recurrences on an observable quotient

[2023:M016: full treatment, proof and worked example](../compendium/readable/years/2023/M016.md).

Cayley–Hamilton always gives a recurrence for a finite linear state, but the observable behavior may require a strictly smaller polynomial. The correct object is the induced operator after all permanently invisible directions have been quotiented out.

**Revised question.** Which sequence of observables satisfies a finite recurrence, and can the minimal polynomial give a shorter recurrence than the characteristic polynomial?

**Result.** N is A-invariant, so A induces A_bar on V/N. A polynomial p gives a universal output recurrence exactly when p(A_bar)=0. Thus the unique least-degree monic universal recurrence is the minimal polynomial of A_bar. Its degree is at most dim(V/N); for a scalar observable with an observable quotient it equals that quotient dimension.

**Limit.** A recurrence fitted to one finite prefix may be accidental. The quotient argument proves a recurrence for all times under the stated model; finite fitting alone does not.

### Ensemble assumptions determine the spectral baseline

[2023:M022: full treatment, proof and worked example](../compendium/readable/years/2023/M022.md).

A random-matrix comparison must preserve dependence, centering and normalization. A simple fourth-moment calculation shows why a sparse adjacency matrix cannot be treated as a dense Wigner matrix without qualification.

**Revised question.** Which random-matrix ensemble matches the dependence and normalization of the matrix being analyzed?

**Result.** E[Tr(W²)/n]=(n−1)/n. Moreover E[Tr(W⁴)/n]=2(n−1)(n−2)/n²+(n−1)[1−3p(1−p)]/[n²p(1−p)]. Thus p=c/n with fixed c>0 yields fourth-moment limit 2+1/c, whereas np(1−p)→∞ removes this extra term.

**Limit.** Two moments do not prove a complete limiting spectral law. The sparse calculation demonstrates a mismatch, not a universal law for every sparse network. No prediction about human behavior follows from these moment identities.

### Exact polynomial Moyal products

[2023:M086: full treatment, proof and worked example](../compendium/readable/years/2023/M086.md).

On polynomial symbols the Moyal exponential terminates, so one can verify noncommutativity and associativity with exact arithmetic rather than relying on an informal infinite series.

**Revised question.** What star product is being used, on what function class or formal series ring, and which limit recovers the Poisson bracket?

**Result.** q⋆p−p⋆q=iℏ. More generally the antisymmetrized product divided by iℏ equals the Poisson bracket plus terms of formal order ℏ². The product is associative in the polynomial or formal setting.

**Limit.** Formal associativity does not prove convergence of the Moyal series for arbitrary smooth functions. Trace-integral identities require integrability and boundary conditions; polynomial symbols on the full plane are usually not integrable.

## 2024

The 2024 collection develops the earlier distinctions into maps and calculations: Hamilton–Jacobi characteristics, local-to-global gluing, spectral calculations, finite-state quantum examples and exact arithmetic certificates. It contains 237 retained treatments, organized in the annual volume by the recovered months. January was not recovered. The March record contains the recovered numbered segment 81–100 plus an unnumbered Laplace item; it does not reconstruct a missing complete first hundred questions.

[Complete 2024 question index](../compendium/readable/years/2024/INDEX.md) · [Full CSV](../tables/treatments_2024.csv).

### Hamilton, Hamilton–Jacobi and Riccati equations meet at a caustic

[2024:Y24-03-031: full treatment, proof and worked example](../compendium/readable/years/2024/Y24-03-031.md).

Three separately named catalog items can be made concrete with one harmonic oscillator. The Hamiltonian flow is a smooth rotation in phase space; a quadratic Hamilton–Jacobi function describes a graph inside it; a scalar Riccati equation controls that graph’s slope. The finite-time pole is therefore a coordinate failure of the graph description, not a singularity in the underlying oscillator.

**Revised question.** Reconstruction: How are Hamilton’s equations related to the Hamilton–Jacobi PDE, how does a quadratic phase produce a Riccati equation, and why can that Riccati variable blow up while the mechanical trajectory remains smooth?

**Result.** For the unit oscillator, q(t)=q₀cos t+p₀sin t and p(t)=p₀cos t−q₀sin t solve Hamilton’s equations for all real t. With initial graph p₀=0, the Hamilton–Jacobi solution S(q,t)=−(tan t)q²/2 is valid for |t|<π/2, and A(t)=−tan t solves the associated Riccati equation.

**Limit.** This is the classical Hamilton–Jacobi equation, not automatically the Hamilton–Jacobi–Bellman equation of an optimal-control problem. A local smooth phase need not exist globally after characteristics cross. The written calculation does not claim global smooth solutions for an arbitrary Hamiltonian.

### Euclidean certificates and a complete Pell example

[2024:Y24-03-024: full treatment, proof and worked example](../compendium/readable/years/2024/Y24-03-024.md).

These arithmetic concepts are connected by explicit certificates rather than a shared formula. The Euclidean algorithm produces a finite integer identity; Pell’s equation supplies an infinite family whose recurrence preserves a norm. A descent argument is included so that the chosen Pell example is more than a list of numerically observed solutions.

**Revised question.** Reconstruction: How does the Euclidean algorithm certify a greatest common divisor, and how does multiplication of quadratic units generate and classify the positive solutions of x²−2y²=1?

**Result.** Replacing (a,b) by (b,a−qb) preserves common divisors; choosing the remainder 0≤r<|b| ensures termination. For Pell D=2, every solution x,y≥0 is x+y√2=(3+2√2)ⁿ for a unique n≥0.

**Limit.** The Pell classification is explicitly restricted to D=2 and nonnegative x,y; signs produce the other integer solutions. For square D the equation has a different character, and the general nonsquare case requires an additional existence and fundamental-unit argument.

### Sheaf notation needs a gluing rule and cohomology needs a complex

[2024:Y24-04-014: full treatment, proof and worked example](../compendium/readable/years/2024/Y24-04-014.md).

Compatible continuous functions on an open cover glue uniquely to a continuous global function. On T² the classes[dx],[dy] have a nonzero product represented by dx∧dy, whose integral is one; each class squares to zero. The treatment supplies actual local-to-global content and an actual product, with their distinct assumptions exposed.

**Revised question.** What local objects are assigned to an open set, and what theorem connects compatible local data to a global section?

**Result.** Compatible continuous functions on an open cover glue uniquely to a continuous global function. On T² the classes[dx],[dy] have a nonzero product represented by dx∧dy, whose integral is one; each class squares to zero.

**Limit.** A function written GeneExpression=f(arguments) in the old fragment has no specified domain, data or sheaf structure and yields no mathematical theorem by itself. Not every presheaf glues: assigning one constant value to every nonempty open set fails on a disconnected union whose components carry different constants.

### Entanglement, dephasing and observability in a two-qubit calculation

[2024:Y24-06-023: full treatment, proof and worked example](../compendium/readable/years/2024/Y24-06-023.md).

The recovered assistant passage mentions CNOT entanglement and Lindblad decoherence. A Bell pair undergoing local dephasing yields an exact channel, a closed-form density matrix and a precise observability distinction between individual marginals and joint correlations.

**Revised question.** Which completely positive channel models the stated decoherence, and which observables can distinguish its effects?

**Result.** The resulting channel is E_t(ρ)=((1+q)/2)ρ+((1−q)/2)ZρZ. It is trace preserving and completely positive. Applied to the first half of |Φ⁺⟩, it leaves each one-qubit marginal I/2, but changes the joint expectation ⟨X⊗X⟩ from1 to q while ⟨Z⊗Z⟩ remains1.

**Limit.** Lindblad form assumes a specified Markovian quantum dynamical model; it does not derive a biological mechanism. Negative time or γ<0 makes the displayed mixture coefficients unsuitable for this channel family. Marginal blindness here is not a claim that all measurements are uninformative.

### Navier plate modes and the Rayleigh quotient share a spectral calculation

[2024:Y24-03-029: full treatment, proof and worked example](../compendium/readable/years/2024/Y24-03-029.md).

A plate equation needs its boundary conditions before a Fourier formula is valid. A simply supported rectangle provides a case where each sine mode diagonalizes both the static equation and the vibration equation. The Rayleigh quotient is the corresponding energy ratio, with a small matrix example showing its algebra transparently.

**Revised question.** Reconstruction: For a simply supported rectangular thin plate, what does a single sine load produce, and how does the Rayleigh quotient bound an eigenvalue and quantify an approximate eigenvector?

**Result.** Let φ_mn=sin(mπx/a)sin(nπy/b), λ_mn=(mπ/a)²+(nπ/b)². Then Δφ=−λφ and Δ²φ=λ²φ. A static load Pφ gives w=Pφ/(Dλ²), and a free vibration in this mode has ω²=Dλ²/μ. Also λ_min(A)≤R_A(v)≤λ_max(A) and dist(R_A(v),spectrum(A))≤||Av−R_A(v)v||/||v||.

**Limit.** This uses a thin, small-deflection, linear plate model. Clamped edges require different mode shapes, so the same sine formula cannot be transferred to them. A Rayleigh quotient is an estimate for a specified self-adjoint operator; it need not be an eigenvalue.

## 2025

The 2025 collection contains 351 treatments. Structures that can sound interchangeable are separated by actual definitions: a modular Hamiltonian depends on a state, a spectral problem includes boundary conditions, a tangent complex derives from a cotangent complex, and equivariant constructions retain stabilizer data. The useful continuity is through well-defined maps and hypotheses, rather than a claim that every recurring word denotes one universal theory.

[Complete 2025 question index](../compendium/readable/years/2025/INDEX.md) · [Full CSV](../tables/treatments_2025.csv).

### A modular Hamiltonian is defined by a state

[2025:Y25-01-023: full treatment, proof and worked example](../compendium/readable/years/2025/Y25-01-023.md).

For a positive density matrix the modular Hamiltonian is−logρ. In a commuting finite model its entropy variation is exact to first order, and the negative second variation quantifies concavity. This is distinct from the weight transformation of a modular form.

**Revised question.** What mathematical relation does a modular Hamiltonian have to entropy, and which extra data are needed before inserting it into a geometric action?

**Result.** S′(0)=Tr(δρK)=−Σv_i logp_i, andS″(0)=−Σv_i²/p_i. The second derivative is strictly negative for every nonzero trace-zero diagonal perturbation.

**Limit.** This finite commuting derivation does not define a modular gravitational action, renormalized black-hole entropy or a modular Hamiltonian for a quantum field region. Matrix positivity and trace normalization are essential.

### The derived tangent complex comes from the cotangent complex

[2025:Y25-01-015: full treatment, proof and worked example](../compendium/readable/years/2025/Y25-01-015.md).

For a hypersurface the cotangent complex is an explicit two-term derivative map. At a double point it detects both a tangent direction and an obstruction, information not supplied byRHom(O_X,O_X).

**Revised question.** Which complex captures infinitesimal deformations and obstructions at a singular point?

**Result.** Atx=0 the tangent-complex differential is zero, soH⁰≅k andH¹≅k. Every first-order displacementx=at satisfiesx²=0 modulot², but it extends tox=at+bt² modulot³ only ifa²=0.

**Limit.** The displayed hypersurface model uses a regular-sequence presentation. General derived schemes require the full cotangent complex and derived base change. A nonzero obstruction space does not mean every deformation is obstructed.

### Boundary conditions are part of a spectral problem

[2025:Y25-01-005: full treatment, proof and worked example](../compendium/readable/years/2025/Y25-01-005.md).

A differential expression alone does not specify an operator. The same second derivative has different spectra under Dirichlet and periodic domains, illustrating the domain gap in a proposed zeta Hamiltonian without pretending to resolve it.

**Revised question.** Which operator domain makes an eigenvalue condition a theorem, and how does changing that domain change the spectrum?

**Result.** The Dirichlet eigenvalues aren² forn≥1, with eigenfunctionssin(nx). The periodic eigenvalues are4n² forn∈Z, including zero, with eigenfunctionse^{2inx}.

**Limit.** The Bender–Brody–Müller proposal is a specific research construction, not a generic synonym for pseudo-Hermitian matrices. Its primary paper explicitly makes the self-adjointness argument conditional. This example proves neither that construction nor the Riemann hypothesis.

### Equivariant cohomology retains the stabilizer of a fixed point

[2025:Y25-01-022: full treatment, proof and worked example](../compendium/readable/years/2025/Y25-01-022.md).

The plane contracts to its origin equivariantly, so its equivariant cohomology isH*(BS¹)=k[u]. Ordinary plane and free-loop-space cohomology are instead justk. These are different constructions with different retained symmetry data.

**Revised question.** What isH*_{S¹}(R²) for the oscillator rotation action, and why does contractibility not make it ordinary point cohomology?

**Result.** H*_{S¹}(C;k)≅k[u], with one generator in every nonnegative even degree and none in odd degree. H*(C;k)=H*(LC;k)=k in degree zero only.

**Limit.** A claimed spectral-sequence degeneration needs its actual fibration or filtered complex and differential bidegrees. No such general degeneration follows merely from the oscillator notation.

### Noncommutative observables still have identities and symmetries

[2025:Y25-01-003: full treatment, proof and worked example](../compendium/readable/years/2025/Y25-01-003.md).

Commuting self-adjoint matrices admit a common orthonormal eigenbasis. Noncommuting examples retain an identity and can have exact unitary symmetries; their uncertainty is a quantitative statement about a state.

**Revised question.** Which algebraic property separates jointly measurable finite observables, without discarding identity operators or symmetry?

**Result.** A finite commuting family of self-adjoint matrices is simultaneously unitarily diagonalizable. Forψ=(1,i)/√2,ΔX=ΔZ=1 and|〈[X,Z]〉|/2=1, attaining the Robertson lower bound.

**Limit.** The finite result does not settle interpretations of quantum measurement or a Platonic ontology. Unbounded observables need common domains; zero commutator expectation in one state does not mean the operators commute.

## 2026

The 2026 collection contains 349 treatments through 21 October. It makes the certificate and the target explicit: reachable-observable state rather than a whole generated algebra, congruence filters plus descent for arithmetic completeness, finite-horizon Gramians with their hypotheses, and cohomology classes rather than a numerical residual for deformation obstructions. October is partial. Nothing is extrapolated into the remainder of October, November or December.

[Complete 2026 question index](../compendium/readable/years/2026/INDEX.md) · [Full CSV](../tables/treatments_2026.csv).

### Hamiltonian conservation follows from the symplectic convention and has an exact pendulum separatrix

[2026:Y26-05-016: full treatment, proof and worked example](../compendium/readable/years/2026/Y26-05-016.md).

The May Invariant Action passage supplies phase space, symplectic form, flow composition and Poisson conservation. Fixing the contraction convention allows a direct theorem and a constructive nonlinear orbit, rather than treating all invariant language as an analogy.

**Revised question.** Reconstruction: Which sign convention gives the Hamilton equations and which invariant identifies the pendulum separatrix?

**Result.** Along any Hamiltonian trajectory, df/dt={f,H}, so {f,H}=0 implies conservation. The pendulum has separatrix q(t)=4arctan(e^t)−π, p(t)=2sech t, which lies on H=2 and joins adjacent unstable lifts.

**Limit.** The chosen contraction convention fixes the Poisson sign. Quantization analogies do not establish a unitary model, and conservation alone does not imply numerical integrator accuracy.

### A complete Pell orbit has exact congruence filters and a logarithmic population

[2026:Y26-09-029: full treatment, proof and worked example](../compendium/readable/years/2026/Y26-09-029.md).

The PerfectPower reconstruction emphasized the difference between finiteness and a complete explicit family. The recovered equation2n²+1=m² admits an elementary complete positive classification, a periodic modular filter and an exact explanation of logarithmic counts. Its shifted triangular version also explains the reported small-parameter logarithmic correction.

**Revised question.** Are all seeds and signs covered, and how do admissible orbit positions change the counting coefficient?

**Result.** All positive solutions of m²−2n²=1 are(m_j,n_j) for j≥1. Hence#{j≥1:n_j≤N}=(logN)/(logE)+O(1). If w of P periodic index classes are admissible, the coefficient becomes w/(PlogE).

**Limit.** A general Pell-type equation can have several inequivalent seeds and sign domains. A tested list or one orbit does not certify all of them. No unproved global A048624 shift uniqueness is inferred.

### Hankel rank measures reachable observable state, not the whole generated algebra

[2026:Y26-09-010: full treatment, proof and worked example](../compendium/readable/years/2026/Y26-09-010.md).

The Wilson work distinguished algebra-build cost from column-execution cost and later corrected reversed words. A small noncommutative example proves why both distinctions matter. The generated matrix algebra, reachable columns and observed word series need not have the same dimension.

**Revised question.** Which word convention describes physical execution, and which Hankel factorization determines the minimal observed realization?

**Result.** Every d-dimensional representation gives rankH≤d. If the reachable columns and observable rows both span dimension d, suitable finite submatrices have rank d and no smaller realization can produce the same series. The generated algebra can have dimension d².

**Limit.** This does not reproduce the historical81/82 or92/114 cost gaps; their operation and support tables were not returned. Algebra rank alone cannot determine an execution-call budget.

### Finite-horizon Gramians certify controllability and observability

[2026:Y26-08-006: full treatment, proof and worked example](../compendium/readable/years/2026/Y26-08-006.md).

The source lists controllability and observability alongside a reported dynamic benchmark. A theorem for declared matrices proves their relationship without adopting benchmark margins whose underlying model was not recovered.

**Revised question.** Why do Gramian positivity and the Kalman rank conditions agree, even on a finite horizon?

**Result.** W_c(T)>0 exactly when the controllability matrix has rankn. LikewiseW_o(T)>0 exactly when the stacked matrix[C;CA;…;CA^{n−1}] has rankn. These statements do not requireA to be stable.

**Limit.** The source’s11-state benchmark, reported PBH margins and covariances were not available for replay. None is validated by this example.

### A second-order Maurer–Cartan obstruction is a cohomology class, not a numerical residual

[2026:Y26-05-029: full treatment, proof and worked example](../compendium/readable/years/2026/Y26-05-029.md).

The homological followup contains the Maurer–Cartan equation and the class of one-half the bracket square. We state a differential graded Lie version with explicit signs and solve a finite obstruction example. This gives constructive deformation content without extending a finite arity check to an unrestricted L∞ theorem.

**Revised question.** Reconstruction: What exact class obstructs extending a first-order deformation to second order?

**Result.** A first-order a extends through order t² exactly when the degree-two cocycle [a,a]/2 is a boundary. Its obstruction class lies in H²(L). In a finite model with L¹=Qa⊕Qb, L²=Qc, db=c, da=0 and [a,a]=2c, the extension α=t a−t²b exists exactly.

**Limit.** An L∞ algebra has higher brackets and additional higher-order obstructions. Verifying identities through arity three does not establish all arities or convergence of a formal series.

### A two-point spectral distance can be computed from the commutator norm

[2026:Y26-01-904: full treatment, proof and worked example](../compendium/readable/years/2026/Y26-01-904.md).

A broad recovered archive topic is made concrete through the specified mathematical object below. The construction supplies a proof and an exact or analytically evaluated example; it does not assert that missing historical formulas have been recovered.

**Revised question.** How does a specified Dirac-type operator turn algebraic observables into a distance?

**Result.** d(δ_1,δ_2)=1/|m|. If m=0, the two states have infinite distance under the same supremum.

**Limit.** This model does not establish an emergent geometry for an unspecified learned representation, or replace the analytic hypotheses of an infinite spectral triple.
