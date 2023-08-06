import json,logging,math,re
from datetime import datetime,timedelta,date
from dateutil.parser import parse as parseDate
from multiprocessing import Process,Pool
from itertools import repeat


#Used to pickle datetimes into json files
def defaultconverter(o):
  if isinstance(o, datetime):
      return o.isoformat()
  elif isinstance(o, date):
      return o.isoformat()
  elif isinstance(o, Name):
      return str(o)
    
#Event tree class used to analyize one-to-many-many-many relationships.
#Use addListener to attache a function to one of the keys of the lists in the one-many relationships.
class TreeAnalysis:
    def __init__(self,path,filename="Looper_output.json"):
        self.filename = filename
        self.listeners = []
        self.data = json.load(open(path))
        self.output = {}

    #Add a function based on the key attached to the one-many relationship in the json
    def addListener(self,function,event):
        listener = (function,event)
        self.listeners.append(listener)

    #Emit an event callaing all the functions with matching event names (case insensitive). 
    def emit(self,event_name,*args,**kwargs):
      output = None
      upper = lambda a: [string.upper().split() for string in a]
      original = upper(re.split('[^a-zA-Z]', event_name))
      logging.debug(f'Emitting event: {event_name}')
      for function,event in self.listeners:
        components = upper(re.split('[^a-zA-Z]', event))
        if all([x==y for x,y in zip(original,components)]):
          logging.debug(f'Listener triggered: {event}')
          response = function(*args,**kwargs)
          if response is not None:
            output = response
      return output

    #Loop through every list in every dict of dataset
    #If pocesses is not None then multiprocessing will be enables throughb batches.
    def loop(self,data=None,processes=None,write=True):
      self.emit('/start',analysis=self)
      if data is None: data = self.data
      if processes is None:
        self.bubbleLayer(data)
        r = self.emit('/write/before',data)
        if r is not None:
          data = r
        if write:
          self.save(data)
          self.emit('/write/after',data)
        response = self.emit('/end')
        return data
      else:
        elements = [element for element in data]
        batch_size = len(elements)/processes
        batches = [
          elements[ round(i*batch_size) : round((1+i)*batch_size) ]
          for i in range(processes)
        ]
        with Pool(processes) as pool:
          outputs = pool.starmap(self.loop,zip(batches,repeat(None),repeat(False)))
        logging.info("Finished processing")
        flat_data = [val for sublist in outputs for val in sublist]
        r = self.emit('/write/before',flat_data)
        if r is not None:
          data = r          
        if write:
          logging.info(f'Writing data; len({len(outputs)})')
          self.save(flat_data)
          self.emit('/write/after',flat_data)          
        self.emit('/end')
        logging.info("Finished.")
      

    # Recusivly look through dicts in list looking for nested lists
    # Will emit an even on any key that defines a list for each object.
    # Events are of the format
    # /event_name/before
    # /event_name/after
    # /event_name/each
    # Where before is preprocessed before nested processes,
    # after is run postprocessing nested processes.
    #
    def bubbleLayer(self,layer,event='',*args,parent=None,**kwargs):
      if isinstance(layer,dict):
        layer = [layer]
      eventful = False
      for i,obj in enumerate(layer):
        if i>0 and i%1_000==0:
          logging.info(f"Processed {i} elements  {event}.")
        if not isinstance(obj,dict):
          continue
        logging.debug(event+'/before')
        self.emit(event+'/before',obj,*args,**kwargs)
        self.emit(event+'/each',obj,*args,**kwargs)
        keys = list(obj)
        for key in keys:
          value = obj[key]
          if isinstance(value,list) and len(value)>0:
            #Enter item
            self.bubbleLayer(value,f"/{key}",obj,*args,**kwargs)
        logging.debug(event+'/after')
        self.emit(event+'/after',obj,*args,**kwargs)

    #Save the data to the specified output file. 
    def save(self,data=None):
      if data is None:
        data = self.data
      if self.filename is None:
        print("No output filename specified.")
      else:
        with open(self.filename,'w+') as f:
          json.dump(data,f,indent=2,default=defaultconverter)
          logging.info(f'Saved to {self.filename}')


if __name__=="__main__":
  #See logging
  logging.basicConfig(level=logging.INFO)
