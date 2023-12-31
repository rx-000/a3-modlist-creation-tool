from flask import Flask, render_template, request, send_file
from datetime import datetime
from bs4 import BeautifulSoup
import os


modlists = []

files = [f for f in os.listdir("./modlists") if os.path.isfile(os.path.join("./modlists", f))]

for file in files:
    modlists.append(file)

def empty_mod_list_table(html_file):
    with open(html_file, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    mod_list_div = soup.find('div', class_='mod-list')

    if mod_list_div:
        table = mod_list_div.find('table')
        if table:
            table.clear()

    return soup


def add_mod(soup, display_name, link):
    mod_table = soup.find('div', class_='mod-list').find('table')

    new_row = soup.new_tag('tr', attrs={'data-type': 'ModContainer'})

    display_name_td = soup.new_tag('td', attrs={'data-type': 'DisplayName'})
    display_name_td.string = display_name

    from_source_td = soup.new_tag('td')
    from_source_td.append(soup.new_tag('span', class_='from-steam'))
    from_source_td.find('span').string = 'Steam'

    link_td = soup.new_tag('td')
    link_td.append(soup.new_tag('a', href=link, attrs={'data-type': 'Link'}))
    link_td.find('a')['href'] = link
    link_td.find('a').string = link

    new_row.append(display_name_td)
    new_row.append(from_source_td)
    new_row.append(link_td)

    mod_table.append(new_row)

    return soup


def extract_mods_info(html_file):

    with open(html_file, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    mod_table = soup.find('div', class_='mod-list').find('table')

    mods_dict = {}

    for mod_entry in mod_table.find_all('tr', attrs={'data-type': 'ModContainer'}):
        display_name = mod_entry.find(
            'td', attrs={'data-type': 'DisplayName'}).get_text(strip=True)
        link = mod_entry.find('a')['href']
        mods_dict[display_name] = link

    return mods_dict


def fill_mandatory_mods(soup, modlist):

    mandatory_mods = extract_mods_info(modlist)

    for display_name, link in mandatory_mods.items():
        soup = add_mod(soup, display_name, link)

    return soup


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def download_html():
    mods_dict = extract_mods_info("whitelist.html")
    if request.method == 'POST':

        modlist = f"./modlists/{request.form['action']}"
        
        soup = empty_mod_list_table(modlist)
        soup = fill_mandatory_mods(soup, modlist)

        selected_mods = request.form.getlist('mod')
        
        for display_name in selected_mods:
            link = mods_dict.get(display_name)
            if link:
                soup = add_mod(soup, display_name, link)

        with open('modlist.html', 'w') as file:
            file.write(str(soup))

        filename = f'modlist_{datetime.now().strftime("%Y%m%d%H%M%S")}.html'

        return send_file('modlist.html', as_attachment=True, download_name=filename)
    return render_template('index.html', mods=mods_dict, modlists=modlists)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=False)
