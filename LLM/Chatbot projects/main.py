import argparse
from utils.config import load_config
from training.train import train  # Import the train wrapper, not train_model
from inference.chatbot import Chatbot

def main():
    parser = argparse.ArgumentParser(description="Chatbot Main Script")
    parser.add_argument(
        '--config', 
        type=str, 
        default='configs/default.yaml', 
        help='Path to config file (JSON or YAML)'
    )
    parser.add_argument(
        '--mode', 
        type=str, 
        choices=['train', 'chat'], 
        default='chat', 
        help='Mode to run: "train" for training, "chat" for interactive chatting'
    )
    args = parser.parse_args()
    
    # Load configuration from file
    config = load_config(args.config)

    if args.mode == 'train':
        train(config)  # Call the train wrapper

    elif args.mode == 'chat':
        bot = Chatbot(config)
        print("Type 'quit' to stop chatting.\n")
        while True:
            user_input = input("You: ")
            if user_input.strip().lower() == 'quit':
                print("Exiting chat. Goodbye!")
                break
            reply = bot.generate_response(user_input)
            print(f"Bot: {reply}")

if __name__ == '__main__':
    main()
