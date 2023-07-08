import numpy as np
import pandas as pd
import os
from skimage.transform import resize
from skimage.io import imread
import pickle
import math

path_own = os.getcwd()

def from_color_to_gray_level(color_image):
    R, G, B = color_image[:, :, 0], color_image[:, :, 1], color_image[:, :, 2]
    gray_img = 0.2989 * R + 0.587 * G + 0.114 * B
    gray_img=gray_img.astype(int)
    
    return gray_img

def LBP(Image_matrix):
    LBP_MATRIX= np.zeros([len(Image_matrix), len(Image_matrix[0])], dtype=int)
    
    i=1
    j=1
    row_size = len(Image_matrix)-1
    col_size = len(Image_matrix[0])-1
    while i < (row_size):
        j=1
        while j<(col_size):
            # ici on applique la formule liée au calcul de d'une cellule LBP pour notre matrice LBP
            LBP_MATRIX[i][j] += (S(Image_matrix[i-1][j-1]-Image_matrix[i][j])*(2**0)+
                                 S(Image_matrix[i-1][j]-Image_matrix[i][j])*(2**1)+
                                 S(Image_matrix[i-1][j+1]-Image_matrix[i][j])*(2**2)+
                                 S(Image_matrix[i][j+1]-Image_matrix[i][j])*(2**3)+
                                 S(Image_matrix[i+1][j+1]-Image_matrix[i][j])*(2**4)+
                                 S(Image_matrix[i+1][j]-Image_matrix[i][j])*(2**5)+
                                 S(Image_matrix[i+1][j-1]-Image_matrix[i][j])*(2**6)+
                                 S(Image_matrix[i][j-1]-Image_matrix[i][j])*(2**7))
            j=j+1
        i=i+1
            
    return LBP_MATRIX

# ici on defini la fonction S pour connaitre le bit
def S(x):
    if(x >= 0):
        return 1
    else:
        return 0

# histogramme LBP Basique
def Hist_LBP(LBP_MATRIX):
    TABLE_LBP_MATRIX=[]
    for i in range(256):
        TABLE_LBP_MATRIX.append(0)
    
    for i in range(len(LBP_MATRIX)):
        for j in range(len(LBP_MATRIX[0])):
            TABLE_LBP_MATRIX[LBP_MATRIX[i][j]] += 1
            
    return TABLE_LBP_MATRIX


# fonction GLCM distance 1 direction 0 dégrés
def GLCM_0(image_matrix):
    row_matrix = len(image_matrix)
    col_matrix = len(image_matrix[1])-1
    GLCM_matrix = np.zeros([256,256],dtype=int)
    for i in range(row_matrix):
        for j in range(col_matrix):
            GLCM_matrix[image_matrix[i,j], image_matrix[i,j+1]] += 1
    return GLCM_matrix

# fonction GLCM distance 1 direction 90 dégrés
def GLCM_90(image_matrix):
    row_matrix = len(image_matrix)-1
    col_matrix = len(image_matrix[1])
    GLCM_matrix = np.zeros([256,256],dtype=int)
    for i in range(row_matrix):
        for j in range(col_matrix):
            GLCM_matrix[image_matrix[i,j], image_matrix[i+1,j]] += 1
    return GLCM_matrix

def mean_h(GLCM_matrix):
    mean=0
    print("GLCM_matrix[1] ------------------------")
    print(GLCM_matrix[1])
    print("GLCM_matrix[1] ------------------------")
    for j in range(len(GLCM_matrix[1])):
        for i in range(len(GLCM_matrix)):
            mean=mean+GLCM_matrix[i,j]
    return mean

def variance(GLCM_matrix):
    var_table= np.zeros([len(GLCM_matrix)],dtype=int)
    var=0
    for i in range (len(GLCM_matrix)):
        for j in range (len(GLCM_matrix[1])):
            var=var+(((i-mean_h(GLCM_matrix))**2)-GLCM_matrix[i,j])
        var_table[i] = var
        var=0
    return var_table

