import openai
import threading

openai.api_key = 'sk- you key'


class AIChatModel:
    def __init__(self):
        self.message_history = [{'role': 'system',
                                 'content': 'Отвечай только на вопрос который написан после последнего User:'}]
        self.chat_lock = threading.Lock()

    def generate_response(self, user_input, gui):
        self.message_history.append({'role': 'user', 'content': user_input})

        if len(self.message_history) > 3:
            self.message_history.pop(0)

        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=self.message_history,
                temperature=0,
                stream=True
            )
            next(response)
            for chunk in response:
                if 'choices' in chunk and len(chunk['choices']) > 0 and chunk['choices'][0]['finish_reason'] != "stop":
                    text = chunk['choices'][0]['delta']['content']
                    gui.update_conversation_display(text)
                else:
                    break

        except Exception as e:
            print("An error occurred:", str(e))
