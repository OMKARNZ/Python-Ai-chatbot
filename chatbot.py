import sys
from google import genai
from google.genai import errors, types

# Configuration constants
API_KEY = "YOUR API_KEY"
MODEL_NAME = "gemini-2.5-flash"
EXIT_COMMANDS = {"exit", "quit", "q"}

def main():
    #Main execution loop for the CMD chatbot.
    # Initialize connection inside a try-block to catch early network/auth errors
    try:
        client = genai.Client(api_key=API_KEY)
        
        config = types.GenerateContentConfig(
            system_instruction="You are a helpful assistant, CMD terminal assistant.Do not use # and * in answer",
            temperature=0.2  #High accuracy
        )
        
        chat = client.chats.create(model=MODEL_NAME, config=config)
    except Exception as init_err:
        print(f"Initialization Failed: Check your API key or network.\nDetails: {init_err}")
        return

    print("-" * 50)
    print(f"Live CMD Chatbot Connected! [{MODEL_NAME}]")
    print(f"Type {', '.join(f'({c})' for c in EXIT_COMMANDS)} to quit.")
    print("-" * 50)

    # Reusable prompt string to avoid recreating string objects in memory
    prompt_str = "\nYou: "

    while True:
        try:
            user_input = input(prompt_str).strip()
            
            # Fast membership check using O(1) set lookups
            if user_input.lower() in EXIT_COMMANDS:
                print("\nBot: Goodbye!")
                break
                
            if not user_input:
                continue
                
            print("\nBot: ", end="", flush=True)
            
            # Stream the text response
            response_stream = chat.send_message_stream(user_input)
            for chunk in response_stream:
                if chunk.text:  # Ensure chunk isn't empty or None
                    print(chunk.text, end="", flush=True)
            print() 

        except errors.APIError as api_err:
            # Catch specific Google API errors (quota limits, invalid keys, server issues)
            print(f"\nGoogle API Error: {api_err.message}")
        except KeyboardInterrupt:
            # Handle Ctrl+C cleanly without spitting out an ugly Python stack trace
            print("\n\nBot: Session interrupted. Goodbye!")
            break
        except Exception as e:
            # Catch-all for unexpected local runtime issues
            print(f"\nUnexpected Error: {e}")

if __name__ == "__main__":
    main()
