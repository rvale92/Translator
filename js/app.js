// API Configuration
const config = {
    API_KEY: '', // This will be set by the user
    API_URL: 'https://api.openai.com/v1/audio/translations'
};

// DOM Elements
const uploadAudioRadio = document.getElementById('uploadAudio');
const recordAudioRadio = document.getElementById('recordAudio');
const uploadSection = document.getElementById('uploadSection');
const recordSection = document.getElementById('recordSection');
const audioFile = document.getElementById('audioFile');
const uploadedAudio = document.getElementById('uploadedAudio');
const recordButton = document.getElementById('recordButton');
const recordedAudio = document.getElementById('recordedAudio');
const translateButton = document.getElementById('translateButton');
const resultsSection = document.getElementById('results');
const transcriptArea = document.getElementById('transcript');
const translationArea = document.getElementById('translation');
const outputAudio = document.getElementById('outputAudio');
const downloadButton = document.getElementById('downloadButton');

// Recording variables
let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let recordingStartTime;
let timerInterval;

// Event Listeners
uploadAudioRadio.addEventListener('change', () => {
    uploadSection.style.display = 'block';
    recordSection.style.display = 'none';
});

recordAudioRadio.addEventListener('change', () => {
    uploadSection.style.display = 'none';
    recordSection.style.display = 'block';
});

audioFile.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        uploadedAudio.src = URL.createObjectURL(file);
        uploadedAudio.style.display = 'block';
    }
});

// Function to update the timer display
function updateTimer() {
    const currentTime = Date.now();
    const elapsedTime = Math.floor((currentTime - recordingStartTime) / 1000);
    const minutes = Math.floor(elapsedTime / 60);
    const seconds = elapsedTime % 60;
    recordButton.textContent = `Stop Recording (${minutes}:${seconds.toString().padStart(2, '0')})`;
}

// Function to check if browser is Safari
function isSafari() {
    return /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
}

// Function to handle Safari-specific audio recording
async function startRecordingSafari() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                sampleRate: 44100
            }
        });
        mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/webm;codecs=opus'
        });
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            recordedAudio.src = URL.createObjectURL(audioBlob);
            recordedAudio.style.display = 'block';
            clearInterval(timerInterval);
            recordButton.textContent = 'Start Recording';
            recordButton.classList.remove('recording');
        };

        mediaRecorder.start();
        isRecording = true;
        recordingStartTime = Date.now();
        timerInterval = setInterval(updateTimer, 1000);
        recordButton.classList.add('recording');
    } catch (err) {
        console.error('Error accessing microphone:', err);
        alert('Error accessing microphone. Please make sure you have granted microphone permissions.');
    }
}

// Update the recordButton click event
recordButton.addEventListener('click', async () => {
    if (!isRecording) {
        if (isSafari()) {
            await startRecordingSafari();
        } else {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.ondataavailable = (event) => {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    recordedAudio.src = URL.createObjectURL(audioBlob);
                    recordedAudio.style.display = 'block';
                    clearInterval(timerInterval);
                    recordButton.textContent = 'Start Recording';
                    recordButton.classList.remove('recording');
                };

                mediaRecorder.start();
                isRecording = true;
                recordingStartTime = Date.now();
                timerInterval = setInterval(updateTimer, 1000);
                recordButton.classList.add('recording');
            } catch (err) {
                console.error('Error accessing microphone:', err);
                alert('Error accessing microphone. Please make sure you have granted microphone permissions.');
            }
        }
    } else {
        mediaRecorder.stop();
        isRecording = false;
        clearInterval(timerInterval);
        recordButton.textContent = 'Start Recording';
        recordButton.classList.remove('recording');
    }
});

