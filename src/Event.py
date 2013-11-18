from weakref import WeakKeyDictionary
class Event(object):
    ''' Events that can be handled by EventManager
    '''
    kind = 'generic'

    def __init__(self):
        '''
        Set the name of the event, Subclass may have other attributes
        '''
        self.name = 'Generic'
        self.sync = 'True'

    def __repr__(self):
        '''
        Custom representation of the event
        '''
        return self.name + 'Event'

    def attributes(self):
        result = ''
        for attr in self.__dict__.keys():
            if attr[:2] == '__':
                result = result + '\tattr %s=\n' %attr
            else:
                result = result + '\tattr %s=%s\n' %(attr, self.__dict__[attr])
        return result

    def __getitem__(self, item):
        if item in self.__dict__.keys():
            return self.__dict__[item]
        return None

    def hasAttribute(self, attr):
        return attr in self.__dict__.keys()

class TickEvent(Event):
    '''
    Tick events are intended to be time events.
    They indicate the speed of the program
    '''
    kind = 'tick'

    def __init__(self, time = None):
        Event.__init__(self)
        '''Set the name and the tick properities'''
        self.name = 'Tick'
        self.tick = time


class EventManager(object):
    def __init__(self):
        '''
        Set up a dictionary to hold references to listeners
        '''
        self.listeners = WeakKeyDictionary()

    def register(self, listener):
        '''
        Register a listener. It must implement the function notify(event)
        '''
        self.listeners[listener] = 1

    def unregister(self, listener):
        '''
        Unregister a listener
        '''
        if listener in self.listeners:
            del self.listeners[listener]

    def post(self, event):
        '''
        Inform all listeners about an event
        '''
        for listener in self.listeners:
            listener.notify(event)

class Manager(object):
    '''
    A collection of EventManagers, filtered by event kinds.
    '''
    def __init__(self):
        self.managers = {}
        self.events = []

    def register(self, clazz, listener):
        self.add(clazz)
        self.managers[clazz.kind].register(listener)

    def add(self, clazz):
        if not clazz.kind in self.managers:
            self.managers[clazz.kind] = EventManager()

    def drop(self, clazz):
        self.managers[clazz.kind] = None

    def registerAll(self, listener):
        '''
        Register for all managers
        '''
        for kind in self.managers:
            self.managers[kind].register(listener)

    def unregister(self, clazz, listener):
        if clazz.kind in self.managers:
            self.managers[clazz.kind].unregiseter(listener)

    def unregisterAll(self, listener):
        for kind in self.managers:
            self.managers[kind].unregister(listener)

    def post(self, event):

        if event.kind == TickEvent.kind:
            self.events.append(event)
            temp = self.events
            self.events = []
            for e in temp:
                if e.kind in self.managers:
                    self.managers[e.kind].post(e)
            else:
                if event.sync:
                    self.events.append(event)
                else:
                    for event.kind in self.managers:
                        self.managers[event.kind].post(event)

class Listener(object):
    '''
    A superclass for listeners. Note that a listener must save the reference
    to the manage if it needs to send events, as opposed to just recieve them.
    '''
    def __init__(self, manager):
        '''
        Register with the manager automatically
        '''
        manager.registerAll(self)

    def notify(self, event):
        '''
        Default implementation for recieving events.
        '''
        pass

################################################################################
# Test
################################################################################
if __name__ == '__main__':
    e = Event()
    print Event
    em = EventManager()

    class Test(Listener):
        def notify(self, event):
            print 'I have recieved a ' + str(event)

    test = Test(em)

    em.post(e)

    e = TickEvent()
    print e[TickEvent.kind]
    e = TickEvent('hi')
    print e[TickEvent.kind]

    print e['anotherAttribute']
