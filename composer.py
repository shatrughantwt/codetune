
import mido


def metrics_to_notes(metrics):
    """Convert source-code metrics into a sequence of MIDI pitches."""

    line_count = metrics["lines"]
    function_count = metrics["functions"]

    # Longer files generate more notes, with a limit of 32.
    note_count = max(1, min(line_count, 32))

    # Functions shift the melody into a higher register.
    base_pitch = min(72, 60 + function_count * 2)

    notes = []

    for i in range(note_count):
        # Keep notes within a simple musical scale.
        scale = [0, 2, 4, 7, 9]
        pitch = base_pitch + scale[(i + function_count) % len(scale)]
        notes.append(pitch)

    return notes


def create_midi(notes, output_path):
    """Save a sequence of MIDI pitches as a MIDI file."""

    midi = mido.MidiFile()
    track = mido.MidiTrack()
    midi.tracks.append(track)

    for pitch in notes:
        track.append(
            mido.Message(
                "note_on",
                note=pitch,
                velocity=64,
                time=0,
            )
        )
        track.append(
            mido.Message(
                "note_off",
                note=pitch,
                velocity=64,
                time=480,
            )
        )

    midi.save(output_path)
