import arcpy
import os
import shutil
from arcpy import env
import time

lower = 0
upper = 1
MumVisibleDistance = 3 # kilometers
InputFolder = r"E:\Viewshed\Input"
def Viewshed(InputFolder,lower,upper,MumVisibleDist):
	OutputFolder = InputFolder.replace("Input", "Output#" + str(lower) + "_" + str(upper - 1))
	if os.path.exists(OutputFolder):
		shutil.rmtree(OutputFolder)
	os.makedirs(OutputFolder)
	ObserverPointFolder = os.path.join(OutputFolder, "oberverPoint#" + str(lower) + "_" + str(upper - 1))
	os.mkdir(ObserverPointFolder)
	ViewshedResultFolder = os.path.join(OutputFolder, "ViewshedResult#" + str(lower) + "_" + str(upper - 1))
	os.mkdir(ViewshedResultFolder)
	ObserverPointGDB = os.path.join(ObserverPointFolder, "oberverPoint.gdb")
	arcpy.CreateFileGDB_management(ObserverPointFolder, "oberverPoint.gdb")
	ClipedViewshedRasterFolder = os.path.join(OutputFolder, "ClipedViewshed#" + str(lower) + "_" + str(upper - 1))
	os.mkdir(ClipedViewshedRasterFolder)
	ClipedViewshedRasterGDB = os.path.join(ClipedViewshedRasterFolder, "ClipedViewshed.gdb")
	arcpy.CreateFileGDB_management(ClipedViewshedRasterFolder, "ClipedViewshed.gdb")
	AllObserverPoints = os.path.join(InputFolder, "observorPoint" + "\\" + "cell.shp")
	arcpy.AddField_management(AllObserverPoints, "ViewCount", "LONG")
	Surface = os.path.join(InputFolder, "surface.gdb" + "\\" + "dem30")
	ViewshedResult = os.path.join(ViewshedResultFolder, "VSD_Result_" + str(lower) + "_" + str(upper) + ".shp")
	Delimiter_ID = arcpy.AddFieldDelimiters(AllObserverPoints, "ID")
	SQL_ID_expression = Delimiter_ID + ">=" + str(lower) + "and" + Delimiter_ID + "<" + str(upper)
	ObserverCursor = arcpy.da.SearchCursor(AllObserverPoints, ["ID"], where_clause=SQL_ID_expression)
	if arcpy.CheckExtension("Spatial") == "Available":
		arcpy.CheckOutExtension("Spatial")
	if arcpy.CheckExtension("analysis") == "Available":
		arcpy.CheckOutExtension("analysis")
	for ObserverID in ObserverCursor:
		CurrentObserverID = str(ObserverID[0])
		expression_1 = Delimiter_ID + " = " + CurrentObserverID
		currentObsPoint = os.path.join(ObserverPointGDB, "observer_" + CurrentObserverID)
		arcpy.FeatureClassToFeatureClass_conversion(AllObserverPoints, ObserverPointGDB,
													"observer_" + CurrentObserverID,
													expression_1)
		outViewshed = arcpy.sa.Viewshed(Surface, currentObsPoint, "", "", "", "#")
		observerBuffer = os.path.join(ObserverPointGDB, "observerBuffer_" + CurrentObserverID)
		arcpy.Buffer_analysis(currentObsPoint, observerBuffer, str(MumVisibleDist) + " " + "KILOMETER")
		ClipedViewshed = os.path.join(ClipedViewshedRasterGDB, "ClipedVSD_" + CurrentObserverID)
		arcpy.Clip_management(outViewshed, "3.96868300288 8.62758838909 4.63701633675 9.47508838977", \
							  ClipedViewshed, observerBuffer, "-32767", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
		arcpy.BuildRasterAttributeTable_management(ClipedViewshed, "Overwrite")
		DelimitersValue = arcpy.AddFieldDelimiters(ClipedViewshed, "VALUE")
		expression_2 = DelimitersValue + "= 1"
		viewShedObjCursor = arcpy.da.SearchCursor(ClipedViewshed, ["VALUE", "COUNT"], expression_2)

		for ViewValue in viewShedObjCursor:
			if ViewValue[0] == 1:
				VisibleCellNumber = ViewValue[1]
				currentObsPointCursor = arcpy.da.UpdateCursor(currentObsPoint, ["ViewCount"])
			else:
				continue
			for observerRow in currentObsPointCursor:
				observerRow[0] = VisibleCellNumber
				currentObsPointCursor.updateRow(observerRow)
			del currentObsPointCursor, observerRow

		del viewShedObjCursor, ViewValue

	del ObserverCursor, ObserverID

	arcpy.env.workspace = ObserverPointGDB
	SubObserver = arcpy.ListFeatureClasses("*", "Point")
	SubObserverList = []
	for fc in SubObserver:
		SubObserverList.append(fc)
	arcpy.Merge_management(SubObserverList, ViewshedResult)

def main():
	Viewshed(InputFolder, lower, upper, MumVisibleDistance)
	print "Viewshed analysis done"
if __name__ == '__main__':
	main()
