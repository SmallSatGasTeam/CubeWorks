import os #Won't lie, I have no idea what these do but it appeared that they were required at the beginning of every program like a C directive
import sys

path = "/home/jjhjj/CubeWorks/tests/resetText.txt" #This is just telling us where we want to go, right now it's set to run locally on Josh's computer
file = open(path,"r+") #This is opening the file and telling python that it can write in it
file.truncate(0) #This is to delete everything
file.close() #This closes the file so it is no longer being edited
print("We ran")