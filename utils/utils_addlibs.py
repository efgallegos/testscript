import os
import sys

def HOME():
    return os.path.normpath(os.path.join(os.getcwd(), '..'))

def RESLIB():
    return os.path.normpath(os.path.join(HOME(), 'Resources/ResourcesLib'))

def GTH():
    return os.path.normpath(os.path.join(HOME(), 'Resources/Ontology/GTH'))

def WORKBENCH():
    return os.path.normpath(os.path.join(HOME(), 'Resources/Workbench'))

def TESTS():
    return os.path.normpath(os.path.join(HOME(), 'Tests'))

def addToSysPath(s):
    for x in sys.path:
        if s == x:
            return
    sys.path.insert(0, s)

def addResLib():
    addToSysPath(RESLIB())

def addWorkbench():
    addToSysPath(WORKBENCH())
