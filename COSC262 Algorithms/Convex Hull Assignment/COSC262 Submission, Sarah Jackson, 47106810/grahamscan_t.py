#'''
    #Sarah Jackson (47106810)
    #May 2015
    #Assignment 2
    #Gift Wrap Algorithm Test
    #-computes the convex hull on a 2-D plane from a list of points using 
    #the Gift Wrap algorithm
    #-reads from a text file of up to 100 points
    #-assume each point have integers in the range(0, 1000)
    #-assume there are no collinear points, or coincident points
    
#'''
import sys



def grahamScan_t(listOfPoints, n):
    '''It takes a list of points, and the size of the list of points, and 
       returns the convex hull indices using the Graham Scan algorithm
    '''
    convexHullIndexes = []
    closedPath = buildSimpleClosedPath(listOfPoints)
    stack = [closedPath[-1], closedPath[0], closedPath[1]] # initializing the stack
    for i in range(2, n): # Begins at 2
        while not isCCW(stack[-2], stack[-1], closedPath[i]): # checks if the current point and top two points
            x = stack.pop()                                   # on the stack form a Counter Clock-wise turn or not
        stack.append(closedPath[i])                           # continue popping off stack until CCW condition is met
    for point in stack:                                       # pushes onto stack otherwise
        convexHullIndexes.append(listOfPoints.index(point))
    return convexHullIndexes[1:]


def isCCW(beforePrevPoint, prevPoint, curPoint):
    ''' Takes a before previous point, a previous point, and a current point,
        and compares the current point to the two previous points and determines
        whether it makes a clock-wise turn, counter clock-wise turn, or if it is 
        colinear.
        angle > 0 CCW turn (counter clock-wise)
        angle < 0 CW turn (clock-wise) 
        angle = 0 colinear
    '''
    turn =  (prevPoint[0] - beforePrevPoint[0]) * (curPoint[1] - beforePrevPoint[1]) - \
            (prevPoint[1] - beforePrevPoint[1]) * (curPoint[0] - beforePrevPoint[0])
    isCCW = False
    if turn > 0: # to include colinear points on convex hull change condition to >=
        isCCW = True
    return isCCW
            
def buildSimpleClosedPath(listOfPoints):
    '''Constructs a simple closed path from a list of points on a plane.
       The path passes through each point without intersecting itself, and 
       returns a list of the path.
    '''
    anchorPoint = getStartingPoint(listOfPoints) #sets the anchor point
    pointAngles = [] #creates a list to append angles and their corresponding points
    for point in listOfPoints:
        angle = theta(anchorPoint, point) #calculates the angle between anchor point and the next point
        pointAngles.append((point,angle)) #appends that point and the angle
    pointAngles = sorted(pointAngles,key = lambda x: x[1])
    return [element[0] for element in pointAngles] # returns a list of the first element of each tuple of pointAngles as an element                   

                
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
    return theta
                
def main():
    '''Calls the giftwrap algorithm, and returns the indices of the list of
       points that are a part of the convex hull
    '''
    file = open(sys.argv[1])
    n = int(file.readline()) # reads the first line (number of points)
    lines = file.readlines() # each line is the element of list as a string
    listOfPoints = [] # going to append each element as a tuple (x,y coord)
    for line in lines: 
        line = line.split() # extracting the x and y coordinates
        point = int(line[0]), int(line[1]) # ensuring it adds integers, not strings
        listOfPoints.append(point) # appending the coordiantes into listOfPoints
    convexHullIndexes = grahamScan_t(listOfPoints, n)
    return convexHullIndexes

convexHull = main()
for index in convexHull:
    print(index, end = ' ')
print()