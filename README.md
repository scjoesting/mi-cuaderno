# Mi Cuaderno — Spanish 1 study tool

A one-file study app for catching up in Spanish 1.

## How to use it

- **Easiest:** open the live site at **https://scjoesting.github.io/mi-cuaderno/** and add it to your phone or laptop home screen. No account needed.
- **Offline:** double-click `index.html` to open it in a browser with nothing to install.
- **On claude.ai:** the same page is published as an artifact, which also unlocks the **Tutor** tab (ask Claude questions, get explanations for wrong answers).

Your progress is saved in the browser you use, so stick with one browser on one device (or bookmark the claude.ai link and use it everywhere).

## What's inside

| Tab | What it does |
|---|---|
| **Hoy** (Today) | Streak, cards due, and a one-tap daily session that mixes review with new words |
| **Tarjetas** (Flashcards) | 323 words across 11 units. Missed words come back sooner, known words later |
| **Prueba** (Quiz) | 10 multiple-choice questions per unit, including *el* vs *la* |
| **Verbos** (Verb drill) | Two levels she picks: *Build* (tap the right ending from the verb's own table) and *Type* (write the form, with an accent keyboard). Covers regular verbs plus ser, estar, tener, ir, hacer, querer |
| **Conversación** (Hablar on phones) | One short scripted conversation per unit, plus *Preguntas rápidas* (10 questions from every unit). She hears a line, picks the reply that fits, then sees what every reply means and other ways to say it. *Escuchar* mode hides the words until she answers. In Chrome, Edge or Safari, *Decir* mode has her answer out loud instead of picking: any reply that fits counts (with her own name, age or dates swapped in), a wrong reply gets its explanation, and *Show the choices* is there when she's stuck. In the other modes a mic button lets her say the reply after answering. Each conversation has a *Vocabulario* lesson (from the list, mid-conversation, or suggested after a low score): the words, verb forms and partner lines it uses, with audio and a flashcard set, then straight into the conversation. On claude.ai she can also role-play the scene with Claude |
| **Apuntes** (Notes) | Plain-English grammar notes: ser vs estar, gustar, gender, adjectives, questions, numbers, time. Every section has a *Practice this* row that launches a matching drill |
| **Grammar drills** | Ten-question drills on one rule each: which pronoun, ser or estar, gusta or gustan, el or la, adjective agreement, telling time. Reachable from Apuntes or the Prueba tab |
| **Tutor** | Ask Claude anything at a Spanish 1 level, or role-play a conversation in Spanish (claude.ai only) |

Tap the speaker icon on any card to hear it. Every Spanish line is recorded with **Lumina**, a native Colombian ElevenLabs voice, for vocab, quizzes, verbs and both sides of each conversation. Anything without a recording falls back to the device's Spanish voice.

### Solo audio

The **Solo audio** button in the header switches the whole app to listening practice. The Spanish in each question and answer is hidden and spoken aloud instead:

- **Tarjetas:** hear the word, then flip to see its meaning (and spelling).
- **Prueba and grammar drills:** the Spanish question is spoken. Spanish choices become speaker buttons, with *Hear every choice* to play them all.
- **Verbos:** hear the pronoun and verb, then pick the form by ear (Build) or type it (Type).
- **Conversación:** runs in Escuchar mode (or Decir, with the partner's words hidden), and the replies are hidden too.

Stuck? Each hidden part has its own reveal button, so she can uncover just what she needs: **Show the question**, then **Show the choices** (quiz), **Show the forms** (verbs) or **Show the replies** (conversation). Flashcards have one **Show the words**. *What does it mean?* still works in Conversación, and everything is shown once you answer. Notes and Tutor are unchanged. The setting is remembered, and it is unavailable in browsers with no Spanish voice.

## Files

- `artifact.html` — the page source (published to claude.ai)
- `index.html` — the same page wrapped so it opens directly in a browser. This is what GitHub Pages serves.
- `audio/` — the recorded clips. `tools/gen_audio.py` makes them.

## Editing the word lists

Open `artifact.html`, find `const UNITS`, and add rows in the form `['spanish', 'english', 'm' | 'f' | '']`. Add a unit by copying one of the unit blocks. Then rebuild `index.html` by copying the file and adding the `<!DOCTYPE html>` wrapper, or just open `artifact.html` directly (it works too, with a plainer default page setup).

## Recording audio for new lines

After adding words or conversations, rebuild `index.html`, then:

```
python3 tools/gen_audio.py          # shows how many lines are missing audio and the credit cost
python3 tools/gen_audio.py --yes    # records them into audio/
```

Clips are named by a hash of the text, so only new or changed lines are recorded. `--prune` deletes clips nothing uses anymore. The script needs Google Chrome and an ElevenLabs API key (from `ELEVENLABS_API_KEY` or the Keychain item `briefing-elevenlabs`).
