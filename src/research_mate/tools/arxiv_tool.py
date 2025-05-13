import logging
from crewai.tools import BaseTool
import os
import requests
from research_mate.utils import sanitize_filename, ensure_output_folders
from pydantic import BaseModel, Field

class ArxivInput(BaseModel):
    topic: str = Field(..., description="The research topic to search for in Arxiv")

class ArxivTool(BaseTool):
    name: str = "Arxiv Search"
    description: str = "Search for papers on Arxiv"
    args_schema: type[BaseModel] = ArxivInput

    def _run(self, topic: str) -> str:
        logging.info("[ArxivTool] Fetching papers from Arxiv...")

        base_url = "http://export.arxiv.org/api/query"
        params = {
            "search_query": f"all:{topic}",
            "start": 0,
            "max_results": 5
        }

        try:
            response = requests.get(base_url, params=params)
            if response.status_code != 200:
                logging.error(f"[ArxivTool] Error fetching from Arxiv: {response.status_code}")
                return "Error fetching papers from Arxiv."
        except requests.RequestException as e:
            logging.error(f"[ArxivTool] Network error: {str(e)}")
            return "Network error while fetching papers from Arxiv."

        papers = []
        ensure_output_folders()
        safe_topic = sanitize_filename(topic)

        # Parse the XML response
        from xml.etree import ElementTree
        try:
            root = ElementTree.fromstring(response.content)
            # Define the namespace for Arxiv's Atom feed
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            entries = root.findall('.//atom:entry', ns)
            if not entries:
                logging.info("[ArxivTool] No Arxiv papers found.")
                return "No papers found."

            for idx, entry in enumerate(entries, start=1):
                # Safely extract elements with namespace
                title_elem = entry.find('atom:title', ns)
                summary_elem = entry.find('atom:summary', ns)
                pdf_link_elem = entry.find(".//atom:link[@title='pdf']", ns)

                title = title_elem.text if title_elem is not None else "No title available"
                summary = summary_elem.text if summary_elem is not None else "No summary available"
                pdf_link = pdf_link_elem.get('href') if pdf_link_elem is not None else "No PDF link available"

                # Save raw XML
                xml_path = f"outputs/articles/arxiv_{idx}_{safe_topic}.xml"
                with open(xml_path, "w", encoding="utf-8") as f:
                    f.write(ElementTree.tostring(entry, encoding='unicode'))
                logging.info(f"[ArxivTool] Saved raw Arxiv XML: {xml_path}")

                # Add paper to list
                papers.append({
                    "title": title,
                    "content": f"Title: {title}\n\nSummary: {summary}\n\nPDF: {pdf_link}"
                })

        except ElementTree.ParseError as e:
            logging.error(f"[ArxivTool] XML parsing error: {str(e)}")
            return "Error parsing Arxiv response."
        except Exception as e:
            logging.error(f"[ArxivTool] Unexpected error: {str(e)}")
            return "Unexpected error while processing Arxiv response."

        return "\n\n".join([paper["content"] for paper in papers])