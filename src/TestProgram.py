import math, pygame
from pygame.locals import *
from Event import *


class QuitEvent(Event):
    kind = 'quit'

    def __init__(self, quitter = True):
        Event.__init__(self)
        self.name = 'Quit'
        self.quit = quitter
        self.sync = False

class FibonacciEvent(Event):
    kind = 'fibonacci'

    def __init__(self, number = None):
        Event.Event.__init__(self)
        self.name = "Fibonacci"
        self.fibonacci = number

class GameTimerEvent(Event):
    kind = 'gameTimer'

    def __init__(self, time = None):
        Event.__init__(self)
        self.name = "Game Timer"
        if not time:
            self.gametimer = pygame.time.get_ticks()
        else:
            self.gametimer = time

class PauseEvent(Event):
    kind = 'pause'

    def __init__(self, pause = None):
        Event.__init__(self)
        self.name = 'Pause'
        self.pause = pause

class TickGeneratorController(Listener):
    FPS = 50
    def __init__(self, manager):
        self.manager = manager
        self.manager.register(QuitEvent, self)

        self.running = True

        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            self.manager.post(TickEvent(pygame.time.get_ticks()))
            self.clock.tick(self.FPS)

    def notify(self, event):
        if event[QuitEvent.kind]:
            self.running = False


class QuitController(Listener):
    def __init__(self, manager, goalClass, goalValue):
        self.manager = manager
        self.manager.register(goalClass, self)

        self.goalAttribute = goalClass.kind
        self.goalValue = goalValue


    def notify(self, event):
        if event[self.goalAttribute] >= self.goalValue:
            event = QuitEvent()
            self.manager.post(event)


class EventLoggerView(Listener):
    '''
    Logs Events to the screen. Note that it does not define init
    it uses the default listener
    '''
    def notify(self, event):
        print event
        print event.attributes()


class FibonacciModel(Listener):
    '''
    Stores some simple information and changes itself on updates.
    This class will generate events so that we can log them.
    '''
    def __init__(self, manager):
        Event.Listener.__init__(self, manager)
        self.manager = manager

        self.last = 0
        self.current = 1

        manager.post(FibonacciEvent(self.current))

    def notify(self, event):
        self.last, self.current = self.current, self.last + self.current
        self.manager.post(FibonacciEvent(self.current))

class GraphicClockView(Listener):
    def __init__(self, manager):
        manager.register(TickEvent, self)
        self.size = (400, 400)
        self.origin = (200,200)
        self.radius = 70
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill((0,0,0))

        pygame.draw.circle(self.screen, (255,255,255), self.origin, self.radius, 1)
        pygame.draw.lind(self.screen, (255,255,255), self.origin, (self.origin[0], self.origin[1] + self.radius))
        pygame.display.flip()

    def notify(self, event):
        x = self.origin[0] + self.radius*math.cos(2*math.pi*event.tick/1000)
        y = self.origin[1] + self.radius*math.sin(2*math.pi*event.tick/1000)

        self.screen.fill(black)
        pygame.draw.circle(self.screen, (255,255,255), self.origin, self.radius, 1)
        pygame.draw.line(self.screen, (255,255,255), self.origin, (x,y))
        pygame.display.flip()


class GameTimerModel(Listener):
    def __init__(self, manager):
        manager.register(TickEvent, self)
        manager.register(PauseEvent, self)

        self.manager = manager
        self.last = 0
        self.time = 0
        self.paused = False

    def notify(self, event):
        if not self.paused:
            if event.kind == TickEvent.kind:
                self.time += event.tick - self.last
                self.last = event.tick
            elif event.kind == PauseEvent.kind:
                self.paused = True
                self.time += event.pause - self.last
        else:
            if event.kind == PauseEvent.kind:
                self.paused = False
                self.last = event.pause
        self.manager.post(GameTimerEvent(self.time))

class KeyboardController(Listener):
    def __init__(self, manager):
        self.manager = manager
        manager.register(TickEvent, self)

    def notify(self, event):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.manager.post(QuitEvent())
            elif event.type == KEYDOWN:
                self.manager.post(PauseEvent(pygame.time.get_ticks()))

class ScreenView(Listener):
    def __init__(self, manager):
        pygame.init()
        manager.register(TickEvent, self)
        self.screen = pygame.display.set_mode((400,500))
        self.screen.fill((0,0,0))

    def notify(self, event):
        pygame.display.flip()
        self.screen.fill((0,0,0))

class DisplayClockView(Listener):
    def __init__(self, manager, clazz, screen, rect):
        manager.register(clazz, self)

        self.screen = screen
        self.rect = rect
        self.origin = (rect[0][0]+rect[1][0]/2, rect[0][1]+rect[1][1]/2)
        self.radius = rect[1][0]/4

        self.attr = clazz.kind

    def notify(self, event):
        x = self.origin[0] + self.radius*math.cos(2*math.pi*event[self.attr]/1000)
        y = self.origin[1] + self.radius*math.sin(2*math.pi*event[self.attr]/1000)

        pygame.draw.circle(self.screen, (255,255,255), self.origin, self.radius, 1)
        pygame.draw.line(self.screen, (255,255,255), self.origin, (x,y))


class DisplayTextView(Listener):
    def __init__(self, manager, clazz, screen, rect):
        manager.register(clazz, self)

        self.screen = screen
        self.rect = rect
        self.position  =  rect[0]

        self.font =  pygame.font.SysFont('Arial', 20)

        self.attr = clazz.kind

    def notify(self, event):
        surface = self.font.render( str(event[self.attr]), False, (255,255,255))
        surface = surface.convert()
        self.screen.blit(surface, self.position)


def main():
    manager = Manager()
    manager.add(TickEvent)
    manager.add(FibonacciEvent)
    manager.add(QuitEvent)
    manager.add(GameTimerEvent)
    manager.add(PauseEvent)

    view = EventLoggerView(manager)
    controller = TickGeneratorController(manager)
    screen = ScreenView(manager)

    clock2 = DisplayClockView( manager, GameTimerEvent, screen.screen, ( (0,100), (400,400) ) )
    gametime2 = DisplayTextView( manager, TickEvent, screen.screen, ( (100,100), (0,0) ) )

    keys = KeyboardController(manager)
    timeModel = GameTimerModel(manager)

    print manager.managers.keys()
    print manager.managers['quit'].listeners.keys()
    print manager.managers['tick'].listeners.keys()


    controller.run()

if __name__ == '__main__':
    main()
