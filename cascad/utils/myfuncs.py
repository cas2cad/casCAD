"""
swtich
"""

class switch(object):
    """             # for case in switch(key):
                    #     if case('$oid'):
                    #         return ObjectId(item)
                    #         break
                    #     if case('$date'):
                    #         return datetime.fromtimestamp(item/1000)
                    #         # datetime.utcfromtimestamp(item)
                    #         break
                    #     if case():
                    #         break
    """
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

"""
单例模式
"""
# from threading import Lock

# class Singleton(type):
#     _instances = {}
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#                 cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]

import threading
class Singleton(type):
  _instance_lock = threading.Lock()
  def __call__(cls, *args, **kwargs):
    if not hasattr(cls, "_instance"):
      with Singleton._instance_lock:
        if not hasattr(cls, "_instance"):
          cls._instance = super(Singleton,cls).__call__(*args, **kwargs)
    return cls._instance

class Foo(metaclass=Singleton):
  def __init__(self):
    pass