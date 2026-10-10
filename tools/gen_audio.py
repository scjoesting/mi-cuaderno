#!/usr/bin/env python3
"""Record every Spanish line in Mi Cuaderno with ElevenLabs voices, into audio/<hash>.mp3.

    python3 tools/gen_audio.py            show what is missing and what it would cost
    python3 tools/gen_audio.py --yes      record the missing clips
    python3 tools/gen_audio.py --prune    also delete clips no line uses any more

The line list comes from the app itself: headless Chrome opens index.html#spoken-lines,
which prints spokenLines() (vocab, drills, verb forms, conversations, grammar notes).
Clip names are an FNV-1a hash of the spoken text, the same as clipName() in the page,
so only new or changed lines cost credits. audio/voices.json records which voice made
each clip, so changing VOICES re-records just the lines whose voice changed. Rebuild index.html before running this.

API key: $ELEVENLABS_API_KEY, or the macOS Keychain item "briefing-elevenlabs".
Python 3.9 built-ins only.
"""
import concurrent.futures
import html
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO = os.path.join(ROOT, "audio")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
API = "https://api.elevenlabs.io/v1"
MODEL = "eleven_multilingual_v2"
FORMAT = "mp3_44100_64"
SPEED = 0.9  # a touch slower than natural, for a Spanish 1 ear
LUMINA = "x5IDPSl4ZUbhosMmVFTk"  # Lumina - Neutral and Clear (Colombian)
ALEJO = "SsO7anq9lnFq4QW8bfch"   # Alejo - Colombian Costeño (partner voice until 2026-10-10)
VOICES = {
    "main": LUMINA,     # vocab, quizzes, verbs, the learner's replies
    "partner": LUMINA,  # conversation partners; set to another voice id to give them their own
}
MANIFEST = "voices.json"  # audio/voices.json: clip file -> voice id it was recorded with
KEYCHAIN = "briefing-elevenlabs"


def fnv1a(text):
    h = 0x811C9DC5
    for b in text.encode("utf-8"):
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return "%08x" % h


def speech_text(t):
    t = unicodedata.normalize("NFC", t)
    t = re.sub(r"\s*\(.*?\)\s*", " ", t).replace("…", "")
    return re.sub(r"\s+", " ", t).strip()


def api_key():
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if key:
        return key
    try:
        return subprocess.run(["security", "find-generic-password", "-s", KEYCHAIN, "-w"],
                              check=True, capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        sys.exit("No ElevenLabs key. Set ELEVENLABS_API_KEY or add Keychain item %r." % KEYCHAIN)


def request(method, path, key, body=None, tries=5):
    data = json.dumps(body).encode() if body is not None else None
    headers = {"xi-api-key": key, "Accept": "*/*"}
    if data:
        headers["Content-Type"] = "application/json"
    delay = 2.0
    for attempt in range(tries):
        try:
            req = urllib.request.Request(API + path, data=data, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:300]
            if (e.code == 429 or e.code >= 500) and attempt < tries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError("HTTP %d: %s" % (e.code, detail))
        except urllib.error.URLError as e:
            if attempt < tries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError("network: %s" % e.reason)


def read_lines():
    url = "file://" + os.path.join(ROOT, "index.html") + "#spoken-lines"
    out = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=5000", "--dump-dom", url],
                         capture_output=True, text=True, timeout=120).stdout
    m = re.search(r'<pre id="spoken-lines">(.*?)</pre>', out, re.S)
    if not m:
        sys.exit("Could not read the line list from index.html. Is index.html rebuilt from artifact.html?")
    lines = json.loads(html.unescape(m.group(1)))
    for ln in lines:  # the page and this script must agree on names
        if speech_text(ln["text"]) != ln["text"] or fnv1a(ln["text"]) + ".mp3" != ln["file"]:
            sys.exit("Hash mismatch between page and script for %r" % ln["text"])
    return lines


def save_manifest(path, made):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(made.items())), f, indent=0)


def main():
    args = set(sys.argv[1:])
    os.makedirs(AUDIO, exist_ok=True)
    lines = read_lines()
    have = {f for f in os.listdir(AUDIO) if f.endswith(".mp3")}
    mpath = os.path.join(AUDIO, MANIFEST)
    try:
        with open(mpath, encoding="utf-8") as f:
            made = json.load(f)
    except (OSError, ValueError):  # clips from before the manifest: main lines Lumina, partner lines Alejo
        made = {ln["file"]: (ALEJO if ln["voice"] == "partner" else LUMINA) for ln in lines if ln["file"] in have}
        save_manifest(mpath, made)
    todo = [ln for ln in lines if ln["file"] not in have or made.get(ln["file"]) != VOICES[ln["voice"]]]
    chars = sum(len(ln["text"]) for ln in todo)
    stale = have - {ln["file"] for ln in lines}
    print("%d lines · %d recorded · %d to record (%s characters ≈ credits) · %d unused clips"
          % (len(lines), len(lines) - len(todo), len(todo), format(chars, ","), len(stale)))
    if "--prune" in args:
        for f in stale:
            os.remove(os.path.join(AUDIO, f))
            made.pop(f, None)
        save_manifest(mpath, made)
        print("removed %d unused clips" % len(stale))
    if not todo:
        return
    key = api_key()
    sub = json.loads(request("GET", "/user/subscription", key))
    left = int(sub.get("character_limit", 0)) - int(sub.get("character_count", 0))
    print("credits remaining: %s" % format(left, ","))
    if chars > left:
        sys.exit("Not enough credits.")
    if "--yes" not in args:
        print("Run again with --yes to record them.")
        return

    def record(ln):
        body = {"text": ln["text"], "model_id": MODEL, "voice_settings": {"speed": SPEED}}
        audio = request("POST", "/text-to-speech/%s?output_format=%s" % (VOICES[ln["voice"]], FORMAT), key, body)
        path = os.path.join(AUDIO, ln["file"])
        with open(path + ".part", "wb") as f:
            f.write(audio)
        os.replace(path + ".part", path)
        made[ln["file"]] = VOICES[ln["voice"]]

    done = failed = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futs = {pool.submit(record, ln): ln for ln in todo}
        for fut in concurrent.futures.as_completed(futs):
            try:
                fut.result()
                done += 1
            except Exception as e:  # keep going; a re-run picks up whatever failed
                failed += 1
                print("failed: %r: %s" % (futs[fut]["text"], e))
            if (done + failed) % 100 == 0:
                print("  %d / %d" % (done + failed, len(todo)))
    save_manifest(mpath, made)
    print("recorded %d clips%s" % (done, ", %d failed (run again to retry)" % failed if failed else ""))


if __name__ == "__main__":
    main()
