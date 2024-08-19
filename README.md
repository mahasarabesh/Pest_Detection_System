# Pest_Detection_System
This project focuses on the development of a custom-trained machine learning model using TensorFlow, Keras, and OpenCV in Python 3 to accurately classify pests. The system is designed as an IoT-based mobile unit capable of real-time data transmission to a remote server. The hardware setup includes a Raspberry Pi 5 equipped with a camera module, which captures and processes images of pests,then uploads the classification results to the cloud via Wi-Fi.

 In addition to the detection unit, the project includes a server program that displays the results in real-time on a remote PC, offering live monitoring capabilities. Furthermore, a summarization program is provided to visualize the aggregated results, enabling detailed analysis and trend tracking. This solution offers a comprehensive approach to pest management, aiding in timely interventions and promoting sustainable farming practices.

# Code_Overview

Program/Server/PestDetectionSystem_Server.py :

    Purpose: Handles the pest classification process and the Data Transmission to the cloud via Wi-Fi.

    Key Components:
        Data Preprocessing: Utilizes PiCamera and OpenCV to preprocess the images captured by the camera module.
        Prediction: Runs inference on new images and labels the identified pests.
        Data Transmission: Transfers the result values to the ThingSpeak Cloud via WiFi.

Program/Server/PestDetectionSystem_Client.py :
    
    Purpose: Runs the server program to receive and display real-time results on a remote PC.

    Key Components:
        Data Retrieval: Gets the result data from the ThingSpeak Cloud.

        Real-Time Visualization: Displays the classification results in real-time using tkinter.

        Data Storing: Stores the retrieved data  into a CSV file for further usage.

Program/Server/PestDetectionSystem_summarize.py :

    Purpose: Provides a summarized visualization of the data received by the server over time.

    Key Components: 
        Data Aggregation: Collects and organizes the classification results.

        Visualization: Uses Matplotlib and seaborn to generate charts and graphs for Representation and Analysis.