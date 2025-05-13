import os
import yaml
from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM
from research_mate.tools.arxiv_tool import ArxivTool
from research_mate.tools.pubmed_tool import PubMedTool
from research_mate.tools.document_search_tool import DocumentSearchTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load configurations from YAML files
def load_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

# Get the absolute path to the config directory relative to this script (crew.py)
config_dir = os.path.join(os.path.dirname(__file__), 'config')

# Load agents and tasks configurations using absolute paths
agents_path = os.path.join(config_dir, 'agents.yaml')
tasks_path = os.path.join(config_dir, 'tasks.yaml')

agents_config = load_yaml(agents_path)
tasks_config = load_yaml(tasks_path)

# Initialize LLM (Gemini 1.5 Flash)
def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")
    
    try:
        return LLM(
            model="gemini/gemini-1.5-flash",  # Explicitly specify provider/model for LiteLLM
            api_key=api_key,
            temperature=0.7
        )
    except Exception as e:
        print(f"Error initializing gemini/gemini-1.5-flash: {str(e)}. Falling back to gemini-pro.")
        return LLM(
            model="gemini/gemini-pro",
            api_key=api_key,
            temperature=0.7
        )

# Define tools for the research agent
tools = {
    "pubmed": PubMedTool(name="PubMed Search", description="Search for articles on PubMed"),
    "arxiv": ArxivTool(name="Arxiv Search", description="Search for papers on Arxiv"),
    "document_search": DocumentSearchTool(name="Document Search", description="Search local documents")
}

# Create agents
def create_agents():
    llm = get_llm()
    agents = {}
    
    for agent_name, config in agents_config.items():
        agent_config = {
            "role": config["role"],
            "goal": config["goal"],
            "backstory": config["backstory"],
            "verbose": True,
            "llm": llm
        }
        
        if "tools" in config:
            agent_config["tools"] = [tools[tool.split(".")[-2].replace("_tool", "").lower()] for tool in config["tools"]]
        
        agents[agent_name] = Agent(**agent_config)
        print(f"Created agent {agent_name}: {agents[agent_name]}")
    return agents

# Create tasks
def create_tasks(agents, topic):
    tasks = []
    
    for task_name, config in tasks_config.items():
        agent = agents[config["agent"]]
        description = config["description"].format(topic=topic).strip()
        expected_output = config["expected_output"].format(topic=topic).strip()
        
        # Initialize task_config as a dictionary
        task_config = {
            "description": description,
            "expected_output": expected_output,
            "agent": agent
        }
        
        # Add config field only if necessary
        task_config["config"] = config.get("config", {"temperature": 0.7})
        
        # Handle context
        context_tasks = None
        if task_name == "summarization":
            context_tasks = [tasks[0]] if tasks else None  # Reference collect_articles task
        elif task_name == "edit_report":
            context_tasks = [tasks[1]] if len(tasks) > 1 else None  # Reference summarization task
        
        # Add tools if present
        if "tools" in config:
            task_config["tools"] = [tools[tool] for tool in config["tools"]]
        
        # Debug log
        print(f"Task config for {task_name}: {task_config}")
        print(f"Type of task_config: {type(task_config)}")
        print(f"Keys in task_config: {task_config.keys()}")
        print(f"Context for {task_name}: {context_tasks}")
        
        try:
            task = Task(**task_config, context=context_tasks)
            tasks.append(task)
        except Exception as e:
            print(f"Error creating task {task_name}: {str(e)}")
            raise
    
    return tasks

# Orchestrate the crew
def run_crew(topic):
    agents = create_agents()
    tasks = create_tasks(agents, topic)
    
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    result = crew.kickoff()
    return result

if __name__ == "__main__":
    topic = "Machine Learning in Healthcare"
    result = run_crew(topic)
    print(result)