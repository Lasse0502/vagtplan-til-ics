# Importer nødvendige biblioteker
import time
from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
from ics import Calendar, Event
import config
import login

def strip_split(data, split_var = " "):
    strip_data = data.strip()
    split_data = strip_data.split(split_var)
    return split_data

def scrape_vagter(page, table_selector):
    captured_rows = set()
    
    vagter = {
        "vagt_id":[],
        "start_tid":[],
        "slut_tid":[],
    }

    count = 1
    scrolled_height = 0 
    distance = 400
    
    while scrolled_height < page.evaluate(f"document.querySelector('{table_selector}').scrollHeight - document.querySelector('{table_selector}').clientHeight"):
        current_html = page.inner_html(table_selector)
        soup = BeautifulSoup(current_html, 'html.parser')
        page.evaluate(f"document.querySelector('{table_selector}').scrollBy(0, {distance})")
        scrolled_height += distance

        rows = soup.find_all(id=re.compile('\d_arbejdstid'))

        for row in rows:
            row_id = row.get('id')
            if row_id not in captured_rows:
                row_text = row.get_text()
                if row_text != "":
                    row_number = row_id.split('_')[0]
                    row_2 = soup.find(id=row_number + "_dato")
                    dato_raw = row_2.get_text()
                    dato = strip_split(dato_raw)[-1]
                    dato = dato.replace("/",".")
                    starttid = strip_split(row_text)[0]
                    sluttid = strip_split(row_text)[-1]
                    start_tid = dato + " " + starttid
                    slut_tid = dato + " " + sluttid
                    vagter["start_tid"].append(start_tid)
                    vagter["slut_tid"].append(slut_tid)
                    vagter["vagt_id"].append(count)
                    count += 1
                captured_rows.add(row_id)
    return vagter

def determine_year(month_day, current_year, current_month):
    shift_month = int(month_day.split('.')[1])
    if current_month > 6 and (current_month - shift_month) > 4:
        return current_year + 1
    elif current_month < 6 and (current_month - shift_month) < -4:
        return current_year - 1
    else:
        return current_year
    
def create_datetime(month_day, time, current_year, current_month):
    year = determine_year(month_day, current_year, current_month)
    return pd.to_datetime(f'{month_day}.{year} {time}', format='%d.%m.%Y %H:%M')     


def my_main_function(update_callback): # Tilføj update_callback og periode
    """
    Denne funktion udfører web scraping og ICS-filgenerering.
    update_callback er en funktion til at sende statusopdateringer til GUI'en.
    periode er den valgte periode
    """
    periode = config.valgt_vagtplan  # Hent den valgte periode fra konfigurationen

    update_callback("Starter web scraping...")
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True) # Ændret til headless=True
            context = browser.new_context()
            page = context.new_page()
            page.goto("http://localhost:5500")

            # Log ind
            page.click("[id=username]")
            page.fill("[id=username]", login.user_brugernavn)
            page.press("[id=username]", "Tab")
            page.get_by_placeholder("Password").fill(login.user_adgangskode)
            page.get_by_placeholder("Password").press("Enter")

            # Naviger til vagtplan og vælg periode
            page.get_by_text("Vagtplan").click()
            page.select_option("[id=period]", value=periode)
            page.wait_for_timeout(2000)

            # Scrap vagter
            table_selector = ".table-wrapper"
            iframe = page.frame("vagtplan_tabel")
            vagter = scrape_vagter(iframe, table_selector)

            context.close()
            browser.close()

        update_callback("Web scraping fuldført.")

        # Behandl data og generer ICS-fil
        update_callback("Behandler data...")
        # ... (din eksisterende kode til databehandling og ICS-generering)
        #print("Indhold af vagter før DataFrame:")
        #print(vagter)
        vagter_df = pd.DataFrame(vagter)
        # Henter dagens dato og definerer nuværende måned og år
        today = datetime.today()
        current_year = today.year
        current_month = today.month

        vagter_df["start_tid"] = vagter_df.apply(lambda row: create_datetime(row["start_tid"][:5],row["start_tid"][6:],current_year,current_month),axis =1)
        vagter_df["slut_tid"] = vagter_df.apply(lambda row: create_datetime(row["slut_tid"][:5],row["slut_tid"][6:],current_year,current_month),axis =1)


        # Tilføjer hver vagt som et begivenhed i en kalender
        update_callback("Tilføjer vagter til kalender")
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

        update_callback("ICS-fil genereret.")

    except Exception as e:
        update_callback(f"Der opstod en fejl: {e}")
    
    update_callback("Processen er fuldført.")
