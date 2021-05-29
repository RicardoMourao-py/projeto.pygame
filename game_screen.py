import pygame
from constantes import FPS, LARGURA, ALTURA, WALKING_LEFT,WALKING_RIGTH,STILL,BLOCO_LARGURA,BLOCO_ALTURA
from assets import blocos, bloco_img, dog_img, som_pulo, background,som_gameover,score_font,texto_inicial,agua
from sprites import Ship, Bloco
import time

pygame.init()
pygame.mixer.init()
def game_screen(window):
    game = True
    background_x=0
    background_y=0
    background_y2=-600
    agua_x=0
    agua_y=ALTURA-100
    agua_speedy=-0.1
    background_speedx=0
    background_speedy=1
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()
    FPS = 50
    # Criando um grupo de meteoros
    todos_sprites = pygame.sprite.Group()
    lista_blocos=pygame.sprite.Group()
    # Criando o jogador

    # Criando os meteoros
    # for i in range(8):
    #     bloco = Bloco(bloco_img)
    #     todos_sprites.add(bloco)
    # bloco1 = Bloco(bloco_img,LARGURA/2,ALTURA-100)
    # bloco2 = Bloco(bloco_img,LARGURA-30,ALTURA-200)
    # bloco3 = Bloco(bloco_img,LARGURA-10,ALTURA-400)
    # lista_blocos.add(bloco1)
    # lista_blocos.add(bloco2)
    # lista_blocos.add(bloco3)

    i=0
    while i<len(blocos(LARGURA,ALTURA)[0]):
        bloco=Bloco(bloco_img,blocos(LARGURA,ALTURA)[0][i],blocos(LARGURA,ALTURA)[1][i],i+1)
        lista_blocos.add(bloco)
        i+=1
    player = Ship(dog_img,lista_blocos,som_pulo)
    todos_sprites.add(player)
    # ===== Loop principal =====
    pygame.mixer.music.play(loops=-1)
    #score = 0
    while game:
        clock.tick(FPS)
        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: #or event.key == pygame.K_UP:
                    player.jump()
                    #score+=100
                        
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    player.animacao = WALKING_LEFT
                    player.speedx -= 8
                if event.key == pygame.K_RIGHT:
                    player.animacao = WALKING_RIGTH
                    player.speedx += 8
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    player.speedx += 8
                    player.state = STILL
                if event.key == pygame.K_RIGHT:
                    player.speedx -= 8 
                    player.state = STILL
            # if event.type == pygame.KEYDOWN:
            #     # Dependendo da tecla, altera o estado do jogador.
            #     if event.key == pygame.K_SPACE: #or event.key == pygame.K_UP:
            #         player.jump()
                
        background_x+=background_speedx
        background_y+=background_speedy
        background_y2+=background_speedy
        #agua_y+=agua_speedy
        if background_y > ALTURA or background_x + BLOCO_LARGURA < 0 or background_x > LARGURA:
            background_x = 0
            background_y = 0
            background_y2=-600
        if player.rect.bottom>ALTURA:
            som_gameover.play()
            time.sleep(1)
            game=False
        todos_sprites.update()
        lista_blocos.update()
        # ----- Atualiza estado do jogo
        # ----- Gera saídas
        window.fill((0, 0, 0))  # Preenche com a cor branca
        window.blit(texto_inicial, (LARGURA/2, ALTURA/2))
        window.blit(background, (background_x, background_y))
        window.blit(background, (background_x, background_y))
        window.blit(background, (background_x, background_y2))
        text_surface = score_font.render("{:08d}".format(player.score), True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (LARGURA-150,  10)
        window.blit(text_surface, text_rect)
        #window.blit(agua, (agua_x,agua_y))
        todos_sprites.draw(window)
        lista_blocos.draw(window)
        window.blit(agua, (agua_x,agua_y))
        #window.blit(agua, (agua_x, agua_y))
        pygame.display.update()  # Mostra o novo frame para o jogador