translateButton.addEventListener('click', async () => {
    if (!config.API_KEY || config.API_KEY === 'YOUR_OPENAI_API_KEY') {
        alert('Please set your OpenAI API key in the js/app.js file');
        return;
    }
    
    const sourceLanguage = document.getElementById('sourceLanguage').value;
    const targetLanguage = document.getElementById('targetLanguage').value;
    
    let audioBlob;
    if (uploadAudioRadio.checked && audioFile.files[0]) {
        audioBlob = audioFile.files[0];
    } else if (recordAudioRadio.checked && audioChunks.length > 0) {
        audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    } else {
        alert('Please provide an audio input first.');
        return;
    }

    try {
        translateButton.disabled = true;
        translateButton.textContent = 'Translating...';
        console.log('Starting translation process...');

        // First, transcribe the audio
        console.log('Step 1: Transcribing audio...');
        const transcript = await transcribeAudio(audioBlob, sourceLanguage);
        transcriptArea.value = transcript;
        console.log('Transcription complete:', transcript);

        // Then, translate the text
        console.log('Step 2: Translating text...');
        const translation = await translateText(transcript, sourceLanguage, targetLanguage);
        translationArea.value = translation;
        console.log('Translation complete:', translation);

        // Finally, convert translation to speech
        console.log('Step 3: Converting to speech...');
        const audioUrl = await textToSpeech(translation, targetLanguage);
        outputAudio.src = audioUrl;
        console.log('Speech conversion complete');
        
        resultsSection.style.display = 'block';
        downloadButton.onclick = () => {
            const a = document.createElement('a');
            a.href = audioUrl;
            a.download = `translated_audio_${targetLanguage}.mp3`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        };
    } catch (error) {
        console.error('Error during translation process:', error);
        alert('Error during translation: ' + error.message);
    } finally {
        translateButton.disabled = false;
        translateButton.textContent = 'Translate Audio';
    }
});

async function transcribeAudio(audioBlob, sourceLanguage) {
    if (!config.API_KEY) {
        throw new Error('API key not initialized');
    }
    console.log('Starting transcription...');
    const formData = new FormData();
    formData.append('file', audioBlob);
    formData.append('model', 'whisper-1');
    formData.append('language', sourceLanguage);

    try {
        console.log('Sending transcription request...');
        const response = await fetch('https://api.openai.com/v1/audio/transcriptions', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${config.API_KEY}`
            },
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Transcription failed:', errorData);
            throw new Error(`Transcription failed: ${errorData.error?.message || 'Unknown error'}`);
        }

        const data = await response.json();
        console.log('Transcription successful:', data);
        return data.text;
    } catch (error) {
        console.error('Transcription error:', error);
        throw error;
    }
}

async function translateText(text, sourceLang, targetLang) {
    if (!config.API_KEY) {
        throw new Error('API key not initialized');
    }
    console.log('Starting translation...', { text, sourceLang, targetLang });
    
    try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${config.API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: 'gpt-3.5-turbo',
                messages: [{
                    role: 'user',
                    content: `Translate this text from ${sourceLang} to ${targetLang}: "${text}"`
                }]
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Translation failed:', errorData);
            throw new Error(`Translation failed: ${errorData.error?.message || 'Unknown error'}`);
        }

        const data = await response.json();
        console.log('Translation successful:', data);
        return data.choices[0].message.content;
    } catch (error) {
        console.error('Translation error:', error);
        throw error;
    }
}

async function textToSpeech(text, targetLang) {
    if (!config.API_KEY) {
        throw new Error('API key not initialized');
    }
    console.log('Starting text-to-speech...', { text, targetLang });
    
    try {
        const response = await fetch('https://api.openai.com/v1/audio/speech', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${config.API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: 'tts-1',
                input: text,
                voice: 'alloy',
                response_format: 'mp3'
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Text-to-speech failed:', errorData);
            throw new Error(`Text-to-speech failed: ${errorData.error?.message || 'Unknown error'}`);
        }

        const audioBlob = await response.blob();
        console.log('Text-to-speech successful');
        return URL.createObjectURL(audioBlob);
    } catch (error) {
        console.error('Text-to-speech error:', error);
        throw error;
    }
}

// Function to initialize the API key
function initializeAPIKey() {
    const apiKey = localStorage.getItem('openai_api_key');
    if (apiKey) {
        config.API_KEY = apiKey;
    }
}

// Call initializeAPIKey when the page loads
document.addEventListener('DOMContentLoaded', () => {
    initializeAPIKey();
    
    // Add API key input field if not already present
    if (!document.getElementById('apiKeyInput')) {
        const apiKeyContainer = document.createElement('div');
        apiKeyContainer.className = 'mt-3';
        apiKeyContainer.innerHTML = `
            <h3>OpenAI API Key</h3>
            <div class="input-group">
                <input type="password" id="apiKeyInput" class="form-control" placeholder="Enter your OpenAI API key">
                <button class="btn btn-outline-secondary" type="button" id="saveApiKey">Save</button>
            </div>
        `;
        document.querySelector('.container').insertBefore(apiKeyContainer, document.querySelector('.row'));
        
        // Add event listener for saving API key
        document.getElementById('saveApiKey').addEventListener('click', () => {
            const apiKey = document.getElementById('apiKeyInput').value;
            if (apiKey) {
                localStorage.setItem('openai_api_key', apiKey);
                config.API_KEY = apiKey;
                alert('API key saved successfully!');
            } else {
                alert('Please enter a valid API key');
            }
        });
    }
}); 