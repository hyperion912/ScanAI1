from django.shortcuts import render
from django.views import View
from .forms import ImageForm
from . models import AlzheimerImages
from django.shortcuts import redirect
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.layers import TFSMLayer
import tensorflow as tf
from tensorflow import keras





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

class AlzheimerResultView(View):
    def get(self, request):
        file_name = request.session.get('file_name', None)
        classes = ['Mild_Demented', 'Moderate_Demented', 'Non_Demented', 'Very_Mild_Demented']
        model = tf.saved_model.load('/home/abhishek/Desktop/ai_project/ScanAI/models/Alzheimer_model_savedmodel')

        def preprocess_image(image_path):
            img = image.load_img(image_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            return img_array

        # Path to your individual image
        image_path =  "/home/abhishek/Desktop/ai_project/ScanAI/media/alzheimer/" + file_name

        # Preprocess the image
        preprocessed_image = preprocess_image(image_path)

        # Make predictions
        predictions = model(preprocessed_image)

        # Print the predicted class
        print(predictions)

        predictcted_class_index = np.argmax(predictions)
        predicted_class = classes[predictcted_class_index]

        return render(request, 'diagnose/result_web/alzheimer_result.html',{
            'predicted': predicted_class
        })
    
