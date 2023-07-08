from django.shortcuts import render, redirect
from django.views import View
from RImageModel.forms import ImageFaceForm
from RImageModel.models import ImageToClassifi
from RImageModel.modelML import *
import os
import numpy as np


path_own = os.getcwd()

from skimage.io import imread


def equi_predict(predprob, classes=np.array(["Assu","EBODE", "Joel", "Lador","Landry", "Lolita", "Ridano", ])):
    return classes[np.argmax(predprob)]

def PretraitementLBP(imagePATH, ):
    imP = path_own+imagePATH
    image = from_color_to_gray_level(imread(imP))
    image = image_transformation(image, "LBP")
    
    return image
    
def PretraitementGLCM0(imagePATH, ):
    imP = path_own+imagePATH
    image = from_color_to_gray_level(imread(imP))
    image = image_transformation(image, "GLCM0")
    
    return image

def SousmodelsGLCM90(imagePATH, ):
    imP = path_own+imagePATH
    image = from_color_to_gray_level(imread(imP))
    model = load_model("GLCM90")
    image = image_transformation(image, "GLCM90")
    
    return equi_predict(model.predict_proba(image.reshape(1, -1)))

def GLModel(imagePATH):
    imP = path_own+imagePATH
    image = from_color_to_gray_level(imread(imP))
    lineDATA = image_transformation_0(image)
    model = load_model("LBP_GLCM0")
    
    print("lineDATA ---------")
    print("lineDATA ---------")
    print(len(lineDATA))
    print(lineDATA)
    print(len(lineDATA))
    print("lineDATA ---------")
    print("lineDATA ---------")
    
    #return model.predict_proba((np.array(lineDATA)).reshape(1, -1))
    return model.predict(lineDATA.reshape(1, -1))[0]

def modelML_(imagePATH, pretraitement):
    if pretraitement=="GLCM0" :
        return SousmodelsGLCM0(imagePATH)
    elif pretraitement=="GLCM90" :
        return SousmodelsGLCM90(imagePATH)
    else :
        return SousmodelsLBP(imagePATH)

def modelML(imagePATH, pretraitement):
    
    if True:
        return GLModel(imagePATH)
        

class ClassifierImView(View):
    
    def get(self, request):
        print(path_own)
        return render(request, "RImageModel/index.html", context={"form" : ImageFaceForm()})
    
    def post(self, request):
        TabP = {
            "LBP_GLCM" : 1,
        }
        formIm = ImageFaceForm(self.request.POST, self.request.FILES)
        print("self.request.POST -------------")
        print(self.request.POST)
        print("self.request.POST -------------")
        if formIm.is_valid():
            ImModel = formIm.save()
            return redirect(f"/identification/{ImModel.id}/{TabP[self.request.POST['pretraitement']]}/")
            #return redirect(f"/identification/{ImModel.id}/")
        return redirect("/predict/", )


class ModelIdentification(View):
    
    def get(self, request, imId, pretraitement):
        TabP = {
            '1' : "LBP_GLCM",
        }
        image = ImageToClassifi.objects.filter(pk=imId).first()
        print("------------------")
        print(image)
        print(image.image.url)
        print("-----------------------")
        ImClass = modelML(image.image.url, TabP[pretraitement])
        context = {"image": image.image, "identite": ImClass}
        return render(request, "RImageModel/visage.html", context=context)

