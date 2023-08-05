import cv2
import numpy as np
import requests
from tqdm import tqdm
import os

class Colorizer:
    def __init__(self, model_dir:str ="model") -> None:
        self.file_list = [{"url":"http://eecs.berkeley.edu/~rich.zhang/projects/2016_colorization/files/demo_v2/colorization_release_v2.caffemodel","fname":"colorization_release_v2.caffemodel"},{"url":"https://github.com/aisociety-in/image_colorisation/blob/main/pts_in_hull.npy?raw=true","fname":"pts_in_hull.npy"},{"url":"https://raw.githubusercontent.com/aisociety-in/image_colorisation/main/colorization_deploy_v2.prototxt","fname":"colorization_deploy_v2.prototxt"}]
        self.model_dir = model_dir
        load = False
        for t in self.file_list:
            if  self.model_dir not in os.listdir() or  t["fname"] not in os.listdir("model"):
                load = True
        if load:
            if "model" not in os.listdir():
                os.mkdir("model")
            self.load_model_files()


        self.net = cv2.dnn.readNetFromCaffe(f'{self.model_dir}/colorization_deploy_v2.prototxt',f'{self.model_dir}/colorization_release_v2.caffemodel')
        self.pts = np.load(f'{self.model_dir}/pts_in_hull.npy')
        
        class8 = self.net.getLayerId("class8_ab")
        conv8 = self.net.getLayerId("conv8_313_rh")
        self.pts = self.pts.transpose().reshape(2,313,1,1)
        self.net.getLayer(class8).blobs = [self.pts.astype("float32")]
        self.net.getLayer(conv8).blobs = [np.full([1,313],2.606,dtype='float32')]

    def load_model_files(self):
        for unit in self.file_list:
            self.download(unit["url"],self.model_dir+"/"+unit["fname"])
    # This method is from https://gist.github.com/yanqd0/c13ed29e29432e3cf3e7c38467f42f51 would reccomend checking it out
    def download(self,url:str,fname:str):
        resp = requests.get(url, stream=True)
        total = int(resp.headers.get('content-length', 0))
        with open(fname, 'wb') as file, tqdm(
                desc=fname,
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)

    
    def load_image(self,path:str):
        image = cv2.imread(path)
        self.image = image
        scaled = image.astype("float32")/255.0
        lab = cv2.cvtColor(scaled,cv2.COLOR_BGR2LAB)
        self.lab = lab

        resized = cv2.resize(lab,(224,224))
        L = cv2.split(resized)[0]
        L -= 50
        self.L = L

    def colorize_img(self):
        self.net.setInput(cv2.dnn.blobFromImage(self.L))
        ab = self.net.forward()[0, :, :, :].transpose((1,2,0))

        ab = cv2.resize(ab, (self.image.shape[1],self.image.shape[0]))

        L = cv2.split(self.lab)[0]
        colorized = np.concatenate((L[:,:,np.newaxis], ab), axis=2)

        colorized = cv2.cvtColor(colorized,cv2.COLOR_LAB2BGR)
        colorized = np.clip(colorized,0,1)

        colorized = (255 * colorized).astype("uint8")

        self.rgb = colorized
    
    def pipeline(self,imgpath):
        self.load_image(imgpath)
        self.colorize_img()
        return self.rgb


        
        