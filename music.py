import argparse, re, time 


class Song():
    NOTES_SHARPS = ("A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#")
    NOTES_FLATS = ("A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab")

    # instantiate a new object
    def __init__(self, key, chords: list):
        self.key = key
        self.chords = chords


    def __str__(self):
        return f"\n\nThis song is in the key of {self.key} and consists of {self.chords} chords"


    @classmethod
    def get_song(cls):
        # Ask the user what key the original song is in and have them enter the chords
        print("\n*** Enter the original key and chords, using sharps for accidentals. Stop inputs by signaling EOF ***")

        # Get key and chords from user
        while True:
            try:
                key = input("Key: ").title().strip()
            except EOFError:
                raise ValueError("Key input cannot be empty.")
            else:
                if key.upper() in cls.NOTES_SHARPS:
                    break
                else:
                    print("Invalid key. Please enter a valid key using sharps (e.g., A, C#, G#).")
        chords = []
        while True:
            try:
                chord = input("Enter chords: ").title().strip()
            except EOFError:
                break
            else:
                if _ := re.search(r"^[A-G](#|b)?(maj|min)?$", chord):
                    chords.append(chord)
                else:
                    raise ValueError("Invalid Chord")

        # Create an obect of class Song using the given key and chords
        return cls(key, chords)


    def transpose(self, new_key):
        # Error checking for new_key
        if new_key not in Song.NOTES_SHARPS:
            raise ValueError("New key must use sharps and be in NOTES_SHARPS.")

        # Error checking for self.key
        if self.key not in Song.NOTES_SHARPS:
            raise ValueError("Original key must use sharps and be in NOTES_SHARPS.")
        
        # Print song as is to ensure correctness
        print(self)

        # Calculate the number of half-steps to the new key
        halfsteps = Song.NOTES_SHARPS.index(new_key) - Song.NOTES_SHARPS.index(self.key)

        # Go through every chord, extract its info
        for index, chord in enumerate(self.chords):
            match = re.search(r"^([A-G])(#|b)?(maj|min|dim)?$", chord)

            # Find out the root and quality of the chord
            root = f"{match.group(1)}{match.group(2)}" if match.group(2) else match.group(1) # type: ignore
            quality = match.group(3) if match.group(3) else "" # type: ignore

            # Make sure root is in NOTES_SHARPS, and
            if root in Song.NOTES_SHARPS:
                new_root = f"{Song.NOTES_SHARPS[(Song.NOTES_SHARPS.index(root) + halfsteps) % 12]}"
                self.chords[index] = f"{new_root}{quality}"

        # Finally, change the value for self.key
        self.key = new_key

        # Show the transposed song
        print("\nTransposed song:", end="")
        print(self)


def main():

    parser = argparse.ArgumentParser(description="A simple music app")
    parser.add_argument("-m", "--metronome",  action='store_true')
    parser.add_argument("-t", "--transpose", action='store_true')
    args = parser.parse_args()
    if args.metronome:
        metronome()
    elif args.transpose:
        # Instantiate a new song
        song = Song.get_song()
        # Ask what key they want to change to
        song.transpose(input("Enter the new key: ").title().strip())
    else:
        print("Please specify an action: --metronome or --transpose.")

# implement a metronome using time.sleep()
def metronome():
    bpm = input("Enter the beats per minute (BPM): ")
    
    while True:
        try:
            bpm = int(bpm)
        except ValueError as e:
            print(f"Invalid input: {e}")
        else:
            if bpm <= 0:
                raise ValueError("BPM must be a positive integer.")
            else:
                break

if __name__ == "__main__":
    main()
