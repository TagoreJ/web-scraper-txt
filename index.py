from flask import Flask, render_template, request, send_file
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

def scrape_website(url):
    """Extracts text from a given website URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract paragraphs
        text = "\n".join([p.get_text() for p in soup.find_all("p")])
        return text if text else "No text found on this page."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    """Main page to input URL and display results."""
    extracted_text = None
    url = ""

    if request.method == "POST":
        url = request.form.get("url")
        extracted_text = scrape_website(url)

        # Save text to a file
        with open("scraped_text.txt", "w", encoding="utf-8") as file:
            file.write(extracted_text)

    return render_template("index.html", extracted_text=extracted_text, url=url)

@app.route("/download")
def download():
    """Allows users to download extracted text as a .txt file."""
    file_path = "scraped_text.txt"
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "No file available to download."

# Required for Vercel
def handler(event, context):
    return app(event, context)

if __name__ == "__main__":
    app.run(debug=True)
