from crewai.tools import BaseTool
import os
import requests
import logging
from research_mate.utils import sanitize_filename, ensure_output_folders
from pydantic import BaseModel, Field

class PubMedInput(BaseModel):
    topic: str = Field(..., description="The research topic to search for in PubMed")

class PubMedTool(BaseTool):
    name: str = "PubMed Search"
    description: str = "Search for articles on PubMed"
    args_schema: type[BaseModel] = PubMedInput

    def _run(self, topic: str) -> str:
        logging.info("[PubMedTool] Fetching articles from PubMed...")

        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        search_url = f"{base_url}esearch.fcgi"
        fetch_url = f"{base_url}efetch.fcgi"

        # Search for article IDs
        params = {"db": "pubmed", "term": topic, "retmax": 5, "retmode": "json"}
        response = requests.get(search_url, params=params)
        ids = response.json().get("esearchresult", {}).get("idlist", [])

        if not ids:
            logging.info("[PubMedTool] No PubMed articles found.")
            return "No articles found."

        articles = []
        ensure_output_folders()
        safe_topic = sanitize_filename(topic)

        # Download each article and save as txt
        for idx, pubmed_id in enumerate(ids, start=1):
            params = {"db": "pubmed", "id": pubmed_id, "retmode": "xml"}
            response = requests.get(fetch_url, params=params)
            raw_text = response.text

            txt_path = f"outputs/articles/pubmed_{idx}_{safe_topic}.txt"
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(raw_text)
            logging.info(f"[PubMedTool] Saved raw PubMed txt: {txt_path}")

            # Add article to list for orchestrator tracking
            articles.append({
                "title": f"PubMed Article {idx} for '{topic}'",
                "content": raw_text
            })

        return "\n\n".join([article["content"] for article in articles])