"""
Main Application - Multi-Agent Support System
Entry point for the support system
"""

from dotenv import load_dotenv
from workflow import create_workflow
load_dotenv()

def format_response(result: dict):
    """Format and display the response"""
    print("\nAgent:")
    print(result['response'])
    
    if result.get('error'):
        print(f"Error: {result['error']}\n")


def interactive_mode(workflow):
    """Run interactive query mode"""
    
    while True:
        try:
            # Get user input
            query = input("\nYour Question: ").strip()
            
            # Check for exit commands
            if query.lower() in ['exit', 'quit', 'q']:
                print("\n Thank you for using the Multi-Agent Support System!")
                break
            
            # Skip empty queries
            if not query:
                continue
            
            # Process query
            result = workflow.run(query)
            
            # Display response
            format_response(result)
        
        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")


def main():
    """Main application entry point"""    
    try:
        # Create workflow
        workflow = create_workflow()
        
        # Run in interactive mode
        interactive_mode(workflow)
    
    except Exception as e:
        print(f"\nFatal Error: {str(e)}")
        print("Please check your configuration and try again.")


if __name__ == "__main__":
    main()
