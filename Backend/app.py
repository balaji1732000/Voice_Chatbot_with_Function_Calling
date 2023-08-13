import os
import speech_recognition as sr
from dotenv import load_dotenv
import requests
from gtts import gTTS
import io

# from flask import Flask, render_template, request, send_file
from flask import Flask, render_template, request, send_file, Response


load_dotenv()

app = Flask(__name__)

azure_api_key = os.getenv("AZURE_OPENAPI_KEY")
is_whisper = False





@app.route("/")
def index():
    return render_template("index.html")  # Create an HTML template for your UI


@app.route("/audio_response", methods=["GET"])
def audio_response():
    # Get the audio response content (modify as needed)
    with open("path_to_your_audio_file.mp3", "rb") as audio_file:
        audio_response_content = audio_file.read()

    # Set the Content-Length header to the total length of the audio content
    response_headers = {
        "Content-Length": len(audio_response_content),
        "Content-Type": "audio/mpeg",
    }

    # Return the audio response with the correct headers
    return Response(audio_response_content, headers=response_headers)


# @app.route("/audio_response", methods=["POST"])
# def audio_response():
#     # Get the audio response content (modify as needed)
#     azure_response = "This is an example audio response."  # Replace with your actual audio response text

#     # Generate the gTTS instance and get audio content bytes
#     response_tts = gTTS(text=azure_response, lang="en")
#     response_audio_content = response_tts.getvalue()

#     # Set the Content-Length header to the total length of the audio content
#     response_headers = {
#         "Content-Length": len(response_audio_content),
#         "Content-Type": "audio/mpeg"
#     }

#     # Return the audio response with the correct headers
#     return Response(response_audio_content, headers=response_headers)


@app.route("/process", methods=["POST"])
def process():
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=0)
    r.dynamic_energy_threshold = False
    r.energy_threshold = 400

    with mic as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source, duration=1.0)
        audio = r.listen(source)
        print(audio)

    try:
        if is_whisper:
            user_input = whisper(audio)
        else:
            user_input = r.recognize_google(audio)
            print(user_input)
    except:
        return render_template(
            "index.html", response="Sorry, couldn't understand the audio."
        )

    azure_response = process_with_azure(user_input, azure_api_key)
    print(azure_response)

    # Convert the response to audio
    response_tts = gTTS(text=azure_response, lang="en")
    response_audio = io.BytesIO()
    response_tts.write_to_fp(response_audio)

    # Create a temporary file to save the audio content
    temp_audio_filename = "temp_response_audio.mp3"
    with open(temp_audio_filename, "wb") as temp_audio_file:
        temp_audio_file.write(response_audio.getvalue())

    # Get the content of the temporary audio file and send it to the client
    with open(temp_audio_filename, "rb") as temp_audio_file:
        response_audio_content = temp_audio_file.read()

    os.remove(temp_audio_filename)  # Remove the temporary file

    return Response(response_audio_content, mimetype="audio/mpeg")


if __name__ == "__main__":
    app.run(debug=True)
