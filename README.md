# Artificial Artists

**A live computational performance system that gives programmed backing instruments a visual, synchronized presence on stage.**

When a solo musician performs with a backing track, the audience hears extra instruments but sees nobody playing them. Artificial Artists explores that gap: each programmed instrument is represented on a screen, and its visuals are driven directly by the musical data, so what the audience sees and what they hear are the same event.

> Status: **Prototype 1 complete** (one instrument, live MIDI to synchronized visual). Prototypes 2-6 are planned.

## How it works

```
Ableton Live (composed MIDI)
        |
        v
loopMIDI virtual port ("Artificial Artists 0")
        |
        v
Python (mido + python-rtmidi) receives note events
        |
        v
Pygame renders the visual performer in real time
```

The system is **event-driven, not video-driven**. There is no prerecorded animation to line up with a song. Each MIDI note-on and note-off message is handled as it arrives, so editing a note in Ableton changes the visual automatically.

## Current capabilities (Prototype 1)

- Receives live MIDI from Ableton Live 11 through a Windows virtual MIDI port
- Parses note-on, note-off, and zero-velocity note-on messages
- Maps MIDI notes to a one-octave visual piano (middle C = leftmost key)
- Lights keys when notes start and releases them when notes end
- Handles chords, since each key's state is tracked independently
- Polls MIDI without blocking, so the render loop keeps running

## Tech stack

| Layer | Tool | Why |
|---|---|---|
| Composition / sound | Ableton Live 11 | Source of truth for the music |
| MIDI routing | loopMIDI | Lets Ableton and Python receive the same MIDI stream at once |
| MIDI input | Python 3.12, mido, python-rtmidi | Simple, readable access to raw MIDI messages |
| Visuals | Pygame | One process, same Python script as the MIDI listener, minimal moving parts |

Design priority order: reliability, then synchronization, then simplicity, then artistic flexibility, then visual sophistication.

## Setup

1. Install Python 3.12 (python-rtmidi has no prebuilt wheels for 3.14 yet)
2. `python -m pip install mido python-rtmidi pygame`
3. Install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) and create a port named `Artificial Artists`
4. In Ableton: Preferences, MIDI, turn **Track** on for the port's output
5. On your MIDI track, set **MIDI To** to the port, and set **MIDI From** to *No Input* (see lessons below)
6. Run `python listener.py` to confirm notes arrive, then `python visual.py` to see the keyboard

## Lessons learned

- **Port names:** loopMIDI appends an index, so the port appears to Python as `Artificial Artists 0`.
- **MIDI feedback loop:** if a track's input is the same virtual port as its output, it re-triggers its own notes endlessly. Keep the input set to *No Input*.
- **Prebuilt wheels:** brand-new Python versions can lack binary wheels for native packages, which forces a C++ compiler install. Using Python 3.12 avoided that.
- **Testing in layers:** printing raw MIDI first, before any graphics, made it easy to tell whether a failure was in routing or in rendering.

## Roadmap

1. ~~**Prototype 1:** one instrument, MIDI event to synchronized visual~~
2. **Prototype 2:** expressive data (velocity to intensity, duration, pitch to position)
3. **Prototype 3:** full instrument part, with latency, drift, and frame-rate testing
4. **Prototype 4:** multiple artificial musicians on separate MIDI channels
5. **Prototype 5:** separate physical displays per performer
6. **Prototype 6:** human performer plus artificial band, live

Generative-AI music is deliberately out of scope for the initial system. The music is composed and programmed by the performer.

## Author

**Lilla Tillo**: musician, producer, and student in Computational Media & Creative Technology at Whitman College. [GitHub](https://github.com/lilltill7) · lillabryar@gmail.com
