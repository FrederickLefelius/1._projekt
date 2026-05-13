# Denne fil er til aftestning af alt kode sammenlagt - når denne virker efter hensigten, bliver den vores main.py, som skal køre kontinuerligt

import subprocess # Denne er åbenbart yderst nødvendig for raspberry pi ift. f.eks. at komme på nettet,
                  # da det er den class der gør det muligt at bruge Linux systemkommandoer.
import time 

ssid = '' 
password = '' 

def do_connect():
    print('Kontrollerer netværksstatus.')
    try:  # Starter en try-blok - hvis noget går galt, hopper Python til except-blokken
        print('Tilslutter til netværk.')
        connect = subprocess.run(    # Kører de følgende terminalkommando og gemmer resultatet i "connect"
                                     # Denne kommando indtaster de følgende værdier og gemmer resultatet af
                                     # dem i "connect" - på den måde kan "connect" aflæses senere i linje 23.
            ['nmcli', 'd', 'wifi', 'connect', ssid, 'password', password],  # Selve kommandoen: tilslut til WiFi med nmcli.
            capture_output=True,  # Fanger det kommandoen udskriver, så vi kan læse det i Python.
            text=True,  # Returnerer outputtet som tekst i stedet for rå bytes.
            timeout=15  # Giver op efter 15 sekunder hvis der intet sker.
        )
        
        if 'successfully' in connect.stdout.lower(): # Tjekker om ordet "successfully" findes i kommandoens output
                                                    # ".lower" delen omdanner resultatet til små bogstaver, så det
                                                    # kan tjekkes ved at skrive "if 'successfully'".
            print('Tilsluttet til WiFi!')
            ip_result = subprocess.run(  # Kører en ny kommando for at hente Pi'ens IP-adresse.
                ['hostname', '-I'],  # Kommandoen der henter IP-adressen.
                capture_output=True,
                text=True
            )
            print('IP-adresse:', ip_result.stdout)  # Udskriver IP-adressen.
        else:
            print('Kunne ikke tilslutte til WiFi:', connect.stderr)  # Udskriver fejlbeskeden fra nmcli hvis tilslutningen fejlede.

    except subprocess.TimeoutExpired:  # Fanger den specifikke fejl hvor de 15 sekunder løb ud.
        print('Forbindelsen tog for lang tid — prøv igen.')
    except Exception as e:
        print(f"WiFi-fejl '{e}' opstod.")

checkNet = subprocess.run(  # Basically den samme som tidligere, bortset fra at den ikke indstiller noget,
                            # den tjekker kun status på den nuværende forbindelse.
            ['nmcli', '-t', '-f', 'GENERAL.CONNECTION', 'device', 'show'],  # -t (Terse) fjerner ligegyldig info - f.eks. den ekstra linje "STATE".
                                                                            # -f (Field) skriver kun dét, den bedes om - i dette tilfælde, får vi
                                                                            # kun 1 linje per forbundet netærk, som eksemeplvis skriver: 
                                                                            # "GENERAL.CONNECTION:<indtastet ssid>". Dette kan vi bruge til at tjekke
                                                                            # om enheden er forbundet på det ønskede netværk.
            capture_output=True,
            text=True,
            timeout=15
        )
if ssid.lower() in checkNet.stdout.lower(): # Checker om der er forbindelse via den "checkNet" funktionen,
                                         # og udfører "do_connect" hvis der ikke er forbindelse.
    print('Du er allerede forbundet til internettet!')
else:
    print('Du er ikke forbundet til det rigtige netværk, det bliver du nu.')
    do_connect()



# ------------------------------------------FORBINDELSE TIL INTERNET ER NU OPRETTET--------------------------------------------------------#
