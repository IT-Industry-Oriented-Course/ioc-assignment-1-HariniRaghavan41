import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import run_agent

def main():
    print("Clinical Workflow Agent CLI")
    print("---------------------------")
    print("Type 'exit' to quit.")
    
    # Check keys
    if not os.getenv("HUGGINGFACEHUB_API_TOKEN") and not os.getenv("OPENAI_API_KEY"):
         print("WARNING: No API keys detected in environment. Please set HUGGINGFACEHUB_API_TOKEN or OPENAI_API_KEY.")
    
    while True:
        user_input = input("\nEnter Request: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        response = run_agent(user_input)
        print("\nAgent Response:")
        print(response)

if __name__ == "__main__":
    main()
