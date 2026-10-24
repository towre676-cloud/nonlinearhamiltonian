# Independent Schur-complement review

Reviewed 24 October 2026. The stated formulas are correct for centered random
variables with finite second moments. Let `A=E[qq^T]`, `S=E[qp^T]`,
`M=E[qF^T]`, and suppose `A` is positive definite. The residuals
`u=p-S^T A^-1 q`, `g=F-M^T A^-1 q` are orthogonal to every linear position
observable. Their covariances are

`U=P-S^T A^-1 S`, `G=L-M^T A^-1 M`, `C=N-S^T A^-1 M`.

For fixed positions and `p+=p+hF`, the new residual is exactly `u+h*g`.
Consequently `U+=U+h(C+C^T)+h^2G`. The block matrix
`[[U,C],[C^T,G]]` is positive semidefinite because it is a covariance matrix.
For every fixed real vector `v`, the reverse triangle inequality gives

`|sqrt(v^T U+ v)-sqrt(v^T U v)| <= |h| sqrt(v^T G v)`.

In one plane, define `a=Var(x)>0`, `b=Cov(x,p)`,
`u=p_centered-(b/a)x_centered`,
`g=F_centered-(Cov(x,F)/a)x_centered`. Since projected squared emittance
is `a E[u^2]`, its exact update and norm bound follow immediately. Centering
must include force means; affine force offsets and own-plane linear focusing
then cancel. The bound is sharp: take independent centered unit-variance
Rademacher variables `x,g`, let `p=g+beta*x`, `F=g+gamma*x`, and `h>0`.
The emittance changes from 1 to `1+h`, attaining the bound.

## Coupling counterexample

Use all 16 equally weighted points `(x,y,p_x,p_y)` in `{-1,1}^4` and the
symmetric Hamiltonian kick `F=(3*y,3*x)`, with `h=2`. The initial covariance is
the identity. Full-position force residual `g` is zero, and the four-dimensional
covariance determinant stays 1. However each projected squared emittance
changes from 1 to 37. Thus removing all position-linear force is valid for the
full Schur residual/determinant but cannot be used as a projected-emittance
error bound. Own-plane regression retains this cross-plane force, as required.
These scalar values were also checked with exact rational arithmetic.

The determinant preservation holds for every linear momentum shear because
its map determinant is 1. Calling that map canonical additionally requires the
position-to-force matrix to be symmetric. The counterexample uses a symmetric
matrix and therefore meets this stronger condition.

## Degeneracies and certificate boundary

If `Var(x)=0`, centered `x=0` almost surely, so projected emittance is zero
before and after a position-preserving kick; do not divide by zero. For singular
`A`, either restrict positions to their covariance support or use the
Moore-Penrose inverse together with the covariance range conditions. Exact
covariance data automatically satisfy those conditions. A simple implementation
may instead reject singular `A` explicitly. The `det(A)*det(U)` factorization
must not be used with an ordinary inverse when `A` is singular.

This review establishes identities conditional on the moments supplied. Ordinary
floating-point diagnostics, approximate positive semidefiniteness and retrospective
moment recovery are not interval certificates for another distribution or a
future self-consistent force. No speedup follows without a cheap validated
bound on the residual force quantities.
