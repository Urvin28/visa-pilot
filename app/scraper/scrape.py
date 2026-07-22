import requests
from bs4 import BeautifulSoup
from pathlib import Path
from app.scraper.urls import pages

project_folder = Path(__file__).parent.parent

headers = {
    "User-Agent": "Mozilla/5.0"
}

for page_name, page_info in pages.items():

    print(f"\nScraping: {page_name}")

    response = requests.get(page_info["url"], headers=headers)

    print("Status:", response.status_code)

    # ==========================
    # Federal Register
    # ==========================
    if page_info["type"] == "federal_register":

        data = response.json()

        article_url = data["raw_text_url"]

        article_response = requests.get(article_url, headers=headers)

        text = article_response.text

    # ==========================
    # Normal HTML pages
    # ==========================
    elif page_info["type"] == "html":

        soup = BeautifulSoup(response.text, "html.parser")

        main = soup.find("main")

        if main:
            text = main.get_text(separator="\n")
        else:
            text = soup.get_text(separator="\n")

    else:
        print(f"Unknown type: {page_info['type']}")
        continue

    # Clean text
    clean_text = "\n".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )

    # Output directory
    output_dir = (
        project_folder
        / "knowledge_base"
        / page_info["folder"]
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{page_name}.md"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(clean_text)

    print(f"Saved -> {output_file.name}")