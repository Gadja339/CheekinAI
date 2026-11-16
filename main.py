from llm import LocalLLM


def main():
    ai = LocalLLM()

    print("CheekinGPT запущен!")
    print("Для выхода введи /exit")

    while True:
        prompt = input("\nВы: ").strip()

        if prompt == "/exit":
            break

        if not prompt:
            continue

        try:
            answer = ai.ask(prompt)

            print(f"\nCheekinGPT: {answer}")

            ai.monitor.display()

        except Exception as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()