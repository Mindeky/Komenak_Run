import pygame

def render_text(font, text, color, outline_color="black", outline= 3):
    base = font.render(text, True, color)
    edge = font.render(text, True, outline_color)

    surface = pygame.Surface(
        (base.get_width() + outline * 2,base.get_height() + outline * 2),
        pygame.SRCALPHA,
    )
    for dx in range(-outline, outline+1):
        for dy in range(-outline, outline+1):
            if dx * dx + dy * dy <= outline * outline:
                surface.blit(edge, (outline + dx, outline + dy))
    surface.blit(base, (outline, outline))
    return surface