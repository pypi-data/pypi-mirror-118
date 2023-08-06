#!/usr/bin/python3

from lazyt import *
import os

def yonex():
    proceed=lazyt.yon("Would you like to proceed?")
    # >>>Would you like to proceed?[Y/n]:
    if(proceed):
        print("ok, proceed")
    else:
        print("never mind, bye")
        exit(0)

    #Default param is True, for setting it to False use:
    proceed=lazyt.yon("Would you like to proceed?",deaf=False)
    # >>>Would you like to proceed?[y/N]:
    if(proceed):
        print("ok, proceed")
    else:
        print("never mind, bye")
        exit(0)

def clearex():
    trash=os.urandom(10000)
    print("{}\n\nThere's something on your console!".format(trash))
    input("Press any button to wipe it away!")
    lazyt.clear_console()
    print("You're welcome.\n")


def bannerex():
    options=['first choice','second choice','third choice',
            'fourth choice','fifth choice','sixth choice']

    print(lazyt.create_banner(options))
    #>>> [0] first choice 	[1] second choice	[2] third choice
    #>>> [3] fourth choice	[4] fifth choice 	[5] sixth choice

    #Default number of cols is 3
    print(lazyt.create_banner(options,cols=2))
    #>>> [0] first choice 	[1] second choice
    #>>> [2] third choice 	[3] fourth choice
    #>>> [4] fifth choice 	[5] sixth choice


def loaderex():
    import time

    l = Loader("While working message...", "Work done message!", 0.05).start()
    #>>>While working message... ⣽
    for i in range(10):
        time.sleep(0.25)
    l.stop()
    #delete the working message and write
    #>>>Work done message!


def tprintex():
    tprint.info("info, yellow text")
    #>>>(yellow)info, yellow text
    tprint.error("error, red text")
    #>>>(red)error, red text
    tprint.system("system, blue text")
    #>>>(blue)system, blue text


def int_choiceex():
    print(lazyt.int_choice(min=-1,banner="Value higher than -1",error_message="This number is lower than -1"))
    print(lazyt.int_choice(max=123))


def main():
    int_choiceex()
    yonex()
    bannerex()
    loaderex()
    tprintex()
    clearex()



if __name__ == '__main__':
	main()
