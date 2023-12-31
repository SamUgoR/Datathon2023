import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from matplotlib import pyplot as plt
import re

# Function to extract the meaningful part from the URL
def extract_meaningful_part(url):
    # Extract the meaningful part of the URL
    parsed_url = urlparse(url)
    path = parsed_url.path
    if path.endswith('/'):
        path = path[:-1]
    return path.split('/')[-1].replace('-', ' ')

# Function to extract and organize data from a single URL
def extract_and_organize_data_from_url(url):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    frames = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'iframe')))
    iframe_urls = [frame.get_attribute('src') for frame in frames]  # Define iframe_urls here
    all_data = []
    current_year = 2022  # Initialize with the most recent year you expect to find

    for iframe_url in iframe_urls:
        driver.get(iframe_url)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'igc-table')))
        table = driver.find_element(By.CLASS_NAME, 'igc-table')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        # The first row contains headers, which we will skip
        for row in rows[1:]:  # Starting from the second row
            cells = row.find_elements(By.TAG_NAME, 'td')
            category = cells[0].text.replace('\n', ' ').strip()
            value = cells[1].text.replace('\n', ' ').strip()

            # Check if we already have this category for the current year
            if not any(d['Category'] == category and d['Year'] == current_year for d in all_data):
                all_data.append({
                    'Organization': extract_meaningful_part(url),
                    'Category': category,
                    'Year': current_year,
                    'Value': value
                })
            else:  # If we do, it means we've moved to the previous year
                current_year -= 1
                all_data.append({
                    'Organization': extract_meaningful_part(url),
                    'Category': category,
                    'Year': current_year,
                    'Value': value
                })

    # Reset the year for the next URL
    current_year = 2022

    return all_data

