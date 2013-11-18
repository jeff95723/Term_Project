import Event, pygame
#test

class QuitEvent(Event.Event):
    kind = 'quit'
    def __init__(self, quitter = True):
        Event.Event.__init__(self)
        self.name = 'Quit'
        self.quit = quitter
        self.sync = False

class FibonacciEvent(Event.Event):
    kind = 'fibonacci'

    def __init__(self, number = None):
        Event.Event.__init__(self)
        self.name = "Fibonacci"
        self.fibonacci = number

class TickGeneratorController(Event.Listener):
    FPS = 30
    def __init__(self, manager):
        self.manager = manager
        self.manager.register(QuitEvent.kind, self)

        self.running = True

        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            self.manager.post(Event.TickEvent(pygame.time.get_ticks()))
            self.clock.tick(self.FPS)

    def notify(self, event):
        if event[QuitEvent.kind]:
            self.running = False


class QuitController(Event.Listener):
    def __init__(self, manager, goalAttribute, goalValue):
        self.manager = manager
        self.manager.register(goalAttribute, self)

        self.goalAttribute = goalAttribute
        self.goalValue = goalValue


    def notify(self, event):
        if event[self.goalAttribute] >= self.goalValue:
            event = QuitEvent()
            self.manager.post(event)


class EventLoggerView(Event.Listener):
    '''
    Logs Events to the screen. Note that it does not define init
    it uses the default listener
    '''
    def notify(self, event):
        print event
        print event.attributes()


class FibonacciModel(Event.Listener):
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

def main():
    manager = Event.Manager()
    manager.add(Event.TickEvent.kind)
    manager.add(FibonacciEvent.kind)
    manager.add(QuitEvent.kind)

    model = FibonacciModel(manager)
    view = EventLoggerView(manager)
    controller = TickGeneratorController(manager)

    #stop1 = QuitController(manager, Event.TickEvent.kind, TickGeneratorController.FPS * 50)
    stop2 = QuitController(manager, FibonacciEvent.kind, 1000)

    controller.run()

if __name__ == '__main__':
    main()
