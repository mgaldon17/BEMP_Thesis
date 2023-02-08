import platform

win = False
def checkSystem():

    global win
    if platform.system() == "Windows":

        win = True
        DATAPATH = "Z:\MY_MCNP\MCNP_DATA"
        sep = "\\"

    else:
        DATAPATH = "/Users/maga2/MCNP/MCNP_DATA"
        sep = "/"
        pass

    return win, DATAPATH, sep
