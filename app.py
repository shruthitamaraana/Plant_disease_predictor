import os
import uuid
import numpy as np
from PIL import Image
from flask import Flask, request, render_template, redirect, url_for, flash
import tensorflow as tf
from werkzeug.utils import secure_filename

# --- Configuration ---
# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flashing messages

# Define the path for uploaded images and set a file size limit (e.g., 16MB)
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# --- Model Loading ---
MODEL_PATH = 'model.keras'
model = None

# First, check if the model file exists at the specified path.
if not os.path.exists(MODEL_PATH):
    print("----------------------------------------------------------------")
    print(f"FATAL ERROR: Model file not found at path: '{MODEL_PATH}'")
    print("Please make sure the 'model.keras' file is in the same directory as 'app.py'.")
    print("The application cannot start without the model file.")
    print("----------------------------------------------------------------")
else:
    # If the file exists, try to load it.
    try:
        # We pass a 'custom_objects' dictionary to tell Keras how to handle custom components.
        custom_objects = {
            "swish": tf.keras.activations.swish,
            "FixedDropout": tf.keras.layers.Dropout
        }
        model = tf.keras.models.load_model(MODEL_PATH, custom_objects=custom_objects)
        print("Model loaded successfully.")
    except Exception as e:
        # Handle other errors during model loading (e.g., corruption, version mismatch).
        print(f"Error loading model: {e}")
        print("The model file was found, but an error occurred while loading it.")
        print("The file may be corrupted or incompatible with the installed TensorFlow/Keras version.")
        model = None # Set model to None to handle this case in the predict route

# --- Define Class Names ---
CLASS_NAMES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy',
    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
    'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot',
    'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

