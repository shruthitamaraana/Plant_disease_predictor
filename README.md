# 🌿 Plant Disease Classification Web App

A Flask-based web application for detecting plant diseases using a TensorFlow/Keras deep learning model. Users can upload images of plant leaves, and the app will predict the disease class with confidence scores.

---

## 📁 Project Structure

plant-disease-app/
│
├── app.py # Main Flask application
├── model.keras # Trained TensorFlow model
├── requirements.txt # Python dependencies
│
├── templates/
│ └── index.html # Frontend HTML template
│
├── static/
│ ├── images/ # Uploaded images storage
│ └── css/
│ └── style.css # CSS styling
│
└── README.md # This file

yaml
Copy code

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher  
- pip package manager  
- Your trained `model.keras` file  

### Installation
1. Clone or download this repository.
2. Navigate to the project directory:
```bash
cd plant-disease-app
Install required dependencies:

bash
Copy code
pip install -r requirements.txt
Place your trained model:

Copy your model.keras file to the root directory of the project.

Ensure the file is named exactly model.keras.

Configure the application in app.py:

python
Copy code
# Update IMG_SIZE to match your model's input size
IMG_SIZE = 224  # Change to 128, 256, etc.

# Update CLASS_NAMES with your actual disease classes
CLASS_NAMES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    # ... add all your classes here in the correct order
]
Running the Application
Start the Flask server:

bash
Copy code
python app.py
Access the application:

Open your web browser: http://localhost:5000

Or from another device on the same network: http://YOUR_IP:5000

Using the App
Click "Choose Plant Leaf Image" to select an image.

Preview the selected image.

Click "Analyze Disease" to get predictions.

View the predicted disease class and confidence score.

📋 Features
✅ Image Upload: JPG, PNG, GIF, BMP

✅ Real-time Preview

✅ AI-powered Disease Detection

✅ Confidence Scores

✅ Top-3 Predictions

✅ Responsive Design

✅ Image Storage in static/images/

🔧 Configuration
Change Server Port

python
Copy code
app.run(debug=True, host='0.0.0.0', port=8080)  # Example: 8080
Adjust File Size Limit

python
Copy code
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
Custom Image Preprocessing

python
Copy code
# Example: For models trained with ImageNet preprocessing
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
img_array = preprocess_input(img_array * 255.0)
📊 Model Requirements
Accept input shape: (batch_size, IMG_SIZE, IMG_SIZE, 3)

Output shape: (batch_size, num_classes)

Softmax activation in the final layer

Images normalized to [0, 1] (or modify preprocessing accordingly)

🐛 Troubleshooting
Model Not Found Error

javascript
Copy code
Error loading model: [Errno 2] No such file or directory: 'model.keras'
Ensure model.keras is in the root directory

File name is exactly model.keras (case-sensitive)

Verify the file is not corrupted

Wrong Predictions

Verify CLASS_NAMES matches training class order

Check IMG_SIZE matches model input size

Ensure preprocessing matches training

Port Already in Use

bash
Copy code
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
Memory Issues

Reduce image size

Use a smaller model

Ensure only one prediction runs at a time

📸 Supported Image Formats
PNG (.png)

JPEG (.jpg, .jpeg)

GIF (.gif)

BMP (.bmp)

Max file size: 16MB (configurable)

🔒 Security Notes
Disable debug mode in production

Add authentication for sensitive data

Implement rate limiting

Use HTTPS for secure communication

Sanitize file uploads (already implemented with secure_filename())

🌐 Deployment Options
Local Network Access

text
Copy code
http://<your-ip-address>:5000
Deploy to Cloud

Heroku

Add Procfile:

makefile
Copy code
web: gunicorn app:app
Add gunicorn==21.2.0 to requirements.txt

Deploy using Heroku CLI

Other Platforms: PythonAnywhere, Render, Railway – follow their guides

Docker Deployment

dockerfile
Copy code
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
📝 API Endpoints
GET / – Home page with upload form

POST /predict – Upload image and get prediction

GET /clear – Clear results and return to home

🤝 Contributing
Add disease information database

Implement user accounts

Batch processing

Create REST API

Webcam support

📄 License
Open source – educational purposes

🆘 Support
Check troubleshooting section

Verify dependencies installed correctly

Ensure model is compatible with TensorFlow 2.15.0

Check CLASS_NAMES order

📚 Additional Resources
Flask Documentation

TensorFlow Guide

Keras Models Documentation

✨ Example Usage
Training your model:

python
Copy code
model.save('model.keras')
Getting class names:

python
Copy code
import json
with open('classes.json', 'w') as f:
    json.dump(class_names, f)
Testing API using curl:

bash
Copy code
curl -X POST -F "file=@path/to/image.jpg" http://localhost:5000/predict
🎯 Performance Tips
Optimize model: TensorFlow Lite

Cache predictions

Async processing: Celery

GPU acceleration if available

📞 Contact
For questions or improvements, feel free to open an issue or submit a pull request.

Happy Plant Disease Detection! 🌱
