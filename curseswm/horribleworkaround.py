
import curses

# Quick disable the workaround to debug stuff
enable_horrible_workaround = True

def horrible_workaround(f):
    """On resize the draw text and the move window crash when the window get smaller TODO FIX THIS MESS"""
    def wrapped(*arg,**kwargs):
            try:
                return f(*arg,**kwargs)
            except curses.error:
                pass

    if enable_horrible_workaround:
        return wrapped
    else:
        return f