# --- Comprehensive Disease Information Database ---
DISEASE_INFO = {
    'Apple___Apple_scab': {
        'description': 'A common fungal disease causing olive-green to brown spots on leaves, fruit, and twigs.',
        'treatment': 'Prune to improve air circulation, remove fallen leaves, and apply fungicides preventatively.',
        'link': 'https://www.google.com/search?q=Apple+scab+disease'
    },
    'Apple___Black_rot': {
        'description': 'A fungal disease leading to fruit rot, leaf spots, and cankers on branches.',
        'treatment': 'Prune out infected wood, remove mummified fruit, and apply appropriate fungicides.',
        'link': 'https://www.google.com/search?q=Apple+black+rot'
    },
    'Apple___Cedar_apple_rust': {
        'description': 'A fungal disease causing bright yellow-orange spots on leaves and fruit. Requires a nearby cedar or juniper host.',
        'treatment': 'Remove nearby cedar hosts if possible. Apply fungicides during the early spring.',
        'link': 'https://www.google.com/search?q=Cedar+apple+rust'
    },
    'Cherry_(including_sour)___Powdery_mildew': {
        'description': 'A fungal disease appearing as white powdery spots on leaves and shoots, which can distort growth.',
        'treatment': 'Ensure good air circulation. Apply fungicides or horticultural oils at the first sign of disease.',
        'link': 'https://www.google.com/search?q=Cherry+powdery+mildew'
    },
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': {
        'description': 'A fungal disease that causes long, narrow, tan-colored lesions on corn leaves, reducing photosynthetic area.',
        'treatment': 'Use resistant hybrids, practice crop rotation, and apply fungicides when necessary.',
        'link': 'https://www.google.com/search?q=Corn+gray+leaf+spot'
    },
    'Corn_(maize)___Common_rust_': {
        'description': 'A fungal disease characterized by cinnamon-brown, powdery pustules on both upper and lower leaf surfaces.',
        'treatment': 'Often minor, but resistant hybrids are available. Fungicides may be needed in severe cases.',
        'link': 'https://www.google.com/search?q=Corn+common+rust'
    },
    'Corn_(maize)___Northern_Leaf_Blight': {
        'description': 'A fungal disease creating long, elliptical, grayish-green or tan lesions on corn leaves.',
        'treatment': 'Plant resistant hybrids, manage crop residue, and apply fungicides if the disease is severe.',
        'link': 'https://www.google.com/search?q=Corn+northern+leaf+blight'
    },
    'Grape___Black_rot': {
        'description': 'A serious fungal disease of grapes, causing dark, circular lesions on leaves and turning berries into hard, black mummies.',
        'treatment': 'Sanitation is key: remove infected canes and mummified fruit. Apply fungicides throughout the growing season.',
        'link': 'https://www.google.com/search?q=Grape+black+rot'
    },
    'Grape___Esca_(Black_Measles)': {
        'description': 'A destructive fungal disease complex causing "measles-like" spots on leaves and berries, leading to vine dieback.',
        'treatment': 'Management is difficult. Prune out infected wood during the dormant season. No highly effective chemical controls exist.',
        'link': 'https://www.google.com/search?q=Grape+Esca+(Black+Measles)'
    },
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': {
        'description': 'A fungal disease causing irregular dark reddish-brown spots on grape leaves, which can lead to defoliation.',
        'treatment': 'Good air circulation and sanitation help. Fungicide sprays for other diseases often control this as well.',
        'link': 'https://www.google.com/search?q=Grape+Isariopsis+leaf+spot'
    },
    'Orange___Haunglongbing_(Citrus_greening)': {
        'description': 'A devastating bacterial disease spread by an insect. It causes blotchy yellow leaves, stunted growth, and bitter, misshapen fruit.',
        'treatment': 'There is no cure. Management focuses on removing infected trees and controlling the insect vector (psyllid).',
        'link': 'https://www.google.com/search?q=Citrus+greening+disease+(Haunglongbing)'
    },
    'Peach___Bacterial_spot': {
        'description': 'A bacterial disease causing angular, water-soaked spots on leaves and pitted spots on fruit.',
        'treatment': 'Use resistant varieties. Copper sprays can help reduce spread but may not be fully effective.',
        'link': 'https://www.google.com/search?q=Peach+bacterial+spot'
    },
    'Pepper,_bell___Bacterial_spot': {
        'description': 'A bacterial disease causing small, water-soaked spots on leaves that turn brown or black. Can also affect fruit.',
        'treatment': 'Plant disease-free seeds/transplants. Use copper-based bactericides preventatively.',
        'link': 'https://www.google.com/search?q=Pepper+bacterial+spot'
    },
    'Potato___Early_blight': {
        'description': 'A fungal disease creating dark, "target-like" spots on lower, older leaves of potato plants.',
        'treatment': 'Practice crop rotation, maintain good plant nutrition, and apply fungicides as needed.',
        'link': 'https://www.google.com/search?q=Potato+early+blight'
    },
    'Potato___Late_blight': {
        'description': 'A destructive water mold disease causing large, dark, water-soaked lesions on leaves and stems, and can rot tubers.',
        'treatment': 'Requires preventative fungicide applications, especially during cool, moist weather.',
        'link': 'https://www.google.com/search?q=Potato+late+blight'
    },
    'Squash___Powdery_mildew': {
        'description': 'A common fungal disease that appears as white, powdery spots on the upper surfaces of squash leaves.',
        'treatment': 'Ensure good air circulation. Apply fungicides, horticultural oil, or neem oil.',
        'link': 'https://www.google.com/search?q=Squash+powdery+mildew'
    },
    'Strawberry___Leaf_scorch': {
        'description': 'A fungal disease causing irregular, purplish blotches on leaves that dry up and make the leaf look "scorched".',
        'treatment': 'Remove infected leaves after harvest. Use resistant varieties and maintain good air circulation.',
        'link': 'https://www.google.com/search?q=Strawberry+leaf+scorch'
    },
    'Tomato___Bacterial_spot': {
        'description': 'A bacterial disease causing small, water-soaked, angular spots on leaves and scabby spots on fruit.',
        'treatment': 'Use disease-free seed, practice crop rotation, and apply copper-based sprays preventatively.',
        'link': 'https://www.google.com/search?q=Tomato+bacterial+spot'
    },
    'Tomato___Early_blight': {
        'description': 'A fungal disease resulting in "target-like" spots on lower leaves, often leading to a "collar rot" lesion on the stem.',
        'treatment': 'Mulch around plants, prune lower leaves, and apply fungicides.',
        'link': 'https://www.google.com/search?q=Tomato+early+blight'
    },
    'Tomato___Late_blight': {
        'description': 'A destructive water mold disease causing large, greasy-looking, grey-green spots on leaves that spread rapidly.',
        'treatment': 'Requires immediate action with targeted fungicides. Destroy infected plants to prevent spread.',
        'link': 'https://www.google.com/search?q=Tomato+late+blight'
    },
    'Tomato___Leaf_Mold': {
        'description': 'A fungal disease causing pale green or yellowish spots on the upper leaf surface and olive-green to brownish mold on the underside.',
        'treatment': 'Improve air circulation, reduce humidity. Fungicides can be effective. Common in greenhouses.',
        'link': 'https://www.google.com/search?q=Tomato+leaf+mold'
    },
    'Tomato___Septoria_leaf_spot': {
        'description': 'A fungal disease causing numerous small, circular spots with dark borders and tan centers on older, lower leaves.',
        'treatment': 'Remove infected lower leaves, mulch plants, and apply fungicides.',
        'link': 'https://www.google.com/search?q=Tomato+Septoria+leaf+spot'
    },
    'Tomato___Spider_mites Two-spotted_spider_mite': {
        'description': 'Caused by tiny arachnids, not a disease. Leads to yellow stippling on leaves, fine webbing, and overall plant decline.',
        'treatment': 'Use miticides, insecticidal soaps, or horticultural oils. Strong sprays of water can dislodge them.',
        'link': 'https://www.google.com/search?q=Two-spotted+spider+mite+on+tomato'
    },
    'Tomato___Target_Spot': {
        'description': 'A fungal disease causing small, water-soaked spots that develop into larger "target-like" lesions on leaves, stems, and fruit.',
        'treatment': 'Improve air circulation, avoid overhead watering, and apply fungicides.',
        'link': 'https://www.google.com/search?q=Tomato+target+spot'
    },
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': {
        'description': 'A viral disease transmitted by whiteflies. Causes severe stunting, upward curling of leaves, and yellowing of leaf margins.',
        'treatment': 'No cure. Control whitefly populations, remove infected plants, and use resistant varieties.',
        'link': 'https://www.google.com/search?q=Tomato+yellow+leaf+curl+virus'
    },
    'Tomato___Tomato_mosaic_virus': {
        'description': 'A viral disease causing a light and dark green mosaic pattern on leaves, along with stunting and malformation.',
        'treatment': 'No cure. Remove and destroy infected plants. Practice good sanitation to prevent mechanical spread.',
        'link': 'https://www.google.com/search?q=Tomato+mosaic+virus'
    },
    'default': {
        'description': 'Information for this disease is not yet available in our database.',
        'treatment': 'Consult a local agricultural extension for advice.',
        'link': 'https://www.google.com/search'
    }
}

