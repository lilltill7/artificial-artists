import mido

print("Available MIDI ports:")
for name in mido.get_input_names():
    print(f"  {name}")

port_name = "Artificial Artists 0"

with mido.open_input(port_name) as inport:
    print(f"\nListening on '{port_name}'... play some notes!")
    for msg in inport:
        print(msg)