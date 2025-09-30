🌿 Plant Disease Classification Web App
A Flask-based web application for detecting plant diseases using a TensorFlow/Keras deep learning model. Users can upload images of plant leaves, and the app will predict the disease class with confidence scores.

📁 Project Structure
plant-disease-app/
│
├── app.py                      # Main Flask application
├── model.keras                 # Trained TensorFlow model
├── requirements.txt            # Python dependencies
│
├── templates/
│   └── index.html             # Frontend HTML template
│
├── static/
│   ├── images/                # Uploaded images storage
│   └── css/
│       └── style.css          # CSS styling
│
└── README.md                  # This file
🚀 Quick Start
Prerequisites
Python 3.8 or higher
pip package manager
Your trained model.keras file
Installation
Clone or download this repository
Navigate to the project directory
bash
   cd plant-disease-app
Install required dependencies
bash
   pip install -r requirements.txt
Place your trained model
Copy your model.keras file to the root directory of the project
The file should be named exactly model.keras
Configure the application Open app.py and update the following variables to match your model:
python
   # Update IMG_SIZE to match your model's input size
   IMG_SIZE = 224  # Change to 128, 256, etc.
   
   # Update CLASS_NAMES with your actual disease classes
   CLASS_NAMES = [
       'Apple___Apple_scab',
       'Apple___Black_rot',
       # ... add all your classes here in the correct order
   ]
Running the Application
Start the Flask server
bash
   python app.py
Access the application
Open your web browser
Navigate to: http://localhost:5000
Or from another device on the same network: http://YOUR_IP:5000
Using the app
Click "Choose Plant Leaf Image" to select an image
Preview the selected image
Click "Analyze Disease" to get predictions
View the predicted disease class and confidence score
📋 Features
✅ Image Upload - Support for JPG, PNG, GIF, BMP formats
✅ Real-time Preview - See your image before analysis
✅ Disease Detection - AI-powered classification
✅ Confidence Scores - Percentage confidence for predictions
✅ Top-3 Predictions - See alternative diagnoses
✅ Responsive Design - Works on desktop and mobile
✅ Image Storage - Uploaded images saved in static/images/

🔧 Configuration
Change Server Port
In app.py, modify the last line:

python
app.run(debug=True, host='0.0.0.0', port=8080)  # Changed to 8080
Adjust File Size Limit
In app.py, change:

python
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB instead of 16MB
Custom Image Preprocessing
If your model requires different preprocessing, modify the preprocess_image() function in app.py:

python
# Example: For models trained with ImageNet preprocessing
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
img_array = preprocess_input(img_array * 255.0)  # Scale back to [0, 255] first
📊 Model Requirements
Your model.keras file should:

Accept input shape: (batch_size, IMG_SIZE, IMG_SIZE, 3)
Output shape: (batch_size, num_classes)
Use softmax activation in the final layer
Be trained with images normalized to [0, 1] range (or modify preprocessing accordingly)
🐛 Troubleshooting
Model Not Found Error
Problem: Error loading model: [Errno 2] No such file or directory: 'model.keras'

Solution:

Ensure model.keras is in the root directory
Check the file name is exactly model.keras (case-sensitive)
Verify the file is not corrupted
Wrong Predictions
Problem: Model gives incorrect predictions

Solution:

Verify CLASS_NAMES list matches your training classes order
Check IMG_SIZE matches your model's input size
Ensure preprocessing matches your training preprocessing
Port Already in Use
Problem: Address already in use

Solution:

bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
Memory Issues
Problem: Out of memory errors

Solution:

Reduce image size before processing
Use a smaller model
Ensure only one prediction runs at a time
📸 Supported Image Formats
PNG (.png)
JPEG (.jpg, .jpeg)
GIF (.gif)
BMP (.bmp)
Maximum file size: 16MB (configurable)

🔒 Security Notes
For production deployment:

Disable debug mode
python
   app.run(debug=False, host='0.0.0.0', port=5000)
Add authentication if handling sensitive data
Implement rate limiting to prevent abuse
Use HTTPS for secure communication
Sanitize file uploads - Already implemented with secure_filename()
🌐 Deployment Options
Local Network Access
Already configured! Other devices on your network can access using:

http://<your-ip-address>:5000
Deploy to Cloud
Heroku:

Add Procfile:
   web: gunicorn app:app
Add gunicorn==21.2.0 to requirements.txt
Deploy using Heroku CLI
PythonAnywhere, Render, or Railway:

These platforms support Flask apps directly
Follow their respective deployment guides
Docker Deployment
Create Dockerfile:

dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
📝 API Endpoints
GET / - Home page with upload form
POST /predict - Upload image and get prediction
GET /clear - Clear results and return to home
🤝 Contributing
To extend this application:

Add disease information database - Display treatment recommendations
Implement user accounts - Track prediction history
Add batch processing - Analyze multiple images at once
Create REST API - Allow programmatic access
Add webcam support - Real-time image capture
📄 License
This project is open source and available for educational purposes.

🆘 Support
If you encounter issues:

Check the troubleshooting section above
Verify all dependencies are installed correctly
Ensure your model file is compatible with TensorFlow 2.15.0
Check that CLASS_NAMES list matches your model's output classes
📚 Additional Resources
Flask Documentation
TensorFlow Guide
Keras Models Documentation
✨ Example Usage
Training your model: Ensure your model is saved in .keras format
python
   model.save('model.keras')
Getting class names: If you're unsure of your class order
python
   # During training, save class names
   import json
   with open('classes.json', 'w') as f:
       json.dump(class_names, f)
Testing the API: Use curl or Postman
bash
   curl -X POST -F "file=@path/to/image.jpg" http://localhost:5000/predict
🎯 Performance Tips
Optimize model: Use TensorFlow Lite for faster inference
Cache predictions: Store results for duplicate images
Async processing: Use Celery for background processing
GPU acceleration: Configure TensorFlow to use GPU if available
📞 Contact
For questions or improvements, feel free to open an issue or submit a pull request.

Happy Plant Disease Detection! 🌱

