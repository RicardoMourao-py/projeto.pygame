# Ricardo, Rodrigo e Ykaro
# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
from blocos import * # Importação dos blocos

pygame.init()

# ----- Gera tela principal
LARGURA = 500
ALTURA = 600
window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('WATER JUMP')

# ----- Inicia assets
BLOCO_LARGURA = 85
BLOCO_ALTURA = 38
DOG_LARGURA = 80
DOG_ALTURA = 80
font = pygame.font.SysFont('Algerian', 48)
text1 = font.render('TESTANDO', True, (255, 0, 0))
background = pygame.image.load('img/ceu.png').convert_alpha()
background= pygame.transform.scale(background, (LARGURA, ALTURA))
bloco_img = pygame.image.load('img/blocks.png').convert_alpha()
bloco_img = pygame.transform.scale(bloco_img, (BLOCO_LARGURA, BLOCO_ALTURA))
dog_img = pygame.image.load('img/dogremove.png').convert_alpha()
dog_img = pygame.transform.scale(dog_img, (DOG_LARGURA, DOG_ALTURA))

# Define a aceleração da gravidade
GRAVITY = 2
# Define a velocidade inicial no pulo
JUMP_SIZE = 30
# Define a altura do chão
GROUND = ALTURA * 5 // 6

# Define estados possíveis do jogador
STILL = 0
JUMPING = 1
FALLING = 2

# ----- Inicia estruturas de dados
# Definindo os novos tipos
class Ship(pygame.sprite.Sprite):
    def __init__(self, img, blocos):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

# Define estado atual
        # Usamos o estado para decidir se o jogador pode ou não pular
        self.state = STILL
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA / 2
        self.rect.bottom = ALTURA - (100+BLOCO_ALTURA)
        self.speedx = 0
        self.speedy = 0
        self.platforms = blocos
        self.highest_y = self.rect.bottom
       


    def update(self):
        # Atualização da posição da nave
        self.rect.x += self.speedx
        # self.rect.y += self.speedy
        self.speedy += GRAVITY
        # Atualiza o estado para caindo
        if self.speedy > 0:
            self.state = FALLING
        self.rect.y += self.speedy
        
        # Atualiza altura no mapa
        if self.state != FALLING:
            self.highest_y = self.rect.bottom

        # Se colidiu com algum bloco, volta para o ponto antes da colisão
    

        # Tratamento especial para plataformas
        # Plataformas devem ser transponíveis quando o personagem está pulando
        # mas devem pará-lo quando ele está caindo. Para pará-lo é necessário que
        # o jogador tenha passado daquela altura durante o último pulo.
        
        if self.speedy > 0:  # Está indo para baixo
            collisions = pygame.sprite.spritecollide(self, self.platforms, False)
            # Para cada tile de plataforma que colidiu com o personagem
            # verifica se ele estava aproximadamente na parte de cima
            for platform in collisions:
                # Verifica se a altura alcançada durante o pulo está acima da
                # plataforma.
                if self.highest_y <= platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    # Atualiza a altura no mapa
                    self.highest_y = self.rect.bottom
                    # Para de cair
                    self.speedy = 0
                    # Atualiza o estado para parado
                    self.state = STILL
                    

        # Tenta andar em x
        self.rect.x += self.speedx
        # Corrige a posição caso tenha passado do tamanho da janela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right >= LARGURA:
            self.rect.right = LARGURA 
        # if self.rect.bottom > ALTURA:
        #     self.rect.bottom = ALTURA
        #     self.speedy=0
        #     # Atualiza o estado para parado
        #     self.state = STILL
        # Se colidiu com algum bloco, volta para o ponto antes da colisão
        # O personagem não colide com as plataformas quando está andando na horizontal
            
    # Método que faz o personagem pular (extraído de: https://github.com/Insper/pygame-snippets/blob/master/jump.py)
    def jump(self):
        # Só pode pular se ainda não estiver pulando ou caindo
        if self.state == STILL:
            self.speedy -= JUMP_SIZE
            self.state = JUMPING 
class Bloco(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = x     #random.randint(0, LARGURA-BLOCO_LARGURA)
        self.rect.y = y           #random.randint(-100, -BLOCO_ALTURA)
        self.speedx = self.rect.x #random.randint(-3, 3)
        self.speedy = 1
  

    def update(self):
        # Atualizando a posição do Blocoo
        #self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se o Bloco passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.top > ALTURA or self.rect.right < 0 or self.rect.left > LARGURA:
            #self.rect.x = random.randint(0, LARGURA-BLOCO_LARGURA)
            self.rect.y =  -2#random.randint(-100, -ALTURA)
            #self.speedx = random.randint(-3, 3)
            self.speedy = 1 #random.randint(2, 9)

game = True

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()
FPS = 50
# Criando um grupo de meteoros
todos_sprites = pygame.sprite.Group()
lista_blocos=pygame.sprite.Group()

# Posição das imagens
background_x=0
background_y=0
background_y2=-600
background_speedx=0
background_speedy=1

# Criando o jogador

i=0
while i<len(blocos(LARGURA,ALTURA)[0]):
    bloco=Bloco(bloco_img,blocos(LARGURA,ALTURA)[0][i],blocos(LARGURA,ALTURA)[1][i])
    lista_blocos.add(bloco)
    i+=1
player = Ship(dog_img,lista_blocos)
todos_sprites.add(player)

# ===== Loop principal =====
while game:
    clock.tick(FPS)
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                player.speedx -= 8
            if event.key == pygame.K_RIGHT:
                player.speedx += 8
            # if event.key == pygame.K_SPACE:
            #     player.speedy += -8
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                player.speedx += 8
            if event.key == pygame.K_RIGHT:
                player.speedx -= 8
            # if event.key == pygame.K_SPACE:
            #     player.speedy += 16
         # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera o estado do jogador.
            if event.key == pygame.K_SPACE: #or event.key == pygame.K_UP:
                player.jump()

    background_x+=background_speedx
    background_y+=background_speedy
    background_y2+=background_speedy
    if background_y > ALTURA or background_x + BLOCO_LARGURA < 0 or background_x > LARGURA:
        background_x = 0
        background_y = 0
        background_y2=-600

    todos_sprites.update()
    lista_blocos.update()
    # ----- Atualiza estado do jogo
    # ----- Gera saídas
       

    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(background, (background_x, background_y))
    window.blit(background, (background_x, background_y))
    window.blit(background, (background_x, background_y2))
    todos_sprites.draw(window)
    lista_blocos.draw(window)
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
