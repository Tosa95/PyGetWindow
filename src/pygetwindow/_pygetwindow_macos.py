import logging
import time
from pprint import pformat, pprint

import Quartz

import pygetwindow
from pygetwindow import BaseWindow


def getAllTitles():
    """Returns a list of strings of window titles for all visible windows.
    """

    # Source: https://stackoverflow.com/questions/53237278/obtain-list-of-all-window-titles-on-macos-from-a-python-script/53985082#53985082
    windows = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
    return ['%s %s' % (win[Quartz.kCGWindowOwnerName], win.get(Quartz.kCGWindowName, '')) for win in windows]


def getActiveWindow():
    return getAllWindows()[0]


def getWindowsAt(x, y):
    windows = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
    matches = []
    for win in windows:
        w = win['kCGWindowBounds']
        if pygetwindow.pointInRect(x, y, w['X'], w['Y'], w['Width'], w['Height']):
            matches.append('%s %s' % (win[Quartz.kCGWindowOwnerName], win.get(Quartz.kCGWindowName, '')))
    return matches

def getAllWindows():
    windows = [MacOSWindow(w) for w in Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)]

    windows = [w for w in windows if w.layer == 0]

    windows[0].isActive = True

    return windows




class MacOSWindow(BaseWindow):
    def __init__(self, window_dict):
        super().__init__()
        self._window_dict = window_dict  # TODO fix this, this is a LP_c_long insead of an int.
        self._active = False

    def __str__(self):
        return pformat(self._window_dict)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, MacOSWindow) and self._window_dict == other._window_dict

    def close(self):
        """Closes this window. This may trigger "Are you sure you want to
        quit?" dialogs or other actions that prevent the window from
        actually closing. This is identical to clicking the X button on the
        window."""
        raise NotImplementedError

    def minimize(self):
        """Minimizes this window."""
        raise NotImplementedError

    def maximize(self):
        """Maximizes this window."""
        raise NotImplementedError

    def restore(self):
        """If maximized or minimized, restores the window to it's normal size."""
        raise NotImplementedError

    def activate(self):
        """Activate this window and make it the foreground window."""
        raise NotImplementedError

    def resizeRel(self, widthOffset, heightOffset):
        """Resizes the window relative to its current size."""
        raise NotImplementedError

    def resizeTo(self, newWidth, newHeight):
        """Resizes the window to a new width and height."""
        raise NotImplementedError

    def moveRel(self, xOffset, yOffset):
        """Moves the window relative to its current position."""
        raise NotImplementedError

    def moveTo(self, newLeft, newTop):
        """Moves the window to new coordinates on the screen."""
        raise NotImplementedError

    @property
    def isMinimized(self):
        """Returns True if the window is currently minimized."""
        raise NotImplementedError

    @property
    def isMaximized(self):
        """Returns True if the window is currently maximized."""
        raise NotImplementedError

    @property
    def isActive(self):
        """Returns True if the window is currently the active, foreground window."""
        return self._active

    @isActive.setter
    def isActive(self, active: bool):
        """Returns True if the window is currently the active, foreground window."""
        self._active = active

    @property
    def title(self):
        """Returns the window title as a string."""
        if Quartz.kCGWindowName in self._window_dict:
            return self._window_dict[Quartz.kCGWindowName]
        else:
            logging.info("Unable to get window name. Please check the script has the screen recording permission")
            return self._window_dict[Quartz.kCGWindowOwnerName]

    @property
    def layer(self):
        return self._window_dict[Quartz.kCGWindowLayer]

    @property
    def visible(self):
        raise NotImplementedError

    @property
    def processId(self):
        return self._window_dict[Quartz.kCGWindowOwnerPID]


if __name__ == "__main__":
    pprint([(w.title, w.isActive, w.processId, w.process.name(), w._window_dict) for w in getAllWindows()])

    for i in range(1000):
        active_w = getActiveWindow()
        pprint((active_w.title, active_w.process.name()))

        time.sleep(1)
