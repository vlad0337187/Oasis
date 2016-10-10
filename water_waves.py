'''Runs with certain delay.
Fro work needs a plain with verticles.

Source: https://blenderartists.org/forum/showthread.php?305608-Realtime-Mesh-Water-Waves%28No-animations-required%29 (26 Aug 2016)
Author: coreystj
'''

import bge

gl = bge.logic#Import Logic as gl

cont = gl.getCurrentController()#Get current controller

own = cont.owner#Get owner

speed = 1#Set wave speed

height = 100#Set Wave Force

if "Vertex" not in own.attrDict:#Run Once

    import random#Import Random

    own.attrDict["Vertex"] = {}#Create Vertex Dict
    
    mesh = own.meshes[0]#Get owner mesh
    
    own.attrDict["Frame"] = 1#Create Frame Variable at frame 1

    for i in range(mesh.getVertexArrayLength(0)):#For each vertex index
        
        vertex = mesh.getVertex(0, i)#Get vertex By index
        
        x = vertex.XYZ[0]#get Vertex X Coordinate
        
        y = vertex.XYZ[1]#get Vertex Y Coordinate
        
        frame = random.randint(100,300)/100.0#Get a random frame from 1.0 - 3.0
        
        if str([x, y]) not in own.attrDict["Vertex"]:#If Coordinate not in vertex library
            
            own.attrDict["Vertex"][str([x, y])] = [[vertex],frame, vertex.XYZ[2]]#Add Coordinate Vertex with random frame number, store vertex default height
            
        else:
            own.attrDict["Vertex"][str([x, y])][0].append(vertex)#Add secondary coordinate to vertrex list NOTE: There can be two vertex in exactly one point
            
for coor in own.attrDict["Vertex"]:#For Corrdinate in vertex library

    value = own.attrDict["Vertex"][str(coor)]#Create variable for ease of access
    
    for vertex in value[0]:#For vertex in vertex list
        
        frame = value[1]#Get frame
    
        if frame  <= 2:#If frame is less than half of animation

            h = (frame **2 - 3*frame) + 2#Formula for parabolic coordinate plotting by frame num
        else:#Else
            frame = frame -1#Reset frame by half its animation
            
            h = -((frame **2 - 3*frame) + 2)#INVERTED Formula for parabolic coordinate plotting by frame num   
        h = h * height/100#Modify height of waves
        
        value[1] += speed/100#Add for the next frame by speed
        
        x = vertex.XYZ[0]#Get vertex X coor
        
        y = vertex.XYZ[1]#Get vertex Y coor
        
        new = [x, y, value[2] + h]#Store New coordinate for vertex relative to default height
        
        vertex.XYZ = new#Apply New coordinate for vertex
    
        if value[1] >= 3:#If end of frame
            
            value[1] = 1#Restart frame