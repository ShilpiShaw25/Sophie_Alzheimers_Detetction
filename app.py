import streamlit as st
from Utils import audio_to_spectrogram, get_prediction, image_to_convert
from Utils import IMAGE_NAME
import os
import csv
import datetime

# Directory to save audio files
AUDIO_DIR = "uploaded_audios"
AUDIO_FILE_NAME = os.path.join(AUDIO_DIR, "uploaded_audio.wav")
PREDICTION_LOG_FILE = "prediction_log.csv"

# Create the directory if it doesn't exist
os.makedirs(AUDIO_DIR, exist_ok=True)

# Set the title
st.title("Alzheimer's Detection")

# Function to log predictions to CSV
def create_prediction_log(audio_filename, prediction):
    # Check if the CSV exists; if not, create it and write headers
    file_exists = os.path.isfile(PREDICTION_LOG_FILE)
    
    with open(PREDICTION_LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Audio File", "Prediction"])
        
        # Write the prediction log
        writer.writerow([datetime.datetime.now(), audio_filename, prediction])

# Function to read the CSV file to download
def read_csv_for_download(file_path):
    with open(file_path, "r") as f:
        csv_content = f.read()
    return csv_content

# Upload the audio file
audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"], help="Upload the audio file of the patient.")

if audio_file:
    # Save the uploaded audio file
    saved_audio_path = os.path.join(AUDIO_DIR, audio_file.name)
    with open(saved_audio_path, "wb") as f:
        f.write(audio_file.getbuffer())
        st.toast("Audio Reading Successful", icon="✅")

    # Generate the spectrogram
    spec_results = audio_to_spectrogram(saved_audio_path)
    if not spec_results:
        st.error("Spectrogram Saving Failed", icon="❌")
    else:
        st.toast("Spectrogram Saving Successful", icon="✅")

        # Display the audio and spectrogram
        with st.sidebar:
            st.title("Alzheimer's Detection")
            # Display the uploaded audio
            st.header("Uploaded Audio")
            st.audio(saved_audio_path)

            # Display the generated spectrogram
            st.header("Generated Spectrogram")
            st.image(IMAGE_NAME)

        # Convert spectrogram to bytes
        image_conversion = image_to_convert(IMAGE_NAME)

        # Get prediction
        pred_label = get_prediction(image_conversion)
        st.subheader("Condition: {}".format(pred_label))

        # Log the prediction with the audio file name and current timestamp
        create_prediction_log(audio_file.name, pred_label)
        st.success(f"Prediction saved: {audio_file.name} -> {pred_label}")


        # Provide a download button for the CSV file
        csv_data = read_csv_for_download(PREDICTION_LOG_FILE)
        st.download_button(
            label="Download Prediction Logs",
            data=csv_data,
            file_name=PREDICTION_LOG_FILE,
            mime=None,
        )
