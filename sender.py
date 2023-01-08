import eel

from Practice import practice

eel.init('Interface')

@eel.expose
def python_log(x):
    print(x)


eel.start('main_menu.html', size=(1920, 1080))  # Start the web.
