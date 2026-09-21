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
| **Apuntes** (Notes) | Plain-English grammar notes: ser vs estar, gustar, gender, adjectives, questions, numbers, time. Every section has a *Practice this* row that launches a matching drill |
| **Grammar drills** | Ten-question drills on one rule each: which pronoun, ser or estar, gusta or gustan, el or la, adjective agreement, telling time. Reachable from Apuntes or the Prueba tab |
| **Tutor** | Ask Claude anything at a Spanish 1 level (claude.ai only) |

Tap the speaker icon on any card to hear it pronounced with your device's Spanish voice.

## Files

- `artifact.html` — the page source (published to claude.ai)
- `index.html` — the same page wrapped so it opens directly in a browser. This is what GitHub Pages serves.

## Editing the word lists

Open `artifact.html`, find `const UNITS`, and add rows in the form `['spanish', 'english', 'm' | 'f' | '']`. Add a unit by copying one of the unit blocks. Then rebuild `index.html` by copying the file and adding the `<!DOCTYPE html>` wrapper, or just open `artifact.html` directly (it works too, with a plainer default page setup).
