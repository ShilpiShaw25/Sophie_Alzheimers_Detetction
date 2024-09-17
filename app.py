import streamlit as st
import csv
import os
import datetime
import pandas as pd

PREDICTION_LOG_FILE = "prediction_log.csv"

# Function to log predictions to CSV
def log_prediction(audio_filename, prediction):
    file_exists = os.path.isfile(PREDICTION_LOG_FILE)

    with open(PREDICTION_LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Audio File", "Prediction"])

        writer.writerow([datetime.datetime.now(), audio_filename, prediction])

# Function to download CSV file
def download_csv():
    if os.path.exists(PREDICTION_LOG_FILE):
        # Read CSV file into a pandas DataFrame
        df = pd.read_csv(PREDICTION_LOG_FILE)
        # Convert DataFrame to CSV
        csv_data = df.to_csv(index=False)
        # Provide a download link for the CSV
        st.download_button(label="Download Prediction Log", 
                           data=csv_data,
                           file_name=PREDICTION_LOG_FILE,
                           mime='text/csv')
    else:
        st.warning("No prediction log available to download yet.")

# App logic
st.title("Alzheimer's Detection")

AUDIO_DIR = "uploaded_audios"
os.makedirs(AUDIO_DIR, exist_ok=True)

audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"], help="Upload the audio file of the patient.")

if audio_file:
    saved_audio_path = os.path.join(AUDIO_DIR, audio_file.name)
    with open(saved_audio_path, "wb") as f:
        f.write(audio_file.getbuffer())
        st.toast("Audio Reading Successful", icon="✅")

    # Generate and save the spectrogram
    spec_results = audio_to_spectrogram(saved_audio_path)
    if not spec_results:
        st.error("Spectrogram Saving Failed", icon="❌")
    else:
        st.toast("Spectrogram Saving Successful", icon="✅")

        # Display the audio and spectrogram
        st.sidebar.header("Uploaded Audio")
        st.audio(saved_audio_path)

        st.sidebar.header("Generated Spectrogram")
        st.image(IMAGE_NAME)

        # Convert to bytes for prediction
        image_conversion = image_to_convert(IMAGE_NAME)
        pred_label = get_prediction(image_conversion)
        st.subheader(f"Condition: {pred_label}")

        # Log the prediction
        log_prediction(audio_file.name, pred_label)
        st.success(f"Prediction saved: {audio_file.name} -> {pred_label}")

# Add download button for CSV file
download_csv()
