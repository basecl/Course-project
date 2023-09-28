from Audio import AudioTranscriber
from Chat import AIChatModel
from App import GUI

audio_transcriber = AudioTranscriber()
ai_chat_model = AIChatModel()
gui = GUI(ai_chat_model, audio_transcriber)
gui.run()