from flask import Flask, render_template, request, url_for
import os
import string 
import tensorflow as tf

app = Flask(__name__)


# Load the pre-trained model
model = tf.keras.models.load_model('static/my_model.keras') #Load model from static folder

# Define known phrases
multi_word_phrases = ["மதிய வணக்கம்", "காலை வணக்கம்", "இரவு வணக்கம்", "எப்படி சுகம்"]  # Add labels for model to predict

@app.route('/', methods=['GET', 'POST'])
def index():
    video_urls = []  # To retrieve corresponding sign video for the input audio
    missing_videos = []  # To store words for which videos are missing
    
    if request.method == 'POST':
        input_text = request.form['input_text']
        print("Received input text (Tamil):", input_text)  # print the input text
        
        # Remove punctuation from the input text
        translator = str.maketrans('', '', string.punctuation)
        cleaned_text = input_text.translate(translator)
        
        # Try to match most probable word first
        matched_phrases = []
        for phrase in multi_word_phrases:
            if phrase in cleaned_text:
                matched_phrases.append(phrase)
                cleaned_text = cleaned_text.replace(phrase, '')  # Remove the matched phrase from the text
        
        # Split the remaining text into words
        words = cleaned_text.strip().split()
        
        # Combine multi-words and individual words
        all_terms = matched_phrases + words
        
        for term in all_terms:
            if term:  # Ensure no empty strings are processed
                video_filename = f"{term}.mp4"  
                video_path = os.path.join('static', 'videos', video_filename) 
                print("Looking for video:", video_path)  # Show the video path being searched
                
                if os.path.exists(video_path):
                    video_url = url_for('static', filename=f'videos/{video_filename}')
                    video_urls.append(video_url)
                else:
                    # If the video is missing, print the missing word/phrase
                    missing_videos.append(term)  # Collect the term with missing video
                    print(f"Video for term '{term}' not found")  # Print missing video
                    video_urls.append(url_for('static', filename='videos/placeholder.mp4')) 

    return render_template('index.html', video_urls=video_urls, missing_videos=missing_videos)

if __name__ == '__main__':
    app.run(debug=True,  port=5001)
