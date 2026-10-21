'use strict';const A=require('./engine.js');const assert=require('assert');let checks=0;function ok(x,msg){assert(x,msg);checks++}
for(let mask=0;mask<64;mask++){let r=A.L01({mask});ok(r.identifies===(r.joinedRank===r.rank),'rank criterion');ok(r.bestCost===4,'minimum sum panel');let s=A.L01({mask,target:'pair'});ok(s.bestCost===6,'minimum pair panel')}
for(let budget=0;budget<=27;budget++){let r=A.L02({budget});ok(r.selected.weight<=budget,'feasible unrank');if(budget===27)ok(r.feasibleCount===64,'full mask count')}
let g=A.L03({total:3,q:0.5});ok(g.binaryCensusEqual,'binary collision');ok(g.configurations===84,'weak compositions');ok(Math.abs(g.value-11025/262144)<1e-14,'exact polynomial value');for(let R=0;R<=6;R++)ok(A.L03({total:R}).binaryCensusEqual,'independent binary census');
for(let mode of ['mild','severe'])for(let r of [.5,1,2,3])for(let L of [4,8,14]){let z=A.L04({mode,r,L});ok(z.selected.total>=z.selected.bias&&z.selected.total>=z.selected.noise,'bound decomposition')}
for(let a=-3;a<=3;a++)for(let b=-3;b<=3;b++)ok(A.L05({a,b}).determinant===1,'unit determinant');for(let angle=5;angle<=85;angle+=5){let z=A.L05({mode:'projection',angle});ok(z.residualBound<=.01+1e-14,'projection iteration count')}
let m=A.L06({a:3,b:0,c:0,d:3});ok(m.terms[0].coefficient==='9'&&m.terms[1].coefficient==='-3/2','cubic Moyal convention');let w=A.L06();ok(w.thirdOrderZero&&!w.exact&&w.terms[1].coefficient==='105','fifth order obstruction');for(let r=0;r<=5;r++)ok(A.L06({a:1,b:3,c:3*r+2,d:r}).exact,'exact qp3 family');
for(let modulus of [6,8,10,12,15,24,30,40,48,60,120]){let z=A.L07({modulus});ok(z.uniform&&z.targetUnits*z.fibreSize===384,'uniform fibres')}ok(A.L07().fibreSize===48,'phase48');
for(let common=0;common<=30;common++){let z=A.L08({common,lo:1,hi:2});ok(z.AAlwaysLarger&&z.difference[0]===1,'joint uncertainty cancellation')}
ok(A.L09().beta1===1,'cycle');ok(A.L09({filled:true}).beta1===0,'filled cycle');ok(A.L09({mode:'k33'}).beta1===4,'K33 cycle rank');
for(let seed of ['1,2','5,4'])for(let n=-20;n<=20;n++)ok(A.L10({seed,n}).norm==='-7','Pell norm');
console.log(JSON.stringify({status:'passed',checks}));
