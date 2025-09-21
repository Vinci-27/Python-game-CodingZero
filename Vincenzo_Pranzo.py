import pygame

pygame.init()

font = pygame.font.SysFont('Times New Roman', 30)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PLAYER_SPEED = 10

# Impostazione dimensioni finestra e titolo
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car League")

# Aggiunta di uno sfondo che prende le dimensioni della finestra
BackgroundImg = pygame.image.load("Background.png")
BackgroundImg = pygame.transform.scale(BackgroundImg, (WIDTH, HEIGHT))

Player_DistanceX = WIDTH / 10
clock = pygame.time.Clock()
FPS = 30

class Player:
    # Chiediamo in input, la posizione iniziale, larghezza, altezza e velocità dell'oggetto
    def __init__(self, posX, posY, speed, width, height):
        self.posX = posX
        self.posY = posY
        self.speed = speed
        self.width = width
        self.height = height

        # Caricamento e ridimensionamento dell'immagine del player
        self.playerImg = pygame.image.load("player.png")
        self.playerImg = pygame.transform.scale(self.playerImg, (width, height))

        # Creazione della hitbox principale per il player
        self.hitboxPlayer = pygame.Rect(posX, posY, width, height)

        # Creazione delle hitbox superiore e inferiore
        self.hitboxTop = pygame.Rect(posX, posY, width, height // 3)  # Hitbox superiore (1/3 dell'altezza)
        self.hitboxBottom = pygame.Rect(posX, posY + (2 * height // 3), width, height // 3)  # Hitbox inferiore (1/3 dell'altezza)

    # Metodo per mostrare il player a schermo
    def display (self):
        screen.blit(self.playerImg, (self.posX, self.posY))

    # Metodo per ribaltare e mostrare il secondo player a schermo
    def display_flipped(self):
        flipped_image = pygame.transform.flip(self.playerImg, True, False)
        screen.blit(flipped_image, (self.posX, self.posY))
    
    # Metodo per aggiornare la posizione del player in base all'input
    def update(self, XLato, Ylato):
        self.posX = self.posX + self.speed * XLato
        self.posY = self.posY + self.speed * Ylato

        # Blocca il player se cerca di uscire dai limiti della finistra
        if self.posY <= 0:                          # Limiti verticali
            self.posY = 0
        elif self.posY + self.height >= HEIGHT:
            self.posY = HEIGHT - self.height
        if self.posX <= 0:                          # Limiti orizzontali
            self.posX = 0
        elif self.posX + self.width >= WIDTH:
            self.posX = WIDTH - self.width
        
        # Aggiorna le hitboxs del player in base alla sua attuale posizione
        self.hitboxPlayer.topleft = (self.posX, self.posY)
        self.hitboxTop.topleft = (self.posX, self.posY)
        self.hitboxBottom.topleft = (self.posX, self.posY + (2 * self.height // 3))

    # Posizione di restart
    def reset1(self):
        self.posX = Player_DistanceX
        self.posY = HEIGHT * 10 / 25
    def reset2(self):
        self.posX = WIDTH - Player_DistanceX * 2
        self.posY = HEIGHT * 10 / 25

    # Metodo per visualizzare il punteggio a schermo
    def displayScore(self, text, score, x, y, color):
        text = font.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)

    # Metodi per ottenere le hitboxs del player
    def getRect(self):
        return self.hitboxPlayer
    def getTopRect(self):
        return self.hitboxTop
    def getBottomRect(self):
        return self.hitboxBottom
    
class Ball:
    # Inizializzazione della palla con posizione, raggio, velocità e colore
    def __init__(self, posX, posY, radius, speed, color):
        self.posX = posX
        self.posY = posY
        self.radius = radius
        self.speed = speed
        self.color = color
        # Direzioni iniziali della palla
        self.xFac = 0
        self.yFac = 0
        self.is_moving = False # Palla inizia da ferma

        self.hitboxBall = pygame.Rect(self.posX - self.radius, self.posY - self.radius, self.radius * 2, self.radius * 2) # Creazione hitbox palla

    def display(self):
        self.ball = pygame.draw.circle(screen, self.color, (self.posX, self.posY), self.radius)

    def update(self, playerSpeed):
        # Movimento palla
        if self.is_moving:
            self.playerSpeed = playerSpeed
            self.posX += (self.playerSpeed - self.speed) * self.xFac
            self.posY += (self.playerSpeed - self.speed) * self.yFac

        # Aggiorna la hitbox della palla in base alla sua posizione attuale
        self.hitboxBall.topleft = (self.posX - self.radius, self.posY - self.radius)

        # Controllo dei limiti verticali (alto e basso)
        if self.posY - self.radius <= 0:  
            self.posY = self.radius       
            self.yFac *= -1               
        elif self.posY + self.radius >= HEIGHT:  
            self.posY = HEIGHT - self.radius     
            self.yFac *= -1                      

        # Controllo dei limiti orizzontali (sinistra e destra)
        if self.posX - self.radius <= 0:  
            self.posX = self.radius       
            self.xFac *= -1               
        elif self.posX + self.radius >= WIDTH:  
            self.posX = WIDTH - self.radius     
            self.xFac *= -1                     
    
    # Reset della palla al centro del campo (palla ferma)
    def reset(self):
        self.posX = WIDTH // 2
        self.posY = HEIGHT // 2
        self.xFac = 0
        self.yFac = 0
        self.is_moving = False

    # Metodo per cambiare la direzione della palla quando viene colpita
    def hit(self):
        if not self.is_moving:
            self.xFac = 1 if self.posX < WIDTH // 2 else -1
            self.yFac = -1 if self.posY < HEIGHT // 2 else 1
            self.is_moving = True
        else:
            self.xFac *= -1

    # Metodo per ottere la hitbox della palla
    def getRect(self):
        return self.hitboxBall

# Preparazione zone dove è possibile effettuare punti
class Goal:
    def __init__(self, x, y, width, height):
        self.zone = pygame.Rect(x, y, width, height)

    def display(self):
        pygame.draw.rect(screen, WHITE, self.zone, 2)

    def getRect(self):
        return self.zone
        

# Funzionamento principale del gioco
def main():
    running = True

    # Creazione dei due player e della palla con dimensioni proporzionate alla finestra
    player1 = Player(Player_DistanceX, HEIGHT * 10 / 25, PLAYER_SPEED * 2, WIDTH / 10, HEIGHT / 6)
    player2 = Player(WIDTH - Player_DistanceX * 2, HEIGHT * 10 / 25, PLAYER_SPEED * 2, WIDTH / 10, HEIGHT / 6)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 10, 2, BLACK)

    # Creazione delle zone goal
    zona_goal1 = Goal(0, HEIGHT // 2 - 100, 30, 200)
    zona_goal2 = Goal(WIDTH - 30, HEIGHT // 2 - 100, 30, 200)

    ListOfCars = [player1, player2]

    # Inizializzazione delle variabili per controllare il movimento dei players e il punteggio
    p1XLato, p1YLato = 0, 0
    p2XLato, p2YLato = 0, 0
    p1Score, p2Score = 0, 0

    while running:
        # Gestione eventi del gioco
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Input movimento Player 2 (freccette)
                if event.key == pygame.K_UP:
                    p2YLato = -1
                if event.key == pygame.K_DOWN:
                    p2YLato = 1
                if event.key == pygame.K_LEFT:
                    p2XLato = -1
                if event.key == pygame.K_RIGHT:
                    p2XLato = 1
                # Input movimento Player 1 (WASD)
                if event.key == pygame.K_w:
                    p1YLato = -1
                if event.key == pygame.K_s:
                    p1YLato = 1
                if event.key == pygame.K_a:
                    p1XLato = -1
                if event.key == pygame.K_d:
                    p1XLato = 1
            # Controllo rilascio input player (stop movimento)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    p2YLato = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    p2XLato = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    p1YLato = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    p1XLato = 0

        # Controllo collisione tra player e palla
        for cars in ListOfCars:
            if pygame.Rect.colliderect(ball.getRect(), cars.getRect()):
                ball.hit()
            # Controllo se la palla colpisce la hitbox superiore
            if pygame.Rect.colliderect(ball.getRect(), cars.getTopRect()):
                ball.yFac = -1
            # Controllo se la palla colpisce la hitbox inferiore
            if pygame.Rect.colliderect(ball.getRect(), cars.getBottomRect()):
                ball.yFac = 1

        # Aggiornamento degli stati degli oggetti
        player1.update(p1XLato, p1YLato)
        player2.update(p2XLato, p2YLato)
        ball.update(PLAYER_SPEED)

        # Controllo collisione con le zone goal
        if pygame.Rect.colliderect(ball.getRect(), zona_goal1.getRect()):
            p2Score += 1
            ball.reset()
            player1.reset1()
            player2.reset2()
        elif pygame.Rect.colliderect(ball.getRect(), zona_goal2.getRect()):
            p1Score += 1
            ball.reset()
            player1.reset1()
            player2.reset2()

        # Disegno dello sfondo e degli oggetti su schermo
        screen.blit(BackgroundImg, (0, 0))
        player1.display()
        player2.display_flipped()
        ball.display()

        # Disegno delle zone goal
        zona_goal1.display()
        zona_goal2.display()

        # Visualizzazione punteggi
        player1.displayScore("Player_1 : ", p1Score, 100, 20, BLACK)
        player2.displayScore("Player_2 : ", p2Score, WIDTH - 100, 20, BLACK)

        pygame.display.update()
        clock.tick(FPS)
    
if __name__ == "__main__":
    main()
    pygame.quit()