# CodeTune

A small Python project that turns code into music. It has two parts: a MIDI generator built with [`mido`](https://mido.readthedocs.io/) and a source-code analyzer that measures Python repositories.

## What's inside

| File | Purpose |
| --- | --- |
| `main.py` | Generates a MIDI file (`first_song.mid`) with a simple C–E–G sequence at 120 BPM |
| `analyze.py` | CLI tool that scans a folder for Python files and reports line and function metrics |
| `first_song.mid` | Sample output produced by `main.py` |

## Requirements

- Python 3.8+
- [`mido`](https://pypi.org/project/mido/) (only needed for `main.py`)

`analyze.py` uses only the standard library.

## Setup

```bash
git clone https://github.com/shatrughantwt/codetune.git
cd codetune

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install mido
```

## Usage

### Generate a MIDI file

```bash
python main.py
```

This writes `first_song.mid` in the current folder and prints:

```
Success! Created first_song.mid
```

It plays three notes in order: C (60), E (64), G (67). Each note is held for 480 ticks at a tempo of 500000 µs per beat (120 BPM). Open the file in any MIDI player or DAW to listen.

To change the melody, edit the `notes` list in `main.py` using [MIDI note numbers](https://en.wikipedia.org/wiki/MIDI_tuning_standard).

### Analyze a Python repository

```bash
# Analyze the current folder
python analyze.py

# Analyze any other folder
python analyze.py path/to/repo
```

For every `.py` file it reports:

- Total lines
- Non-empty lines
- Number of functions (`def` and `async def`)

It then prints repository totals. These folders are skipped: `.git`, `.venv`, `venv`, `node_modules`, `__pycache__`.

Example output:

```
CodeTune - Repository Analysis

File: /path/to/repo/main.py
  Lines: 29
  Non-empty lines: 17
  Functions: 0

Repository totals:
  Files: 1
  Lines: 29
  Non-empty lines: 17
  Functions: 0
```

## Project structure

```
codetune/
├── .gitignore
├── analyze.py
├── first_song.mid
└── main.py
```

## Status

Early stage. Both scripts work on their own; the goal is to connect code metrics from `analyze.py` with the MIDI generation in `main.py`.

## Contributing

Issues and pull requests are welcome.
