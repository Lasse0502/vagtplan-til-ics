# Importer nødvendige biblioteker
from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
from ics import Calendar, Event
from setup import setup
import config

periode = setup()


# Fjerner mellemrum fra starten og slutningen, derefter opdeler dataen baseret på given variable (standard variable = mellemrum)
def strip_split(data, split_var = " "):
    strip_data = data.strip()
    split_data = strip_data.split(split_var)
    return split_data

# Funktion til at scrape hjemmesidens table og derefter returnere vagterne i en dictionary
def scrape_vagter(page, table_selector):
    captured_rows = set()
    
    # Dictionary til at opbevare vagter
    vagter = {
            "vagt_id":[],
            "start_tid":[],
            "slut_tid":[],
        }

    count = 1
    # Angiver variablen scrolled height (længde der er scrollet) og fortæller der skal scrolles med distancen xx pr gang
    scrolled_height = 0 
    distance = 400
   
    # Mens længden der er scrolled er mindre end forskellen mellem scrollhøjden og clienthøjden scrolles og hentes dataen fra tabelen med lazyload
    while scrolled_height < page.evaluate(f"document.querySelector('{table_selector}').scrollHeight - document.querySelector('{table_selector}').clientHeight"):
        # Henter det loadet html og kører det gennem BeatifulSoup til at parse dataen til en mere brugbar form
        current_html = page.inner_html(table_selector)
        soup = BeautifulSoup(current_html, 'html.parser')
        # Scroller med den defineret længde og tilføjer længde til scrolled højde
        page.evaluate(f"document.querySelector('{table_selector}').scrollBy(0, {distance})")
        scrolled_height += distance

        # Finder alle rows der har et id der matcher regex i dette tilfælde alle rows med et id der indeholder "arbejdstid"
        rows = soup.find_all(id=re.compile('\d_arbejdstid'))

        # For hver row der er fundet i den loadede html, så tjekker vi om den er blevet captured før. Hvis ikke så henter vi dataen og gemmer det i dictionaryen
        for row in rows:
            row_id = row.get('id')
            if row_id not in captured_rows:
                # Henter texten fra row for at se om der er en vagt, hvis den er tom kan den springes over
                row_text = row.get_text()
                # Omvendt if statement til at tjekke om der er en vagt i row_text og kun behandle den hvis der er en vagt
                if row_text != "":
                    # Splitter rækkens id og gemmer rækkens nummer så den kan bruges til at matche med datoen
                    row_number = row_id.split('_')[0]
                    # Finder rækkens dato ud fra kendte række nummer og viden om datoens id
                    row_2 = soup.find(id=row_number + "_dato")
                    dato_raw = row_2.get_text()
                    # Fjerner mellemrum og splitter datoen vha. tidligere defineret funktion og gemmer kun datoen ikke ugedagen
                    dato = strip_split(dato_raw)[-1]
                    # Ændre datoen til korrekt format (dd.mm) fra (dd/mm)
                    dato = dato.replace("/",".")
                    # Fjerner igen mellemrum og splitter vagt texten og gemmer start og slut tid
                    starttid = strip_split(row_text)[0]
                    sluttid = strip_split(row_text)[-1]
                    # Omskriver start og slut tid til ønsket format
                    start_tid = dato + " " + starttid
                    slut_tid = dato + " " + sluttid
                    # Tilføjer data til dictionary
                    vagter["start_tid"].append(start_tid)
                    vagter["slut_tid"].append(slut_tid)
                    vagter["vagt_id"].append(count)
                    count += 1
                # Tilføjer rækkens id til listen over rækker der allerede er blevet behandlet så den samme række ikke bruges 2 gange
                captured_rows.add(row_id)
    return vagter

# Åbner browser vha playwright og går til localhost (mockup hjemmesiden)
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
    # Navigere til vagtplan og vælger ønsket periode
    page.get_by_text("Vagtplan").click()
    page.select_option("[id=period]", value=periode)
    # Venter i 2 sekund for at se det er korrekt
    page.wait_for_timeout(2000)

 # Scroll and capture the specific table using Python equivalent to your JavaScript approach

    # Definerer selectors for tabel og henter dataen fra iframe
    table_selector = ".table-wrapper"
    iframe = page.frame("vagtplan_tabel")
    # Tabel selectoren og dataen fra iframe bruges i funktionen scrape_vagter til at scrape vagter til et dictionary med 
    # starttid, sluttid og et vagt id 
    vagter = scrape_vagter(iframe, table_selector)

    context.close()
    browser.close()

# Henter dagens dato og definerer nuværende måned og år
today = datetime.today()
current_year = today.year
current_month = today.month

# Funktion til at bestemme korrekte år for vagtplanen ud fra antagelse om at vagtplanen er maks 4 måneder lang
def determine_year(month_day, current_year, current_month):
    shift_month = int(month_day.split('.')[1])
    # Tjekker om den nuværende måned er efter den 6. måned og vagtens måned er mindst 4 måneder lavere end nuværende måned
    # Hvis dette er tilfælde antages der at vagten ligger i næste år
    if current_month > 6 and (current_month - shift_month) > 4:
        return current_year + 1
    # Tjekker om den nuværende måned er før den 6. måned og vagtens måned er mindst 4 måneder større end nuværende måned
    # Hvis dette er tilfælde antages der at vagten ligger i forrige år
    elif current_month < 6 and (current_month - shift_month) < -4:
        return current_year - 1
    else:
        return current_year

# Funktion til at lave vagter om til panda datetime element og tilføjer korrekt år    
def create_datetime(month_day, time, current_year, current_month):
    year = determine_year(month_day, current_year, current_month)
    return pd.to_datetime(f'{month_day}.{year} {time}', format='%d.%m.%Y %H:%M')    

# Laver panda dataframe kaldet vagter der indeholder alle vagter
vagter_df = pd.DataFrame(vagter)

# Tager hver enkelt vagt i dataframet med vagter og kører dem genem funktionen til at lave dem om til panda datetime elementer
vagter_df["start_tid"] = vagter_df.apply(lambda row: create_datetime(row["start_tid"][:5],row["start_tid"][6:],current_year,current_month),axis =1)
vagter_df["slut_tid"] = vagter_df.apply(lambda row: create_datetime(row["slut_tid"][:5],row["slut_tid"][6:],current_year,current_month),axis =1)

# Tilføjer hver vagt som et begivenhed i en kalender
cal = Calendar()
evt = Event()
for index, row in vagter_df.iterrows():
    evt = Event()
    if row["start_tid"].month > current_month-1 or (current_month - row["start_tid"].month) > 4:
        evt.name = "Vagt"
        evt.begin = row['start_tid']
        evt.end = row['slut_tid']
        cal.events.add(evt)
    else: continue

# Skriver kalenderen ind i en fil kaldet vagtplan.ics
with open('vagtplan.ics', 'w') as f:
    f.writelines(cal.serialize_iter())

# Da python ics biblotektet automatisk tilføjer tidszone information læses filen ind igen og tidszone informationen slettes
with open('vagtplan.ics', 'r') as f:
    ics_data = f.read()
ics_data = ics_data.replace('Z', '')

# Overskriver ics filen med det modificeret data uden tidszone
with open('vagtplan.ics', 'w') as f:
    f.write(ics_data)

print("Succesfuldt exporteret vagter")