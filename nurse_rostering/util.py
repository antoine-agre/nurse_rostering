import os

def findFilenameWithoutExtension(path):
    
    folderSep = os.path.sep
    filename = path.split(folderSep)[-1]
    return filename.split(".")[0]