def inertie(GLCM_matrix):
    inertie=0
    for j in range(len(GLCM_matrix[1]-1)):
        for i in range(len(GLCM_matrix)):
                inertie = inertie+((i-j)**2)*GLCM_matrix[i,j]
    return inertie

def Moment_differentiel(GLCM_matrix):
    moment=0
    for i in range(len(GLCM_matrix)):
        for j in range(len(GLCM_matrix[1]-1)):
                moment = moment+ ((1/(1+(i-j)**2))*GLCM_matrix[i,j])
    return moment

def ENTROPIE(GLCM_matrix):
    entropie=0
    for j in range(len(GLCM_matrix[1])):
        for i in range(len(GLCM_matrix)):
            if GLCM_matrix[i, j] != 0:
                entropie = entropie + (-(GLCM_matrix[i,j])*(np.log(GLCM_matrix[i,j])))
    return entropie

def energie(GLCM_matrix):
    energie=0
    for j in range(len(GLCM_matrix[1]-1)):
        for i in range(len(GLCM_matrix)):
                energie=energie+GLCM_matrix[i,j]**2
    return energie

def haralick_np_feature_render(GLCM_matrix):
    res = []
    res.append(mean_h(GLCM_matrix))
    #res.append(variance(GLCM_matrix))
    res.append(inertie(GLCM_matrix))
    res.append(Moment_differentiel(GLCM_matrix))
    res.append(ENTROPIE(GLCM_matrix))
    res.append(energie(GLCM_matrix))
    
    return np.array(res)


def load_model(model_type):
    if model_type == "LBP" :
        modelFile = 'img_model_lbp.p'
    elif model_type == "GLCM0":
        modelFile = 'img_model_glcm_0.p'
    elif model_type == "LBP_GLCM0":
        modelFile = 'MODEL_GLCM_LBP.p'
    else :
        modelFile = 'img_model_glcm_90.p'
        
    path_model = path_own+"/RImageModel/model_SML/"+modelFile
    dataU = pickle.Unpickler(open(path_model,'rb'))
    model = dataU.load()

    print("chargement reussi")

    return model

def image_transformation(image, transformation_type):
    if transformation_type == "LBP" :
        img_array= LBP(image) # ici on trouve le LBP correspondant a chaque image
        img_array= np.array(Hist_LBP(img_array)) 
        img_array = (img_array - np.min(img_array))/np.max(img_array) # ici on normalise nos données en faisant du centré et réduire
        return img_array
    elif transformation_type == "GLCM0":
        img_array=GLCM_0(image)
        img_array = (img_array - np.min(img_array))/np.max(img_array) # ici on normalise nos données en faisant du centré et réduire
        feature_image = haralick_np_feature_render(img_array)
        feature_image = (feature_image - np.min(feature_image))/np.max(feature_image)
        
        return feature_image

    else:
        img_array=GLCM_90(image)
        img_array = (img_array - np.min(img_array))/np.max(img_array) # ici on normalise nos données en faisant du centré et réduire
        feature_image = haralick_np_feature_render(img_array)
        feature_image = (feature_image - np.min(feature_image))/np.max(feature_image)
        
        return feature_image

def image_transformation_0(image):
    img_array_LBP= Hist_LBP(LBP(image)) # ici on trouve le LBP correspondant a chaque image
    img_array_LBP = (img_array_LBP - np.min(img_array_LBP))/(np.max(img_array_LBP)-np.min(img_array_LBP))
    img_array_GLCM= GLCM_90(image) # ici on trouve les caractéristiques correspondant a chaque image
    img_array_GLCM = (img_array_GLCM - np.min(img_array_GLCM))/(np.max(img_array_GLCM)-np.min(img_array_GLCM))
    feature_image = haralick_np_feature_render(img_array_GLCM)
    feature_image = (feature_image - np.min(feature_image))/(np.max(feature_image)-np.min(feature_image))
    img_array = np.concatenate((img_array_LBP,feature_image))# ici on normalise nos données en faisant du centré et réduire
    
    return img_array


