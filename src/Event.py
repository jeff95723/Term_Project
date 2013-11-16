from weakref import WeakKeyDictionary
class Event(object):
    ''' Events that can be handled by EventManager
    '''

    def __init__(self):
        '''
        Set the name of the event, Subclass may have other attributes
        '''
        self.name = 'Generic'

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

    def hasAttribute(self, attr):
        return attr in self.__dict__.keys()



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

class Listener(object):
    '''
    A superclass for listeners. Note that a listener must save the reference
    to the manage if it needs to send events, as opposed to just recieve them.
    '''
    def __init__(self, manager):
        '''
        Register with the manager automatically
        '''
        manager.register(self)

    def notify(self, event):
        '''
        Default implementation for recieving events.
        '''
        pass


