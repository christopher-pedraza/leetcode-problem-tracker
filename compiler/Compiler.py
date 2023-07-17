import PyInstaller.__main__

PyInstaller.__main__.run([
    '..\\ProblemTracker.py',
    '--onefile',
    '--icon=res\\icon.ico',
    '--distpath=..\\'
])