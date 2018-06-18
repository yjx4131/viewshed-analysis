import shutil
InputFolder = "E:\Viewshed"
outfolder = "F:\Viewshed"
outfolder1 = "F:\Viewshed\output#0_1"
shutil.copytree(InputFolder,outfolder)

shutil.copytree(outfolder1,InputFolder)
