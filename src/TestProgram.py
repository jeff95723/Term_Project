import Event, pygame

class TickGeneratorController(Event.Listener):
    def __init__(self, manager):
        self.manager = manager
        self.manager.register(self)

        self.running = True

        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            event = Event.Event()
            event.tick = pygame.time.get_ticks()
            self.manager.post(event)
            self.clock.tick(30)

    def notify(self, event):
        if event.hasAttribute('quit'):
            self.running = False


class QuitAtGoalController(Event.Listener):
    def __init__(self, manager):
        self.manager = manager
        self.manager.register(self)

        FPS = 30
        self.stopAfterTick = 5*FPS

    def notify(self, event):
        if event.hasAttribute('tick') and event.tick >= self.stopAfterTick:
            event = Event.Event()
            event.quit = False
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
        self.last = 0
        self.current = 1

        print "NUMBER: %s" %self.current

    def notify(self, event):
        self.last, self.current = self.current, self.last+self.current

        print "Number: %s" % self.current
        #event = Event.Event()
        #event.number = self.current
        #self.manager.post(event)

def main():
    manager = Event.EventManager()
    model = FibonacciModel(manager)
    view = EventLoggerView(manager)
    controller = TickGeneratorController(manager)

    stop = QuitAtGoalController(manager)

    controller.run()

if __name__ == '__main__':
    main()
