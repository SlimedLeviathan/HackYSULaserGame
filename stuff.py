
class Player:
    def __init__(self, frame, health):
        self.frame = 0
        self.health = 10

        self.is_jumping = True
        self.is_falling = False
        
        def gravity(self):
            if self.is_jumping:
                self.move += 3.2

        groundhit = pg.sprite.spritecollide(self, groundhit, False)
        for h in groundhit:
            self.move = 0
            self.rect.botton = h.rect.top
            self.is_jumping = False

        def jump(self):
            if self.is_jummping is False
