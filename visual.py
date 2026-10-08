import pygame
import mido

pygame.init()

WIDTH, HEIGHT = 700, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Artificial Artists - Prototype 1")

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (60, 60, 60)
LIT = (255, 200, 0)

NUM_KEYS = 12
KEY_WIDTH = WIDTH // NUM_KEYS
BASE_NOTE = 60  # MIDI note 60 = middle C = leftmost key

active_keys = set()

port_name = "Artificial Artists 0"
inport = mido.open_input(port_name)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check for any new MIDI messages, non-blocking
    for msg in inport.iter_pending():
        if msg.type == "note_on" and msg.velocity > 0:
            key_index = msg.note - BASE_NOTE
            if 0 <= key_index < NUM_KEYS:
                active_keys.add(key_index)
        elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
            key_index = msg.note - BASE_NOTE
            active_keys.discard(key_index)

    screen.fill(BLACK)

    for i in range(NUM_KEYS):
        x = i * KEY_WIDTH
        rect = pygame.Rect(x, 50, KEY_WIDTH - 2, HEIGHT - 100)
        color = LIT if i in active_keys else WHITE
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, GRAY, rect, 2)

    pygame.display.flip()

inport.close()
pygame.quit()