from research_mate.crew import run_crew

def run(topic: str = None) -> str:
    """
    Entry point to execute the research mate crew.
    
    Args:
        topic (str, optional): The research topic to investigate. If None, a default topic is used.
    
    Returns:
        str: The final report content.
    """
    # Define a list of possible topics
    available_topics = [
        "Machine Learning in Healthcare",
        "Artificial Intelligence in Education",
        "Deep Learning for Climate Modeling",
        "Natural Language Processing in Finance",
        "Computer Vision in Autonomous Vehicles"
    ]
    
    # If no topic is provided, use a default
    if topic is None:
        topic = available_topics[0]  # Default to the first topic
    
    print(f"Starting research on topic: {topic}")
    
    result = run_crew(topic)
    
    # Extract the final report from CrewOutput
    final_report = str(result.tasks_output[-1])  # Get the output of the last task (edit_report)
    
    # Save the final report to a file
    with open("report.md", "w", encoding="utf-8") as f:
        f.write(final_report)
    print("Final report saved to report.md")
    
    return final_report

def main():
    # You can change the topic here by selecting from available_topics
    selected_topic = "Machine Learning in Healthcare"  # Change this to any topic from available_topics
    run(selected_topic)

if __name__ == "__main__":
    main()