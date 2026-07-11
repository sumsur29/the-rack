#!/usr/bin/env python3
import json, re, os, sys, urllib.request, ssl
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA={'User-Agent':'Mozilla/5.0','Referer':'https://exercisedb.dev/'}
def get(url, binary=False):
    req=urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, context=ctx, timeout=45) as r:
        return r.read() if binary else r.read().decode('utf-8')
if not os.path.exists('index.html'):
    print("Run this from inside your the-rack repo folder (where index.html lives)."); sys.exit(1)
html=open('index.html','r',encoding='utf-8').read()
m=re.search(r'const DB_RAW=(\[.*?\]);', html, re.S)
if not m: print("Could not find exercise data in index.html."); sys.exit(1)
db=json.loads(m.group(1))
def mid(s):
    f=s.split('/')[-1].rsplit('.',1)[0]; d=f.find('-'); return f[d+1:] if d>=0 else f
ours=[(mid(e['img']), e['n']) for e in db]
print("Reading JahelCuadrado catalogue...")
jc=json.loads(get("https://raw.githubusercontent.com/JahelCuadrado/ExerciseGymGifsDB/v1.1.0/api/en/exercises.json"))['exercises']
def norm(s):
    s=s.lower(); s=re.sub(r'[^a-z0-9 ]',' ',s); s=re.sub(r'\bv\s*\d+\b','',s)
    return ' '.join(sorted(set(s.split())))
jidx={}
for e in jc: jidx.setdefault(norm(e['name']), e)
os.makedirs('gifs', exist_ok=True)
base="https://raw.githubusercontent.com/JahelCuadrado/ExerciseGymGifsDB/v1.1.0/"
ok=miss=0; total=len(ours)
print("Re-mirroring %d gifs (a few minutes)..."%total)
for i,(mediaid,name) in enumerate(ours,1):
    j=jidx.get(norm(name))
    if not j: miss+=1; continue
    try:
        data=get(base+j['id']+".gif", binary=True)
        if data[:4]==b'GIF8' and len(data)>800:
            open("gifs/%s.gif"%mediaid,'wb').write(data); ok+=1; sys.stdout.write('.'); sys.stdout.flush()
        else: miss+=1
    except Exception: miss+=1
    if i%100==0: print(" [%d/%d]"%(i,total))
print()
sz=sum(os.path.getsize('gifs/'+f) for f in os.listdir('gifs'))//(1024*1024)
print("Upgraded: %d   No match (kept as-is): %d   of %d"%(ok,miss,total))
print("gifs/ now has %d files, %d MB"%(len(os.listdir('gifs')), sz))
print("Then: git add gifs && git commit -m 'HQ gif re-mirror' && git push && vercel --prod")
