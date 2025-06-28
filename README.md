# YouTube動画要約ツール

このPythonスクリプトは、YouTube動画から字幕、タイトル、説明を抽出し、Google Geminiモデルを使用して多言語の要約を生成します。

## 機能

- YouTube動画のリンクを入力すると、自動的に動画IDを抽出します。
- `youtube-transcript-api` を使用して、動画の英語字幕を取得します。
- YouTube Data API v3 を使用して、動画のタイトルと説明を取得します。
- 字幕、タイトル、説明を結合して1つのテキストを作成します。
- Google Gemini API を呼び出して以下を生成します。
    - 中学生にも理解できる簡潔な中国語の要約
    - 対応する日本語訳
    - 英語の原文要約
- 結果をターミナルに出力し、Markdownファイルとして保存します。

## インストール

1. **リポジトリのクローン (該当する場合):**
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **仮想環境の作成とアクティベート (推奨):**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **依存関係のインストール:**
   ```bash
   pip install -r requirements.txt
   ```

## APIキーの設定

以下の2つのAPIキーが必要です。

- **Google Gemini API Key:** Google Geminiモデルにアクセスするために使用します。
- **YouTube Data API v3 Key:** YouTube動画データにアクセスするために使用します。

1. **APIキーの取得:**
   - **Google Gemini API Key:** [Google AI Studio](https://aistudio.google.com/app/apikey) にアクセスして作成します。
   - **YouTube Data API v3 Key:** [Google Cloud Console](https://console.cloud.google.com/apis/credentials) にアクセスして作成し、YouTube Data API v3 を有効にします。

2. **`.env` ファイルの作成:**
   プロジェクトのルートディレクトリに `.env` という名前のファイルを作成し、以下の内容を追加します。
   ```
   GEMINI_API_KEY="あなたのGemini APIキー"
   YOUTUBE_API_KEY="あなたのYouTube Data API v3キー"
   ```
   `"あなたのGemini APIキー"` と `"あなたのYouTube Data API v3キー"` を実際のキーに置き換えてください。

   **重要:** `.env` ファイルは `.gitignore` に追加されており、APIキーが誤ってバージョン管理にコミットされるのを防ぎます。

## 使用方法

1. **スクリプトの実行:**
   ```bash
   python main.py
   ```

2. **YouTube動画リンクの入力:**
   スクリプトを実行すると、YouTube動画のリンクの入力を求められます。プロンプトが表示されたら、要約したい動画のURLを貼り付けてEnterキーを押してください。

3. **結果の確認:**
   スクリプトは生成された要約をターミナルに出力し、Markdownファイル（ファイル名は `[video_id]_summary.md` 形式）として保存します。

## ターミナル出力例

```
中文摘要：
[中国語の要約内容]

日本語訳：
[日本語の翻訳内容]

English Summary:
[英語の原文要約内容]
```

## Markdownファイル出力例

```markdown
# YouTube Video Summary

## Original Video Details
**Title:** 動画のタイトル
**Description:** 動画の説明
**YouTube URL:** 動画のリンク

## Generated Summaries
中文摘要：
[中国語の要約内容]

日本語訳：
[日本語の翻訳内容]

English Summary:
[英語の原文要約内容]
```