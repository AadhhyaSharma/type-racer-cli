#!/usr/bin/env python3
"""type-racer-cli — terminal typing speed game."""
import time, json, os, sys, argparse, random

PROMPTS = [
    "the quick brown fox jumps over the lazy dog",
    "code is like poetry written for machines to execute and humans to understand",
    "every great developer you know got there by solving problems they were unqualified to solve",
    "the best way to predict the future is to invent it yourself with your own two hands",
    "simplicity is the ultimate sophistication and that is why python feels so natural",
]

SCORES_FILE = "scores.json"

def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE) as f: return json.load(f)
    return []

def save_score(wpm, acc):
    scores = load_scores()
    scores.append({"wpm": wpm, "accuracy": acc, "time": time.strftime("%Y-%m-%d %H:%M")})
    scores.sort(key=lambda x: -x["wpm"])
    with open(SCORES_FILE, "w") as f: json.dump(scores[:20], f, indent=2)

def show_scores():
    scores = load_scores()
    if not scores: print("No scores yet. Go type something!"); return
    print("\n🏆 Your Top Scores\n" + "─"*35)
    for i, s in enumerate(scores[:10], 1):
        print(f"  {i:2}. {s['wpm']:3} WPM  {s['accuracy']:5.1f}%  {s['time']}")
    print()

def race(prompt):
    print(f"\n📝 Prompt:\n   {prompt}\n")
    print("Press ENTER when ready...", end=""); input()
    print("\nGO!\n   ", end="", flush=True)
    start = time.time()
    try:
        typed = input()
    except KeyboardInterrupt:
        print("\nAborted."); return
    elapsed = time.time() - start
    words = len(prompt.split())
    wpm = int((words / elapsed) * 60)
    correct = sum(a==b for a,b in zip(typed, prompt))
    acc = (correct / max(len(prompt),1)) * 100
    print(f"\n  ⚡ {wpm} WPM  |  🎯 {acc:.1f}% accuracy  |  ⏱ {elapsed:.2f}s")
    save_score(wpm, acc)
    scores = load_scores()
    if scores and scores[0]["wpm"] == wpm:
        print("  🏆 New personal best!")
    print()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--hard",   action="store_true")
    p.add_argument("--scores", action="store_true")
    p.add_argument("--reset",  action="store_true")
    a = p.parse_args()
    if a.scores: show_scores(); return
    if a.reset:
        if os.path.exists(SCORES_FILE): os.remove(SCORES_FILE)
        print("Scores cleared."); return
    prompt = random.choice(PROMPTS)
    if a.hard: prompt = prompt + " " + random.choice(PROMPTS)
    race(prompt)

if __name__ == "__main__":
    main()
