from django.shortcuts import render
from django.http  import HttpResponse
# Create your views here.
from django.http import FileResponse
from django.conf import settings
import os
import pandas as pd
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.models import model_from_json
from sklearn.preprocessing import StandardScaler
import statistics
import matplotlib.pyplot as plt
import pandas as pd
import base64
import io
from .models import ContactForm
def get_model():
    
    global model
    #json_file = open("D:\dowmload\model3.json","r")
    json_file = open("E:\BEproj\model3.json","r")
    loaded_model_json = json_file.read()
    model = model_from_json(loaded_model_json)
    json_file.close()
    
    #model.load_weights("D:\dowmload\model_for_json3.h5")
    model.load_weights("E:\BEproj\model_for_json3.h5")
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
    form_name = request.POST.get('form_name')
    if request.method == 'POST' and request.POST.get('name'):
        

        if(form_name == "form2"):
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')

        # Create a new instance of the ContactForm model
            contact_form = ContactForm(name=name, email=email, message=message)

        # Save the contact_form instance to the database
            contact_form.save()
    
    if request.method == 'POST' and  form_name == "form1":
        file = request.FILES.get('file', None)
        if file is not None:
            df = pd.read_csv(file)
            scaler = StandardScaler()

            df.iloc[:,:-1] = scaler.fit_transform(df.iloc[:,:-1])
            print(df)
            df = df[:1300]
            X = df.iloc[:,1:].values.reshape(-1, 20, 13, 1)


            get_model()
            pred = model.predict(X).argmax(axis=1)
            dictio = {0: 'F0L', 1: 'F0M', 2: 'F1L', 3: 'F1M', 4: 'F2L', 5: 'F2M', 6: 'F3L', 7: 'F3M', 8: 'F4L', 9: 'F4M', 10: 'F5L', 11: 'F5M', 12: 'F6L', 13: 'F6M', 14: 'F7L', 15: 'F7M'}
            fault_pie = {
                2: 'Inverter fault',
                4: 'Feedback Sensor fault',
                6: 'Grid anomaly',
                8: 'PV array mismatch',
                10: 'PV array mismatch',
                12: 'MPPT/IPPT controller fault',
                14: 'Boost converter controller fault',
                3: 'Inverter fault',
                5: 'Feedback Sensor fault',
                7: 'Grid anomaly',
                9: 'PV array mismatch',
                11: 'PV array mismatch',
                13: 'MPPT/IPPT controller fault',
                15: 'Boost converter controller fault',
                1 : 'NORMAL',
                0 : 'NORMAL',

            }
            df_pred = pd.DataFrame({'Prediction': pred})
            class_counts = df_pred['Prediction'].value_counts()
            class_counts.index = class_counts.index.map(fault_pie)
            fig, ax = plt.subplots()
            ax.pie(class_counts, labels=class_counts.index, autopct='%1.1f%%')
            ax.set_aspect('equal')
            ax.set_title('Prediction Distribution')
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            chart_data = base64.b64encode(buffer.read()).decode('utf-8')

            mode = statistics.mode(pred)

            fault_names = {
                'F1L': 'Inverter fault',
                'F2L': 'Feedback Sensor fault',
                'F3L': 'Grid anomaly',
                'F4L': 'PV array mismatch',
                'F5L': 'PV array mismatch',
                'F6L': 'MPPT/IPPT controller fault',
                'F7L': 'Boost converter controller fault',
                'F1M': 'Inverter fault',
                'F2M': 'Feedback Sensor fault',
                'F3M': 'Grid anomaly',
                'F4M': 'PV array mismatch',
                'F5M': 'PV array mismatch',
                'F6M': 'MPPT/IPPT controller fault',
                'F7M': 'Boost converter controller fault',
                'F0M' : 'NORMAL',
                'F0L' : 'NORMAL',

            }
            fault_description = {
                'F1L': "<center><h2>Major Fault:Inverter Fault in Solar Panel(F1L)</h2></center><h3>Fault Description</h3><p>An inverter fault in a solar panel system refers to a malfunction or failure specifically in the inverter component. In a solar panel setup, the inverter is responsible for converting the direct current (DC) power generated by the solar panels into usable alternating current (AC) power for various electrical devices.</p><p>There can be various causes of inverter faults in solar panels, such as electrical surges, component failure, excessive heat, or improper installation. When an inverter fault occurs, it can lead to a disruption in the power supply and may result in the inverter shutting down or producing unstable AC power.</p><h3>Solution</h3><button onclick='toggleSolution()'>Show Solution</button><div id='solution' style='display: none;'><p>When encountering an inverter fault in a solar panel system, it is important to follow these steps to resolve the issue:</p><ol><li>Check the display or indicators on the inverter to identify the specific fault or error message.</li><li>Refer to the inverter's user manual or documentation to understand the meaning of the fault code or error message.</li><li>If possible, try to reset the inverter by turning it off and then back on. This can sometimes resolve minor faults or temporary issues.</li><li>If the fault persists, it is advisable to contact a qualified electrician or the manufacturer's technical support for further assistance. They will be able to diagnose the problem accurately and provide guidance on the necessary repairs or replacements.</li></ol></div><script>function toggleSolution(){var solution=document.getElementById('solution');if(solution.style.display==='none'){solution.style.display='block';}else{solution.style.display='none';}}</script>",
                'F2L': "<center><h2>Major Fault:Feedback Sensor Fault(F2L)</h2></center><h3>Sensor Fault in Solar Panel</h3><p>A feedback sensor fault in a solar panel system refers to a malfunction or failure specifically in the sensor component. Sensors are used in solar panels to measure various parameters such as sunlight intensity, temperature, or position to optimize the panel's performance.</p><p>A sensor fault can occur due to various reasons, including sensor damage, wiring issues, or sensor calibration problems. When a sensor fault happens, it can lead to inaccurate readings, improper system control, or even system shutdown.</p><h3>Solution</h3><button onclick='toggleSolution()'>Show Solution</button><div id='solution' style='display: none;'><p>To address a sensor fault in a solar panel system, follow these steps:</p><ol><li>Check the sensor connections and wiring to ensure they are securely connected and free from any damage or corrosion.</li><li>Inspect the sensor for any physical damage or signs of wear. If the sensor is damaged, it may need to be replaced.</li><li>Calibrate the sensor according to the manufacturer's instructions. Incorrect calibration can lead to faulty readings.</li><li>If the sensor fault persists, consult a qualified technician or contact the manufacturer for further assistance. They can provide guidance on troubleshooting and resolving the sensor fault.</li><li>Regular maintenance and monitoring of the sensor system can help detect and prevent sensor faults. Consider implementing a scheduled maintenance plan to ensure the sensors are functioning correctly.</li></ol></div><script>function toggleSolution(){var solution=document.getElementById('solution');if(solution.style.display==='none'){solution.style.display='block';}else{solution.style.display='none';}}</script>",
                'F3L': "<center><h2>Major Fault:Grid Anomaly Fault in Solar Panel(F3L)</h2></center><h3>Description</h3><p>A grid anomaly fault in a solar panel system refers to an issue where the solar panel system is unable to properly synchronize with the electrical grid. In a grid-tied solar panel system, the generated electricity is typically fed back into the grid. However, a grid anomaly fault disrupts this process, leading to inefficient power utilization or complete disconnection from the grid.</p><p>Grid anomalies can occur due to various reasons, such as voltage fluctuations, frequency mismatches, or problems with the grid infrastructure. These faults can impact the stability and performance of the solar panel system, affecting its overall energy production.</p><h3>Solution</h3><button onclick='toggleSolution()'>Show Solution</button><div id='solution' style='display:none;'><p>To address a grid anomaly fault in a solar panel system, the following steps can be taken:</p><ol><li>Check the electrical connections and ensure they are properly grounded and securely connected to the grid.</li><li>Inspect the solar inverter to ensure it is functioning correctly and configured to synchronize with the grid.</li><li>Verify the voltage and frequency settings of the solar panel system to match the requirements of the electrical grid.</li><li>If the fault persists, contact the local utility company or a qualified electrician to investigate and resolve any grid-related issues.</li><li>Consider implementing additional protective devices, such as surge protectors or voltage regulators, to mitigate the impact of future grid anomalies.</li></ol></div><script>function toggleSolution(){var solution=document.getElementById('solution');if(solution.style.display==='none'){solution.style.display='block';}else{solution.style.display='none';}}</script>",
                'F4L': "<center><h2>Major Fault:PV Array Mismatch(F4L)</h2></center><h3>10 to 20% Nonhomogeneous Partial Shading Fault in Solar Panel</h3><p>A PV array mismatch refers to an issue in a solar panel system where there is a 10 to 20% nonhomogeneous partial shading fault. Nonhomogeneous partial shading occurs when certain sections or cells of the PV array are shaded, leading to an imbalance in power production.</p><p>Shading can occur due to various factors, such as nearby structures, trees, or debris on the solar panels. When shaded, some parts of the PV array produce less electricity, resulting in a mismatch between the shaded and unshaded areas.</p><p>This mismatch can lead to a decrease in the overall power output of the solar panel system. It can also cause hotspots, voltage drops, and reduced efficiency.</p><h3>Solution</h3><button onclick='toggleSolution()'>Show Solution</button><div id='solution'><p>To address a 10 to 20% nonhomogeneous partial shading fault in the PV array of a solar panel system, consider the following solutions:</p><ul><li>Conduct a shading analysis to identify the specific areas of shading in the PV array. This analysis can help determine the extent and impact of the shading on the system's performance.</li><li>Consider repositioning or trimming any nearby objects, structures, or vegetation that are causing shading on the solar panels.</li><li>Opt for technologies like bypass diodes or power optimizers that can mitigate the effects of shading by redirecting or optimizing the current flow.</li><li>If the shading issue is persistent, it may be necessary to redesign the PV array configuration or consider alternative locations for the solar panels.</li><li>Regular cleaning and maintenance of the solar panels can help minimize the impact of shading and ensure optimal performance.</li></ul></div><style>#solution{display:none;}</style><script>function toggleSolution(){var solution=document.getElementById('solution');if(solution.style.display==='none'){solution.style.display='block';}else{solution.style.display='none';}}</script>",
                'F6L': "<center><h2>Major Fault:MPPT/IPPT Controller Fault in Solar Panel(F6L)</h2></center><h3>Description</h3><p>An MPPT (Maximum Power Point Tracking) or IPPT (Integrated Power Point Tracking) controller fault in a solar panel system refers to an issue with the controller responsible for optimizing the power output from the solar panels. The MPPT/IPPT controller is designed to adjust the operating voltage and current to maximize the power generated by the solar panels.</p><p>A fault in the MPPT/IPPT controller can occur due to various reasons, such as component failure, improper configuration, or environmental factors. This fault can result in suboptimal power output, inefficient energy conversion, or even complete shutdown of the solar panel system.</p><h3>Solution</h3><button onclick='toggleSolution()'>Show Solution</button><div id='solution'><p>When encountering an MPPT/IPPT controller fault in a solar panel system, it is important to follow these steps to address the issue:</p><ol><li>Check the controller's display or indicators for any error messages or fault codes.</li><li>Refer to the controller's user manual or documentation to understand the meaning of the fault code or error message.</li><li>Inspect the wiring connections between the controller and the solar panels to ensure they are secure and properly connected.</li><li>If possible, try resetting the controller by turning it off and then back on. This may help resolve minor faults or temporary issues.</li><li>If the fault persists, contact the manufacturer or a qualified technician for further assistance. They will be able to diagnose the problem accurately and provide guidance on repairs or replacements.</li></ol></div><script>function toggleSolution(){var solution=document.getElementById('solution');if(solution.style.display==='none'){solution.style.display='block';}else{solution.style.display='none';}}</script><style>#solution{display:none;}</style>",
                'F7L': "<center><h2>Major Fault:Boost Converter Controller Fault in Solar Panel(F7L)</h2></center><h3>Description</h3><p>A boost converter controller fault in a solar panel system refers to a malfunction or failure specifically in the boost converter controller. The boost converter is an electronic device used in solar panel systems to efficiently increase the voltage output from the solar panels.</p><p>A controller fault in the boost converter can occur due to various reasons, such as component failure, improper calibration, software issues, or electrical surges. When the controller is faulty, it can result in unstable voltage output, inefficient power conversion, or even complete system shutdown.</p><h3>Solution</h3><button onclick='toggleSolution()'>Show Solution</button><div id='solution' style='display: none;'><p>To address a boost converter controller fault in a solar panel system, the following steps can be taken:</p><ol><li>Check the boost converter controller for any visible signs of damage or loose connections.</li><li>Ensure that the controller is properly calibrated and configured according to the manufacturer's specifications.</li><li>Inspect the wiring connections between the boost converter and the solar panels to ensure they are secure and correctly connected.</li><li>If possible, reset the boost converter controller by turning it off and on again. This can sometimes resolve minor software or transient issues.</li><li>If the fault persists, consult the manufacturer's documentation or contact their technical support for further assistance. They can provide guidance on troubleshooting steps or arrange for repairs or replacement of the boost converter controller if necessary.</li></ol></div><script>function toggleSolution(){var solution=document.getElementById('solution');if(solution.style.display==='none'){solution.style.display='block';}else{solution.style.display='none';}}</script>",
                'F1M': "<center><h2>Major Fault:Inverter Fault in Solar Panel(F1M)</h2></center><h3>Fault Description</h3><p>An inverter fault in a solar panel system refers to a malfunction or failure specifically in the inverter component. In a solar panel setup, the inverter is responsible for converting the direct current (DC) power generated by the solar panels into usable alternating current (AC) power for various electrical devices.</p><p>There can be various causes of inverter faults in solar panels, such as electrical surges, component failure, excessive heat, or improper installation. When an inverter fault occurs, it can lead to a disruption in the power supply and may result in the inverter shutting down or producing unstable AC power.</p><h3>Solution</h3><button onclick='toggleSolution()'>Show Solution</button><div id='solution' style='display: none;'><p>When encountering an inverter fault in a solar panel system, it is important to follow these steps to resolve the issue:</p><ol><li>Check the display or indicators on the inverter to identify the specific fault or error message.</li><li>Refer to the inverter's user manual or documentation to understand the meaning of the fault code or error message.</li><li>If possible, try to reset the inverter by turning it off and then back on. This can sometimes resolve minor faults or temporary issues.</li><li>If the fault persists, it is advisable to contact a qualified electrician or the manufacturer's technical support for further assistance. They will be able to diagnose the problem accurately and provide guidance on the necessary repairs or replacements.</li></ol></div><script>function toggleSolution(){var solution=document.getElementById('solution');if(solution.style.display==='none'){solution.style.display='block';}else{solution.style.display='none';}}</script>",
                'F2M': "<center><h2>Major Fault:Feedback Sensor Fault(F2M)</h2></center><h3>Sensor Fault in Solar Panel</h3><p>A feedback sensor fault in a solar panel system refers to a malfunction or failure specifically in the sensor component. Sensors are used in solar panels to measure various parameters such as sunlight intensity, temperature, or position to optimize the panel's performance.</p><p>A sensor fault can occur due to various reasons, including sensor damage, wiring issues, or sensor calibration problems. When a sensor fault happens, it can lead to inaccurate readings, improper system control, or even system shutdown.</p><h3>Solution</h3><button onclick='toggleSolution()'>Show Solution</button><div id='solution' style='display: none;'><p>To address a sensor fault in a solar panel system, follow these steps:</p><ol><li>Check the sensor connections and wiring to ensure they are securely connected and free from any damage or corrosion.</li><li>Inspect the sensor for any physical damage or signs of wear. If the sensor is damaged, it may need to be replaced.</li><li>Calibrate the sensor according to the manufacturer's instructions. Incorrect calibration can lead to faulty readings.</li><li>If the sensor fault persists, consult a qualified technician or contact the manufacturer for further assistance. They can provide guidance on troubleshooting and resolving the sensor fault.</li><li>Regular maintenance and monitoring of the sensor system can help detect and prevent sensor faults. Consider implementing a scheduled maintenance plan to ensure the sensors are functioning correctly.</li></ol></div><script>function toggleSolution(){var solution=document.getElementById('solution');if(solution.style.display==='none'){solution.style.display='block';}else{solution.style.display='none';}}</script>",
                'F3M': "<center><h2>Major Fault:Grid Anomaly Fault in Solar Panel(F3M)</h2></center><h3>Description</h3><p>A grid anomaly fault in a solar panel system refers to an issue where the solar panel system is unable to properly synchronize with the electrical grid. In a grid-tied solar panel system, the generated electricity is typically fed back into the grid. However, a grid anomaly fault disrupts this process, leading to inefficient power utilization or complete disconnection from the grid.</p><p>Grid anomalies can occur due to various reasons, such as voltage fluctuations, frequency mismatches, or problems with the grid infrastructure. These faults can impact the stability and performance of the solar panel system, affecting its overall energy production.</p><h3>Solution</h3><button onclick='toggleSolution()'>Show Solution</button><div id='solution' style='display:none;'><p>To address a grid anomaly fault in a solar panel system, the following steps can be taken:</p><ol><li>Check the electrical connections and ensure they are properly grounded and securely connected to the grid.</li><li>Inspect the solar inverter to ensure it is functioning correctly and configured to synchronize with the grid.</li><li>Verify the voltage and frequency settings of the solar panel system to match the requirements of the electrical grid.</li><li>If the fault persists, contact the local utility company or a qualified electrician to investigate and resolve any grid-related issues.</li><li>Consider implementing additional protective devices, such as surge protectors or voltage regulators, to mitigate the impact of future grid anomalies.</li></ol></div><script>function toggleSolution(){var solution=document.getElementById('solution');if(solution.style.display==='none'){solution.style.display='block';}else{solution.style.display='none';}}</script>",
                'F4M': "<center><h2>Major Fault:PV Array Mismatch(F4M)</h2></center><h3>10 to 20% Nonhomogeneous Partial Shading Fault in Solar Panel</h3><p>A PV array mismatch refers to an issue in a solar panel system where there is a 10 to 20% nonhomogeneous partial shading fault. Nonhomogeneous partial shading occurs when certain sections or cells of the PV array are shaded, leading to an imbalance in power production.</p><p>Shading can occur due to various factors, such as nearby structures, trees, or debris on the solar panels. When shaded, some parts of the PV array produce less electricity, resulting in a mismatch between the shaded and unshaded areas.</p><p>This mismatch can lead to a decrease in the overall power output of the solar panel system. It can also cause hotspots, voltage drops, and reduced efficiency.</p><h3>Solution</h3><button onclick='toggleSolution()'>Show Solution</button><div id='solution'><p>To address a 10 to 20% nonhomogeneous partial shading fault in the PV array of a solar panel system, consider the following solutions:</p><ul><li>Conduct a shading analysis to identify the specific areas of shading in the PV array. This analysis can help determine the extent and impact of the shading on the system's performance.</li><li>Consider repositioning or trimming any nearby objects, structures, or vegetation that are causing shading on the solar panels.</li><li>Opt for technologies like bypass diodes or power optimizers that can mitigate the effects of shading by redirecting or optimizing the current flow.</li><li>If the shading issue is persistent, it may be necessary to redesign the PV array configuration or consider alternative locations for the solar panels.</li><li>Regular cleaning and maintenance of the solar panels can help minimize the impact of shading and ensure optimal performance.</li></ul></div><style>#solution{display:none;}</style><script>function toggleSolution(){var solution=document.getElementById('solution');if(solution.style.display==='none'){solution.style.display='block';}else{solution.style.display='none';}}</script>",
                'F5L': "<center><h2>Major Fault:PV Array Mismatch Fault(F5L)</h2></center><h3>15% Open Circuit in PV Array in Solar Panel</h3><p>A PV array mismatch fault refers to an issue in a solar panel system where there is a 15% open circuit in the PV (Photovoltaic) array. The PV array consists of multiple solar panels connected in series or parallel to generate electricity from sunlight.</p><p>An open circuit in the PV array occurs when there is a break or disconnection in the electrical circuit, preventing the flow of current. In the case of a 15% open circuit fault, it means that approximately 15% of the PV array is not contributing to the overall electricity generation.</p><p>This fault can happen due to mismatched solar panels, where one or more panels have different electrical characteristics compared to the rest of the array. Mismatched panels can result from variations in manufacturing, shading, soiling, aging, or different orientations. These differences lead to a mismatch in the current or voltage output, reducing the overall performance of the PV array.</p><h3>Solution</h3><button onclick='toggleSolution()'>Show Solution</button><div id='solution' style='display: none;'><p>To address a 15% open circuit fault due to PV array mismatch, the following steps can be taken:</p><ol><li>Inspect the PV array carefully to identify any visibly mismatched panels, such as panels with shading, damage, or dirt accumulation.</li><li>Ensure that all the panels are properly connected and the wiring is secure.</li><li>If a mismatched panel is identified, it may need to be replaced or repositioned to minimize the mismatch and restore optimal performance.</li><li>Consider cleaning the panels to remove any dirt or debris that could contribute to shading or soiling mismatch.</li><li>Regularly monitor the PV array's performance and consider conducting periodic maintenance to identify and address any potential mismatch issues.</li></ol></div><script>function toggleSolution(){var solution=document.getElementById('solution');if(solution.style.display==='none'){solution.style.display='block';}else{solution.style.display='none';}}</script>",
                'F5M': "<center><h2>Major Fault:PV Array Mismatch Fault(F5M)</h2></center><h3>15% Open Circuit in PV Array in Solar Panel</h3><p>A PV array mismatch fault refers to an issue in a solar panel system where there is a 15% open circuit in the PV (Photovoltaic) array. The PV array consists of multiple solar panels connected in series or parallel to generate electricity from sunlight.</p><p>An open circuit in the PV array occurs when there is a break or disconnection in the electrical circuit, preventing the flow of current. In the case of a 15% open circuit fault, it means that approximately 15% of the PV array is not contributing to the overall electricity generation.</p><p>This fault can happen due to mismatched solar panels, where one or more panels have different electrical characteristics compared to the rest of the array. Mismatched panels can result from variations in manufacturing, shading, soiling, aging, or different orientations. These differences lead to a mismatch in the current or voltage output, reducing the overall performance of the PV array.</p><h3>Solution</h3><button onclick='toggleSolution()'>Show Solution</button><div id='solution' style='display: none;'><p>To address a 15% open circuit fault due to PV array mismatch, the following steps can be taken:</p><ol><li>Inspect the PV array carefully to identify any visibly mismatched panels, such as panels with shading, damage, or dirt accumulation.</li><li>Ensure that all the panels are properly connected and the wiring is secure.</li><li>If a mismatched panel is identified, it may need to be replaced or repositioned to minimize the mismatch and restore optimal performance.</li><li>Consider cleaning the panels to remove any dirt or debris that could contribute to shading or soiling mismatch.</li><li>Regularly monitor the PV array's performance and consider conducting periodic maintenance to identify and address any potential mismatch issues.</li></ol></div><script>function toggleSolution(){var solution=document.getElementById('solution');if(solution.style.display==='none'){solution.style.display='block';}else{solution.style.display='none';}}</script>",
                'F6M': "<center><h2>Major Fault:MPPT/IPPT Controller Fault in Solar Panel(F6M)</h2></center><h3>Description</h3><p>An MPPT (Maximum Power Point Tracking) or IPPT (Integrated Power Point Tracking) controller fault in a solar panel system refers to an issue with the controller responsible for optimizing the power output from the solar panels. The MPPT/IPPT controller is designed to adjust the operating voltage and current to maximize the power generated by the solar panels.</p><p>A fault in the MPPT/IPPT controller can occur due to various reasons, such as component failure, improper configuration, or environmental factors. This fault can result in suboptimal power output, inefficient energy conversion, or even complete shutdown of the solar panel system.</p><h3>Solution</h3><button onclick='toggleSolution()'>Show Solution</button><div id='solution'><p>When encountering an MPPT/IPPT controller fault in a solar panel system, it is important to follow these steps to address the issue:</p><ol><li>Check the controller's display or indicators for any error messages or fault codes.</li><li>Refer to the controller's user manual or documentation to understand the meaning of the fault code or error message.</li><li>Inspect the wiring connections between the controller and the solar panels to ensure they are secure and properly connected.</li><li>If possible, try resetting the controller by turning it off and then back on. This may help resolve minor faults or temporary issues.</li><li>If the fault persists, contact the manufacturer or a qualified technician for further assistance. They will be able to diagnose the problem accurately and provide guidance on repairs or replacements.</li></ol></div><script>function toggleSolution(){var solution=document.getElementById('solution');if(solution.style.display==='none'){solution.style.display='block';}else{solution.style.display='none';}}</script><style>#solution{display:none;}</style>",
                'F7M': "<center><h2>Major Fault:Boost Converter Controller Fault in Solar Panel(F7M)</h2></center><h3>Description</h3><p>A boost converter controller fault in a solar panel system refers to a malfunction or failure specifically in the boost converter controller. The boost converter is an electronic device used in solar panel systems to efficiently increase the voltage output from the solar panels.</p><p>A controller fault in the boost converter can occur due to various reasons, such as component failure, improper calibration, software issues, or electrical surges. When the controller is faulty, it can result in unstable voltage output, inefficient power conversion, or even complete system shutdown.</p><h3>Solution</h3><button onclick='toggleSolution()'>Show Solution</button><div id='solution' style='display: none;'><p>To address a boost converter controller fault in a solar panel system, the following steps can be taken:</p><ol><li>Check the boost converter controller for any visible signs of damage or loose connections.</li><li>Ensure that the controller is properly calibrated and configured according to the manufacturer's specifications.</li><li>Inspect the wiring connections between the boost converter and the solar panels to ensure they are secure and correctly connected.</li><li>If possible, reset the boost converter controller by turning it off and on again. This can sometimes resolve minor software or transient issues.</li><li>If the fault persists, consult the manufacturer's documentation or contact their technical support for further assistance. They can provide guidance on troubleshooting steps or arrange for repairs or replacement of the boost converter controller if necessary.</li></ol></div><script>function toggleSolution(){var solution=document.getElementById('solution');if(solution.style.display==='none'){solution.style.display='block';}else{solution.style.display='none';}}</script>",
                'F0M' : "<center><h2>Major Fault:No Fault in Solar Panel</h2></center><p>The solar panel system is operating without any faults. All components are functioning correctly, and there are no issues affecting the system's performance.</p><p>Regular monitoring and maintenance of the solar panel system are essential to ensure its continued optimal operation. It is recommended to schedule periodic inspections, clean the solar panels as needed, and monitor the system's power output to detect any potential future faults or inefficiencies.</p>",
                'F0L' : "<center><h2>Major Fault:No Fault in Solar Panel</h2></center><p>The solar panel system is operating without any faults. All components are functioning correctly, and there are no issues affecting the system's performance.</p><p>Regular monitoring and maintenance of the solar panel system are essential to ensure its continued optimal operation. It is recommended to schedule periodic inspections, clean the solar panels as needed, and monitor the system's power output to detect any potential future faults or inefficiencies.</p>",

            }
            name=fault_names[dictio[mode]]
            desc = fault_description[dictio[mode]]
            context = {'df': df,'chart_data': chart_data, 'pred' : name,'description': desc}
            return render(request, 'result.html', context)
    return render(request, 'index.html')

def other_faults_view(request, fault):
    # Render the appropriate template based on the fault parameter
    template_name = fault + '.html'
    return render(request, template_name)


    