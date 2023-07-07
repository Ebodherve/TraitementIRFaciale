from django.shortcuts import render, redirect
from django.views import View
from RImageModel.forms import ImageFaceForm
from RImageModel.models import ImageToClassifi



def modelML(imageQS, pretraitement):
    return "Unknow"


class ClassifierImView(View):
    
    def get(self, request):
        return render(request, "RImageModel/index.html", context={"form" : ImageFaceForm()})
    
    def post(self, request):
        TabP = {
            "GLCM" : 1,
            "LGP" : 2,
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
            '1' : "GLCM",
            '2' : "LGP",
        }
        image = ImageToClassifi.objects.filter(pk=imId).first()
        print("------------------")
        print(image)
        print(image.image.url)
        print("-----------------------")
        ImClass = modelML(image, TabP[pretraitement])
        context = {"image": image.image, "identite": ImClass}
        return render(request, "RImageModel/visage.html", context=context)

