
import mido

# Create a new MIDI file and one track.
midi = mido.MidiFile()
track = mido.MidiTrack()
midi.tracks.append(track)

# Set the tempo to 120 beats per minute.
track.append(mido.MetaMessage("set_tempo", tempo=500000))

# Play three notes: C, E, G.
notes = [60, 64, 67]

for note in notes:
    # Start the note.
    track.append(
        mido.Message("note_on", note=note, velocity=64, time=0)
    )

    # Stop the note after 480 MIDI ticks.
    track.append(
        mido.Message("note_off", note=note, velocity=64, time=480)
    )

# Save the MIDI file.
midi.save("first_song.mid")

print("Success! Created first_song.mid")
