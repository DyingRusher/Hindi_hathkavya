# Hindi Hand Sign Language Detection

Approximately 6.3% of India's population experiences hearing or speaking impairments, underscoring the need for effective communication tools. Our project, "Hindi Hand Sign Language Detection," aims to bridge this gap by developing a real-time system that accurately recognizes Hindi hand signs.

## Project Overview

We collected a dataset of 12,000 images for training and used Mediapipe to extract coordinates for all 21 landmarks on the hand. A Random Forest model was trained on this dataset, achieving an impressive testing accuracy of 98.6%. This system is designed to detect and interpret Hindi hand signs, facilitating seamless communication for individuals with hearing or speech impairments.

## Features

* Real-Time Detection: Processes live video input to identify hand signs instantaneously.

* High Accuracy: Employs robust algorithms to ensure precise recognition of hand gestures.

* User-Friendly Interface: Designed for intuitive use, making it accessible to a broad audience.

## Installation

1. Clone the repo:   
   `git clone https://github.com/DyingRusher/Hindi_hathkavya.git`  
2. Navigate to the Project Directory:  
   `cd Hindi_hathkavya`  
3. Install Dependencies:  
   `pip install -r requirements.txt`
   
## Usage  

1. Run the Application:
   `python main.py`
2. Interact with the System:  
   For adding vanjan(consanant) hold that sign for 3 sec, and for adding matra(vowal) hold sign for 5 sec.For adding space do not detect any hand for 3 sec.  
   (Demo is attached below)

## Contributing  

We welcome contributions to enhance this project. Please fork the repository and submit a pull request with your proposed changes.  

## Acknowledgments    

This project is a collaborative effort by Arjav Ankoliya, Vatsal Jajadiya, and Goldi Ladani.

## demo


https://github.com/user-attachments/assets/5abb7b66-69c8-4cd8-a1b6-a62b0fefeea8


   


