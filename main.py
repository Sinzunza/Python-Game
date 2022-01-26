import pygame
import random

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()


win = pygame.display.set_mode((700, 700))

pygame.display.set_caption("Arcade")

backGround = pygame.image.load('images/Rick Morty BG.jpg')
gameFace = pygame.image.load('images/Rick Sanchez Game Face.png')
worriedFace = pygame.image.load('images/Rick Sanchez Worried Face.png')
monsterFace = pygame.image.load('images/Cromulon.png')
ammo = pygame.image.load('images/Pickle Rick.png')
charHit = pygame.image.load('images/Pick Hit Rick.png')
monsterHit = pygame.image.load('images/Warp.png')
gameOver = pygame.image.load('images/Game Over.png')
ammoSound = pygame.mixer.Sound("sound/Wobble.wav")
monsterHitSound = pygame.mixer.Sound('sound/Hit Monster.wav')
charHitSound = pygame.mixer.Sound('sound/Game Over.wav')
forTheDamagedCoda = pygame.mixer.Sound("sound/For The Damaged Coda.wav")

#init attributes
font = pygame.font.SysFont('comicsans', 30, True)
runGame = True
levelWon = True

#game attributes
runLevel = 0
playOnce = 0
level = 0
numberMonsters = 1
velocityMonsters = 1
def newGame():
    global runLevel
    global playOnce
    global level
    global  numberMonsters
    global  velocityMonsters

    runLevel = True
    playOnce = True
    level = 1
    numberMonsters = 1
    velocityMonsters = 1
    pygame.mixer.Sound.play(forTheDamagedCoda)

newGame()

#character attributes
vel_Char = 0
xPos_Char = 0
yPos_Char = 0
def setChar():
    global vel_Char
    global xPos_Char
    global yPos_Char
    vel_Char = 19
    xPos_Char = 318
    yPos_Char = 313

#monster attributes
xVel_Monsters = 0
yVel_Monsters = 0
xPos_Monsters = 0
yPos_Monsters = 0
monstersHit = 0
timerMonsterCreation = 0
timerMonsterMovement = 0
monstersCreated = 0
monstersAlive = 0
moveAvailable = 0
isHit = 0
whosHit = 0
def setMonsters(_numberMonsters, _velocityMonsters):
    global xVel_Monsters
    global yVel_Monsters
    global xPos_Monsters
    global yPos_Monsters
    global monstersHit
    global timerMonsterCreation
    global timerMonsterMovement
    global monstersCreated
    global monstersAlive
    global moveAvailable
    global isHit
    global whosHit
    xVel_Monsters = []
    yVel_Monsters = []
    xPos_Monsters = []
    yPos_Monsters = []
    monstersHit = []
    for x in range(_numberMonsters):
        xVel_Monsters.append(_velocityMonsters)
        yVel_Monsters.append(_velocityMonsters)
        xPos_Monsters.append(0)
        yPos_Monsters.append(0)
        monstersHit.append(0)
    timerMonsterCreation = 65
    timerMonsterMovement = 0
    monstersCreated = 0
    monstersAlive = _numberMonsters
    moveAvailable = True
    isHit = 0
    whosHit = False

#ammo attributes
vel_Ammo = 0
xPos_Ammo = 0
yPos_Ammo = 0
ammo_First = 0
ammo_Second = 0
noAmmo = 0
def setAmmo():
    global vel_Ammo
    global xPos_Ammo
    global yPos_Ammo
    global ammo_First
    global ammo_Second
    global noAmmo
    vel_Ammo = 17
    xPos_Ammo = 0
    yPos_Ammo = 0
    ammo_First = False
    ammo_Second = False
    noAmmo = True

# Gui of game
def redrawGameWindow(): # this is ran constantly in loop, this call redrawLevel as long as runLevel is true
    global runLevel
    global playOnce
    global levelWon
    global level

    win.blit(backGround, (0,0))
    levelText = font.render('Level: ' + str(level), 1, (255, 255, 255))
    monstersText = font.render('Croms: ' + str(monstersAlive), 1, (255, 255, 255))
    win.blit(levelText, (583, 5))
    win.blit(monstersText, (570, 30))

    if runLevel:
        if levelWon: # run at the beginning of a level
            levelWon = False
            setChar()
            setMonsters(numberMonsters, velocityMonsters)
            setAmmo()
        redrawLevel(True)
    else:
        redrawLevel(False)
        win.blit(gameOver, (85, 190))
        keysOver = pygame.key.get_pressed()
        if keysOver[pygame.K_p]:
            newGame()
            setChar()
            setMonsters(numberMonsters, velocityMonsters)
            setAmmo()

    pygame.display.update()

