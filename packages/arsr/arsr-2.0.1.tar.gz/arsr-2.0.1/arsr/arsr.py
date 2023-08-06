import cv2 as cv
from cv2 import dnn_superres
from PIL import Image
import os 

class sr:
    
    def __init__(self,main='edsr',method='ensemble'):
        self.espcn = None
        self.fsrcnn = None
        self.edsr   = None
        self.model  = None
        self.method = method
        self.main   = main
        self.root   = os.path.abspath(os.path.dirname(__file__))
        if main in ['edsr','espcn','fsrcnn','lapsrn']:
            self.sr = dnn_superres.DnnSuperResImpl_create()
            model_name = main
            fixedscale = 2
            if model_name == 'lapsrn':
                model_name = 'LapSRN'
#                 if scale2 == 3 : 
#                     raise ValueError("LapSRN has no 3x scale")
                path = f"./srmodels/{model_name}_x{fixedscale}.pb"
                path = os.path.join(self.root,path)
            else :
                path = f"./srmodels/{model_name.upper()}_x{fixedscale}.pb"
                path = os.path.join(self.root,path)
                
            self.sr.readModel(path)
            self.sr.setModel(model_name.lower(), fixedscale)
            
        elif main in ['rdn', 'esrgan', 'srgan'] :
            upimg = None
            
    def setmodel(self,main):
        pass
    
    def up2x(self,img):
        if self.main in ['edsr','espcn','fsrcnn','lapsrn']:
            upimg = self.sr.upsample(img)
            
        elif self.main in ['rdn', 'esrgan', 'srgan'] :
            upimg = None
            
        return upimg
            
    def upsample(self,img,scale): #,main=None,method='ensemble'):
        methods = self.method.split('_')
        main    = self.main
        h,w = img.shape[:2]
        
        if methods[0].lower() == 'ensemble':
            
            main = main.lower()
            # inter + 2x_sr            
            uw,uh = int(w*scale),int(h*scale)
            fw,fh = uw,uh       
            if scale < 2 :
                return cv.resize(img, (uw,uh),interpolation=cv.INTER_CUBIC) 

            if uw%2!=0:
                uw = uw -1 
            if uh%2!=0:
                uh = uh -1 
            uw = uw//2
            uh = uh//2        

            # inter 
            img = cv.resize(img, (uw,uh),interpolation=cv.INTER_CUBIC) 
            # 2x_sr 
            img = self.up2x(img)
            scale = 2
            


            if (uw != fw) or (uh != fh) :
                img = cv.resize(img, (fw,fh),interpolation=cv.INTER_CUBIC) 
                
        return img