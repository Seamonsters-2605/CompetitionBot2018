__author__ = "jacobvanthoog"

from xml.etree import ElementTree # XML

def readPoints(filePath, pixelsPerUnit, leftMargin, bottomMargin):
    print('Load SVG at: ' + str(filePath))
    tree = ElementTree.parse(filePath)
    root = tree.getroot()
    path = root.find('{http://www.w3.org/2000/svg}path')
    pathData = str(path.get('d'))

    pathData = pathData.split('C', maxsplit=1)[1] # get all text after "C"
    pathData = pathData.strip()
    pathLines = pathData.split()

    numPoints = int(len(pathLines) / 3) + 1
    print('Path has', numPoints, 'points.')

    points = [ None for i in range(0, numPoints) ]
    points[0] = _parseLine(pathLines[0])
    for i in range(1, numPoints):
        line = pathLines[i * 3 - 2]
        points[i] = _parseLine(line)

    viewBox = root.get('viewBox')
    imageHeight = int(viewBox.split()[3])

    pathPoints = [_imageCoordinatesToUnits(p, imageHeight, pixelsPerUnit,
                                           leftMargin, bottomMargin)
                  for p in points]
    print("Done")
    return pathPoints

def _parseLine(line):
    values = line.strip().split(',', 1)
    return (float(values[0]), float(values[1]))

def _imageCoordinatesToUnits(coords, imageHeight, pixelsPerUnit,
                            leftMargin, bottomMargin):
    x = (coords[0] - leftMargin) / float(pixelsPerUnit)
    y = (imageHeight - bottomMargin - coords[1]) / float(pixelsPerUnit)
    return (x, y)
