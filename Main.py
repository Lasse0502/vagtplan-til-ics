#Importer nødvendige biblioteker
from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
from ics import Calendar, Event
from setup import setup
import config

periode = setup()


#Fjerner mellemrum fra starten og slutningen, derefter opdeler dataen baseret på given variable (standard variable = mellemrum)
def strip_split(data, split_var = " "):
    strip_data = data.strip()
    split_data = strip_data.split(split_var)
    return split_data

#Funktion til at scrape hjemmesidens table og derefter returnere vagterne i en dictionary
def scrape_vagter(page, table_selector):
    captured_rows = set()
    total_height = 0
    distance = 400
    
    #Dictionary til at opbevare vagter
    vagter = {
            "vagt_id":[],
            "start_tid":[],
            "slut_tid":[],
        }

    count = 1
    #Angiver variablen total height (længde der er scrollet) og fortæller der skal scrolles med distancen xx pr gang
    total_height = 0 
    distance = 400
    #Scroll funktion skrevet i javascript til scroll gennem tabel. Stopper automatisk når den rammer bunden. Henter loadet html (tabel med lazyload)
    while total_height < page.evaluate(f"document.querySelector('{table_selector}').scrollHeight - document.querySelector('{table_selector}').clientHeight"):
        page.evaluate(f"document.querySelector('{table_selector}').scrollBy(0, {distance})")
        total_height += distance
        #Henter det loadet html og kører det gennem BeatifulSoup til at parse dataen til en mere brugbar form
        current_html = page.inner_html(table_selector)
        soup = BeautifulSoup(current_html, 'html.parser')

        #Finder alle rows der har et id der matcher regex i dette tilfælde alle rows med et id der indeholder "arbejdstid"
        rows = soup.find_all(id=re.compile('\d_arbejdstid'))

        #For hver row der er fundet i den loadede html, så tjekker vi om den er blevet captured før. Hvis ikke så henter vi dataen og gemmer det i dictionaryen
        for row in rows:
            row_id = row.get('id')
            if row_id not in captured_rows:
                #Henter texten fra row for at se om der er en vagt, hvis den er tom kan den springes over
                row_text = row.get_text()
                #Omvendt if statement til at tjekke om der er en vagt i row_text og kun behandle den hvis der er en vagt
                if row_text != "":
                    #Splitter rækkens id og gemmer rækkens nummer så den kan bruges til at matche med datoen
                    row_number = row_id.split('_')[0]
                    #Finder rækkens dato ud fra kendte række nummer og viden om datoens id
                    row_2 = soup.find(id=row_number + "_dato")
                    dato_raw = row_2.get_text()
                    #Fjerner mellemrum og splitter datoen vha. tidligere defineret funktion og gemmer kun datoen ikke ugedagen
                    dato = strip_split(dato_raw)[-1]
                    #Ændre datoen til korrekt format (dd.mm) fra (dd/mm)
                    dato = dato.replace("/",".")
                    #Fjerner igen mellemrum og splitter vagt texten og gemmer start og slut tid
                    starttid = strip_split(row_text)[0]
                    sluttid = strip_split(row_text)[-1]
                    #Omskriver start og slut tid til ønsket format
                    start_tid = dato + " " + starttid
                    slut_tid = dato + " " + sluttid
                    #Tilføjer data til dictionary
                    vagter["start_tid"].append(start_tid)
                    vagter["slut_tid"].append(slut_tid)
                    vagter["vagt_id"].append(count)
                    count += 1
                #Tilføjer rækkens id til listen over rækker der allerede er blevet behandlet så den samme række ikke bruges 2 gange
                captured_rows.add(row_id)
    return vagter

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:5500")
    
    # Log in steps
    page.click("[id=username]")
    page.fill("[id=username]", config.user_brugernavn)
    page.press("[id=username]", "Tab")
    page.get_by_placeholder("Password").fill(config.user_adgangskode)
    page.get_by_placeholder("Password").press("Enter")
    # Navigere til vagtplan og vælg ønsket periode
    page.get_by_text("Vagtplan").click()
    page.select_option("[id=period]", value="next")
    page.wait_for_timeout(2000)
    #page.select_option("#period", value="next")

   # page.get_by_text("Næste periode",exact=False).click()
    #page.get_by_text(periode).click()
    #page.wait_for_timeout(1000)

   

    #print(page.content())
 # Scroll and capture the specific table using Python equivalent to your JavaScript approach

    table_selector = ".table-wrapper"
    iframe = page.frame("vagtplan_tabel")
    #print(iframe.content())
    vagter = scrape_vagter(iframe, table_selector)

    context.close()
    browser.close()


today = datetime.today()
current_year = today.year
current_month = today.month

def determine_year(month_day, current_year, current_month):
    shift_month = int(month_day.split('.')[1])
    # Check if the current month is greater than 6 and the shift month is at least 4 months lower than the current month
    if current_month > 6 and (current_month - shift_month) > 4:
        return current_year + 1
    elif current_month < 6 and (current_month - shift_month) < -4:
        return current_year - 1
    else:
        return current_year
    
def create_datetime(month_day, time, current_year, current_month):
    year = determine_year(month_day, current_year, current_month)
    return pd.to_datetime(f'{month_day}.{year} {time}', format='%d.%m.%Y %H:%M')    


vagter_df = pd.DataFrame(vagter)

vagter_df["start_tid"] = vagter_df.apply(lambda row: create_datetime(row["start_tid"][:5],row["start_tid"][6:],current_year,current_month),axis =1)
vagter_df["slut_tid"] = vagter_df.apply(lambda row: create_datetime(row["slut_tid"][:5],row["slut_tid"][6:],current_year,current_month),axis =1)

#print(vagter_df)

# Function to ensure datetime is naive
def make_naive(dt):
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt

cal = Calendar()
evt = Event()
for index, row in vagter_df.iterrows():
    evt = Event()
    if row["start_tid"].month > current_month or (current_month - row["start_tid"].month) > 4:
        evt.name = "Vagt"
        evt.begin = row['start_tid']
        evt.end = row['slut_tid']
        cal.events.add(evt)
    else: continue

with open('vagtplan.ics', 'w') as f:
    f.writelines(cal.serialize_iter())


with open('vagtplan.ics', 'r') as f:
    ics_data = f.read()

# Replace timezone information with empty string
ics_data = ics_data.replace('Z', '')

# Write modified data back to file
with open('vagtplan.ics', 'w') as f:
    f.write(ics_data)

print("Succesfuldt exporteret vagter")