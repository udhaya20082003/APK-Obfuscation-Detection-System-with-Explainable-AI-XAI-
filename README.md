# APK Obfuscation Detection System with Explainable AI (XAI)

**DEMO**

https://github.com/user-attachments/assets/918c4ea3-5e67-438c-b54b-b9c15b5964a1

This project is a machine learning-based system for detecting obfuscation in Android APK files. It incorporates Explainable AI (SHAP analysis) to provide feature importance insights, helping users understand the reasoning behind the predictions.

---

## Features
- **Obfuscation Detection**: Classifies APK files as either "Obfuscated" or "Not Obfuscated."
- **Explainability**: Visualizes feature importance using SHAP (SHapley Additive exPlanations).
- **APK Feature Extraction**: Extracts features such as file size, DEX count, and permissions from APK files.
- **Streamlit Web Interface**: User-friendly interface to upload APK files and view analysis results.

---

## Technologies Used
- **Frontend**: [Streamlit](https://streamlit.io/) for the web interface.
- **Backend**: Python for feature extraction and model integration.
- **Machine Learning**: A deep neural network built with TensorFlow/Keras.
- **Explainability**: SHAP for feature importance analysis.
- **Data Preprocessing**: StandardScaler and MultiLabelBinarizer for normalization and encoding.
- **Dataset**: APK metadata and permission information.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/apk-obfuscation-detector.git
   cd apk-obfuscation-detector

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows:  venv\Scripts\activate

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Ensure the required files are in place:
  - model.keras: Trained neural network model.
  - multi_label_binarizer.pkl: Encoder for permissions.
  - scaler.pkl: Pre-trained StandardScaler.
  - background_data.csv: Data for SHAP analysis.
  - xai_explainer.pkl: Pre-computed SHAP explainer (optional).

## Usage
1. Launch the Streamlit app:
   ```bash
    streamlit run app.py
2. Upload an APK file via the web interface.

3. View the analysis results:

- Obfuscation Status: Displays "Obfuscated" or "Not Obfuscated" with confidence.
- Permissions and Features: Lists extracted features like file size, DEX count, and permissions.
- Explainability Insights: Feature importance visualized using SHAP.

## Dataset and Model Details
1. Data Preprocessing:

- Target encoding using MultiLabelBinarizer.
- Features normalized using StandardScaler.
2. Model:

- Deep neural network with 4 hidden layers.
- Regularization techniques: L2 and Dropout.
- Optimized using Adam optimizer and Binary Cross-Entropy loss.
3. Explainability:

- SHAP analysis for feature importance.

## License
This project is licensed under the MIT License.
Yet to be published please contact before cloning and using this project. 
Do not use this repository without permission.
