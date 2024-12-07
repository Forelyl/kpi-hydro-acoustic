# -----------------
# Work
# -----------------


# -----------------
# Debug
# -----------------
import pygame
import io


def play_audio(file):
    mp3_bytes = io.BytesIO(file.file.read())

    pygame.mixer.init()
    # Load the MP3 file from the BytesIO object
    pygame.mixer.music.load(mp3_bytes, "mp3")

    # Play the audio
    pygame.mixer.music.play()

    # Keep the script running while the audio is playing
    i = 0
    while pygame.mixer.music.get_busy() and i < 30:
        i += 1
        pygame.time.Clock().tick(10)  # Wait for the music to finish

    pygame.mixer.music.stop()