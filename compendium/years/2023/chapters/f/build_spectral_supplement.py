from pathlib import Path
import json
P=Path(__file__).resolve().parent
entry={
 'id':'S013',
 'title':'An exact exceptional point and its two-sheeted spectral cover',
 'status':'Finite parameter-family classification and exact Jordan/projector certificates; no novelty claim',
 'summary':'The three-site sl₂ Gaudin family has an explicit exceptional locus where two highest-weight eigenlines coalesce. At that locus a genuine Jordan block replaces the two eigenvectors. Nearby spectral projectors diverge although their sum stays constant. Analytic continuation of the eigenvalue labels exchanges the two lines. This is spectral-cover monodromy in a parameter, not monodromy of a KZ connection or of the scalar differential equation in its spatial variable.',
 'definitions':[
  'Use the one-magnon sector and normalization of S010, with sites z=(0,1,t), t≠0,1. Put p_t(x)=x(x−1)(x−t), D(t)=t²−t+1 and w±=(1+t±sqrt(D))/3.',
  'For D≠0, let v± have components 1/(w±−z_j), and E_i±=E_i⁰+1/(w±−z_i). The uniform vector is u=(1,1,1)ᵀ and the highest-weight projection is Q=I−uuᵀ/3.',
  'Transpose is the complex bilinear transpose, not the Hermitian adjoint. For complex t the resulting spectral projectors need not be orthogonal for the standard Hermitian norm. Their divergence is compatible with Q remaining bounded.'
 ],
 'result':{
  'name':'Jordan degeneration, projector cancellation and spectral-label exchange',
  'statement':'The only critical-root collisions in this family occur at t₀=(1±i√3)/2, the simple zeros of D. At t=t₀, w₀=(1+t₀)/3 and v₀=v(w₀) satisfy (H_i−E_i)v₀=0 and (H_i−E_i)v′₀=−a_i²v₀, where a_i=1/(w₀−z_i). Thus each H_i has a size-two Jordan block on im Q. For D≠0, P±=∓p_t(w±)v±v±ᵀ/(2sqrt(D)), and P++P−=Q exactly. As t approaches t₀ on either local sheet, sqrt(D)P+→−p_(t₀)(w₀)v₀v₀ᵀ/2 and sqrt(D)P− has the opposite limit. A loop encircling just one zero of D exchanges P+ and P−.',
  'proof':'Differentiating p_t gives p′=3x²−2(1+t)x+t, so the critical roots have the displayed quadratic formula. Its discriminant vanishes precisely at the two stated sites, and D′(t₀)=2t₀−1≠0. At the collision B=p′/p and B′ both vanish at w₀, while p(w₀)≠0 because the physical sites are still distinct. The off-shell identity from S010 is H_i v(w)=E_i(w)v(w)−a_i(w)B(w)e_i. Differentiating in w at fixed t₀ eliminates both residual terms and gives the generalized-eigenvector relation, with E_i′=−a_i²≠0. If v′ were proportional to v, all a_j would have to be equal, contrary to distinct sites. Both vectors have coordinate sum zero; with u they span the full sector. Therefore the block is genuinely Jordan, not a repeated diagonal eigenvalue.\n\nAt a simple critical root the bilinear square is v(w)ᵀv(w)=−p″(w)/p(w). Since p″(w±)=±2sqrt(D), the projector formula follows. The eigenvectors u,v+,v− form a bilinear-orthogonal basis when D≠0, so their projectors sum to I and P++P−=Q. The numerator of P+ tends to a nonzero rank-one matrix, giving divergence proportional to |D|^(−1/2) in any fixed finite-dimensional matrix norm. With ε=sqrt(D), one has t−t₀=O(ε²), w±=w₀±ε/3+O(ε²), and p_t(w±)=p_(t₀)(w₀)+O(ε²). Thus P±=∓p₀v₀v₀ᵀ/(2ε)−p₀(v′₀v₀ᵀ+v₀v′₀ᵀ)/6+O(ε). The divergent terms cancel. In fact Q=−p₀(v′₀v₀ᵀ+v₀v′₀ᵀ)/3 at the exceptional point. The finite surviving nilpotent is N_i=(H_i−E_i)Q=(p₀a_i²/3)v₀v₀ᵀ. It is nonzero and N_i²=0 because v₀ᵀv₀=0.\n\nFinally D=(t−t₀)(t−t₁). A sufficiently small loop around t₀ winds D once around zero because t₁ lies outside. Analytic continuation of sqrt(D) therefore changes sign, exchanging the two roots, eigenvalues and projectors. This proof concerns the two-sheeted algebraic spectral cover; it introduces no connection or parallel-transport operator.'
 },
 'example':{
  'setup':'Perform the exceptional calculation exactly in K=Q(τ), τ²−τ+1=0, taking t₀=τ and w₀=(1+τ)/3.',
  'calculation':'The supplemental verifier constructs all three 3×3 Hamiltonians over K. It checks their commutators, the eigenvector and generalized-eigenvector identities, rank(u,v₀,v′₀)=3, the constant-projector formula and N_i=(p₀a_i²/3)v₀v₀ᵀ with N_i≠0 and N_i²=0. These are exact algebraic calculations, independent of numerical eigenvalue separation. Additional complex-number evaluations approach the exceptional point along D=ε² and check the leading projector coefficient and cancellation. A separately tracked square root around a small parameter loop exchanges the two labels, agreeing with the analytic winding argument.',
  'conclusion':'This closes the finite three-site exceptional-point question: location, Jordan structure, projector blowup, cancellation and label exchange are explicit. The exact field certificate carries the algebraic result; numerical paths illustrate its limiting and continuation behavior.'
 },
 'limits':'For real distinct sites, D=(t−1/2)²+3/4 is positive and cannot reach this exceptional locus; the real-site orthogonal projectors therefore do not develop this singularity. The result does not classify every higher-site exceptional locus. Spectral-cover label exchange, spatial scalar-ODE monodromy and KZ connection monodromy are three different constructions and must not be identified.',
 'extension':'S014 completes the distinct-site one-magnon answer: each multiplicity-m root of p′ gives exactly one size-m Jordan block, and the commuting spectral algebra retains its nilpotent direction. Further work should address multi-magnon sectors or collisions of the physical sites, where the present hypotheses and one-coordinate construction do not apply unchanged.',
 'links':['S010','M104','M105','M042','S014'],
 'references':[{'label':'Frenkel Gaudin model and opers for the general framework','url':'https://arxiv.org/abs/math/0407524'}]
}
entry['word_count']=len(' '.join([entry['summary'],*entry['definitions'],*entry['result'].values(),*entry['example'].values(),entry['limits'],entry['extension']]).split())
P.joinpath('spectral_supplemental.json').write_text(json.dumps([entry],ensure_ascii=False,indent=2))
print(json.dumps({'id':'S013','words':entry['word_count']}))
