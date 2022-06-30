import random
import pygame
pygame.init()
#根据屏幕调整窗口大小
HERO_FIRE_EVENT = pygame.USEREVENT + 1
SCREEN_RECT = pygame.Rect(0,0,480,700)
FRAME_PER_SEC = 60
CREATE_ENEMY_EVENT = pygame.USEREVENT
HERO_DIE = ['me1.png','me_destroy_1.png','me_destroy_2.png','me_destroy_3.png','me_destroy_4.png']
ENEMY_DIE = ['enemy1.png','enemy1_down1.png','enemy1_down2.png','enemy1_down3.png','enemy1_down4.png']
HERO_DIE_sum = 0
ENEMY_DIE_sum = 0
KONGZHI_JIANPAN =True
class Plane(pygame.sprite.Sprite):
    def __init__(self,imagename,speed=1,speedone = 0):
        super().__init__()
        self.image= pygame.image.load(imagename)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.speedone = speedone
    def update(self):
        self.rect.y+=self.speed
class Background(Plane):
    def __init__(self,is_alt=False):
        super().__init__('./images/background.png')
        if is_alt:
            self.rect.y = -self.rect.height
    def update(self):
        super().update()
        if self.rect.y >=SCREEN_RECT.height:
            self.rect.y = -self.rect.height
class Enemy(Plane):
    def __init__(self):
        super().__init__('./images/enemy1.png')
        self.speed = random.randint(1,3)
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x=random.randint(0,max_x)
        self.bullets = pygame.sprite.Group()
    def update(self):
        super().update()
        if self.rect.y>= SCREEN_RECT.height:
            self.kill()
            print('1')
    def __del__(self):
        pass
class PlaneGame(object):
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        pygame.time.set_timer(CREATE_ENEMY_EVENT,1000)
        pygame.time.set_timer(HERO_FIRE_EVENT,500)
    def __create_sprites(self):
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1,bg2)
        self.enemy_group = pygame.sprite.Group()
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
    def star_game(self):
        while True:
            self.clock.tick(FRAME_PER_SEC)
            self.__event_handler()
            self.__check_collide()
            self.__update_sprites()
            pygame.display.update()
            pass
    def __event_handler(self):
        for keyxia in pygame.event.get():
            if keyxia.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif keyxia.type == CREATE_ENEMY_EVENT:
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif keyxia.type == HERO_FIRE_EVENT:
                self.hero.fire()
        key_s = pygame.key.get_pressed()
        if key_s[pygame.K_RIGHT]:
            self.KONGZHI_JIANPAN =True
            self.hero.speed = 3
        elif key_s[pygame.K_LEFT]:
            self.KONGZHI_JIANPAN = True
            self.hero.speed = -3
        elif key_s[pygame.K_UP]:
            self.KONGZHI_JIANPAN = False
            self.hero.speedone =-3
        elif key_s[pygame.K_DOWN]:
            self.KONGZHI_JIANPAN = False
            self.hero.speedone = 3
        else:
            self.hero.speed = 0
            self.hero.speedone = 0
    def __check_collide(self):
        gg = pygame.sprite.groupcollide(self.hero.bullets,self.enemy_group,True,True)
        if len(gg) > 0:
            pass
        cc = pygame.sprite.spritecollide(self.hero,self.enemy_group,True)
        if len(cc) > 0:
            self.hero.kill()
            PlaneGame.__game_over()
    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)
    @staticmethod
    def __game_over():
        print('游戏结束')
        pygame.quit()
        exit()
class Hero(Plane):
    def __init__(self):
        #初始化主飞机位置
        super().__init__('./images/me1.png',0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom-120
        self.bullets = pygame.sprite.Group()
    def update(self):
        #判断主飞机是否出界 控制主飞机动
        self.rect.x += self.speed
        self.rect.y += self.speedone
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right >SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom -100 >SCREEN_RECT.bottom-100:
            self.rect.bottom = SCREEN_RECT.bottom
    def fire(self):
        for i in (-150,-120,-90,-60,-30,0,30,60,90,120,150):
            bullet = Bullet()
            bullet.rect.bottom = self.rect.y-20
            bullet.rect.centerx = self.rect.centerx +i
            self.bullets.add(bullet)
class Bullet(Plane):
    def __init__(self):
        super().__init__('./images/bullet1.png',-3)
    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()
    def __del__(self):
        pass
if __name__ == '__main__':
    game = PlaneGame()
    game.star_game()
