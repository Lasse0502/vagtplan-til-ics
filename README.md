# vagtplan-til-ics

**Dette Python-script henter vagtplaner fra en hjemmeside og konverterer dem til en kalenderfil (.ics), som kan importeres til f.eks. Google Calendar.**

Det er vigtigt at bemærke at hjemmesiden der tages udgangspunkt i for dette projekt er en mockup hjemmeside lavet i samarbejde med AI. Mockup hjemmesiden indholder en login side, et dashboard og en vagtplan side med en tabel i et iframe. Dataen omkring vagtplanen hentes altså fra tabellen i iframet og databehandles så det bliver omdannet til en .ics fil. Scriptet er ikke i stand til at automatisk tilpasse sig selv til forskellige hjemmesider, men fungere i stedet baseret på en masse ids og classes aflæst fra hjemmesidens html kode. 

## Installation
For at køre scriptet på egen computer med samme mockup hjemmeside, skal der hostes en localserver som scriptet kan tilgå (i scriptet tages der udgangspunkt i følgende addresse http://localhost:5500), derudover skal din python have adgang til bibliotekerne i requirements.txt filen. Det kan anbefales at kører en virtual enviroment der opfylder kravene i requirements.txt og mit tilfælde har jeg brugt python 3.10.7.

## Showcase af funktioner
Det som scriptet kan er at hente vagter fra en tabel som denne og konverter dem til en ics fil der kan indlæses i en kalender som google calender. Se nedenstående billede.
![Funktion](https://github.com/user-attachments/assets/8277c4b3-24da-412d-b583-a623a4823790)

Her ses hvordan python scriptet fungerer og processen fra hjemmeside til indlæsning af kalender fil i google kalender.

https://github.com/user-attachments/assets/a02817c6-7a0b-4f1d-bca4-d30df9e1efc7

### Ekstra billeder af hjemmeside og kalender med vagterne
![Mockup hjemmeside](https://github.com/user-attachments/assets/829f0c46-68fd-48c0-a48f-75d323edb929)

![Kalender](https://github.com/user-attachments/assets/1e08c960-12b5-4be9-9b81-516d1512694c)

