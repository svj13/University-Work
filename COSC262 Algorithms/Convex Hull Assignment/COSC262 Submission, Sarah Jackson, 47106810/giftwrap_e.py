'''
    Sarah Jackson (47106810)
    May 2015
    Assignment 2
    Gift Wrap Algorithm Evaluation
    -computes the time taken to find the convex hull on a 2-D plane from a 
    list of points using the Gift Wrap algorithm
    -self generates rectangular and circular input data in 
    between 1000 and 20000 points
    -assume each point have integers in the range(0, 1000)
    -assume there are collinear points, and/or coincident points
    
'''

import sys
import random
import time

     

def giftwrap_e(listOfPoints, n):
    '''It takes a list of points, and the size of the list of points, and 
       returns the convex hull indices using the gift wrap algorithm
    '''

    startPoint = getStartingPoint(listOfPoints) #point of minY
    
    listOfPoints.append(startPoint) #appends the start to the end as well (0, 360 are at the same position)
    listOfPointsCopy = listOfPoints[:]
    minAngPoint = listOfPoints.index(startPoint)
    convexHullIndex = [minAngPoint]       

    curPoint = 0 #index of the current point
    ang_v = 0 #angle of the vertex    
    n += 1 #n needs to be made larger as we appended another value onto the list
    while minAngPoint < n -1: #starts at y value and finishes at the vertex before it
        listOfPoints[curPoint], listOfPoints[minAngPoint] = \
            listOfPoints[minAngPoint], listOfPoints[curPoint] #swapping the point with the min angle with the current point in the list
       
        minAngPoint, ang_v = minAngle(curPoint, ang_v, listOfPoints, n) #finds index of min angle vertex in relation to curPoint
        curPoint += 1 #increment here because swapping occurs to the element to the right of curPoint
        #print(minAngPoint)
        pointOnHull = listOfPoints[minAngPoint]
        if minAngPoint == n - 1:
            return convexHullIndex
        convexHullIndex.append(listOfPointsCopy.index(pointOnHull))
    return convexHullIndex
    
def minAngle(curPoint, ang_v, listOfPoints, n):
    '''Takes a current point, a starting point, list of points and the number of
       points, and returns the minimum angle between these points. It begins at
       the starting point, and iterates through the list of points and 
       calculates the minimum angle of each current point in order to maintain
       the counterclockwise property. If there are two points with the same 
       minimum angle from the current point, it will return the point that is
       fartherst from the current point. This function returns the index of the
       point with the minimum angle 
       We can assume there are no collinear points.
    '''
    angleMin = 361 # setting the min angle, no angle can exceed this
    idxAngleMin = n - 1 # the index of the point with minimum angle
    for pointIndex in range(curPoint + 1, n): # prevents current point from comparing itself to previous points (that have been calculated already)
        if not listOfPoints[pointIndex] == curPoint: # to stop the current point comparing an angle to itself
            angle = theta(listOfPoints[curPoint], listOfPoints[pointIndex])
            if angle < angleMin and angle >= ang_v:
                angleMin = angle
                idxAngleMin = pointIndex
            elif angle == angleMin: # if points are colinear
            # use the distance formula to determine which of the two points is the farthest from the current point
                curDist = (abs(listOfPoints[idxAngleMin][0] - listOfPoints[curPoint][0])**2 + \
                           abs(listOfPoints[idxAngleMin][1] - listOfPoints[curPoint][1])**2)**0.5
                newDist = (abs(listOfPoints[pointIndex][0] - listOfPoints[curPoint][0])**2 + \
                           abs(listOfPoints[pointIndex][1] - listOfPoints[curPoint][1])**2)**0.5  
                if newDist == max(curDist, newDist):
                    idxAngleMin = pointIndex
    return idxAngleMin, angleMin
                
def getStartingPoint(listOfPoints):
    '''Find the minimum - rightmost y value out of the list of data points. If 
    there are duplicates of the minimum y-value, the x values are compared for 
    the largest (right-most) value.
    '''
    minY_point = listOfPoints[0] #the first y value in the data set
    for point in listOfPoints: #iterating through list of points to extract y-values
        x = point[0] #setting the x value
        y = point[1] #setting the y value
        if y < minY_point[1]: #comparing the y values
            minY_point = point
        elif y == minY_point[1]: #if there is a duplicate min y value
            if x == (max(x, minY_point[0])): #evaluting the x values, choosing largest
                minY_point = point
    return minY_point

def theta(pointA, pointB):
    '''Compute the approximation of the angle between the line AB
       to a horizonal line through A
    '''
    dx = pointB[0] - pointA[0]
    dy = pointB[1] - pointA[1]
    if abs(dx) < 1.e-6 and abs(dy) < 1.e-6: #so small it's basically 0, degenerate case
        t = 0
    else:
        t = dy/(abs(dx) + abs(dy))
    
    if dx < 0:
        t = 2 - t
    elif dy < 0:
        t = 4 + t
    theta = t * 90
    if theta == 0: #the 0 degrees point is equivalent to 360 degrees point
        theta = 360
    return theta
                

def inputGenerator(numElements):
    '''Computes input data within the program consisting of 1000 to 20000 points
       of random integers inbetween the values of 0 to 1000. Returns a 
       rectangular distribution and a circular distribution of the points. 
       It also returns the size of the generated input data.
    '''
    
    recPoints = [] #list for rectangular distribution
    circPoints = [] #list for circular distribution
    # numElements = range(1000, 20000, 1000) # determines number of points at random 
    isCircleDone = False
    isRectangleDone = False
    while not isCircleDone:
        x = random.randint(0, 999) # 0 <= x < 1000
        y = random.randint(0, 999) # 0 <= y < 1000
        if not isRectangleDone: 
            recPoints.append((x, y))
            if len(recPoints) == numElements:
                isRectangleDone = True
        if ((x-500)**2+(y-500)**2) < 25000:
            circPoints.append((x, y))
            if len(circPoints) == numElements:
                isCircleDone = True        
    return circPoints, recPoints
        
        
def main():
    '''Calls the graham scan algorithm, and records the length of time it takes
       to compute a randomly generated set of points with a rectangular and
       circular distribution
    '''
    print("GIFTWRAP ALGORITHM ANALYSIS")
    for numElements in range(1000, 21000, 1000): # change the range around as required
        circData, recData = inputGenerator(numElements) # generating random input
        startTime = time.clock()
        giftwrap_e(circData, numElements)
        endTime = time.clock()
        runTime = endTime - startTime
        
        startTime = time.clock()
        giftwrap_e(recData, numElements)
        endTime = time.clock()
        runTime2 = endTime - startTime
        print('\n' + 'Circular Distribution: ' + '\n' + 'time: ' + str(runTime) + '\n' + \
              'size: ' + str(numElements) + '\n' + \
              'Rectangular Distribution: ' + '\n' + 'time: ' + str(runTime2) + '\n' + \
              'size: ' + str(numElements) + '\n')

main()  