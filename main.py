import requests
from bs4 import BeautifulSoup


def scrape_details_page(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    peak_name = soup.find('h1').text
    elevation = soup.find('h2').text
    print(peak_name)
    print(elevation)
    main_info_tables = soup.find_all('table', {'class': 'gray'})

    table_left = main_info_tables[0]
    lat_long_section = table_left.find('td', string='Latitude/Longitude (WGS84)').findParent('tr')

    s1 = lat_long_section.find('td').text.strip()
    s2 = extract_content(lat_long_section.find('td').find_next('td'), 0)
    s3 = extract_content(lat_long_section.find('td').find_next('td'), 2)
    s4 = extract_content(lat_long_section.find('td').find_next('td'), 4)

    # Print or use the values as needed
    print(s1)
    print(s2)
    print(s3)
    print(s4)


def extract_content(element, index):
    try:
        return element.contents[index].strip()
    except IndexError:
        return ''


def scrape_los_angeles_0_11000():
    base_url = 'https://www.peakbagger.com/'
    list_url = f'{base_url}List.aspx?lid=-565916'
    response = requests.get(list_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table with the specified heading
        target_table = soup.find('th', string='Peak').find_parent('table')

        # Extract "href" values of all table rows in the target table
        href_values = [row.a['href'] for row in target_table.find_all('tr') if row.a and 'Rank' not in row.text]

        # details_url = f'{base_url}{href_values[0]}'
        # scrape_details_page(details_url)
        for href in href_values:
            details_url = f'{base_url}{href}'
            print(details_url)
            scrape_details_page(details_url)
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")


if __name__ == '__main__':
    scrape_los_angeles_0_11000()


# def scrape_peaks():
#     url = "https://en.wikipedia.org/wiki/List_of_mountains_by_elevation"
#     response = requests.get(url)
#
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         print(soup)
#         mountain_tables = soup.find_all('table', {'class': 'wikitable'})
#
#         for mountain_table in mountain_tables:
#             rows = mountain_table.find_all('tr')
#
#             for row in rows[1:]:  # Skip the header row
#                 columns = row.find_all(['td', 'th'])
#                 mountain_name = columns[1].text.strip()
#                 elevation = columns[2].text.strip()
#                 range_info = columns[3].text.strip()
#
#                 print(f"Mountain: {mountain_name}, Elevation: {elevation}, Range: {range_info}")
#     else:
#         print(f"Failed to retrieve page. Status code: {response.status_code}")