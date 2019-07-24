import pygame


class GUI:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def delete_start(self):
        self.elements = self.elements[1:]

    def render(self, surface):
        for element in self.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(surface)

    def update(self):
        for element in self.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                element.get_event(event)


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, text):
        super().__init__()
        if text == 'start':
            self.image = pygame.image.load("start.png")
        elif text == 'exit':
            self.image = pygame.image.load("exit.png")
        self.rect = self.image.get_rect()
        self.rect.x = rect[0]
        self.rect.y = rect[1]
        self.pressed = False

    def render(self, surface):
        surface.blit(self.image, self.rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                return self.pressed
