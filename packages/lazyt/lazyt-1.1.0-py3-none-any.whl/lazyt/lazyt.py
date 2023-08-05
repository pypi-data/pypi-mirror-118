
class lazyt:

    def yon(question,deaf=True):
        """
        This function prompt the question and allow the user to answer
        with y/n enabling a default option;

        Return value: bool
        """

        yn=""
        if(deaf):
            yn=" [Y/n]"
        else:
            yn=" [y/N]"
        while "The answer is not valid":
            reply = str(input(question+yn+': ')).lower().strip()
            if len(reply) == 0:
                return deaf
            if reply[:1] == 'y':
                return True
            if reply[:1] == 'n':
                return False

    def clear_console():
        """
        This function will clear the console.
        """

        import platform
        import os,sys
        if(platform.os == "Windows"):
            os.system("cls")
        else:
            os.system("clear")

    def create_banner(options,cols=3):
        """
        This function will return a string "display-ready" with all the element of
        the options array as choice.
        #>>> [0] first choice   [1] second choice
        #>>> [2] third choice   [3] fourth choice

        Return value: str
        """

        tmp=[]
        data=[]
        base_banner=''
        l = len(options)
        for x in range(1,l+1):#create an array of <cols> array, every array is a row
            s = str('[{}] {}'.format(x-1,options[x-1]))
            tmp.append(s)
            if( x % cols == 0):
                data.append(tmp)
                tmp=[]
        tmp=[]

        if(l-(l-cols)-l>0):
            for x in range(l-(l-cols),l):#add the remaining(carriage) element to the last row-array
                tmp.append(str('[{}] {}'.format(x,options[x])))
            data.append(tmp)

        longest_string =len(max(data[0], key=len)) #get the longest string in the first array, as reference
                                                    #will use this for the padding

        for x in data:#find the longest
            if (longest_string < len(max(x, key=len))):
                longest_string = len(max(x, key=len))

        for x in data:
            for el in x:
                while True:#add padding and make every option of the same length
                    if(len(el) < longest_string):
                        el+=' '
                    else:
                        break
                base_banner +=el+'\t'#add a tab between every option
            base_banner+='\n'#and of row, new line

        return str(base_banner)


class tprint:

    def error(content):
        from sty import fg, bg, ef, rs
        """
        print red text
        """
        print(fg.red + content +fg.rs)

    def info(content):
        from sty import fg, bg, ef, rs
        """
        print yellow text
        """
        print(fg.yellow + content +fg.rs)

    def system(content):
        from sty import fg, bg, ef, rs
        """
        print blue text
        """
        print(fg.blue + content +fg.rs)

class Loader:#ok this one is stolen, don't rember where, i'm sorry:(

    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        from threading import Thread
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        ========== EXAMPLE
        with Loader("work in progress text","work is ended text"):
                print("at the end of these operations it will end by itself")

        loader = Loader("Loading with object...", "That was fast!", 0.05).start()
        for i in range(10):
            sleep(0.25)
        loader.stop()
        """

        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        from itertools import cycle
        from sty import fg, bg, ef, rs
        import time
        for c in cycle(self.steps):
            if self.done:
                break
            print(fg.yellow +f"\r{self.desc} {c}"+fg.rs, flush=True, end="")
            time.sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        from shutil import get_terminal_size
        from sty import fg, bg, ef, rs
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(fg.blue +f"\r{self.end}"+fg.rs, flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()
