from transformers import AutoModelForCausalLM, AutoTokenizer
from inference.chatbot import Chatbot

def main():
    print("Loading model and tokenizer...")
    model_name = "microsoft/DialoGPT-small"  # Change to your fine-tuned model if needed
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    bot = Chatbot(model, tokenizer)

    print("Chatbot is ready. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        response = bot.generate_response(user_input)
        print(f"Bot: {response}\n")

if __name__ == "__main__":
    main()
