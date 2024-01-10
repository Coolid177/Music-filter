from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from mutagen import File
import shutil
import os

# get list of files. The path is the full system path
def getFileList(): 
    fileList = []
    cwd = os.getcwd() + "/Music"
    for root, dirs, files in os.walk(cwd):
        for file in files:
            filePath = os.path.join(root, file)
            fileList.append(filePath)
    return fileList

# create main folder
def createStorageFolder():
    try: 
        os.mkdir("Output")
    except FileExistsError:
        print("Output folder already exists. Not overwriting.")


# create folder with genre
def createMusicFolder(folderName):
    path = os.getcwd() + "/output" + "/" + folderName
    try: 
        os.mkdir(path)
    except FileExistsError:
        print("Folder " + folderName + " already exists. Not overwriting.")

# copy src to dst file. Also copies the metadata that belongs to the file.
def copyFile(src, dst):
    shutil.copy(src, dst)

    try:
        srcAudio = File(src, easy = True)
        dstAudio = File(dst + "/" + os.path.basename(src), easy = True)
        for key, value in srcAudio.items():
            dstAudio[key] = value
        dstAudio.save()
    except: 
        return

def classifySong(genres, file):
    splitGenres = [item.split('/') for item in genres]
    flattenedGenres = [item for sublist in splitGenres for item in sublist]
    if(flattenedGenres == []): 
        createMusicFolder("Various genres")
        copyFile(file, os.getcwd() + "/Output/Various genres")
        return
    for genre in flattenedGenres:
        if(genre.strip() == ""):
            createMusicFolder("Various genres")
            copyFile(file.strip(), os.getcwd() + "/Output/Various genres")
        else: 
            createMusicFolder(genre.strip())
            copyFile(file.strip(), os.getcwd() + "/Output/" + genre.strip())

# open files and read their genre
def main():
    createStorageFolder()
    for file in getFileList():
        extension = os.path.splitext(file)[1].lower()
        if(extension == ".flac"):
            audio = FLAC(file)
            genres = audio.get('genre', [])
            classifySong(genres, file)
        if(extension == ".mp3"):
            audio = EasyID3(file)
            genres = audio.get('genre', [])
            classifySong(genres, file)

main()