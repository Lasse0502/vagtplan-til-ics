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
