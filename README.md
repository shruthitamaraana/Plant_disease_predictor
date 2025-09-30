# 🌿 Plant Disease Classification Web App

A Flask-based web application that detects plant diseases from leaf images using a TensorFlow/Keras model. Users can upload images, and the app predicts the disease class with confidence scores.

---

## 📁 Project Structure

plant-disease-app/
│
├── app.py # Main Flask backend
├── model.keras # Trained TensorFlow model
├── requirements.txt # Python dependencies
├── templates/
│ └── index.html # HTML template
├── static/
│ ├── images/ # Uploaded images storage
│ └── css/
│ └── style.css # Styling
└── README.md # This file

yaml
Copy code

---

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Plant_disease_predictor.git
cd Plant_disease_predictor
Install dependencies

bash
Copy code
pip install -r requirements.txt
Place your trained model

Copy model.keras to the root directory.

Run the app

bash
Copy code
python app.py
Open browser: http://localhost:5000

📋 Features
Image Upload: JPG, PNG, GIF, BMP

Real-time Preview

AI-powered Disease Detection

Confidence Scores & Top-3 Predictions

Responsive Design

Uploaded Images Stored in static/images/

🔧 Configuration
Change server port: Update app.run() in app.py

Max upload size: app.config['MAX_CONTENT_LENGTH']

🐛 Troubleshooting
Model not loaded: Ensure model.keras is in root and not corrupted

Incorrect predictions: Check CLASS_NAMES order & IMG_SIZE

Port in use: Kill process using the port

Memory issues: Reduce image size or use a smaller model

🌐 Deployment
Local Network: Access via http://<your-ip>:5000

Cloud: Heroku, Render, PythonAnywhere, Railway

Docker: Optional containerization

📄 License
Open-source for educational purposes

📞 Contact
For questions or improvements, open an issue or submit a pull request.

Happy Plant Disease Detection! 🌱
