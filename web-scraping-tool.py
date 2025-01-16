import requests
import time
import json
import csv
import re
import sys
from bs4 import BeautifulSoup
from pathlib import Path

welcome_message = """

░██╗░░░░░░░██╗███████╗██████╗░  ░██████╗░█████╗░██████╗░░█████╗░██████╗░██╗███╗░░██╗░██████╗░
░██║░░██╗░░██║██╔════╝██╔══██╗  ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║████╗░██║██╔════╝░
░╚██╗████╗██╔╝█████╗░░██████╦╝  ╚█████╗░██║░░╚═╝██████╔╝███████║██████╔╝██║██╔██╗██║██║░░██╗░
░░████╔═████║░██╔══╝░░██╔══██╗  ░╚═══██╗██║░░██╗██╔══██╗██╔══██║██╔═══╝░██║██║╚████║██║░░╚██╗
░░╚██╔╝░╚██╔╝░███████╗██████╦╝  ██████╔╝╚█████╔╝██║░░██║██║░░██║██║░░░░░██║██║░╚███║╚██████╔╝
░░░╚═╝░░░╚═╝░░╚══════╝╚═════╝░  ╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚══╝░╚═════╝░

████████╗░█████╗░░█████╗░██╗░░░░░
╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░
░░░██║░░░██║░░██║██║░░██║██║░░░░░
░░░██║░░░██║░░██║██║░░██║██║░░░░░
░░░██║░░░╚█████╔╝╚█████╔╝███████╗
░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝
By Creepcomp (Parsa Rostamzadeh)
Github: https://github.com/creepcomp
Telegram: https://telegram.me/creepcomp
"""

print(welcome_message)

def scrape(config_file):
    with open(config_file) as file:
        config = json.load(file)
    
    output_file = Path(config_file).stem + ".csv"
    field_names = [field["name"] for field in config["fields"]]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        
        base_url = config["url"]
        page_number = 1
        total_items = 0
        
        while True:
            try:
                current_url = base_url.format(id=page_number)
                response = requests.get(current_url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.select(config["item"])
                
                if items:
                    for item in items:
                        try:
                            total_items += 1
                            scraped_data = {}
                            for field in config["fields"]:
                                if "selector" in field:
                                    if "link" in field:
                                        scraped_data[field["name"]] = item.select_one(field["selector"]).get("href")
                                    else:
                                        scraped_data[field["name"]] = ", ".join(
                                            [element.get_text(strip=True) for element in item.select(field["selector"])]
                                        )
                                    if "pattern" in field:
                                        match = re.search(field["pattern"], scraped_data[field["name"]])
                                        if match:
                                            scraped_data[field["name"]] = match.group(1)
                                elif "autoincrement" in field:
                                    scraped_data[field["name"]] = total_items
                            writer.writerow(scraped_data)
                        except Exception as error:
                            print("An error occurred while processing the request:", error)
                    print(f"[{current_url}] {len(items)} items scraped.")
                    page_number += 1
                    time.sleep(config["delay"])
                else:
                    break
            except Exception as error:
                print("An error occurred while processing the request:", error)
        
        print(f"{total_items} item scraped.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_config.json>")
        sys.exit(1)
    
    config_file_path = sys.argv[1]
    scrape(config_file_path)
