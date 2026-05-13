# Denne fil er til aftestning af alt kode sammenlagt - når denne virker efter hensigten, bliver den vores main.py, som skal køre kontinuerligt

import subprocess 
import time 

ssid = 'JABREEZY' 
password = '68e69Q12' 

def do_connect():
    print('Kontrollerer netværksstatus.')
    try:  # Starter en try-blok - hvis noget går galt, hopper Python til except-blokken
        print('Tilslutter til netværk.')
        result = subprocess.run(  # Kører en terminalkommando og gemmer resultatet i 'result'
            ['nmcli', 'd', 'wifi', 'connect', ssid, 'password', password],  # Selve kommandoen: tilslut til WiFi med nmcli
            capture_output=True,  # Fanger det kommandoen udskriver, så vi kan læse det i Python
            text=True,  # Returnerer outputtet som tekst i stedet for rå bytes
            timeout=15  # Giver op efter 15 sekunder hvis der intet sker
        )

        if 'successfully' in result.stdout.lower():  # Tjekker om ordet "successfully" findes i kommandoens output
            print('Tilsluttet til WiFi!')
            ip_result = subprocess.run(  # Kører en ny kommando for at hente Pi'ens IP-adresse
                ['hostname', '-I'],  # Kommandoen der henter IP-adressen
                capture_output=True,  # Fanger outputtet fra kommandoen
                text=True
            )
            print('IP-adresse:', ip_result.stdout)  # Udskriver IP-adressen 
        else:
            print('Kunne ikke tilslutte til WiFi:', result.stderr)  # Udskriver fejlbeskeden fra nmcli hvis tilslutningen fejlede

    except subprocess.TimeoutExpired:  # Fanger den specifikke fejl hvor de 15 sekunder løb ud
        print('Forbindelsen tog for lang tid — prøv igen.')
    except Exception as e:
        print(f"WiFi-fejl '{e}' opstod.")

do_connect()



# ------------------------------------------FORBINDELSE TIL INTERNET ER NU OPRETTET--------------------------------------------------------#