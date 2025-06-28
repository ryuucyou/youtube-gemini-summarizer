import os
import re
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import google.generativeai as genai
import textwrap

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def get_video_id(url):
    match = re.search(r"(?<=v=)[a-zA-Z0-9_-]+", url)
    if not match:
        match = re.search(r"(?<=youtu.be/)[a-zA-Z0-9_-]+", url)
    if not match:
        raise ValueError("無効なYouTube URLです")
    return match.group(0)

def get_youtube_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript = " ".join([item['text'] for item in transcript_list])
        return transcript
    except Exception as e:
        print(f"字幕の取得中にエラーが発生しました: {e}")
        return None

def get_youtube_video_details(video_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    if response['items']:
        snippet = response['items'][0]['snippet']
        title = snippet['title']
        description = snippet['description']
        return title, description
    return None, None

def generate_summary(text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""请根据以下YouTube视频的字幕、标题和描述，生成以下内容：
1. 一个中学生能理解的简洁中文摘要。
2. 对应的日语翻译。
3. 英文原文摘要。

请以以下格式输出，并确保每个摘要内容都分段，易于阅读：

中文摘要：
[中文摘要内容]

日本語訳：
[日语翻译内容]

English Summary:
[英文原文摘要内容]

视频内容：
{text}
"""
    response = model.generate_content(prompt)
    return response.text

def main():
    youtube_url = input("YouTube動画リンクを入力してください: ")
    video_id = get_video_id(youtube_url)

    transcript = get_youtube_transcript(video_id)
    if not transcript:
        print("動画の字幕を取得できませんでした。動画IDまたは字幕の利用可能性を確認してください。")
        return

    title, description = get_youtube_video_details(video_id)
    if not title:
        print("動画のタイトルと説明を取得できませんでした。動画IDまたはYouTube APIキーを確認してください。")
        return

    full_text = f"Title: {title}\nDescription: {description}\nTranscript: {transcript}"
    print("\n--- 要約を生成中 ---\n")
    summary_output = generate_summary(full_text)
    print(summary_output)

    # Save to Markdown file
    with open(f"{video_id}_summary.md", "w", encoding="utf-8") as f:
        f.write(f"# YouTube動画要約\n\n")
        f.write(f"## 元の動画の詳細\n")
        f.write(f"**タイトル:** {title}\n")
        f.write(f"**説明:** {description}\n")
        f.write(f"**YouTube URL:** {youtube_url}\n\n")
        f.write(f"## 生成された要約\n")
        # 确保每个部分都有足够的换行
        formatted_summary = summary_output.replace("中文摘要：", "\n中文摘要：\n").replace("日本語訳：", "\n日本語訳：\n").replace("English Summary:", "\nEnglish Summary：\n")
        f.write(formatted_summary)
    print(f"
要約は {video_id}_summary.md に保存されました")

if __name__ == "__main__":
    main()
