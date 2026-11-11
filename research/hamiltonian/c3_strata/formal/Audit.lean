import SexticC3
import Lean.Util.CollectAxioms

open Lean Elab Command

elab "audit_axioms " decl:ident : command => do
  let name ← liftCoreM <| Lean.Elab.realizeGlobalConstNoOverloadWithInfo decl
  let axioms ← Lean.collectAxioms name
  let allowed := [``propext, ``Classical.choice, ``Quot.sound]
  let unexpected := axioms.filter fun axiomName => !allowed.contains axiomName
  unless unexpected.isEmpty do
    throwError "{name} depends on unexpected axioms: {unexpected}"
  logInfo m!"{name} depends on axioms: {axioms}"

audit_axioms SexticC3.delta_eq_derivativeMultiplicationDet

audit_axioms SexticC3.Degree6.recorded_identity
audit_axioms SexticC3.Degree6.discriminant_in_selected_span
audit_axioms SexticC3.Degree6.kernel_bound
audit_axioms SexticC3.Degree6.lift1_eq_hCoeff
audit_axioms SexticC3.Degree6.hamiltonian_kernel

audit_axioms SexticC3.Degree1.recorded_identity
audit_axioms SexticC3.Degree1.discriminant_in_selected_span
audit_axioms SexticC3.Degree1.kernel_bound

audit_axioms SexticC3.Degree2.recorded_identity
audit_axioms SexticC3.Degree2.discriminant_in_selected_span
audit_axioms SexticC3.Degree2.kernel_bound

audit_axioms SexticC3.Degree3.recorded_identity
audit_axioms SexticC3.Degree3.discriminant_in_selected_span
audit_axioms SexticC3.Degree3.kernel_bound

audit_axioms SexticC3.Degree4.recorded_identity
audit_axioms SexticC3.Degree4.discriminant_in_selected_span
audit_axioms SexticC3.Degree4.kernel_bound

audit_axioms SexticC3.Degree5.recorded_identity
audit_axioms SexticC3.Degree5.discriminant_in_selected_span
audit_axioms SexticC3.Degree5.kernel_bound

audit_axioms SexticC3.Degree7.recorded_identity
audit_axioms SexticC3.Degree7.discriminant_in_selected_span
audit_axioms SexticC3.Degree7.kernel_bound

audit_axioms SexticC3.Degree8.recorded_identity
audit_axioms SexticC3.Degree8.discriminant_in_selected_span
audit_axioms SexticC3.Degree8.kernel_bound

audit_axioms SexticC3.Degree9.recorded_identity
audit_axioms SexticC3.Degree9.discriminant_in_selected_span
audit_axioms SexticC3.Degree9.kernel_bound

audit_axioms SexticC3.Degree10.recorded_identity
audit_axioms SexticC3.Degree10.discriminant_in_selected_span
audit_axioms SexticC3.Degree10.kernel_bound

audit_axioms SexticC3.Degree11.recorded_identity
audit_axioms SexticC3.Degree11.discriminant_in_selected_span
audit_axioms SexticC3.Degree11.kernel_bound

audit_axioms SexticC3.Degree12.recorded_identity
audit_axioms SexticC3.Degree12.discriminant_in_selected_span
audit_axioms SexticC3.Degree12.kernel_bound

audit_axioms SexticC3.Degree13.recorded_identity
audit_axioms SexticC3.Degree13.discriminant_in_selected_span
audit_axioms SexticC3.Degree13.kernel_bound

audit_axioms SexticC3.Degree14.recorded_identity
audit_axioms SexticC3.Degree14.discriminant_in_selected_span
audit_axioms SexticC3.Degree14.kernel_bound

audit_axioms SexticC3.Degree15.recorded_identity
audit_axioms SexticC3.Degree15.discriminant_in_selected_span
audit_axioms SexticC3.Degree15.kernel_bound

audit_axioms SexticC3.Degree16.recorded_identity
audit_axioms SexticC3.Degree16.discriminant_in_selected_span
audit_axioms SexticC3.Degree16.kernel_bound

audit_axioms SexticC3.finite_kernel_bound

audit_axioms SexticC3.Exceptional411.first_iterate
audit_axioms SexticC3.Exceptional411.second_iterate
audit_axioms SexticC3.Exceptional411.static_gates
audit_axioms SexticC3.Exceptional411.second_obstruction
audit_axioms SexticC3.Exceptional411.second_obstruction_nonzero

audit_axioms SexticC3.StaticTail.intCast_falling
audit_axioms SexticC3.StaticTail.weight_three
audit_axioms SexticC3.StaticTail.weight_five
audit_axioms SexticC3.StaticTail.static_pivot
audit_axioms SexticC3.StaticTail.rowValue_static
audit_axioms SexticC3.StaticTail.rowValue_top_split
audit_axioms SexticC3.StaticTail.kernel_zero_of_edge_zero
audit_axioms SexticC3.StaticTail.certificate_pivot
audit_axioms SexticC3.StaticTail.certificate_top_equation
audit_axioms SexticC3.StaticTail.reconstruct_eq
audit_axioms SexticC3.StaticTail.reconstructed_fifth_rows
audit_axioms SexticC3.StaticTail.target_factorization
audit_axioms SexticC3.StaticTail.delta_zero_of_targets
audit_axioms SexticC3.StaticTail.pDerivative_monomial
