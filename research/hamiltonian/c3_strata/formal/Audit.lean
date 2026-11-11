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
