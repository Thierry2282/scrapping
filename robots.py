import os
import requests
from bs4 import BeautifulSoup
import json
import logging
from urllib.parse import urljoin, urlparse

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class WebScraper:
    def __init__(self, start_url):
        self.start_url = start_url
        self.visited_urls = set()
        self.data = []

        self.image_dir = "images"
        os.makedirs(self.image_dir, exist_ok=True)

        logging.info(f"Initialisation du WebScraper pour {self.start_url}")

    def download_image(self, img_url):
        try:
            response = requests.get(img_url, timeout=10)
            response.raise_for_status()

            img_name = os.path.basename(urlparse(img_url).path)
            if not img_name:
                img_name = "image.jpg"

            img_path = os.path.join(self.image_dir, img_name)

            # éviter les doublons
            base, ext = os.path.splitext(img_path)
            counter = 1
            while os.path.exists(img_path):
                img_path = f"{base}_{counter}{ext}"
                counter += 1

            with open(img_path, 'wb') as f:
                f.write(response.content)

            logging.info(f"Image téléchargée: {img_path}")
            return img_path
        except Exception as e:
            logging.warning(f"Échec du téléchargement de l'image {img_url} : {e}")
            return None

    def scrape(self, url, level=1):
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)

        logging.info(f"Scraping: {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.warning(f"Erreur lors de la requête vers {url} : {e}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraction des données
        images = [urljoin(url, img['src']) for img in soup.find_all('img') if img.get('src')]
        downloaded_images = []

        for img_url in images:
            local_path = self.download_image(img_url)
            if local_path:
                downloaded_images.append(local_path)

        page_data = {
            'url': url,
            'title': soup.title.string.strip() if soup.title else None,
            'paragraphs': [p.get_text(strip=True) for p in soup.find_all('p')],
            'images': downloaded_images
        }

        self.data.append(page_data)

        # Scraping récursif (niveau 2 uniquement)
        if level < 2:
            links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
            domain = urlparse(self.start_url).netloc
            internal_links = [link for link in links if urlparse(link).netloc == domain]

            logging.info(f"Démarrage du niveau {level + 1} de scraping ({len(internal_links)} URLs)")
            for link in internal_links:
                self.scrape(link, level=level + 1)

    def export_to_json(self, filename='scraped_data.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        logging.info(f"Données exportées vers {filename}")


# Exécution principale
if __name__ == '__main__':
    scraper = WebScraper('https://www.example.com/')
    scraper.scrape(scraper.start_url)
    scraper.export_to_json()
