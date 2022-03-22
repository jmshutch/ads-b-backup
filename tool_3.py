# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
    File name: tool_3.py
    Author: Shawn Hutchinson
    Credits: Shawn Hutchinson, Brian Peterson
    Description:  Combines daily ADS-B files into mergeed waypoints and flightlines
    Status:  Development
    Date created: 12/15/2021
    Date last modified: 2/23/2022
    Python Version: 3.72
"""

# Import libraries
import arcpy, os, time

# User-specified local variable(s) for ArcGIS script tool
inputWorkspace = arcpy.GetParameterAsText(0)
parkBoundaryFile = arcpy.GetParameterAsText(1)
outputWorkspace = arcpy.GetParameterAsText(2)
outputPoints = arcpy.GetParameterAsText(3)
outputLines = arcpy.GetParameterAsText(4)

# User-specified local variable(s) for stand-alone Python script
#inputWorkspace = "D:/GIS_Research/ResearchProjects/NPS_ADS_B/NPS_ADS_B_GRSM.gdb"
#parkBoundaryFile = "D:/GIS_Research/ResearchProjects/NPS_ADS_B/NPS_ADS_B_GRSM.gdb/Boundary_GRSM"
#outputWorkspace = "D:/GIS_Research/ResearchProjects/NPS_ADS_B/NPS_ADS_B_GRSM.gdb"
#outputPoints = "MergedWaypoints"
#outputLines = "MergedFlightlines"

# Set local environments
arcpy.env.workspace = inputWorkspace
arcpy.env.overwriteOutput = True

# Fixed local variables
pointList = []
lineList = []

try:
    
    # Start timer
    start = time.time()
       
    # Search input workspace and identify aircraft waypoint point and flight line feature classes
    print("Creating a list of daily aircraft waypoint and flightline files...")
    arcpy.AddMessage("Creating a list of daily aircraft waypoint and flightline files...")
    for fc in arcpy.ListFeatureClasses():
        desc = arcpy.Describe(fc)
        if desc.shapeType == "Point":
            pointList.append(fc)
        if desc.shapeType == "Polyline":
            lineList.append(fc)     
            
    # Merge point and line feature classes into single files and filter by horizontal and vertical buffers
    if len(pointList) > 0:
        desc = arcpy.Describe(pointList[0])
        parkName = desc.baseName[5:9]
        arcpy.management.Merge(pointList, os.path.join(outputWorkspace, outputPoints))
        count1 = arcpy.management.GetCount(os.path.join(outputWorkspace, outputPoints))
        print("There are {0} point feature classes to be merged...".format(str(len(pointList))))
        arcpy.AddMessage("There are {0} point feature classes to be merged...".format(str(len(pointList))))
    if len(lineList) > 0:
        desc = arcpy.Describe(lineList[0])
        parkName = desc.baseName[5:9]
        arcpy.management.Merge(lineList, os.path.join(outputWorkspace, outputLines))
        count2 = arcpy.management.GetCount(os.path.join(outputWorkspace, outputLines))
        print("There are {0} line feature classes to be merged...".format(str(len(lineList))))
        arcpy.AddMessage("There are {0} line feature classes to be merged...".format(str(len(lineList))))
    else:
        print("There are no waypoints or flight lines in the workspace.")
        arcpy.AddMessage("There are no waypoints or flight lines in the workspace.")
       
except arcpy.ExecuteError:
    for i in range(0, arcpy.GetMessageCount()):
        arcpy.AddMessage("{0}:  {1}".format(arcpy.GetSeverity(i), arcpy.GetMessage(i)))

finally:    
    # Report aircraft and flight summaries and execution time
    end = time.time()
    print("There are {0} total aircraft waypoints in the merged output.".format(str(count1))) 
    arcpy.AddMessage("There are {0} total aircraft waypoints in the merged output.".format(str(count1)))
    print("There are {0} total aircraft flights in the merged output.".format(str(count2))) 
    arcpy.AddMessage("There are {0} total aircraft flights in the merged output.".format(str(count2)))
    print("Total Execution Time (secs) = {0}".format(str(round(end - start, 3))))    
    arcpy.AddMessage("Total Execution Time (secs) = {0}".format(str(round(end - start, 3))))