# --- (New) Information for Healthy Plants ---
HEALTHY_INFO = {
    'title': 'Plant appears to be Healthy',
    'description': 'No disease was detected. Continue to monitor your plant for any signs of stress or disease. Regular care, proper watering, and good nutrition are key to keeping it healthy.'
}


# --- Utility Functions ---
def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    """
    Preprocesses the image for model prediction.
    """
    try:
        img = Image.open(image_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img = img.resize((224, 224))
        img_array = np.array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

# --- Flask Routes ---
@app.route('/', methods=['GET'])
def index():
    """Renders the home page."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handles the image upload and prediction process.
    """
    if model is None:
        flash("Model is not loaded. Please check the server logs.", "error")
        return redirect(url_for('index'))

    if 'file' not in request.files:
        flash('No file part in the request.', 'error')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No file selected. Please choose an image to upload.', 'error')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        try:
            # Secure and unique filename handling
            original_filename = secure_filename(file.filename)
            unique_filename = str(uuid.uuid4()) + "_" + original_filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)

            # Preprocess the image for prediction
            processed_image = preprocess_image(filepath)
            if processed_image is None:
                flash("Could not process the image. Please try another one.", "error")
                return redirect(url_for('index'))

            # Make a prediction
            prediction = model.predict(processed_image)

            # Process prediction results
            predicted_class_index = np.argmax(prediction)
            original_class_name = CLASS_NAMES[predicted_class_index]
            predicted_class_name = original_class_name.replace('___', ' - ').replace('_', ' ')
            confidence = float(np.max(prediction))

            # Get additional info for the predicted disease
            is_healthy = 'healthy' in original_class_name.lower()
            disease_info = None if is_healthy else DISEASE_INFO.get(original_class_name, DISEASE_INFO['default'])


            # Get the top 3 predictions
            top_3_indices = np.argsort(prediction[0])[-3:][::-1]
            top_3_predictions = [
                {
                    "class": CLASS_NAMES[i].replace('___', ' - ').replace('_', ' '),
                    "confidence": f"{prediction[0][i]*100:.2f}%"
                }
                for i in top_3_indices
            ]

            # Render the template with prediction results and additional info
            return render_template('index.html',
                                   prediction=predicted_class_name,
                                   confidence=f"{confidence*100:.2f}%",
                                   top_3=top_3_predictions,
                                   image_path=filepath,
                                   disease_info=disease_info,
                                   healthy_info=HEALTHY_INFO if is_healthy else None)

        except Exception as e:
            # Handle file too large error specifically
            if isinstance(e, request.exceptions.RequestEntityTooLarge):
                flash("The uploaded file is too large. Please upload an image smaller than 16MB.", "error")
            else:
                flash(f"An error occurred during prediction: {e}", "error")
            return redirect(url_for('index'))

    else:
        flash('Invalid file type. Please upload a PNG, JPG, or JPEG file.', 'error')
        return redirect(request.url)

@app.route('/clear', methods=['GET'])
def clear():
    """Redirects to the home page, effectively clearing the form and results."""
    return redirect(url_for('index'))

# --- Main Application Runner ---
if __name__ == '__main__':
    # Set host to '0.0.0.0' to make it accessible on your local network
    app.run(host='0.0.0.0', port=5000, debug=True)

