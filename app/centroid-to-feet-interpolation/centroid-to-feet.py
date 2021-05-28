import yaml
import numpy as np
from scipy.interpolate import Rbf
from redisConnection import redisDB
import funzioniUtili as F

def computeRbf():
    with open("/home/davide/Documenti/progetti/playground/centroid-to-feet-interpolation/101_640x480.yaml", 'r') as stream:
            try:
                data = yaml.safe_load(stream)
                centroidCoordinates = np.array(data['feet_calib'], dtype='f')[:,0,:]
                feetCoordinates = np.array(data['feet_calib'], dtype='f')[:,1,:]
                image_width = np.array(data['feet_calib_image_width'])
                image_height = np.array(data['feet_calib_image_height'])

                # Normalizing coordinates
                for v in [centroidCoordinates,feetCoordinates]:
                    v[:,0] /= image_width
                    v[:,1] /= image_height
                

            except yaml.YAMLError as exc:
                print(exc)

    RbfX = Rbf(centroidCoordinates[:,0],centroidCoordinates[:,1], feetCoordinates[:,0]) # rbf instance
    RbfY = Rbf(centroidCoordinates[:,0],centroidCoordinates[:,1], feetCoordinates[:,1]) # rbf instance

    return RbfX, RbfY
        
dataBaseConnection = redisDB(streamIn='camera:0:yolo', streamOut='camera:0:feet')

def processFrame():

    RbfX, RbfY = computeRbf()

    frameID = b'0'
    frameID_old = b'0'
    while True:
        ret = False
        while not ret or frameID==frameID_old:
            frameID_old = frameID
            
            data = dataBaseConnection.inputXrevrange()
            ret = data[0]
            #print(data[1][1][b'ref'])
            frameID = data[1][1][b'ref']
            #ret, frameID, frame = db.ffR()

            new = frameID
            #print(old, new)
        xyxy = np.fromstring(data[1][1]['boxes'.encode('utf-8')][1:-1], sep=',')
        peopleNumber = data[1][1][b'people']

        #print(peopleNumber)
        feet = []
        if peopleNumber != b'0':
            #print(xyxy)
            for box in range(int(data[1][1][b'people'])):  # Draw boxes
                #print('xyxy[box*4]', xyxy[box*4])
                x1 = xyxy[box*4] / 640
                y1 = xyxy[box*4+1] / 480
                x2 = xyxy[box*4+2] / 640
                y2 = xyxy[box*4+3] / 480
                
                # disegno del centroide
                centroidX = ((x2+x1)/2)
                centroidY = ((y2+y1)/2)

                print(centroidX, '\t', type(centroidX))

                computedFeetCoordinatesX = float(RbfX(centroidX , centroidY )) 
                computedFeetCoordinatesY = float(RbfY(centroidX , centroidY ))

                feet += [computedFeetCoordinatesX, computedFeetCoordinatesY]

        dataBaseConnection.outputXadd(frameID,feet, peopleNumber) 
        #return 


if __name__ == '__main__':
    #processFrame()
    F.pointsMap()
    #F.centroidFeetFromFile()