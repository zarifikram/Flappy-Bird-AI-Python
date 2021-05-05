import pygame

class Score():
    def __init__(self):
        self.val = 0
        self.hival = 0
        self.refresh = 50
        self.CHECK = pygame.USEREVENT + 2
        pygame.time.set_timer(self.CHECK, self.refresh)
        
    def update(self):
        if self.val > self.hival:
            self.hival = self.val
            print("updated", self.val, self.hival)

    def increase(self):
        self.val += .5
        print("increased")
        self.update() 
    
    def clear(self):
        self.val = 0