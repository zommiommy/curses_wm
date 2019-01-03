
import curses

def horrible_workaround(f):
    """On resize the draw text and the move window crash when the window get smaller TODO FIX THIS MESS"""
    def wrapped(*arg,**kwargs):
        try:
            return f(*arg,**kwargs)
        except curses.error:
            pass
    return wrapped
