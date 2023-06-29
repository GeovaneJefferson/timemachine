from setup import *

def restart_kde_session():
    sub.Popen("kquitapp5 plasmashell; kstart5 plasmashell",shell=True)
