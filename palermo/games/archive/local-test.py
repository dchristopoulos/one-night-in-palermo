import json, subprocess, sys, time, urllib.request
LMS = __import__("os").path.expanduser("~/.lmstudio/bin/lms")
PROMPT = ("WHAT YOU KNOW: your role is CITIZEN. Players: Sonnet, Haiku, Gemma, Sol, Luna, Terra.\n"
          "WHAT YOU HEAR: Haiku: Terra, you're too quiet.\nYOUR TASK: say one line to the table, under 20 words.\n"
          "Reply exactly:\nMONOLOGUE: <one sentence>\nSAY: <one line>\nNOTE: <importance 1-3>: <fact> or none\nFORGET: none")
def ask(model, think_off):
    body = {"model": model, "max_tokens": 200, "temperature": 0.7,
            "messages": [{"role": "system", "content": "You are a player in a party game of social deduction. Short plain lines." + ("" if think_off else "")},
                         {"role": "user", "content": PROMPT + ("" if think_off else "")}]}
    if think_off:
        body["chat_template_kwargs"] = {"enable_thinking": False}
        body["messages"][1]["content"] += " /no_think"
    t = time.time()
    r = urllib.request.urlopen(urllib.request.Request("http://localhost:1234/v1/chat/completions", data=json.dumps(body).encode(),
                                                      headers={"Content-Type": "application/json"}), timeout=180)
    d = json.load(r); c = d["choices"][0]
    txt = c["message"]["content"].strip().replace("\n", " | ")
    return f"{time.time()-t:5.1f}s finish={c['finish_reason']:6} tokens={d.get('usage',{}).get('completion_tokens')}  {txt[:160]}"
for model in sys.argv[1:]:
    print(f"=== {model}", flush=True)
    t = time.time(); subprocess.run([LMS, "load", model, "--context-length", "8192", "-y"], capture_output=True, timeout=600)
    print(f"load {time.time()-t:.0f}s", flush=True)
    for i in range(3):
        try: print(f"  think off: {ask(model, True)}", flush=True)
        except Exception as e: print("  think off: ERROR", e, flush=True)
    try: print(f"  think on : {ask(model, False)}", flush=True)
    except Exception as e: print("  think on : ERROR", e, flush=True)
    if model != "gemma-4-12b-it-qat":
        subprocess.run([LMS, "unload", model], capture_output=True, timeout=120)
