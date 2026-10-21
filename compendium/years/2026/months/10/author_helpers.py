import json,re
from pathlib import Path
P=Path(__file__).resolve().parent
def source_blocks():
    out=[]
    for fn in sorted(P.glob("root_*.json")):
        data=json.loads(fn.read_text())
        records=data if isinstance(data,list) else [data]
        for ri,r in enumerate(records):
            raw=r.get("result",r)
            messages=raw.get("structuredContent",{}).get("messages",[])
            for mi,m in enumerate(messages):
                for block in re.split(r"(?m)(?=^- \[)",m.get("content","")):
                    if block.startswith("- ["):
                        out.append({"file":fn.name,"record":ri,"message":mi,"text":block.split("\n\n",1)[0].strip()})
    return out
def make_entry(n,title,source,date,evidence,field,question,summary,definitions,name,statement,proof,setup,calculation,conclusion,limits,extension,references,status="Classical mathematics or a newly chosen finite model developed with proof; historical claims delimited"):
    return {"id":f"Y26-10-{n:03d}","title":title,"status":status,"summary":summary,"definitions":definitions,"result":{"name":name,"statement":statement,"proof":proof},"example":{"setup":setup,"calculation":calculation,"conclusion":conclusion},"limits":limits,"extension":extension,"references":[{"label":a,"url":b} for a,b in references],"original":{"date":date,"month":"2026-10","evidence":evidence,"field":field,"concept":title,"origin":"Dated recovered conversation evidence" if evidence!="T" else "Retrieved file passage carrying a historical date","question":question,"math":statement,"finish":"Definitions, proved proposition, worked example, limitations and extension","kind":"Revised mathematical development","refs":[b for a,b in references],"source_excerpt":source["text"],"retrieval_receipt":f'{source["file"]} record {source["record"]}',"original_question":None,"attribution_note":"The retrieved source passage and its author attribution are preserved. The revised question, proof and worked example are newly authored. Historical assistant claims, including claimed Lean or repository verification, are not treated as independently replayed certificates unless a specific executed certificate is expressly identified."}}
