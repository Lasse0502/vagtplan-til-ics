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
    #Scroll funktion skrevet i javascript til scroll gennem tabel. Stopper automatisk når den rammer bunden. Henter html fra 
    while total_height < page.evaluate(f"document.querySelectorAll('{table_selector}')[1].scrollHeight - document.querySelectorAll('{table_selector}')[1].clientHeight"):
        page.evaluate(f"document.querySelectorAll('{table_selector}')[1].scrollBy(0, {distance})")
        total_height += distance
        current_html = page.inner_html('#grid-wrapper')
        soup = BeautifulSoup(current_html, 'html.parser')

            # Extract rows and add only new rows
        rows = soup.find_all(id=re.compile('\d_scheduleshift'))

        #print(rows)
        for row in rows:
            #print(row)
            row_id = row.get('id')
            #print(row_str)
            if row_id not in captured_rows:
                row_title = row.get('title')
                if row_title != "":
                    #print(row.get('title'))
                    row_number = row_id.split('_')[0]
                    #print(row_number + "_date")
                    row_2 = soup.find(id=row_number + "_date")
                    dato_raw = row_2.get('title')
                    dato = strip_split(dato_raw)[-1]
                    dato = dato.replace("/",".")
                    starttid = strip_split(row_title)[0]
                    sluttid = strip_split(row_title)[-1]
                    
                    start_tid = dato + " " + starttid
                    slut_tid = dato + " " + sluttid

                    #Append data
                    vagter["start_tid"].append(start_tid)
                    vagter["slut_tid"].append(slut_tid)
                    vagter["vagt_id"].append(count)
                    count += 1
                    #count += 1
                #print(row_title != "")
                captured_rows.add(row_id)
                #html_content.append(row)
    #print(vagter)
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
    
    page.locator("[id=\"\\31 01\"]").click()
    page.get_by_text("Nuværende lønperiode").click()
    page.get_by_text(periode).click()
    #page.wait_for_timeout(1000)

    # Wait for the spinner to disappear, indicating the table has fully loaded
    spinner_selector = "#spinnerCircles"
    page.wait_for_selector(spinner_selector, state="hidden")  # Wait until the spinner is detached (gone)


 # Scroll and capture the specific table using Python equivalent to your JavaScript approach
    table_selector = ".ui-grid-viewport"
    table_selector = "#grid-wrapper"
    vagter = scrape_vagter(page, table_selector, html_selector)

    context.close()
    browser.close()
