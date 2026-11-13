import SexticC3.WeightedCubicForm
import Lean.Util.CollectAxioms

open Lean Elab Command in
elab "audit_axioms " n:ident : command => do
  let c ← liftCoreM <| realizeGlobalConstNoOverloadWithInfo n
  let ax ← Lean.collectAxioms c
  logInfo m!"{c} depends on axioms: {ax.toList}"

audit_axioms WeightedCubicForm.row_four
audit_axioms WeightedCubicForm.row_five
audit_axioms WeightedCubicForm.cube_of_brackets
audit_axioms WeightedCubicForm.tail_collapse
