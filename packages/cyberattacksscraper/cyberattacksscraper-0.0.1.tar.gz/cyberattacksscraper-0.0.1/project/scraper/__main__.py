import project
from .scraper import Scraper

URL= "https://microsites-live-backend.cfr.org/cyber-operations"
scraper=Scraper()
scraper.get_links('//div[@class="field-content cst-issue views-field-title "]')
scraper.get_csv_from_dict(dict_attacks)

