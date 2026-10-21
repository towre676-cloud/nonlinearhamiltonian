# The equation that opened the Hamiltonian programme

This is an edited mathematical reconstruction of the favorite-equation discussion. It preserves the identity and explains its derivation; it does not claim to reproduce an unavailable original chat transcript word for word.

For one canonical pair with $\{F,G\}=F_qG_p-F_pG_q$, the favorite identity is

$$
\boxed{\frac{[qp^3,q^{3r+2}p^r]_\star}{i\hbar}
=-(8r+6)q^{3r+2}p^{r+2},\qquad r=0,1,2,\ldots.}
$$

The left side is the normalized Weyl–Moyal commutator, as a formal polynomial in $\hbar$. The right side is exactly its classical Poisson bracket. The degree of the partner $q^{3r+2}p^r$ grows without bound, so this is an infinite family for a fixed nonlinear Hamiltonian.

The computation exposes the structure. For $H=qp^3$ and $G=q^c p^d$,

$$
\{H,G\}=(d-3c)q^c p^{d+2},\qquad
T_3(H,G)=6c(c-1)(3d-c+2)q^{c-2}p^d.
$$

All odd corrections of order five or higher vanish because $H$ has total degree four. Choosing $c=3d+2$ kills the remaining third-order correction. Substituting $d=r$ gives $d-3c=-8r-6$, and proves the displayed identity in every degree.

This points to a concrete organizing mechanism: cancellation of the deformation obstruction imposes a resonance condition on the exponent lattice. It also reveals the limit of a first bracket calculation. A one-step exact partner need not remain exact after further Hamiltonian evolution. For this Hamiltonian the full one-step space is

$$
\mathcal E(qp^3)=\mathbb C[p]\oplus q\mathbb C[p]\oplus q^2\mathbb C[q^3p],
$$

whereas its largest dynamically invariant exact subspace is

$$
\mathcal D_\infty(qp^3)=\mathbb C[p]\oplus q\mathbb C[p].
$$

The complete [research paper](../research/hamiltonian/GITHUB_RESEARCH.md) proves the classification, develops the quantum ladders, and treats general cubic, quartic, $qF(p)$ and monomial Hamiltonians with their precise scope and limits.
