# Voice Translation App

A web application that allows users to translate voice messages between different languages using OpenAI's Whisper and GPT models.

## Features

- Record audio directly in the browser
- Upload existing audio files
- Translate between multiple languages
- Get both text and audio translations
- Download translated audio files

## Supported Languages

- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)

## Deployment

This app is deployed using GitHub Pages. To deploy your own version:

1. Fork this repository
2. Go to your repository settings
3. Navigate to "Pages" under "Code and automation"
4. Select "main" branch as the source
5. Click "Save"

Your app will be available at `https://<your-username>.github.io/<repository-name>/`

## Local Development

To run the app locally:

1. Clone the repository
2. Open `index.html` in your web browser
3. Or use a local server:
   ```bash
   python3 -m http.server 8000
   ```
4. Open `http://localhost:8000` in your browser

## API Key Setup

To use the app, you need to set up your OpenAI API key:

1. Get an API key from [OpenAI](https://platform.openai.com/api-keys)
2. Open `js/app.js`
3. Replace `'YOUR_OPENAI_API_KEY'` with your actual API key

## Technologies Used

- HTML5
- CSS3
- JavaScript
- OpenAI API (Whisper, GPT-3.5, Text-to-Speech)
- Bootstrap 5

## License

MIT License