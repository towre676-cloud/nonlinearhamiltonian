"""Optional fused guard+map; same matrices/domain as the standard compiler.

Only use after the local FixedDeltaBlockPass build. No upstream kernel replaced.
"""
import copy
import time
import numpy as np
import at
from compiler import compile_ring as standard_compile
from compiler import track_with_fallback


def compile_ring(ring,dp=0.,sext_steps=None,guards=True):
    if not guards:raise ValueError('fused pass requires guarded semantics')
    start=time.perf_counter()
    standard,receipt=standard_compile(ring,dp,sext_steps,guards=True)
    out=[];mapping=[];guards_new=[];blocks=iter(receipt['blocks'])
    i=0
    while i<len(standard):
        if standard[i].FamName=='LinearGuardQ':
            block=next(blocks);m=np.asarray(block['matrix'])
            native_last=receipt['native_index_map'][i+4]
            e=at.Element('FusedGuardedLinearBlock',PassMethod='FixedDeltaBlockPass',
                         Length=standard[i+4].Length,A4=np.asfortranarray(m[:4,:4]),
                         B4=np.array(m[:4,4]),Radius4=np.array(block['input_radius']),FixedDelta=float(dp))
            guards_new.append(len(out));out.append(e);mapping.append(native_last);i+=5
        else:
            out.append(standard[i].deepcopy());mapping.append(receipt['native_index_map'][i]);i+=1
    result=at.Lattice(out,**vars(ring))
    receipt=copy.deepcopy(receipt)
    receipt.update(guard_indices=guards_new,native_index_map=mapping,compiled_elements=len(result),
                   construction_seconds=time.perf_counter()-start,variant='fused_guard_matrix_c')
    return result,receipt
