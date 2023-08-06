from typing import Union
import color as c
from color import red
import sys
from threading import Timer
from time import sleep
from json import dumps

k = 0
val = 0


class SetInterval:
    """
    Set interval 
  @param interval:
    Time to perform function.
    In Seconds
  @param  Function:
    function to perform
  @param  end:
    Time to end interval after
    Defaults to 1000 seconds
  @param lock:
    If to allow execution of other codes 
    """

    def __init__(self, interval:Union[int, float], function, end:int=1000, callback:bool=None, \
                show_progress:bool=False, req:bool=False, args:list=None, kwargs:dict=None):
        global k, val
        self.k = k
        self.callback = callback
        k = self.k
        self.interval = interval
        self.function = function
        self.end = int(end)
        self.show_progress = show_progress
        if show_progress:
            self.progress = ProgressBar(len=end, color="green")
            if self.end > 50:
                self.progress.set_len(self.end//50)
        self.req = req
        self.args = args
        self.val = val
        self.kwargs = kwargs
        self._interval()

    def _interval(self):
        global val
        self.k2 = Timer(self.interval, self._interval)
        self.k = self.k+1
        if self.show_progress:
            if self.end > 50:
                if self.end // 50 == 0:
                    self.progress.pulse()
            else:
                self.progress.pulse()
        kwargs = self.kwargs
        args = self.args
        if self.req and self.args is None and self.kwargs is None:
            val = self.function(self)
        elif self.args is not None and self.req:
            val = self.function(self, *self.args)
        elif self.args is not None and self.kwargs and self.req:
            val = self.function(self, *self.args, **kwargs)
        elif self.kwargs is not None and self.req:
            val = self.function(self, **kwargs)
        elif self.kwargs is not None:
            val = self.function(**kwargs)
        elif self.args is not None:
            val = self.function(*args)
        else:
            val = self.function()
            
        self.val = val
        if self.k == self.end:
            self.cancel()
            return

        self.k2.start()

    def cancel(self):
        self.k = self.end
        self.k2.cancel()
        if self.callback is not None: 
            self.callback()
        val = self.val
        del self
        return val


class InvalidColor(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = "No Such Color"
    pass


class Print:
    """Print Letters individualy according to given time
    Usage
    -----
    >>> from niceprint import Print
    >>> Print(\"Hello\",color=\"red\",time=0.1)
    Hello

    Exceptions
    ----------
    Throws InvalidColor exception is the color
    is not in color list

    Accepted colors:
    ---------------
    To get the accepted colors 
    >>> from niceprint import Print
    >>> Print.get_colors()
    """
    colors = ['red', 'green', 'blue', 'magenta',
              'black', 'yellow', "cyan", None]

    @staticmethod
    def get_colors():
        return Print.colors[:]

    def _process_color(self, c):
        Print.colors[4] = "kblack"
        if c in Print.colors:
            return Print.colors[Print.colors.index(c)]
        if c in [c[0] for c in Print.colors[:len(Print.colors)-1]]:
            oc = [c[0] for c in Print.colors[:len(Print.colors)-1]]
            Print.colors[4] = "black"
            return Print.colors[oc.index(c)]

    def _get_text(self):

        if self.color is not None:
            print(eval(f"c.{self.color}")(
                (self.text[self.i])), end="", flush=True)
        else:
            print(self.text[self.i], end="", flush=True)

        self.i += 1
        if self.i == len(self.text):
            print()

    def _print(self, *args):
        self.inter = SetInterval(
            self.time, self._get_text, len(self.text))

    def _locking_print(self):
        for i, t in enumerate(self.text, 0):
            if self.color is not None:
                print(eval(f"c.{self.color}")(
                    (t)), end="", flush=True)
            else:
                print(t, end="", flush=True)
            try:
                sleep(self.time)
            except KeyboardInterrupt:
                print("\n", red("[INFO] : Canceled"))
                break

    def __init__(self, *text, color=None, time=0.03, lock=True, end="\n", format=False):
        for ind, content in enumerate(text, 0):
            self.i = 0
            if type(content) is dict:
                content = dumps(content, indent=2)
            self.text = [x for x in str(content)]
            self.inter = None
            r_e = color not in [c[0]
                                for c in Print.colors[:len(Print.colors)-1]]
            r_e2 = color not in Print.colors
            if r_e is True and r_e2 is True:
                raise InvalidColor(
                    f"{color} Color is not in the list of colors")
            if color == "k":
                self.color = "black"
            else:
                self.color = self._process_color(color)
            self.time = time
            if lock:
                self._locking_print()
            else:
                self._print()
            print(end=end)
        print()
        return


class MultiColoredPrint:
    """
    MultiColoredPrint
    ----------------------
    Prints words or text individually according to the given time and color
    
    Usage
    -------
    >>> from niceprint import MultiColoredPrint as MP
    >>> text = \"Multiple Text\"
    >>> MP(text, color=[\'c\', 'g'])
    """
    @staticmethod
    def get_colors():
        return Print.colors
    def __init__(self, *args, color: list = [''], delimiter=" ", time: list = [0.03], lock: bool = True):
        args = [str(x) for x in args]
        if len(args) == len(color):
            for ind, text in enumerate(args, 0):
                Print(text, color=color[ind], end=delimiter, lock=lock)
            print()
        elif len(args) < len(color):
            la = len(args)
            lc = len(color)
            ll = lc//la
            for ind, text in enumerate(args):
                tt = text.split(" ")
                tt_ = []
                n = int(round(len(tt)/ll, 0))
                s = 0
                constn = n
                for t in range(ll):
                    tt_.append(" ".join(tt[s:n]))
                    s = n
                    temp = n
                    n += constn
                for ind_, wt in enumerate(tt_):
                    Print(wt, color=color[ind_], end=delimiter, lock=lock)
        pass
        
class ProgressBar:
    def _process_len(self, *args):
        self.diff = 1
        if self.len > 20:
            self.diff = self.len//20
            self.len = 20
    def __init__(self, len=10, color="", bg="", char="#", **kwargs):
        self.len = len
        self._old_len = len
        self._process_len()
        len = self.len
        self.color = color
        self.tick = 0
        self.charcter = char
        if char==" ":
            color = ""
        if color != "":
            try:
                char = eval(f"c.{color}")(char)
            except Exception as e:
                color = ""
                print(e)
        self.char = char
        start = "["
        stop = ']'
        bar = f"[" + " "*len + "]"
        self.pg = 0
        self.chw = 0
        sys.stdout.write(u"\u001b[1000D"+bar)
        sys.stdout.flush()
        
    def set_len(self, len):
        self.len = len
        self.pulse()
        
    def fill(self, ms=10, sec=None):
        char=self.char
        self.len = self.len-self.pg
        if sec is not None:
            t = sec
        elif ms is not None:
            t = ms/100
        for _ in range(self.len+1):
            sleep(t)
            bar = "[" + (char*(self.pg+_)) +" "*(self.len-_) + "]"
            self.tick += 1
            sys.stdout.write(u"\u001b[1000D"+bar)
            sys.stdout.flush()
        print()
    def set_color(self, color):
        if color != "":
            try:
                self.char = eval(f"c.{color}")(self.charcter)
                self.color = color
            except Exception as e:
                color = ""
                print(e)
                return False
            return True
    def set_char(self, char, *args):
        try:
            self.char = eval(f"c.{self.color}")(char)
            self.charcter = char
            return True
        except Exception as e:
            print(e)
            return False
    
    #def pulse(self, step=1, ms=1, sec=None):
        #try:
        #    self._pulse(step=1, ms=1, sec=None)
        #except Exception as e:
        #    MultiColoredPrint("ProgressBar interupted", e, color="mr")
    
    def pulse(self, step=1, ms=1, sec=None):
        if step > 1:
            self.len = self._old_len*2
            self._process_len()
        if self.len <= self.pg:
            return
        try:
            t = ms/100 if sec is None else sec
            sleep(t)
        except Exception as e:
            Print("[ERROR] : ", e, color="r")
        char = self.char
        self.tick += 1
        self.chw = step
        
        if self.tick % self.diff == 0:
            self.pg += step
            bar = "[" + (char*(self.pg)) +" "*(self.len-self.pg) + "]"
            sys.stdout.write(u"\u001b[1000D"+bar)
            sys.stdout.flush()
        if self.pg == self.len:
            print()

if __name__ == "__main__":
    MultiColoredPrint(
        """Print Letters individualy according to given time
    Usage
    -------
    >>> from niceprint import Print
    >>> Print(\"Hello\",color=\"red\",time=0.1)
    Hello
    
    Exceptions
    ----------
    Throws InvalidColor exception is the color
    is not in color list

    Accepted colors:
    --------------
    To get the accepted colors 
    >>> from niceprint import Print
    >>> Print.get_colors()
    """, color='mgr')
    ProgressBar().fill()

