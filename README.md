# CTRL+ALTF4EVER

*too many windows. not enough patience. somehow, it's getting worse.*

Ever wanted to spend your free time dealing with suspicious popup windows? Well, now you can make questionable decisions while doing exactly that.

**CTRL+ALTF4EVER** is a tiny desktop chaos simulator made with Python and Pygame. Random windows keep appearing on your desktop, and not all of them are what they seem. Some are harmless notifications. Others are suspicious messages pretending to be something important.

Your job? Figure out which is which, click the right button, and try not to absolutely destroy your score.

It's got fake errors, questionable offers, legitimate notifications, misleading warnings, achievements, and a desktop that is definitely not passing its security audit.

## A little about the project

This is my **first ever Pygame project**!

I'm still learning Python game development, so this is basically my playground for experimenting with game mechanics, UI, animations, random events, and whatever else I feel like adding.

I've broken things, fixed things, broken them again, and occasionally celebrated when the code worked without me understanding why.

It's not perfect. It's not supposed to be. It's a work in progress, and I'm building it one update at a time.

## What's new in v3.0?

The popups have officially stopped being random boxes with random messages. Now they actually have personalities. Unfortunately.

- **GOOD and BAD popups:** Not every window is suspicious. Some are perfectly normal notifications, while others are definitely up to something.
- **Two-button decisions:** Every popup comes with an `X` button and an `OK` button. Choose wisely.
- **Consequences:** Clicking the wrong button affects your score. Closing a window doesn't automatically mean you made the right decision.
- **More popup variety:** Different types of windows, messages, and situations keep things unpredictable.
- **Updated scoring:** Good decisions earn points, while bad decisions can cost you.
- **More desktop chaos:** Random popups keep appearing, so there's always something demanding your attention.

Basically, the game has gone from *close everything* to *maybe read before clicking*.

## What's in the game?

- A boot screen to start your questionable desktop experience.
- Random popup windows with different messages and appearances.
- GOOD popups containing legitimate notifications.
- BAD popups containing suspicious messages and questionable requests.
- Separate `X` and `OK` buttons with different outcomes.
- A score system that rewards good decisions and punishes bad ones.
- Increasing popup spawn speed as the game progresses.
- Unlockable score-based achievements.
- Random reactions and developer-themed messages.
- A dark, terminal-inspired desktop aesthetic.

## How to play

Welcome to your desktop. It's a mess already. Let's make it worse.

1. **Start the game:** Launch the game and click `LETS GOO` on the boot screen.
2. **Watch for popups:** Windows will randomly appear on your desktop. Some are GOOD, and some are BAD.
3. **Read before clicking:** Every popup has a message. Figure out whether it's legitimate or suspicious.
4. **Choose your button:** Each popup has two options: `X` and `OK`. Your choice determines what happens to your score.
5. **Keep your score positive:** Wrong decisions cost points. If your score drops below zero, it's game over.
6. **Survive the chaos:** Popups keep appearing, and their spawn speed increases as you progress. Stay alert!

### Scoring system

| Popup type | Correct button | Points |
|---|---|---:|
| BAD | `X` | +5 |
| BAD | `OK` | -10 |
| GOOD | `OK` | +1 |
| GOOD | `X` | -2 |

**Remember:** Closing a popup isn't always the right decision. Sometimes the `OK` button is your friend. Sometimes it's absolutely not.

*Read carefully. Click wisely. Blame the developer when things go wrong.*

## Screenshots

Coming soon. The desktop is currently dealing with multiple incidents.

## Installation

### Requirements

- Python 3
- Pygame-compatible environment

### Get the code

```bash
git clone https://github.com/AkshatPaji/CTRL-ALTF4EVER.git
cd CTRL-ALTF4EVER
```

### Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
python -m pip install pygame-ce
```

### Run it

```bash
python main.py
```

If your system uses `python3`, use:

```bash
python3 main.py
```

## Controls

| Action | Control |
|---|---|
| Start the game | Click `LETS GOO` |
| Close a popup | Click `X` or `OK` |
| Rage quit | `ESC` |

## What's next?

There's still plenty of room for more chaos.

Some ideas floating around:

- More popup categories and behaviours.
- Hidden clues and misleading messages.
- More interesting popup behaviours.
- New achievements and challenges.
- More animations and visual effects.
- Extra desktop interactions.
- Even more questionable messages.

No promises on when these arrive. I'm still figuring things out, one feature, one commit, and one questionable decision at a time.

## Built with

- Python
- Pygame CE
- A questionable amount of patience
- Several windows that should probably have stayed closed

## Final words

Read the popup. Think about your decision. Click responsibly.

Or don't. It's your score.

Thanks for checking out my first Pygame project and following its progress!

**CTRL+ALTF4EVER // v3.0**

*please close responsibly. consequences may apply.*