def redrawLevel(notOver):
    global runGame
    global runLevel
    global xVel_Monsters
    global yVel_Monsters
    global timerMonsterCreation
    global timerMonsterMovement
    global monstersCreated
    global monstersAlive
    global moveAvailable
    global isHit
    global whosHit
    global ammo_First
    global ammo_Second
    global yPos_Ammo
    global noAmmo
    global levelWon
    global numberMonsters
    global velocityMonsters
    global level

    # character display
    if xPos_Char < xPos_Ammo + 16 and xPos_Char + 64 > xPos_Ammo + 16 and yPos_Char < yPos_Ammo + 16 and yPos_Char + 64 > yPos_Ammo + 16 and ammo_Second:
        if notOver:
            pygame.mixer.Sound.stop(forTheDamagedCoda)
            pygame.mixer.Sound.play(charHitSound)
        win.blit(charHit, (xPos_Char - 43, yPos_Char - 43))
        runLevel = False
        notOver = False
    elif ammo_Second and notOver:
        win.blit(worriedFace, (xPos_Char, yPos_Char))
    elif notOver:
        win.blit(gameFace, (xPos_Char, yPos_Char))


    # monster display
    if timerMonsterCreation is 66 and monstersCreated < numberMonsters and notOver: # creates a monster every timerMonsterCreation tick
            timerMonsterCreation = 0
            monstersCreated += 1
    if monstersAlive > 0:
        for x in range(monstersCreated - (numberMonsters - monstersAlive)): # range is for number of monsters created that are still alive
            if notOver: # move the monster
                xPos_Monsters[x] += xVel_Monsters[x]
                yPos_Monsters[x] += yVel_Monsters[x]
                moveAvailable = True

            win.blit(monsterFace, (xPos_Monsters[x], yPos_Monsters[x]))
            #monster hits char, game over
            if xPos_Monsters[x] < xPos_Char + 32 and xPos_Monsters[x] + 64 > xPos_Char + 32 and yPos_Monsters[x] < yPos_Char + 32 and yPos_Monsters[x] + 64 > yPos_Char + 32:
                if notOver:
                    pygame.mixer.Sound.stop(forTheDamagedCoda)
                    pygame.mixer.Sound.play(charHitSound)
                win.blit(charHit, (xPos_Char - 43, yPos_Char - 43))
                runLevel = False
                notOver = False

            #ammo hits monster
            if xPos_Monsters[x] < xPos_Ammo + 16 and xPos_Monsters[x] + 64 > xPos_Ammo + 16 and yPos_Monsters[x] < yPos_Ammo + 16 and yPos_Monsters[x] + 64 > yPos_Ammo + 16 and ammo_First and notOver:
                win.blit(monsterHit, (xPos_Monsters[x] - 18, yPos_Monsters[x] - 18))
                pygame.mixer.Sound.play(monsterHitSound)
                isHit = True
                whosHit = x
                ammo_First = False
                noAmmo = True

            # change monster movements
            if xPos_Monsters[x] < 0 or xPos_Monsters[x] > 636 and notOver: # keep monster in frame horizontally
                xVel_Monsters[x] *= -1
                moveAvailable = False
            if yPos_Monsters[x] < 0 or yPos_Monsters[x] > 636 and notOver: # keep monster in frame vertically
                yVel_Monsters[x] *= -1
                moveAvailable = False
            if timerMonsterMovement is 40 and moveAvailable and notOver: # change angle of monsters movement every timerMonsterMovement tick
                xVel_Monsters[x] *= [-1, 1][random.randrange(2)]
                yVel_Monsters[x] *= [-1, 1][random.randrange(2)]
                timerMonsterMovement = 0

        if isHit: # delete monster who has been hit
            del xPos_Monsters[whosHit]
            del yPos_Monsters[whosHit]
            del xVel_Monsters[whosHit]
            del yVel_Monsters[whosHit]
            isHit = False
            monstersAlive -= 1

        if monstersAlive is 0:
            levelWon = True
            level += 1
            numberMonsters += 1
            velocityMonsters += 1

    # ammo display
    if notOver is False and ammo_Second:
        win.blit(ammo, (xPos_Ammo + 16, yPos_Ammo))
    if ammo_First and notOver:
        win.blit(ammo, (xPos_Ammo + 16, yPos_Ammo))
        yPos_Ammo -= vel_Ammo
        if yPos_Ammo < 17:
            ammo_First = False
            ammo_Second = True
    if ammo_Second and notOver:
        win.blit(ammo, (xPos_Ammo + 16, yPos_Ammo))
        yPos_Ammo += vel_Ammo
        if yPos_Ammo > 700:
            ammo_Second = False
            noAmmo = True


#Main Loop
while runGame:
    redrawGameWindow()
    pygame.time.delay(40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False

    if runLevel:
        timerMonsterCreation += 1
        timerMonsterMovement += 1
        #key binding
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and xPos_Char > 0:
            xPos_Char -= vel_Char
        if keys[pygame.K_RIGHT] and xPos_Char < 636:
            xPos_Char += vel_Char
        if keys[pygame.K_UP] and yPos_Char > 0:
            yPos_Char -= vel_Char
        if keys[pygame.K_DOWN] and yPos_Char < 636:
            yPos_Char += vel_Char
        if keys[pygame.K_SPACE] and noAmmo:
            pygame.mixer.Sound.play(ammoSound)
            xPos_Ammo = xPos_Char
            yPos_Ammo = yPos_Char
            ammo_First = True
            noAmmo = False


pygame.quit()
