# Advanced-Automatic-Number-Plate-Recognition-ANPR-System-for-Challenging-Number-Plates-
The proposed solution project is byild to accurately recognize the non-standard number plates with varying font styles and handle the adverse environmental conditions.

 # Introduction
 Automatic license plate detection has the ability to automatically identify the vehicle by capturing and recognizing the number plates of any vehicle with the help of an image, provided by video surveillance cameras.It has many practical applications like noting vehicle numbers at toll gate operation, tracing cars, finding stolen cars from CCTVs, etc.

 # Approach 
 To predict the license plate number, the following things need to be done:

 ![Picture1](https://github.com/ankit1970/Advanced-Automatic-Number-Plate-Recognition-ANPR-System-for-Challenging-Number-Plates-/assets/87433976/364eed40-713e-4c20-a7f8-3f892c04119a)
1. The license plate needs to be detected from the overall image. This can be done using object detection methods like finding contours, using You-Only-Look-Once (YOLO), etc.
2. After extracting the license plate, individual characters need to be seperated and segregated using character segmentation techniques like finding rectangular contours.
3. The last phase is performing character recognition, where the segmented characters are recognized using deep learning classifiers. We used CNN in this project as CNNs work the best with images.

# Project GUI
![7 starting window](https://github.com/ankit1970/Advanced-Automatic-Number-Plate-Recognition-ANPR-System-for-Challenging-Number-Plates-/assets/87433976/1c12b798-40fc-43f6-b6b4-c2b58c825a13)
![12 Overall Working](https://github.com/ankit1970/Advanced-Automatic-Number-Plate-Recognition-ANPR-System-for-Challenging-Number-Plates-/assets/87433976/7eaea635-e24a-4099-8b2c-a3c49c9fb415)
