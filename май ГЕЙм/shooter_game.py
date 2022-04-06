from pygame import *
from random import randint
 
mixer.init()
mixer.music.load('la.ogg')
mixer.music.play()
fire_sound = mixer.Sound('a.ogg')
mixer.music.set_volume(0.2)

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('ХАРОООООШ!', True, (0, 255, 0))
lose = font1.render('ПОТРАЧЕНО!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)
 
img_back = "l.png" #фон игры
img_hero = "jej.jpg" #герой
img_bullet = "pudge.jpg" #пуля
img_enemy = "joj.jpg" #враг
img_asteroid = "mom.jpg"


score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
max_lost = 3 #проиграли, если пропустили столько

 
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))   
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x<win_width-80:
            self.rect.x += self.speed
    def fire(self):
        pass
 

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 30, 40, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroids(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            
            

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
player = Player(img_hero, 5, win_height - 100, 80, 100, 10)


hp = 1

asteroids = sprite.Group()
for i in range(5):
    asteroid = Asteroids(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
bullets = sprite.Group()
finish = False
run = True
 
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
  
    if not finish:
        window.blit(background,(0,0))
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
  
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_hp = font2.render("Здоровье: " + str(hp), 1, (255, 255, 255))
        window.blit(text_hp, (10, 80))

        healthpoints = font2.render(str(hp), 1, (255, 255, 255))
        window.blit(healthpoints, (10, 80))


        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        
            
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        
        

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        collides = sprite.spritecollide(player, monsters, True)
        for c in collides:
            if hp > 1:
                hp -= 1
                monster = Enemy("joj.jpg", randint(80, win_width-80), -40, 80, 70, randint(1, 5))
                monsters.add(monster)
            else:
                finish = True
                window.blit(lose, (200, 200))

        collides = sprite.spritecollide(player, asteroids, True)
        for c in collides:
            if hp > 1:
                hp -= 1
                asteroid = Asteroids("mom.jpg", randint(80, win_width-80), -40, 80, 70, randint(1, 5))
                asteroids.add(asteroid)
            else:
                finish = True
                window.blit(lose, (200, 200))

        if lost >= 3:
            finish = True
            window.blit(lose, (200, 200))
        if score >= 10:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    time.delay(50)
            



 

 
