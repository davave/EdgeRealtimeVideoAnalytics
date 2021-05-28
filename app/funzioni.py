
from scipy.interpolate import Rbf
import yaml 
import numpy as np

def centroid(x1,y1,x2,y2):
    ''' 
    Return rectangle centroid 
    
    :param x1: x coordinate of upper left corner
    :param y1: y coordinate of upper left corner
    :param x2: x coordinate of lower left corner
    :param y2: x coordinate of lower left corner
    '''

    cX = (x1 + x2) / 2.
    cY = (y1 + y2) / 2.
    
    return cX , cY

def computeRbf():
    with open("./centroid-to-feet-interpolation/101_640x480.yaml", 'r') as stream:
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

  