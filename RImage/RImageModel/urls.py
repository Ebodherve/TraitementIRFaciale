from django.contrib import admin
from django.urls import path, include
from RImageModel.views import ClassifierImView, ModelIdentification


urlpatterns = [
    path('predict/', ClassifierImView.as_view(), name="predict"),
    path('identification/<imId>/<pretraitement>/', ModelIdentification.as_view(), name="identification"),
]

