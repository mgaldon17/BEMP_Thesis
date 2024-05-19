import platform


def checkSystem():
    is_windows = platform.system() == "Windows"
    if is_windows:
        datapath = "Z:\\MY_MCNP\\MCNP_DATA"
        sep = "\\"
    else:
        datapath = "/Users/galdon/MCNPSimulationScripts/MCNP_DATA"
        sep = "/"

    return is_windows, datapath, sep
