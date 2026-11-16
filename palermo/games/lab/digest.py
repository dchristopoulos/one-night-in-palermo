import json, sys, collections
for f in sys.argv[1:]:
    ev=json.load(open(f))
    cast=next(e for e in ev if e['type']=='cast')
    print('##',f,' '.join(f"{p['name']}={p['role']}{'*' if p.get('shown') else ''}" for p in cast['players']))
    n=0; cut=collections.Counter()
    for e in ev:
        t=e['type']
        if t in('say','ghost','note') and e['text'].rstrip().endswith('…'): cut[e['name']]+=1
        if t=='phase': print('--',e.get('text'))
        elif t=='say':
            n+=1
            if e.get('claim') or e.get('why') in('last words','before the game'): print(f"  {e['name']} [{e.get('why','')}{' CLAIM' if e.get('claim') else ''}]: {e['text']}")
        elif t=='votes': print('  VOTES:',', '.join(f"{v[0]}->{v[1]}" for v in e['votes']), '(runoff)' if e.get('runoff') else '')
        elif t=='death': print('  x',e['name'],e.get('how'),e.get('role'))
        elif t=='note': print('  NOTE',e['name'],':',e['text'])
        elif t=='ghost': print('  ghost',e['name'],':',e['text'])
        elif t=='night_action': print('  .',e['name'],e['action'],e.get('target'),e.get('result',''))
        elif t=='gm' and e.get('aside'): print('  (host)',e['text'])
        elif t=='recap': print('  RECAP:',e['text'])
        elif t=='end': print('== winner',e.get('winner'),'t',e.get('t'),'says',n,'cut',dict(cut))
