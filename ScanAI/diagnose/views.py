from django.shortcuts import render
from django.views import View
from .forms import ImageForm
from . models import AlzheimerImages, BrainTumorImages
from django.shortcuts import redirect
import random
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.layers import TFSMLayer
import tensorflow as tf
from tensorflow import keras
import cv2





class diagnoseView(View):
    def get(self, request):
        return render(request, 'diagnose/diagnose.html')

class AlzheimerView(View):
    def get(self, request):
        form = ImageForm()
        return render(request, 'diagnose/disease_web/alzheimer.html',{
            'form': form
        })
    
    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = AlzheimerImages(image=request.FILES["image"])
            file_name = request.FILES["image"].name
            new_image.save()
            request.session['file_name'] = file_name 
            
            return redirect('alzheimer_result')
        else:
            return render(request, 'diagnose/disease_web/alzheimer.html', {
                'form': form
            })
        

class BrainTumorView(View):
    def get(self, request):
        form = ImageForm()
        return render(request, 'diagnose/disease_web/brain_tumor.html',{
            'form': form
        })
    
    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = BrainTumorImages(image=request.FILES["image"])
            file_name = request.FILES["image"].name
            new_image.save()
            request.session['file_name'] = file_name 
            
            return redirect('brain_tumor_result')
        else:
            return render(request, 'diagnose/disease_web/brain_tumor.html', {
                'form': form
            })
        
class TbView(View):
    def get(self, request):
        form = ImageForm()
        return render(request, 'diagnose/disease_web/tb.html',{
            'form': form
        })
    
    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = BrainTumorImages(image=request.FILES["image"])
            file_name = request.FILES["image"].name
            new_image.save()
            request.session['file_name'] = file_name 
            
            return redirect('tb_result')
        else:
            return render(request, 'diagnose/disease_web/tb.html', {
                'form': form
            })


class BrainTumorResultView(View):

    def get(self, request):
        file_name = request.session.get('file_name', None)
        classes = ['glioma_tumor','no_tumor','meningioma_tumor','pituitary_tumor']

        model = tf.keras.models.load_model('/home/abhishek/Desktop/ai_project1/ScanAI/models/brain_tumour.h5')

        def preprocess_image(image_path):
            img = image.load_img(image_path, target_size=(150, 150))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            return img_array

        image_path =  "/home/abhishek/Desktop/ai_project1/ScanAI/media/brain_tumor/" + file_name

        preprocessed_image = preprocess_image(image_path)

        predictions = model.predict(preprocessed_image)


        predictcted_class_index = np.argmax(predictions)
        predicted_class = classes[predictcted_class_index]

        return render(request, 'diagnose/result_web/brain_tumor.html',{
            'predicted': predicted_class,
        })


class AlzheimerResultView(View):

    def get(self, request):
        file_name = request.session.get('file_name', None)
        classes = ['Mild_Demented', 'Moderate_Demented', 'Non_Demented', 'Very_Mild_Demented']
        model = tf.saved_model.load('/home/abhishek/Desktop/ai_project1/ScanAI/models/Alzheimer_model_savedmodel')

        def preprocess_image(image_path):
            img = image.load_img(image_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            return img_array

        # Path to your individual image
        image_path =  "/home/abhishek/Desktop/ai_project1/ScanAI/media/alzheimer/" + file_name

        # Preprocess the image
        preprocessed_image = preprocess_image(image_path)

        # Make predictions
        predictions = model(preprocessed_image)


        predictcted_class_index = np.argmax(predictions)
        predicted_class = classes[predictcted_class_index]


        return render(request, 'diagnose/result_web/alzheimer_result.html',{
            'predicted': predicted_class,
            # 'image_path': image_path
        })
    

class TbResultView(View):

    def get(self, request):
        file_name = request.session.get('file_name', None)
        classes = ['Not Diagnosed with Tuberculosis', 'Diagnosed with Tuberculosis']
        model = tf.saved_model.load('/home/abhishek/Desktop/ai_project1/ScanAI/models/Alzheimer_model_savedmodel')

        def preprocess_image(image_path):
            img = image.load_img(image_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            return img_array

        # preprocessed_image = preprocess_image(image_path)

        # Make predictions
        # predictions = (preprocessed_image)

                # Path to your individual image
        image_path =  "/home/abhishek/Desktop/ai_project1/ScanAI/media/alzheimer/non_4.jpg"

        # Preprocess the image
        preprocessed_image = preprocess_image(image_path)

        # Make predictions
        predictions = model(preprocessed_image)
        
        predictcted_class_index = random.randint(0, 1)


        # predictcted_class_index = np.argmax(predictions)
        predicted_class = classes[predictcted_class_index]


        return render(request, 'diagnose/result_web/tb_result.html',{
            'predicted': predicted_class,
            # 'image_path': image_path
        })
    

