"""
Simple example demonstrating basic multi-agent workflow
Perfect for learning the fundamentals
"""

from multi_agent_system import MultiAgentSystem
import os
from dotenv import load_dotenv

load_dotenv()


def simple_example():
    """Basic example with a simple task"""
    print("="*60)
    print("EXAMPLE 1: Basic Multi-Agent Workflow")
    print("="*60)
    
    system = MultiAgentSystem(temperature=0.7)
    task = "Benefits of meditation for mental health"
    result = system.run(task)
    
    print("\n✍️  FINAL REPORT:")
    print(result["final_report"])


def custom_task_example():
    """Example with custom task"""
    print("\n\n" + "="*60)
    print("EXAMPLE 2: Custom Task")
    print("="*60)
    
    system = MultiAgentSystem(temperature=0.5)
    task = input("\nEnter your research task: ")
    result = system.run(task)
    
    print("\n📊 ALL OUTPUTS:")
    print("\n1️⃣  Research:")
    print("-" * 60)
    print(result["research_output"])
    
    print("\n\n2️⃣  Analysis:")
    print("-" * 60)
    print(result["analysis_output"])
    
    print("\n\n3️⃣  Final Report:")
    print("-" * 60)
    print(result["final_report"])


def batch_processing_example():
    """Process multiple tasks in batch"""
    print("\n\n" + "="*60)
    print("EXAMPLE 3: Batch Processing")
    print("="*60)
    
    system = MultiAgentSystem(temperature=0.7)
    
    tasks = [
        "Impact of social media on teenagers",
        "Benefits of electric vehicles",
        "Future of remote work"
    ]
    
    results = []
    for i, task in enumerate(tasks, 1):
        print(f"\n\n📋 Processing Task {i}/{len(tasks)}: {task}")
        result = system.run(task)
        results.append({
            "task": task,
            "report": result["final_report"]
        })
    
    # Display all reports
    print("\n\n" + "="*60)
    print("📊 BATCH RESULTS")
    print("="*60)
    
    for i, result in enumerate(results, 1):
        print(f"\n\n{'='*60}")
        print(f"Report {i}: {result['task']}")
        print('='*60)
        print(result['report'])


def main():
    """Run examples"""
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Error: OPENAI_API_KEY not found!")
        print("Please create a .env file with your API key:")
        print("OPENAI_API_KEY=your_key_here")
        return
    
    print("""
╔════════════════════════════════════════════════════════════╗
║        Multi-Agent System - Usage Examples                 ║
╚════════════════════════════════════════════════════════════╝

Choose an example to run:
1. Simple example (pre-defined task)
2. Custom task (enter your own)
3. Batch processing (multiple tasks)
4. Run all examples

""")
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        simple_example()
    elif choice == "2":
        custom_task_example()
    elif choice == "3":
        batch_processing_example()
    elif choice == "4":
        simple_example()
        custom_task_example()
        batch_processing_example()
    else:
        print("Invalid choice. Running simple example...")
        simple_example()
    
    print("\n\n✅ Examples completed!")


if __name__ == "__main__":
    main()
