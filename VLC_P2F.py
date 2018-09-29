#Title: VLC Playlist-to-Folder
#Description: Takes a VLC playlist and copies all files on the list to a folder.
#Author: dandruk (https://github.com/dandruk)

import os
import shutil
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import ntpath
import xml.etree.ElementTree as etree
from urllib.parse import unquote

#opens dialog window for user to select playlist file
def open_selection():
	root = Tk()
	root.withdraw() #hides tk root window
	root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("VLC playlists","*.xspf"),("all files","*.*")))
	return (root.filename)
	
#extra function to print list of titles in playlist, not used by default
def print_titles(playlist):
	tree = etree.parse(playlist)
	root = tree.getroot()
	trackList = root[1]
	
	print("titles found in " + playlist + ":")
	
	for track in trackList:
		title = track[1]
		print(title.text)

#parses playlist file and returns a list of the full file paths
def get_filenames(playlist):
	tree = etree.parse(playlist)
	root = tree.getroot()
	trackList = root[1]
	
	fileList = []
	
	for track in trackList:
		location = track[0]
		file = location.text.strip('file:///')
		uqFile = unquote(file) #replaces %20 with spaces, etc.
		fileList.append(unquote(uqFile))
			
	return fileList
	
#creates a new directory with the same name as the playlist
#	no error checking yet, will get mad if the directory already exists
def create_directory(path, fileName):
	splitName = os.path.splitext(ntpath.basename(fileName))
	newDir = splitName[0]
	newPath = path + '/' + newDir
	os.mkdir(newPath)
	return newPath
	
#copies files into the newly created directory
def copy_files(list, path):
	newFolder = ntpath.basename(path)
	messagebox.showinfo("Copying Files", "Folder '" + newFolder + "' is being filled...")
	for file in list:
		shutil.copy2(file, path)

#PROGRAM START

selectPath = open_selection() #select playlist file
selectDir = ntpath.dirname(selectPath) #path without filename
selectFile = ntpath.basename(selectPath) #filename without path

if selectFile.endswith('.xspf'):
	filesList = get_filenames(selectPath) #get list of files from playlist file
	copyPath = create_directory(selectDir, selectFile) #create new directory
	copy_files(filesList, copyPath) #copy files to new directory
	messagebox.showinfo("Complete", "Playlist folder created!")
	
else:
	messagebox.showinfo("Bad File", '"' + selectFile + '"' + " is not a VLC playlist, exiting...")