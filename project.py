import pygame
import neat
import time
import os
import random

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird:
    # These are the class variables not the instance variables
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25  # How much the bird is gonna tilt when the bird moves up or down
    ROT_VEL = 20       # How much we are going to rotate on each frame or each time we move the bird
    ANIMATION_TIME = 5 # How fast the bird is going to flapping it's wings

    def __init__(self, x, y):
        self.x = x           # This represents the starting position of our bird
        self.y = y
        self.tilt = 0       # How much the image is actually tilted
        self.tick_count = 0  # The physics of our bird when we jump or when we fall down
        self.vel = 0
        self.height = self.y
        self.img_count = 0   # So that we know which image we are showing for the bird so that we can animate it and keep track of that
        self.img = self.IMGS[0]

    # The function we call when we want the bird to flap up and jump upwards
    def jump(self):
        self.vel = -10.5     # When we move up, the velocity is negative in the y direction cuz the origin is at the top-left
        self.tick_count = 0  # Keep track of when we last jump, we need to know when we are changing directions or changing velocities for our physical formulars in the next method to work
        self.height = self.y # Keep track of where do the bird jump from, or where do we originally started moving from

    # What we call every single frame to move our bird
    def move(self):
        self.tick_count += 1 # This represented that a tick heppened or a frame went by, keeping track of how much we moved since the last jump

        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2 # This is what we end up actually moving, based on the bird's current velocity. self.tick_count is keeping track of how many seconds we've been moving for since the last jump

        if d >= 16: # Make sure we don't have a velocity moving way to far up or way to far down
            d = 16
        if d < 0: # Make the bird move up a bit more if we are moving upwards, fine tunes our movement a little bit
            d -= 2

        self.y = self.y + d

        # After we know whether we are moving up or down, we also know whether we need to tilt up or down
        if d < 0 or self.y < self.height + 50: # self.height is our original position and self.y is our position after moving
            if self.tilt < self.MAX_ROTATION:  # Making sure we don't tilt the bird backwards
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL # When we tilt up, we want to only tilt slightly up, but when we tilt down, we want to go all the way down

    def draw(self, win):
        self.img_count += 1 # We need to keep track of how many ticks we've shown the current image for

        if self.img_count < self.ANIMATION_TIME: # We want to show each picture an animation time, and have the wing flap up and flap down
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1: # instantly goes back to it's starting position
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1] # Making sure our bird is not flapping it's wings going down
            self.img_count = self.ANIMATION_TIME * 2 # Making sure that when our bird goes back up, it starts from image 2, and it doesn't skip a frame

        rotated_image = pygame.transform.rotate(self.img, self.tilt) # Tilts our bird
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center) # This makes sure our bird image tilts at the center
        win.blit(rotated_image, new_rect.topleft) # We have the window that's going to be drew to, so we are going to blit the rotated image onto the window

    def get_mask(self): # Based on the image, it gaves us mask, which is a two dimentional list
        return pygame.mask.from_surface(self.img) # this is how we deal with collisions

class Pipe:
    GAP = 200 # How much space are in between of the pipes
    VEL = 5 # How much are the pipes moving, since our birds doesn't move, we need to have our pipes moving backwards

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True) # The last two attributes let the image not to be converted horizontally and to be converted vertically
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False # If the bird is already passed by the pipe. For collision purpose and for our AI later
        self.set_height() # Set an arbitrary height for our pipe
    
    def set_height(self):
        self.height = random.randrange(50, 450) 
        self.top = self.height - self.PIPE_TOP.get_height() # To get the correct position of our top pipe, we need to know the top left position fo the pipe. What we had is the lower bound of the top pipe and we need to subtract the height of the pipe
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL # All we need to do is to change the x posiiton according to the velocity of the pipe
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, win):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)



def draw_window(win, bird): # Draw the background image and draw the bird on top of it
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    pygame.display.update() # This update the display to be after we drew the background and the bird



def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) # Initialize the video system, set up the window for displaying
    clock = pygame.time.Clock() 

    run = True
    # We have a game loop here This is called thirty times a second, we call brid move on the bird objects we have and it will
    while run:
        clock.tick(30) # We are going to do at most 30 tick every second 
        for event in pygame.event.get(): # Keep track of whenever something happens like when user click the mouse
            if event.type == pygame.QUIT: # If we click the close button on our window, we are going to quit the game
                run = False
        bird.move()        
        draw_window(win, bird)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
