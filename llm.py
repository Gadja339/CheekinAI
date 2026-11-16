from ollama import Client

from config import (
    OLLAMA_HOST,
    MODEL,
    CONTEXT_SIZE,
    TEMPERATURE,
    MAX_TOOL_STEPS,
    SYSTEM_PROMPT
)

from browser import open_website
from monitoring import ContextMonitor
from config import CONTEXT_SIZE

class LocalLLM:
    def __init__(self):
        self.monitor = ContextMonitor(CONTEXT_SIZE)
        self.client = Client(host=OLLAMA_HOST)
        self.model = MODEL

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        self.tools = {
            "open_website": open_website
        }

    def ask(self, prompt: str) -> str:
        self.messages.append({
            "role": "user",
            "content": prompt
        })

        for _ in range(MAX_TOOL_STEPS):
            response = self.client.chat(
                model=self.model,
                messages=self.messages,
                tools=list(self.tools.values()),
                options={
                    "num_ctx": CONTEXT_SIZE,
                    "temperature": TEMPERATURE
                }
            )
            self.monitor.update(response)

            self.messages.append(response.message)

            if not response.message.tool_calls:
                return response.message.content or ""

            for call in response.message.tool_calls:
                name = call.function.name
                args = call.function.arguments

                if name not in self.tools:
                    result = "Неизвестный инструмент."
                else:
                    try:
                        result = self.tools[name](**args)
                    except (TypeError, ValueError) as error:
                        result = f"Ошибка аргументов: {error}"

                self.messages.append({
                    "role": "tool",
                    "tool_name": name,
                    "content": str(result)
                })

        return "Превышено максимальное количество шагов."