from django.shortcuts import render, redirect
from django.views import View
from RImageModel.forms import ImageFaceForm
from RImageModel.models import ImageToClassifi
from RImageModel.modelML import *
import os
import numpy as np


path_own = os.getcwd()

from skimage.io import imread


def equi_predict(predprob, classes=np.array(["Assu","EBODE", "Joel", "Lador","Landry", "Ridano", ])):
    return classes[np.argmax(predprob)]

def SousmodelsLBP(imagePATH, ):
    imP = path_own+imagePATH
    image = from_color_to_gray_level(imread(imP))
    model = load_model("LBP")
    image = image_transformation(image, "LBP")
    
    classes = np.array
    return equi_predict(model.predict_proba(image.reshape(1, -1)))

def SousmodelsGLCM0(imagePATH, ):
    imP = path_own+imagePATH
    image = from_color_to_gray_level(imread(imP))
    model = load_model("GLCM0")
    image = image_transformation(image, "GLCM0")
    
    return equi_predict(model.predict_proba(image.reshape(1, -1)))

def SousmodelsGLCM90(imagePATH, ):
    imP = path_own+imagePATH
    image = from_color_to_gray_level(imread(imP))
    model = load_model("GLCM90")
    image = image_transformation(image, "GLCM90")
    
    return equi_predict(model.predict_proba(image.reshape(1, -1)))

def modelML(imagePATH, pretraitement):
    
    if pretraitement=="GLCM0" :
        return SousmodelsGLCM0(imagePATH)
    elif pretraitement=="GLCM90" :
        return SousmodelsGLCM90(imagePATH)
    else :
        return SousmodelsLBP(imagePATH)
    
    #return "Unknow"


class ClassifierImView(View):
    
    def get(self, request):
        print(path_own)
        return render(request, "RImageModel/index.html", context={"form" : ImageFaceForm()})
    
    def post(self, request):
        TabP = {
            "LBP" : 1,
            "GLCM0" : 2,
            "GLCM90" : 3,
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
            '1' : "LBP",
            '2' : "GLCM0",
            '3' : "GLCM90",
        }
        image = ImageToClassifi.objects.filter(pk=imId).first()
        print("------------------")
        print(image)
        print(image.image.url)
        print("-----------------------")
        ImClass = modelML(image.image.url, TabP[pretraitement])
        context = {"image": image.image, "identite": ImClass}
        return render(request, "RImageModel/visage.html", context=context)

