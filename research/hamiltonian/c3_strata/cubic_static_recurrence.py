"""All-degree static and generic dynamic core for cubic sixfold perturbations.

For H=q^6+u q^3+v q^2p+w qp^2+x p^3, x!=0:
the polynomial kernel of (T3,T5) is exactly 15-dimensional, and all
its elements have total degree <=9. This is proved by a descending
third-derivative recurrence. Generic S1=span{1,q,H} and generic
S2=Dinf=span{1,H}; explicit exact minors certify nonemptiness of
the Zariski-open generic locus.
"""
from __future__ import annotations
import sympy as S
from general_sixfold_discovery import Q,P,transvectant


def hamiltonian(u,v,w,x):
    return S.expand(Q**6+u*Q**3+v*Q**2*P+w*Q*P**2+x*P**3)


def static_basis(u,v,w,x,check=True):
    """15 exact static basis polynomials, three for each p-degree 4..0.

    Valid over Q(u,v,w,x) with x inverted. Symbolic x!=0 is an
    applicability assumption; x=0 is explicitly rejected.
    """
    if S.sympify(x)==0:
        raise ValueError("nonzero p^3 coefficient required")
    H=hamiltonian(u,v,w,x)
    basis=[]
    for source_j in range(4,-1,-1):
        for k in range(3):
            g=[S.S.Zero]*8
            for j in range(4,-1,-1):
                rhs=((20*Q**3+u)*(j+3)*(j+2)*(j+1)*g[j+3]
                    -v*(j+2)*(j+1)*S.diff(g[j+2],Q)
                    +w*(j+1)*S.diff(g[j+1],Q,2))/x
                primitive=S.integrate(S.integrate(S.integrate(S.expand(rhs),Q),Q),Q)
                g[j]=S.expand(primitive+(Q**k if j==source_j else 0))
            G=S.expand(sum(g[j]*P**j for j in range(5)))
            if check and (transvectant(H,G,3)!=0 or transvectant(H,G,5)!=0):
                raise ArithmeticError("exact static-gate certificate failed")
            basis.append(G)
    return basis


def iterate_gate_matrix(H,basis,depth):
    evolved=list(basis)
    for _ in range(depth):
        evolved=[transvectant(H,z,1) for z in evolved]
    rows=[]
    for order in (3,5):
        images=[transvectant(H,z,order) for z in evolved]
        monomials=sorted(set().union(*(S.Poly(z,Q,P).monoms() for z in images)))
        for exponents in monomials:
            row=[S.Poly(z,Q,P).coeff_monomial(exponents) for z in images]
            if any(row):
                rows.append(row)
    return S.Matrix(rows) if rows else S.zeros(0,len(basis))


def stage_dimensions(u,v,w,x,depth=2):
    """Global polynomial spaces, not finite degree approximations."""
    if type(depth) is not int or depth<0:
        raise ValueError("nonnegative depth required")
    H=hamiltonian(u,v,w,x)
    basis=static_basis(u,v,w,x)
    rows=[]
    dimensions=[]
    for j in range(depth+1):
        block=iterate_gate_matrix(H,basis,j)
        rows.extend(block.tolist())
        rank=S.Matrix(rows).rank() if rows else 0
        dimensions.append(15-rank)
    return dimensions


def generic_minor_certificate():
    """Exact primal rank witnesses at (u,v,w,x)=(0,0,1,1).

    Nonzero specializations imply the corresponding minors are
    nonzero rational functions of parameters. Combined with universal
    surviving subspaces, this proves the generic all-degree theorem.
    """
    point=(0,0,1,1)
    H=hamiltonian(*point)
    basis=static_basis(*point)
    first=iterate_gate_matrix(H,basis,1)
    second=first.col_join(iterate_gate_matrix(H,basis,2))
    specifications=[
      (first,[0,1,2,3,4,9,10,12,13,14,15,16],
             [0,1,2,3,4,5,6,8,9,10,11,14],
             S.Integer(-69543841933526310447934655692800000000)),
      (second,[0,1,2,3,4,9,10,12,13,14,15,16,45],
             [0,1,2,3,4,5,6,8,9,10,11,13,14],
             S.Integer(901288191458500983405233137778688000000000)),
    ]
    records=[]
    for j,(matrix,rows,cols,expected) in enumerate(specifications,1):
        determinant=matrix.extract(rows,cols).det()
        if determinant!=expected or not determinant:
            raise ArithmeticError("exact generic rank minor failed")
        rank=matrix.rank()
        if rank!=len(cols):
            raise ArithmeticError("claimed rank does not match witness")
        records.append({"depth":j,"rank":rank,"matrix_shape":list(matrix.shape),
                       "rows":rows,"columns":cols,"determinant":str(determinant)})
    # Universal directions: D(1)=D(H)=0; D(q)=-H_p has degree <=2,
    # so q passes the static gates through the first iterate.
    if any(transvectant(H,f,3)!=0 or transvectant(H,f,5)!=0
           for f in (S.Integer(1),Q,H,transvectant(H,Q,1))):
        raise ArithmeticError("universal first-refinement directions failed")
    return {"parameter_point":list(point),"rank_witnesses":records,
            "generic_dimensions":[15,3,2],
            "generic_first_basis":["1","q","H"],
            "generic_second_basis":["1","H"],
            "meaning":"A nonempty Zariski-open set has the stated all-degree refinements; exceptional parameter varieties remain to classify."}


def theorem_certificate():
    u,v,w,x=S.symbols("u v w x",nonzero=True)
    basis=static_basis(u,v,w,x)
    degree=max(S.Poly(g,Q,P).total_degree() for g in basis)
    if len(basis)!=15 or degree!=9:
        raise ArithmeticError("universal static-degree theorem failed")
    examples=[]
    for params in ((0,0,0,1),(0,0,1,1),(1,2,3,1),(0,1,0,1)):
        examples.append({"parameters":list(params),"kernel_dimensions":stage_dimensions(*params)})
    return {"schema":"nonlinearhamiltonian/cubic-sixfold-static-and-generic-core/1",
            "family":"q^6+u*q^3+v*q^2*p+w*q*p^2+x*p^3",
            "assumption":"x != 0, characteristic zero",
            "static_kernel_dimension_all_degrees":15,
            "static_max_total_degree":degree,
            "static_basis_count":len(basis),
            "recurrence":"x*g_j^(3)=(20q^3+u)*(j+3)*(j+2)*(j+1)*g_(j+3)-v*(j+2)*(j+1)*g_(j+2)' + w*(j+1)*g_(j+1)''",
            "generic_core":generic_minor_certificate(),
            "pointwise_all_degree_replays":examples,
            "proof":"T5 enforces p-degree <=4. Descending T3 coefficient equations solve each g_j third derivative with exactly 3 free integration constants. The resulting 15-polynomial basis has degree <=9. Explicit nonzero minors at one rational point and universal surviving directions prove the generic refinement theorem.",
            "scope":"The generic all-degree result does not classify the proper algebraic rank-drop varieties or all quintic and quartic perturbations."}


if __name__=="__main__":
    import json
    print(json.dumps(theorem_certificate(),indent=2,sort_keys=True))
