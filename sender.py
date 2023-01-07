import eel

from Practice import practice

eel.init('Interface')

@eel.expose
def python_log(x):
    print(x)


eel.start('main_menu.html', size=(1500, 900))  # Start the web.
