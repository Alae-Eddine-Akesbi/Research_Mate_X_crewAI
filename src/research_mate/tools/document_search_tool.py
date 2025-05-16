from crewai.tools import BaseTool
import os
import logging
from research_mate.utils import sanitize_filename, ensure_output_folders
from pydantic import BaseModel, Field

class DocumentSearchInput(BaseModel):
    topic: str = Field(..., description="The research topic to search for in local documents")

class DocumentSearchTool(BaseTool):
    name: str = "Document Search"
    description: str = "Search local documents"
    args_schema: type[BaseModel] = DocumentSearchInput

    def _run(self, topic: str) -> str:
        logging.info("[DocumentSearchTool] Searching local documents...")
        
        # Define the directory to search in
        search_dir = "outputs/articles"
        ensure_output_folders()
        
        if not os.path.exists(search_dir):
            logging.info("[DocumentSearchTool] No local documents found.")
            return "No local documents found."
        
        results = []
        for filename in os.listdir(search_dir):
            if filename.endswith(('.txt')):
                file_path = os.path.join(search_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if topic.lower() in content.lower():
                            results.append(f"Found in {filename}:\n{content[:500]}...")
                except Exception as e:
                    logging.error(f"[DocumentSearchTool] Error reading {filename}: {str(e)}")
        
        if not results:
            return "No matching documents found."
        
        return "\n\n".join(results)