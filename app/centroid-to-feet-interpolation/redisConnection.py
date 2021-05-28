from walrus import Database

class redisDB:
    def __init__(self,host='localhost',port=6379,db=0,streamIn='camera:0', streamOut='camera:0:yolo'):

        self.r_data = Database(host=host, port=port, db=db)
        
        # input stream
        self.streamName = streamIn # data

        # output stream
        self.detectionsStreamName = streamOut

        # consumer group per lettura
        #self.cg = self.r_data.consumer_group('people-detection', self.streamName)
        #self.cg.create()  # Create the consumer group.
        #self.cg.set_id('$')
    
    def outputXadd(self, ref, feet, people):
        data = {
            b"ref" : ref,
            b"feet" : str(feet), 
            b"people" : people
        }  
        res_id = self.r_data.xadd(self.detectionsStreamName,data,maxlen=1000)
        return

    def inputXrevrange(self):  

        try:
            streamValue = self.r_data.xrevrange(self.streamName,count=1)[0]
            #streamID = streamValue[0]
            #reathis = streamValue[1]
        except:
            print('exception')
            return False, False
        else:
            return True, streamValue