from django.shortcuts import render
from django.http  import HttpResponse
# Create your views here.
import pandas as pd
from tensorflow.keras.models import load_model

from tensorflow.keras.models import model_from_json

from sklearn.preprocessing import StandardScaler
import statistics

def get_model():
    
    global model
    json_file = open("D:\dowmload\model.json","r")
    loaded_model_json = json_file.read()
    model = model_from_json(loaded_model_json)
    json_file.close()
    
    model.load_weights("D:\dowmload\model_for_json.h5")
    model.compile(optimizer='adam',
              loss='categorical_crossentropy', # this is different instead of binary_crossentropy (for regular classification)
                  metrics=['accuracy'])
    print("Model loaded successfully")
    
''' def upload_csv(request):
        
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        df = pd.read_csv(file)
        scaler = StandardScaler()

        df = scaler.fit_transform(df)
        print(df)
        df = pd.DataFrame(df,columns= [a for a in range(0,14)])
        print(df.head())
        print(type(df))
        X = df.iloc[0:8,1:14]
        print("-----------------------------------",X,"------------------------------")
        get_model()
        pred = model.predict(X).argmax(axis=1)
        dictio = {0: 'F0L', 1: 'F0M', 2: 'F1L', 3: 'F1M', 4: 'F2L', 5: 'F2M', 6: 'F3L', 7: 'F3M', 8: 'F4L', 9: 'F4M', 10: 'F5L', 11: 'F5M', 12: 'F6L', 13: 'F6M', 14: 'F7L', 15: 'F7M'}
        
        mode = statistics.mode(pred)

        context = {'df': df, 'pred' : dictio[mode]}
        return render(request, 'result.html', context)
    return render(request, 'upload_csv.html') '''

def home_page(request):
          
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        df = pd.read_csv(file)
        scaler = StandardScaler()

        df = scaler.fit_transform(df)
        print(df)
        df = pd.DataFrame(df,columns= [a for a in range(0,14)])
        print(df.head())
        print(type(df))
        X = df.iloc[0:8,1:14]
        print("-----------------------------------",X,"------------------------------")
        get_model()
        pred = model.predict(X).argmax(axis=1)
        dictio = {0: 'F0L', 1: 'F0M', 2: 'F1L', 3: 'F1M', 4: 'F2L', 5: 'F2M', 6: 'F3L', 7: 'F3M', 8: 'F4L', 9: 'F4M', 10: 'F5L', 11: 'F5M', 12: 'F6L', 13: 'F6M', 14: 'F7L', 15: 'F7M'}
        
        mode = statistics.mode(pred)

        context = {'df': df, 'pred' : dictio[mode]}
        return render(request, 'result.html', context)
    return render(request, 'index.html')
    