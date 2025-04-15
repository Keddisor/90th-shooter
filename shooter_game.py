from pygame import *
from random import *
from time import time as timer
mixer.init()
font.init()
font = font.SysFont('Arial', 40)
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
lose_points = 0
bullets = sprite.Group()
fire = mixer.Sound('fire.ogg')
class GameSprite(sprite.Sprite):
    def __init__(self, picture, pos_1, pos_2, speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(picture), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = pos_1
        self.rect.y = pos_2
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
        '''if keys_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 425:
            self.rect.y += self.speed'''
    def fire(self):
        '''keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE]:
            bullet = Bullet('bullet.png', ship.rect.centerx, ship.rect.top, 5, 5, 10)
            bullets.add(bullet)
            fire.play()'''
class Enemy(GameSprite):
    def update(self):
        if self.rect.y >= 500:
            self.rect.y = -75
            self.rect.x = randint(0, 625)
            self.speed = randint(1, 3)
            global lose_points
            lose_points += 1
        self.rect.y += self.speed
class Bullet(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if self.rect.y > -10:
            self.rect.y -= self.speed                             
        else:
            self.kill()
        window.blit(self.image, (self.rect.x, self.rect.y))
class Rock(GameSprite):
    def update(self):
        if self.rect.y >= 500:
            self.rect.y = -75
            self.rect.x = randint(0, 625)
            self.speed = randint(1, 5)
        self.rect.y += self.speed
game = True
finish = False
run = True
clock = time.Clock()
FPS = 60
x = 325
y = 425
ship = Player('rocket.png', x, y, 15, 50, 75)
monsters = sprite.Group()
asters = sprite.Group()
win_points = 0
win = font.render('YOU WIN', True, (124,252,0))
lose = font.render('YOU LOSE', True, (255,36,0))
lifes = 3
strike_points = 0
bullets_fired = 0
rel = False
for i in range(5):
    monster = Enemy('ufo.png', randint(0, 625), 0, randint(1, 3), 75, 50)
    monsters.add(monster)
for i in range(3):
    aster = Rock('asteroid.png', randint(0, 625), 0, randint(1, 3), 75, 50)
    asters.add(aster)
while game:
    if run != False:
        for e in event.get():
            if e.type == QUIT:
                game = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if bullets_fired < 6 and rel == False:
                        bullet = Bullet('bullet.png', ship.rect.centerx, ship.rect.top, 5, 5, 10)
                        bullets.add(bullet)
                        fire.play()
                        bullets_fired += 1
                    if bullets_fired >= 6 and rel == False:
                        last_time = timer()
                        rel = True
        if finish != True:
            window.blit(background, (0, 0))
            ship.reset()
            ship.update()
            ship.fire()
            monsters.update()
            monsters.draw(window)
            asters.update()
            asters.draw(window)
            bullets.update()
            bullets.draw(window)
            if bullets_fired >= 6:
                rel = True
            if rel == True:
                now_time = timer()
                if now_time - last_time < 3:
                    reload_bullet = font.render('Wait, reload...', 1, (255,36,0))
                    window.blit(reload_bullet, (250, 450))
                elif now_time - last_time >= 3:
                    bullets_fired = 0
                    rel = False
            collides = sprite.groupcollide(monsters, bullets, True, True)
            for collide in collides:
                win_points += 1
                monster = Enemy('ufo.png', randint(0, 625), 0, randint(1, 3), 75, 50)
                monsters.add(monster)
            if win_points >= 10:
                finish = True
                window.blit(win, (275, 225))
            if sprite.spritecollide(ship, monsters, True) or sprite.spritecollide(ship, asters, True):
                lifes -=1
            if lose_points >= 5 or lifes <= 0:
                finish = True
                window.blit(lose, (275, 225))
            sprite.groupcollide(asters, bullets, False, True)
            if lifes == 3:
                counter_life = font.render(str(lifes), 1, (124,252,0))
            elif lifes == 2:
                counter_life = font.render(str(lifes), 1, (247,150,5))
            elif lifes == 1:
                counter_life = font.render(str(lifes), 1, (247,247,5))
            else:
                counter_life = font.render(str(lifes), 1, (255,36,0))
            window.blit(counter_life, (675, 0))
            counter_lose = font.render('Пропущено:' + str(lose_points), 1, (255, 255, 255))
            window.blit(counter_lose, (0, 0))
            counter_win = font.render('Счёт:' + str(win_points), 1, (255, 255, 255))
            window.blit(counter_win, (0, 30))
        display.update()
        clock.tick(FPS)