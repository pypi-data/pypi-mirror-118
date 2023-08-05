import os
import Modern_GUI
try:
    Modern_GUI.build(os.getcwd())
    os.chdir('..\\..\\')
    print(f'Build Modern GUI v3.0 in {os.getcwd()}')
except Exception as error:
    print(f'Sorry, An Error Occured While Building Modern GUI v3.0:\n{error}')