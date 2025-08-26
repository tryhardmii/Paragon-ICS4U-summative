import pygame

pygame.init()
def difficulty():
    from menu import bgx
    from sprites import buttons
    bgx += 70
    active = True
    screen = pygame.display.set_mode((1200, 800))

    bg = pygame.image.load('menugraphics/scrollingbackground.png').convert()
    def diff1():
        return 1
    def diff2():
        return 2
    def diff3():
        return 3
    def diff4():
        return 4
    def end():
        return 2
    #backbutton = buttons(200,75,"menugraphics/backbutton.png",end)
    difficultybuttons = [buttons(600,200,"menugraphics/easybutton.png",diff1),
                         buttons(600,350,"menugraphics/mediumbutton.png",diff2),
                         buttons(600,500,"menugraphics/medium2button.png",diff3),
                         buttons(600,650,"menugraphics/hardbutton.png",diff4)]

    buttons = pygame.sprite.Group()
    #buttons.add(backbutton) 
    for x in difficultybuttons:
        buttons.add(x)
    cycle = pygame.USEREVENT + 1
    pygame.time.set_timer(cycle, 100)
    
    while active == True:
        for event in pygame.event.get():
            if bgx==bg.get_width():
                bgx=0
            if event.type == cycle:
                bgx+=2
            for button in buttons:
                button.jiggle()
                i = button.checkpressed(event)
                if button.posx==200 and i==2:
                    active = False
                elif i!=0:
                    difficulty1 = i
                    active = False

            if event.type == pygame.QUIT:
                active = "quit"
        screen.blit(bg,(bgx,0))
        screen.blit(bg,(bgx-bg.get_width(),0))
        buttons.draw(screen)
        pygame.display.update()
        pygame.time.Clock().tick(60)
    if active=="quit":
        pygame.quit()
    else:
        return [bgx, difficulty1]
