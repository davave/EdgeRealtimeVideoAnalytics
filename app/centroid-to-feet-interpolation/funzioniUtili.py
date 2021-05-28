import cv2
import yaml
import numpy as np

def pointsMap(imgName='640x480.jpg',windowName='Disposizione punti del centroide'):
    img = cv2.imread(imgName)
    windowName = windowName

    centroidCoordinates, feetCoordinates = centroidFeetFromFile()

    #img = cv2.drawMarker(img, (320,240), color=(255,255,0), markerType = cv2.MARKER_CROSS)#, markerSize[, thickness[, line_type]]]]	) -> 	img
    img = drawLine(img, centroidCoordinates,feetCoordinates, color=(255, 0, 0))
    img = insertPoints(img,centroidCoordinates)
    img = insertPoints(img,feetCoordinates,color=(0, 255, 0))
    
    cv2.putText(img, 'centroid', (10,415), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(img, 'feet', (10,400), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imshow(windowName, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def insertPoints(CV2Img, centroidCoordinates, color=(0, 0, 255)):
    
    for value in centroidCoordinates:

        img = cv2.circle(CV2Img, (value[0], value[1]), radius=2, color=color, thickness=-1)    

    return img

def centroidFeetFromFile(fileName="/home/davide/Documenti/progetti/playground/centroid-to-feet-interpolation/101_640x480.yaml", normalization=False):
    '''
    funzione che carica e restituisce le coordinate di centroide e piedi nel formato [[x y]]
    '''
    with open(fileName, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            centroidCoordinates = np.array(data['feet_calib'], dtype='i')[:,0,:]
            feetCoordinates = np.array(data['feet_calib'], dtype='i')[:,1,:]
            image_width = np.array(data['feet_calib_image_width'])
            image_height = np.array(data['feet_calib_image_height'])

            if normalization:
                # Normalizing coordinates
                for v in [centroidCoordinates,feetCoordinates]:
                    v[:,0] /= image_width
                    v[:,1] /= image_height

            #print(centroidCoordinates[0,0])           

        except yaml.YAMLError as exc:
            print(exc)

    return centroidCoordinates,feetCoordinates  

def drawLine(CV2Img, centroidCoordinates,feetCoordinates, color=(0, 0, 255)):
    #print(centroidCoordinates[:,0])
    for index in range(len(centroidCoordinates[:,0])):

        #img = cv2.circle(CV2Img, (value[0], value[1]), radius=2, color=color, thickness=-1)    
        img = cv2.line(CV2Img, (centroidCoordinates[index,0], centroidCoordinates[index,1]), (feetCoordinates[index,0], feetCoordinates[index,1]), color, 1)

    return img