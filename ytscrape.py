import pandas as pd
from pytube import YouTube
from pymongo import MongoClient

def get_video_details(url):
    try:
        yt = YouTube(url)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    try:
        video_details = {
            "Title": yt.title or "No title available",
            "Views": yt.views or "No views available",
            "Duration": yt.length or "No duration available",
            "Description": yt.description or "No description available",
            "Rating": yt.rating or "No ratings available",
            "Publish Date": yt.publish_date or "No publish date available",
            "Author": yt.author or "No author available",
            "Keywords": yt.keywords or "No keywords available",
            "Thumbnail URL": yt.thumbnail_url or "No thumbnail available",
            "Channel URL": yt.channel_url or "No channel URL available",
            "Captions Text": get_captions_text(yt)
        }
        return video_details
    except Exception as e:
        print(f"An error occurred while fetching video details: {e}")
        return None

def get_captions_text(yt):
    captions = yt.captions
    if captions:
        for lang_code in captions:
            if 'en' in lang_code:
                srt_captions = captions[lang_code].generate_srt_captions()
                return extract_text_from_srt(srt_captions)
        return "No English captions found for this video."
    else:
        return "No captions found for this video."

def extract_text_from_srt(srt_captions):
    lines = srt_captions.split('\n')
    text_lines = [line for line in lines if not line.isdigit() and '-->' not in line]
    return ' '.join(text_lines).replace('  ', ' ')

def save_to_mongodb(video_details):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['youtube_db']
    collection = db['videos']
    result = collection.insert_one(video_details)
    print(f"Inserted document id: {result.inserted_id}")

if __name__ == "__main__":
    #link = input("Enter the link of the YouTube video: ")
    link = "https://www.youtube.com/watch?v=ERCMXc8x7mc&pp=ygUSUHl0aG9uIHByb2dyYW1taW5n"
    video_details = get_video_details(link)
    
    if video_details:
        # Print the video details as a DataFrame
        df = pd.DataFrame([video_details])
        print("Video details:")
        print(df)
        
        # Save to CSV
        df.to_csv("video_details.csv", index=False)
        print("\nVideo details saved to 'video_details.csv'.")
        
        # Save to MongoDB
        save_to_mongodb(video_details)
        print("\nVideo details saved to MongoDB.")
