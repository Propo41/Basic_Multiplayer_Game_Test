import pygame

from network import Network

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Player:
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = 1

    def get_size(self):
        return self.x, self.y, 50, 50

    def update(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_player(self):
        # advantage of this over the traditional method is that we can press more than one key at once
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT]:
            self.x -= self.velocity
        if key_pressed[pygame.K_RIGHT]:
            self.x += self.velocity
        if key_pressed[pygame.K_UP]:
            self.y -= self.velocity
        if key_pressed[pygame.K_DOWN]:
            self.y += self.velocity


# converts the string into tuple
# used to read data when sent from server
def read_pos(msg):
    msg = msg.split(',')
    return int(msg[0]), int(msg[1])


# converts tuple into string
# used to send data to server
def make_pos(msg):
    return str(msg[0]) + "," + str(msg[1])


class TangleFight:
    def __init__(self):
        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.n = Network()
        p1_pos = read_pos(self.n.get_pos())  # receives data in format: "x,y" which is converted into tuple
        self.player_1 = Player(WHITE, p1_pos[0], p1_pos[1])
        # this coordinate doesnt matter, as it's gonna be updated inside the game loop
        self.player_2 = Player(RED, 0, 0)
        self.game_loop()

    def game_loop(self):
        while self.running:
            self.fetch_data_from_server()
            self.event_handling()
            self.game_mechanics()
            self.display()
            pygame.display.update()

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def game_mechanics(self):
        self.player_1.move_player()
        pass

    def display(self):
        pygame.display.set_caption("Client")
        self.screen.fill((0, 0, 0))
        # draw rectangle
        pygame.draw.rect(self.screen, WHITE, self.player_1.get_size(), 0)
        pygame.draw.rect(self.screen, RED, self.player_2.get_size(), 0)

    def fetch_data_from_server(self):
        # get position of the other player from server
        p2_pos = read_pos(self.n.send(make_pos((self.player_1.x, self.player_1.y))))
        self.player_2.x = p2_pos[0]
        self.player_2.y = p2_pos[1]
        # self.player_2.update()


TEST = TangleFight()
