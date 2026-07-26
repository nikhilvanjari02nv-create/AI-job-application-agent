from app.services.llm import ask_llm


def main():
    prompt = "Reply with exactly these two words: Hello World"

    response = ask_llm(prompt)

    print("\n========== RESPONSE ==========\n")
    print(response)
    print("\n==============================\n")


if __name__ == "__main__":
    main()