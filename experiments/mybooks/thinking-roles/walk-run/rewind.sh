#!/bin/sh
# t-2006: bring the story copy back to "S6 manual half of the 23 cards" from the backup taken before the walk.
P=C:/AI/Factory/exp-thinking-roles/pkg-walk/ai-packages/qa-factory/scripts; C=C:/AI/Factory/mybooks-stand/tr-walk; T=$C/qa-factory/artifacts/LOCAL-1; R=C:/AI/Factory/yml-text-factory/experiments/mybooks/thinking-roles/walk-run
export CLAUDE_PROJECT_DIR=$C
K=$(date +%H%M%S); [ -d $T/state ] && mv $T/state $T/state.rewound-$K; cp -r $C/_before-walk-state $T/state; mv $T/state/driver-question.md $T/state/driver-question.before-walk.md 2>/dev/null
python -B $R/clean_driver_state.py --task-root $T | tail -1 | cut -c1-100
python -B - "$T" <<'PY'
import json,sys
p=sys.argv[1]+'/pipeline.json'; d=json.load(open(p,encoding='utf-8')); s=d['stages']['S6']
for k in ('code_only','receipt_id','finished','reason','digest'): s.pop(k,None)
s['status']='pending'; json.dump(d,open(p,'w',encoding='utf-8',newline=''),ensure_ascii=False,indent=2)
PY
A=""; for f in $C/test-cases/walk/*.md; do A="$A --case-file $f"; done
python -B $P/case_versions.py --task-root $T $A | tail -1 | cut -c1-60
python -B - "$T" "$R" "$C" invalidate <<'PY'
import json,sys
T,R,C,_=sys.argv[1:]; c=json.load(open(T+'/state/controller.json',encoding='utf-8'))
iv=json.load(open(R+'/invalidate.json',encoding='utf-8')); iv['expected_revision']=c['revision']; json.dump(iv,open(R+'/invalidate.json','w',encoding='utf-8'))
PY
python -B $P/controller.py --task-root $T --operation invalidate --input $R/invalidate.json | tail -1 | cut -c1-60
python -B - "$T" "$R" "$C" <<'PY'
import json,sys,hashlib,glob,os
T,R,C=sys.argv[1:]; c=json.load(open(T+'/state/controller.json',encoding='utf-8')); h=hashlib.sha256(open(T+'/work/test-plan.json','rb').read()).hexdigest()
ids=sorted(os.path.basename(f)[:-3] for f in glob.glob(C+'/test-cases/walk/*.md'))
json.dump({'idempotency_key':'t2006-revise-r','expected_revision':c['revision'],'scope':ids,'plan_revision':'sha256:'+h,'reason':'t-2006 live proof: the 23 cards'},open(R+'/revise.json','w',encoding='utf-8'))
PY
python -B $P/controller.py --task-root $T --operation revise_plan --input $R/revise.json | tail -1 | cut -c1-60
python -B $P/controller.py --task-root $T --operation gate-decision --gate A --words-file $R/gate-a.txt --no-answers | tail -1 | cut -c1-120
python -B $R/check_prep.py --task-root $T --stage ready --package-scripts $P | tail -1
