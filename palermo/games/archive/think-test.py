import json, subprocess, sys, time, urllib.request
LMS = __import__("os").path.expanduser("~/.lmstudio/bin/lms")
U = ("WHAT YOU KNOW: your role is CITIZEN. Players: Sonnet, Haiku, Gemma, Sol, Luna, Terra.\nWHAT YOU HEAR: Haiku: Terra, you're too quiet.\n"
     "YOUR TASK: say one line to the table, under 20 words.\nReply exactly:\nMONOLOGUE: <one sentence>\nSAY: <one line>\nNOTE: none\nFORGET: none")
S = "You are a player in a party game of social deduction. Short plain lines."
VARIANTS = {
    "plain, 1500 tokens": {},
    "chat_template_kwargs enable_thinking=false": {"chat_template_kwargs": {"enable_thinking": False}},
    "reasoning_effort=none": {"reasoning_effort": "none"},
    "reasoning: {effort: none}": {"reasoning": {"effort": "none"}},
    "assistant prefill <think></think>": {"prefill": True},
    "system: /no_think + thinking off": {"sys_suffix": " /no_think Do not think, answer directly. thinking: off"},
}
def ask(model, v):
    msgs = [{"role": "system", "content": S + v.get("sys_suffix", "")}, {"role": "user", "content": U}]
    if v.get("prefill"):
        msgs.append({"role": "assistant", "content": "<think>\n\n</think>\n\n"})
    body = {"model": model, "max_tokens": 1500, "temperature": 0.7, "messages": msgs}
    body.update({k: x for k, x in v.items() if k not in ("prefill", "sys_suffix")})
    t = time.time()
    try:
        r = urllib.request.urlopen(urllib.request.Request("http://localhost:1234/v1/chat/completions", data=json.dumps(body).encode(),
                                                          headers={"Content-Type": "application/json"}), timeout=240)
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code} {e.read()[:150]!r}"
    d = json.load(r); m = d["choices"][0]["message"]
    extra = {k: (len(x) if isinstance(x, str) else x) for k, x in m.items() if k not in ("role", "content")}
    return (f"{time.time()-t:5.1f}s finish={d['choices'][0]['finish_reason']:6} tokens={d.get('usage',{}).get('completion_tokens')} "
            f"content={len(m.get('content') or '')}ch other={extra} | {(m.get('content') or '').strip()[:110].replace(chr(10),' | ')}")
for model in sys.argv[1:]:
    print(f"=== {model}", flush=True)
    subprocess.run([LMS, "load", model, "--context-length", "8192", "-y"], capture_output=True, timeout=600)
    for name, v in VARIANTS.items():
        print(f"  {name:44} {ask(model, v)}", flush=True)
    subprocess.run([LMS, "unload", model], capture_output=True, timeout=120)
