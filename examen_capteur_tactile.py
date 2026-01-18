import RPi.GPIO as GPIO
import time
from RPLCD.i2c import CharLCD

# =============================
# CONFIGURATION
# =============================

GPIO.setmode(GPIO.BCM)  # Configure les GPIO en mode BCM (numérotation des broches physiques)

PIN_TACTILE = 17  # Broche GPIO17 utilisée pour le capteur tactile
GPIO.setup(PIN_TACTILE, GPIO.IN)  # Configure la broche en entrée (lecture du capteur)

lcd = CharLCD(
    i2c_expander='PCF8574',  
    address=0x27,            
    port=1,                  
    cols=16,                 
    rows=2                   
)

lcd.clear()                    
lcd.write_string("En attente...")  

etat_precedent = 0  # État précédent du capteur (0 = relâché, 1 = pressé)

# =============================
# BOUCLE PRINCIPALE
# =============================

while True:
    etat = GPIO.input(PIN_TACTILE)  

    # Nouveau toucher (détection d'arête montante)
    if etat == 1 and etat_precedent == 0:
        lcd.clear()                    
        lcd.write_string("Touche detecte")  
        lcd.crlf()                     # Saut de ligne
        lcd.write_string("Bienvenue !")    
        time.sleep(0.15)               

    # Relâchement du capteur
    elif etat == 0 and etat_precedent == 1:
        lcd.clear()                    
        lcd.write_string("En attente...")  
        time.sleep(0.15)               

    etat_precedent = etat  
    time.sleep(0.05)