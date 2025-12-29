# photobooth

## Software Requirements 

click==8.3.1
colorama==0.4.6
numpy==2.2.6
opencv-python==4.12.0.88
pillow==12.0.0
PyQt5==5.15.9
pyqt5-plugins==5.15.9.2.3
PyQt5-Qt5==5.15.2
pyqt5-tools==5.15.9.3.3
PyQt5_sip==12.17.2
python-dotenv==1.2.1
qt5-applications==5.15.2.2.3
qt5-tools==5.15.2.1.3

## Setup to Code

Create your environment: 
    python3 -m venv venv

Activate you environment: 
    .\venv\Scripts\Activate.ps1

Install PyQt5 Packages: 
    pip install PyQt5 PyQt5-tools pillow opencv-python

Launch Drag and Drop: 
    .\venv\Lib\site-packages\qt5_applications\Qt\bin\designer.exe


### organization notes 
* I am setting the screen sizes to 1024x600 for the 7" display 
* all the the designer files will go into qt_designer_files 
* then all the python screens will go into ui_screens folder 
* all of the screens functions will go into ui_functions folder 
* each screen will have a corresponding functions file. This is so that designer can be changes without having to rewrite all of the functions over and over again. 
* we will be using a stacked widget where we have a main function that is controlling which screen is shown. This is the format I found that was the easiest to edit when working on Aquaquest. 

