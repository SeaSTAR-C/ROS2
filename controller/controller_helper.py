import pygame

class SwitchController:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            raise RuntimeError("No controller detected")

        self.js = pygame.joystick.Joystick(0)
        self.js.init()

        print("Connected controller:", self.js.get_name()) 
        print("Axes:", self.js.get_numaxes(), "Buttons:", self.js.get_numbuttons())

    def update(self):
        # Handle ALL controller events
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                print("BUTTON DOWN:", event.button)
            elif event.type == pygame.JOYBUTTONUP:
                print("BUTTON UP:", event.button)

    def get_left_stick(self):
        return self.js.get_axis(0), self.js.get_axis(1)

    def get_right_stick(self):
        return self.js.get_axis(2), self.js.get_axis(3)

    def get_triggers(self):
        return self.js.get_axis(4), self.js.get_axis(5)

    def get_pressed_buttons(self):
        pressed = []
        for b in range(self.js.get_numbuttons()):
            if self.js.get_button(b):
                pressed.append(b)
        return pressed
