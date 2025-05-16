import sys
import os
import base64
from datetime import datetime
import re

# Ajoute le répertoire racine du projet au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from research_mate.crew import run_crew
import logging
from research_mate.utils import sanitize_filename, ensure_output_folders

# Configure logging
logging.basicConfig(level=logging.INFO)

# Nettoyage du Markdown
def clean_markdown(text):
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'(\*\*|__)(.*?)\1', r"\2", text)
    text = re.sub(r'(\*|_)(.*?)\1', r"\2", text)
    return text.strip()

# Génération du PDF
def write_pdf_using_platypus(text, topic, article_sources, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='TitleCenter', parent=styles['Heading1'], alignment=1, spaceAfter=20))
    styles.add(ParagraphStyle(name='SectionHeader', parent=styles['Heading2'], spaceAfter=10))
    styles.add(ParagraphStyle(name='Body', parent=styles['Normal'], spaceAfter=8))

    elems = []
    elems.append(Paragraph("ResearchMate Final Report 📄", styles['TitleCenter']))
    elems.append(Paragraph(f"<b>Topic:</b> {topic} 🧠", styles['Body']))
    elems.append(Paragraph(f"<b>Date:</b> {datetime.now():%Y-%m-%d %H:%M:%S} ⏰", styles['Body']))
    elems.append(Spacer(1, 12))

    lines = text.splitlines()
    in_list, items = False, []
    for raw in lines:
        line = raw.strip()
        if not line:
            if in_list:
                elems.append(ListFlowable(items, bulletType='bullet'))
                items, in_list = [], False
            continue

        if raw.lstrip().startswith('#') or re.match(r'^\d+\.\s+', raw):
            if in_list:
                elems.append(ListFlowable(items, bulletType='bullet'))
                items, in_list = [], False
            elems.append(Paragraph(clean_markdown(line), styles['SectionHeader']))
        elif re.match(r'^[\*-]\s+', raw):
            if not in_list:
                in_list, items = True, []
            item = re.sub(r'^[\*-]\s+', '', line)
            items.append(ListItem(Paragraph(clean_markdown(item), styles['Body'])))
        else:
            if in_list:
                elems.append(ListFlowable(items, bulletType='bullet'))
                items, in_list = [], False
            elems.append(Paragraph(clean_markdown(line), styles['Body']))

    if in_list:
        elems.append(ListFlowable(items, bulletType='bullet'))

    if article_sources:
        elems.append(Spacer(1, 12))
        elems.append(Paragraph("References:", styles['SectionHeader']))
        for i, art in enumerate(article_sources, 1):
            elems.append(Paragraph(f"[{i}] {art['title']}", styles['Body']))

    doc.build(elems)
    return output_path

# ---- Streamlit App ----

# Configuration Streamlit en tout premier
st.set_page_config(page_title="Research Mate", layout="wide")

def main():
    # Animation de bienvenue: neige
    st.snow()

    st.title("Research Mate: Academic Research Assistant ✨")
    st.markdown("Generate academic research reports by entering a topic. 🚀")

    state = st.session_state
    if 'pdf_path' not in state:
        state.pdf_path = None
    if 'show_pdf' not in state:
        state.show_pdf = False
    if 'articles' not in state:
        state.articles = []

    # Sidebar: articles générés dans cette session
    st.sidebar.header("📰 Collected Articles")
    if state.articles:
        for idx, art in enumerate(state.articles):
            st.sidebar.markdown(f"**{art['title']}**")
            b64 = base64.b64encode(open(art['path'], 'rb').read()).decode()
            link = f"data:application/octet-stream;base64,{b64}"
            st.sidebar.markdown(
                f"<a href='{link}' download='{os.path.basename(art['path'])}'>📥 Download</a>",
                unsafe_allow_html=True
            )
            # Bouton pour afficher l'article
            if st.sidebar.button('👁️ Afficher', key=f"show_{idx}"):
                state.display_article = art
    else:
        st.sidebar.info("No articles yet. Generate a report to see them here.")

    # Entrée de sujet
    st.subheader("Enter your research topic: ✏️")
    state.user_topic = st.text_input("", value=state.get('user_topic', ''))
    final = state.user_topic.strip()

    ensure_output_folders()

    # Bouton génération
    if st.button("Generate Research Report 📚"):
        if not final:
            st.error("Please enter a topic before generating. ⚠️")
        else:
            with st.spinner(f"Generating report for: {final}..."):
                try:
                    res = run_crew(final)
                    report = clean_markdown(str(res.tasks_output[-1]))

                    # Lecture des articles
                    art_dir = 'outputs/articles'
                    new_articles = []
                    if os.path.isdir(art_dir):
                        for fname in sorted(os.listdir(art_dir)):
                            if fname.endswith('.txt'):
                                path = os.path.join(art_dir, fname)
                                with open(path, 'r', encoding='utf8') as f:
                                    lines = f.read().splitlines()
                                title = next((l.replace('Title: ', '') for l in lines if l.startswith('Title: ')), fname)
                                new_articles.append({'title': title, 'path': path})
                    state.articles = new_articles

                    # Générer PDF
                    pdf_out = f"outputs/report_{sanitize_filename(final)}.pdf"
                    state.pdf_path = write_pdf_using_platypus(report, final, new_articles, pdf_out)
                    state.show_pdf = False
                    st.success(f"Report generated for: {final}! 🎉")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error generating report: {e} 😢")

    # Toggle affichage PDF
    if state.pdf_path:
        st.checkbox("Show PDF Report 📄", key='show_pdf')
        if state.show_pdf:
            pdf_bytes = open(state.pdf_path, 'rb').read()
            st.markdown(
                f"<iframe src='data:application/pdf;base64,{base64.b64encode(pdf_bytes).decode()}' width='100%' height='600'></iframe>",
                unsafe_allow_html=True
            )

    # Affichage d'un article sélectionné
    if state.get('display_article'):
        art = state.display_article
        st.subheader(f"{art['title']} 📖")
        with open(art['path'], 'r', encoding='utf8') as f:
            content = f.read()
        st.markdown(f"```text\n{content}\n```")

if __name__ == '__main__':
    main()
