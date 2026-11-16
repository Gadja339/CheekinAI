
class ContextMonitor:
    def __init__(self, max_tokens: int):
        self.max_tokens = max_tokens
        self.prompt_tokens = 0
        self.generated_tokens = 0

    def update(self, response):
        self.prompt_tokens = response.prompt_eval_count or 0
        self.generated_tokens = response.eval_count or 0

    @property
    def used(self) -> int:
        return self.prompt_tokens + self.generated_tokens

    @property
    def percentage(self) -> float:
        return min(
            self.used / self.max_tokens * 100,
            100.0
        )

    @property
    def free(self) -> int:
        return max(self.max_tokens - self.used, 0)

    def display(self):
        print("\n--- Контекст ---")
        print(f"Вход: {self.prompt_tokens} токенов")
        print(f"Ответ: {self.generated_tokens} токенов")
        print(
            f"Всего: {self.used}/{self.max_tokens} "
            f"({self.percentage:.1f}%)"
        )
        print(f"Свободно: ~{self.free} токенов")

        if self.percentage >= 85:
            print("Внимание: контекст почти заполнен!")
        elif self.percentage >= 70:
            print("Контекст заполняется.")
