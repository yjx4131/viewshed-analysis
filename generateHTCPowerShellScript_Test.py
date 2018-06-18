import os
PSFileName = r"E:\Viewshed\Scripts\PSFile.ps1"
PSFile = open(PSFileName,"w")
PSFile.write("Add-PSSnapIn Microsoft.HPC \n")
i = 0
step = 2
AllObserverNum = 5
MumVisibleDist = 3
while i < AllObserverNum - step:
	lower = i
	upper = lower + step
	JobName = str(lower) + "_" + str(upper)
	JobStr1 = "$j = New-HpcJob -Name " + "'" + "Observer#" + JobName + "' " + "-RequestedNodes '" + "CAGIS121,CAGIS122' " + "-Exclusive $True \n"
	JobStr2 = "$j | Add-HpcTask -WorkDir '" + "C:\Program Files' -Name '" + "Viewshed Task' -Type Basic -Command '" + "python " + "\\\\CagisCondor\\Viewshed\\Scripts\\viewshed_V2.py" + " " + str(
		lower) + " " + str(upper) + " " + str(MumVisibleDist) + " " + "C:\\Viewshed\\Input' \n"
	JobStr3 = "$j | Submit-HpcJob  \n"
	i += step
	PSFile.write(JobStr1)
	PSFile.write(JobStr2)
	PSFile.write(JobStr3)
else:
	lower = i
	upper = AllObserverNum
	JobName = str(lower) + "_" + str(upper)
	JobStr1 = "$j = New-HpcJob -Name " + "'" + "Observer#" + JobName + "' " + "-RequestedNodes '" + "CAGIS121,CAGIS122' " + "-Exclusive $True \n"
	JobStr2 = "$j | Add-HpcTask -WorkDir '" + "C:\Program Files' -Name '" + "Viewshed Task' -Type Basic -Command '" + "python " + "C:\\Viewshed\\Scripts\\viewshed_V2.py" + " " + str(
		lower) + " " + str(upper) + " " + str(MumVisibleDist) + " " + "C:\\Viewshed\\Input' \n"
	JobStr3 = "$j | Submit-HpcJob  \n"
	PSFile.write(JobStr1)
	PSFile.write(JobStr2)
	PSFile.write(JobStr3)
