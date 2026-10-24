"""Replay the conservative rational magnitude bound for removed linear updates."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import re


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model',type=Path,required=True)
    a=p.parse_args()
    data=a.model.read_bytes()
    assert hashlib.sha256(data).hexdigest()=='cbe4cbdc19ddec39e2e999c5337bf7cde93113570fd0639ac1e03007aa8355cb'
    text=data.decode().replace('&\n','')
    magn=[];dr=[]
    for line in text.splitlines():
        if ':'not in line:continue
        name,definition=line.split(':',1)
        if not definition.startswith((' CSBEND',' KQUAD',' EDRIFT')):continue
        values={k:F(v)for k,v in re.findall(r'([A-Z][A-Z0-9_]*)=([+\-0-9.eE]+)',definition)}
        if definition.startswith(' EDRIFT'):
            dr.append(values['L']);continue
        assert abs(values.get('K1',F(0)))<=26
        assert values['L']<=F(46,100)
        if definition.startswith(' CSBEND'):
            assert abs(values['ANGLE']/values['L'])<F(14,100)
            assert abs(values['E1'])<F(1,100)and abs(values['E2'])<F(1,100)
        magn.append(values)
    assert magn and dr and max(dr)<=F(93,20)
    exponent=F(46,100)*(F(1703,1000)+F(4405,1000)*(26+F(14,100)**2))+F(1,100)
    assert exponent<54
    primitive=3**54
    total=2580*4096*2*primitive**2
    assert total<10**60
    print(json.dumps({'status':'passed','norm_exponent_upper':str(exponent),
                      'removed_ct_increment_4096_turns_less_than':'10**60',
                      'scope':'Exact source-field/rational magnitude argument for removed linear maps; no full nonlinear or IEEE proof.'}))


if __name__=='__main__':main()
