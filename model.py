import kfserving
from typing import List, Dict
from PIL import Image
import base64
import io
import logging
import SimpleITK as sitk
import numpy as np
import requests, json
import sys, os
from enum import Enum
import cv2
import subprocess

model_name = sys.argv[3]
model_name = model_name.split("=")[1]

def b64_filewriter(filename, content):
    string = content.encode('utf8')
    b64_decode = base64.decodebytes(string)
    fp = open(filename, "wb")
    fp.write(b64_decode)
    fp.close()


class KFServingSampleModel(kfserving.KFModel):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.ready = False

    def load(self):
        self.ready = True

    def predict(self, inputs: Dict) -> Dict:
        #del inputs['instances']
        logging.info("prep =======> %s",str(type(inputs)))
        try:
            json_data = inputs
        except ValueError:
            return json.dumps({ "error": "Recieved invalid json" })
        
        data = json_data["image"]
        
        b64_filewriter('sample.jpeg',data)
        
       # Resize Image
        img = cv2.imread('sample.jpeg')

       # Stress Load
        loadCmd = "stress-ng -c 8 -l 80 -t 900"
        subprocess.Popen(["bash", "-c", loadCmd])

        return {"Output_msg": "Task in-progress"}

        while True:
            logging.warning('The CPU usage is: %s', str(psutil.cpu_percent()), ' percent')
            sleep(5)

if __name__ == "__main__":
    model = KFServingSampleModel(model_name)
    model.load()
    kfserving.KFServer(workers=1).start([model])
