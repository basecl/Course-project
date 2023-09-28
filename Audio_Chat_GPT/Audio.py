import torch
import sounddevice as sd
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import threading

sampling_rate = 16000
input_duration = 3

speech_to_text_model_name = "jonatasgrosman/wav2vec2-large-xlsr-53-russian"
speech_to_text_model = Wav2Vec2ForCTC.from_pretrained(speech_to_text_model_name)
speech_to_text_processor = Wav2Vec2Processor.from_pretrained(speech_to_text_model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
speech_to_text_model = speech_to_text_model.to(device)


class AudioTranscriber:
    def __init__(self):
        self.recording_lock = threading.Lock()

    def transcribe_audio(self, device_id=1):
        with self.recording_lock:
            print("Recording voice...")
            audio_input = sd.rec(
                int(input_duration * sampling_rate),
                samplerate=sampling_rate,
                channels=1,
                dtype='float32',
                device=device_id
            )
            sd.wait()
            print("Recording finished.")

        audio_input = torch.from_numpy(audio_input.squeeze()).to(device)

        if audio_input.shape[0] != sampling_rate * input_duration:
            resampler = torchaudio.transforms.Resample(audio_input.shape[0], sampling_rate * input_duration)
            audio_input = resampler(audio_input)

        input_values = speech_to_text_processor(audio_input, sampling_rate=sampling_rate,
                                                return_tensors="pt").input_values.to(device)

        with torch.no_grad():
            logits = speech_to_text_model(input_values).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = speech_to_text_processor.decode(predicted_ids[0])

        return transcription