# Setup the Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# List of URLs to process
urls = ['https://2050today.org/cagi-international-geneva-welcome-center/', 'https://2050today.org/cagi-international-geneva-welcome-center/', 'https://2050today.org/ccig-chambre-de-commerce-dindustrie-et-des-services-de-geneve/', 'https://2050today.org/ccig-chambre-de-commerce-dindustrie-et-des-services-de-geneve/', 'https://2050today.org/cern-european-organization-for-nuclear-research/', 'https://2050today.org/cern-european-organization-for-nuclear-research/', 'https://2050today.org/diplomatic-club-of-geneva/', 'https://2050today.org/diplomatic-club-of-geneva/', 'https://2050today.org/dndi-drugs-for-neglected-diseases-initiative/', 'https://2050today.org/dndi-drugs-for-neglected-diseases-initiative/', 'https://2050today.org/ebu-european-broadcasting-union/', 'https://2050today.org/ebu-european-broadcasting-union/', 'https://2050today.org/egpaf-elisabeth-glaser-pediatric-aids-foundation-geneva-office/', 'https://2050today.org/egpaf-elisabeth-glaser-pediatric-aids-foundation-geneva-office/', 'https://2050today.org/epfl-swiss-federal-institute-of-technology-in-lausanne-2/', 'https://2050today.org/epfl-swiss-federal-institute-of-technology-in-lausanne-2/', 'https://2050today.org/fipoi-foundation-for-buildings-for-international-organisations/', 'https://2050today.org/fipoi-foundation-for-buildings-for-international-organisations/', 'https://2050today.org/fondation-pour-geneve/', 'https://2050today.org/fondation-pour-geneve/', 'https://2050today.org/geneva-call/', 'https://2050today.org/geneva-call/', 'https://2050today.org/gichd-geneva-international-centre-for-humanitarian-demining/', 'https://2050today.org/gichd-geneva-international-centre-for-humanitarian-demining/', 'https://2050today.org/graduate-institute-geneva/', 'https://2050today.org/graduate-institute-geneva/', 'https://2050today.org/hes-so-geneva/', 'https://2050today.org/hes-so-geneva/', 'https://2050today.org/icva-international-council-of-voluntary-agencies/', 'https://2050today.org/icva-international-council-of-voluntary-agencies/', 'https://2050today.org/ilo-international-labour-organization/', 'https://2050today.org/ilo-international-labour-organization/', 'https://2050today.org/ioc-the-international-olympic-committee/', 'https://2050today.org/ioc-the-international-olympic-committee/', 'https://2050today.org/ishr-international-service-for-human-rights/', 'https://2050today.org/ishr-international-service-for-human-rights/', 'https://2050today.org/iso-international-organization-for-standardization/', 'https://2050today.org/iso-international-organization-for-standardization/', 'https://2050today.org/itu-international-telecommunication-union/', 'https://2050today.org/itu-international-telecommunication-union/', 'https://2050today.org/kofi-annan-foundation/', 'https://2050today.org/kofi-annan-foundation/', 'https://2050today.org/permanent-mission-of-the-principality-of-andorra/', 'https://2050today.org/permanent-mission-of-the-principality-of-andorra/', 'https://2050today.org/permanent-mission-of-barbados/', 'https://2050today.org/permanent-mission-of-barbados/', 'https://2050today.org/permanent-mission-of-brazil/', 'https://2050today.org/permanent-mission-of-brazil/', 'https://2050today.org/permanent-mission-of-chile/', 'https://2050today.org/permanent-mission-of-chile/', 'https://2050today.org/permanent-mission-of-the-republic-of-costa-rica/', 'https://2050today.org/permanent-mission-of-the-republic-of-costa-rica/', 'https://2050today.org/permanent-mission-of-denmark/', 'https://2050today.org/permanent-mission-of-denmark/', 'https://2050today.org/permanent-mission-of-the-arab-republic-of-egypt/', 'https://2050today.org/permanent-mission-of-the-arab-republic-of-egypt/', 'https://2050today.org/permanent-mission-of-the-fiji-republic/', 'https://2050today.org/permanent-mission-of-the-fiji-republic/', 'https://2050today.org/permanent-mission-of-finland/', 'https://2050today.org/permanent-mission-of-finland/', 'https://2050today.org/permanent-mission-of-france/', 'https://2050today.org/permanent-mission-of-france/', 'https://2050today.org/permanent-mission-of-the-federal-republic-of-germany/', 'https://2050today.org/permanent-mission-of-the-federal-republic-of-germany/', 'https://2050today.org/permanent-mission-of-india/', 'https://2050today.org/permanent-mission-of-india/', 'https://2050today.org/permanent-mission-of-ireland/', 'https://2050today.org/permanent-mission-of-ireland/', 'https://2050today.org/permanent-mission-of-israel/', 'https://2050today.org/permanent-mission-of-israel/', 'https://2050today.org/permanent-mission-of-italy/', 'https://2050today.org/permanent-mission-of-italy/', 'https://2050today.org/permanent-mission-of-the-republic-of-mauritius/', 'https://2050today.org/permanent-mission-of-the-republic-of-mauritius/', 'https://2050today.org/permanent-mission-of-mexico/', 'https://2050today.org/permanent-mission-of-mexico/', 'https://2050today.org/permanent-mission-of-the-principality-of-monaco/', 'https://2050today.org/permanent-mission-of-the-principality-of-monaco/', 'https://2050today.org/permanent-mission-of-the-kingdom-of-morocco/', 'https://2050today.org/permanent-mission-of-the-kingdom-of-morocco/', 'https://2050today.org/permanent-mission-of-the-republic-of-mozambique/', 'https://2050today.org/permanent-mission-of-the-republic-of-mozambique/', 'https://2050today.org/permanent-mission-of-norway/', 'https://2050today.org/permanent-mission-of-norway/', 'https://2050today.org/permanent-mission-of-portugal/', 'https://2050today.org/permanent-mission-of-portugal/', 'https://2050today.org/permanent-mission-of-the-republic-of-rwanda/', 'https://2050today.org/permanent-mission-of-the-republic-of-rwanda/', 'https://2050today.org/permanent-mission-of-the-republic-of-senegal/', 'https://2050today.org/permanent-mission-of-the-republic-of-senegal/', 'https://2050today.org/permanent-mission-of-the-republic-of-slovenia/', 'https://2050today.org/permanent-mission-of-the-republic-of-slovenia/', 'https://2050today.org/permanent-mission-of-spain/', 'https://2050today.org/permanent-mission-of-spain/', 'https://2050today.org/permanent-mission-of-norway-2/', 'https://2050today.org/permanent-mission-of-norway-2/', 'https://2050today.org/permanent-mission-of-switzerland/', 'https://2050today.org/permanent-mission-of-switzerland/', 'https://2050today.org/permanent-mission-of-tunisia/', 'https://2050today.org/permanent-mission-of-tunisia/', 'https://2050today.org/permanent-mission-of-the-united-kingdom-of-great-britain-and-nothern-ireland/', 'https://2050today.org/permanent-mission-of-the-united-kingdom-of-great-britain-and-nothern-ireland/', 'https://2050today.org/united-states-of-america/', 'https://2050today.org/united-states-of-america/', 'https://2050today.org/permanent-delegation-of-the-european-union/', 'https://2050today.org/permanent-delegation-of-the-european-union/', 'https://2050today.org/nrc-norwegian-refugee-council-geneva-office-idmc-internal-displacement-monitoring-centre/', 'https://2050today.org/nrc-norwegian-refugee-council-geneva-office-idmc-internal-displacement-monitoring-centre/', 'https://2050today.org/open-geneva/', 'https://2050today.org/open-geneva/', 'https://2050today.org/path-foundation-for-appropriate-technologies-in-health/', 'https://2050today.org/path-foundation-for-appropriate-technologies-in-health/', 'https://2050today.org/unaids/', 'https://2050today.org/unaids/', 'https://2050today.org/office-of-the-united-nations-in-geneva/', 'https://2050today.org/office-of-the-united-nations-in-geneva/', 'https://2050today.org/undp-office-in-geneva-united-nations-development-programme-2/', 'https://2050today.org/undp-office-in-geneva-united-nations-development-programme-2/', 'https://2050today.org/united-nations-environment-programme-geneva-office/', 'https://2050today.org/united-nations-environment-programme-geneva-office/', 'https://2050today.org/unhcr-the-un-refugee-agency/', 'https://2050today.org/unhcr-the-un-refugee-agency/', 'https://2050today.org/un-human-rights-office-of-the-high-commissioner-for-human-rights/', 'https://2050today.org/un-human-rights-office-of-the-high-commissioner-for-human-rights/', 'https://2050today.org/unige-university-of-geneva/', 'https://2050today.org/unige-university-of-geneva/', 'https://2050today.org/upov-international-union-for-the-protection-of-new-varieties-of-plants/', 'https://2050today.org/upov-international-union-for-the-protection-of-new-varieties-of-plants/', 'https://2050today.org/wcc-world-council-of-churches/', 'https://2050today.org/wcc-world-council-of-churches/', 'https://2050today.org/who-world-health-organization/', 'https://2050today.org/who-world-health-organization/', 'https://2050today.org/world-intellectual-property-organization/', 'https://2050today.org/world-intellectual-property-organization/', 'https://2050today.org/wmo-world-meteorological-organization/', 'https://2050today.org/wmo-world-meteorological-organization/']
urls = list(set(urls))
# CSV file setup
csv_filename = "organized_table_data.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['Organization', 'Category', 'Year', 'Value']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # Process each URL
    for url in urls:
        print(f'Processing: {str(extract_meaningful_part(url))}')
        try:
            organized_data = extract_and_organize_data_from_url(url)
            for data in organized_data:
                writer.writerow(data)
        except Exception as e:
            print(f'An error occurred while processing {str(extract_meaningful_part(url))}: {e}')

# Close the driver
driver.quit()

print(f"Data extracted and organized in {csv_filename}")
