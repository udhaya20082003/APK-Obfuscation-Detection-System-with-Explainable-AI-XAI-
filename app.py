import streamlit as st
import pickle
import joblib
import pandas as pd
from androguard.core.bytecodes.apk import APK
import shap
import matplotlib.pyplot as plt
import os
from tensorflow.keras.models import load_model

# Function to load the model, MultiLabelBinarizer, and background data
@st.cache_resource
def load_model_and_mlb_and_background():
    """
    Load the trained Keras model, MultiLabelBinarizer, and background data.
    """
    try:
        # Load MultiLabelBinarizer
        with open('multi_label_binarizer.pkl', 'rb') as file:
            mlb = pickle.load(file)
        
        # Load the Keras model
        model = load_model('model.keras')
        
        # Load background data
        background_data = pd.read_csv('background_data.csv')
        return model, mlb, background_data
    except Exception as e:
        st.error(f"Error loading model or background data: {e}")
        return None, None, None

# Function to extract features from APK
def extract_features(apk_path):
    """
    Extract features from the APK file.
    """
    try:
        apk = APK(apk_path)
        dex_files = list(apk.get_dex_names())
        return {
            'size': os.path.getsize(apk_path),  # File size in bytes
            'dex_count': len(dex_files),  # Number of DEX files
            'permissions': list(apk.get_permissions())  # Permissions extracted
        }
    except Exception as e:
        raise Exception(f"Error extracting features: {e}")

# Main Streamlit app
def main():
    st.title("APK Obfuscation Detector with XAI")
    st.write("Upload an APK file to analyze obfuscation status and get explainability insights.")

    # File uploader
    uploaded_file = st.file_uploader("Choose an APK file", type="apk")

    if uploaded_file is not None:
        try:
            # Save the uploaded file temporarily
            temp_apk_path = "temp_uploaded_apk.apk"
            with open(temp_apk_path, "wb") as f:
                f.write(uploaded_file.read())

            # Load the model, MultiLabelBinarizer, and background data
            model, mlb, background_data = load_model_and_mlb_and_background()
            if not model or not mlb or background_data is None:
                st.error("Failed to load the model, MultiLabelBinarizer, or background data.")
                return

            # Extract features from the uploaded APK
            features = extract_features(temp_apk_path)

            permissions_encoded = mlb.transform([features['permissions']])
            permissions_df = pd.DataFrame(permissions_encoded, columns=mlb.classes_)

            # Prepare input data
            input_data = pd.DataFrame({
                'size': [features['size']],
                'dex_count': [features['dex_count']]
            })
            final_input = pd.concat([input_data, permissions_df], axis=1)

            # Predict obfuscation status
            prediction = model.predict(final_input)[0][0]
            result = "Obfuscated ⚠️" if prediction > 0.5 else "Not Obfuscated ✓"
            confidence = prediction * 100 if prediction > 0.5 else (1 - prediction) * 100

            # Display the results
            st.subheader("Analysis Results")
            st.markdown(f"**Status:** {result}")
            st.markdown(f"**Confidence:** {confidence:.2f}%")
            st.markdown(f"**File Size:** {features['size'] / 1024:.2f} KB")
            st.markdown(f"**DEX Count:** {features['dex_count']}")
            st.markdown(f"**Permissions Count:** {len(features['permissions'])}")

            # Display the list of permissions
            if len(features['permissions']) > 0:
                st.markdown("### Detected Permissions")
                for perm in sorted(features['permissions']):
                    st.write(f"- {perm}")

            # XAI Section
            st.markdown("### Explainability (SHAP Analysis)")
            explainer = shap.KernelExplainer(model.predict, background_data)

            # Calculate SHAP values for the current input
            shap_values = explainer.shap_values(final_input)

            # Feature importance plot
            st.write("**Feature Importance:**")
            fig, ax = plt.subplots(figsize=(10, 6))
            shap.summary_plot(shap_values, final_input, plot_type="bar", show=False)
            st.pyplot(fig) 
            # shap.summary_plot(shap_values, final_input, plot_type="bar", show=False)
            # st.pyplot()

            # Cleanup temporary file
            os.remove(temp_apk_path)

        except Exception as e:
            st.error(f"Error during analysis: {e}")

# Run the app
if __name__ == "__main__":
    main()
