import pygame
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext

#-------------------------------------------------------------------------------
# Name:         TT.py
# Purpose:      Schulprojekt
#
# Author:       Muhammad Ahmad
#
# Created:     06.2024
# Copyright:   (c)  2024
#-------------------------------------------------------------------------------

pygame.init()

# Fenstergröße und Titel
BREITE, HÖHE = 700, 500
FPS = 60  # Bildwiederholrate

# Farben
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)

# Schläger- und Ballgröße
SCHLÄGER_BREITE, SCHLÄGER_HÖHE = 20, 100
BALL_RADIUS = 7

# Schriftarten
PUNKTZAHL_SCHRIFT = pygame.font.SysFont("comicsans", 50)
EINGABE_SCHRIFT = pygame.font.SysFont("comicsans", 30)
#########################################################################################################################################################################################################################################

# Ergänzung
# Dateiname und Liste für Spielhistorie
historie_datei = "spiel_historie.txt"
spiel_historie = [] #Leere Liste

#########################################################################################################################################################################################################################################

# Klasse für Schläger
class Schläger:
    farbe = WEISS
    geschwindigkeit = 5

    def __init__(self, x, y, breite, höhe):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.breite = breite
        self.höhe = höhe
    
    def zeichnen(self, fenster):
        pygame.draw.rect(fenster, self.farbe, (self.x, self.y, self.breite, self.höhe))

    def bewegen(self, hoch=True):
        if hoch:
            self.y -= self.geschwindigkeit
        else:
            self.y += self.geschwindigkeit

    def zurücksetzen(self):
        self.x = self.original_x
        self.y = self.original_y

# Klasse für Ball
class Ball:
    FARBE = WEISS

    def __init__(self, x, y, radius, geschwindigkeit):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.geschwindigkeit = geschwindigkeit
        self.x_geschwindigkeit = self.geschwindigkeit
        self.y_geschwindigkeit = 0
    
    def zeichnen(self, fenster):
        pygame.draw.circle(fenster, self.FARBE, (self.x, self.y), self.radius)

    def bewegen(self):
        self.x += self.x_geschwindigkeit
        self.y += self.y_geschwindigkeit

    def zurücksetzen(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_geschwindigkeit = 0
        self.x_geschwindigkeit = self.geschwindigkeit if self.x_geschwindigkeit < 0 else -self.geschwindigkeit

# Zeichenfunktion für das Spielfeld
def zeichnen(fenster, schläger, ball, linker_punktestand, rechter_punktestand, linker_spieler, rechter_spieler):
    fenster.fill(SCHWARZ)

    linker_punktestand_text = PUNKTZAHL_SCHRIFT.render(f"{linker_punktestand}", 1, WEISS)
    rechter_punktestand_text = PUNKTZAHL_SCHRIFT.render(f"{rechter_punktestand}", 1, WEISS)
    fenster.blit(linker_punktestand_text, (BREITE // 4 - linker_punktestand_text.get_width() // 2, 20))
    fenster.blit(rechter_punktestand_text, (BREITE * 3 // 4 - rechter_punktestand_text.get_width() // 2, 20))

    linker_spieler_text = PUNKTZAHL_SCHRIFT.render(linker_spieler, 1, WEISS)
    rechter_spieler_text = PUNKTZAHL_SCHRIFT.render(rechter_spieler, 1, WEISS)
    fenster.blit(linker_spieler_text, (BREITE // 4 - linker_spieler_text.get_width() // 2, 60))
    fenster.blit(rechter_spieler_text, (BREITE * 3 // 4 - rechter_spieler_text.get_width() // 2, 60))

    for s in schläger:
        s.zeichnen(fenster)

    for i in range(10, HÖHE, HÖHE // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(fenster, WEISS, (BREITE // 2 - 5, i, 10, HÖHE // 20))

    ball.zeichnen(fenster)
    pygame.display.update()

# Kollisionsbehandlung
def kollisionsbehandlung(ball, linker_schläger, rechter_schläger):
    if ball.y + ball.radius >= HÖHE:
        ball.y_geschwindigkeit *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_geschwindigkeit *= -1

    if ball.x_geschwindigkeit < 0:
        if linker_schläger.y <= ball.y <= linker_schläger.y + linker_schläger.höhe:
            if ball.x - ball.radius <= linker_schläger.x + linker_schläger.breite:
                ball.x_geschwindigkeit *= -1

                mitte_y = linker_schläger.y + linker_schläger.höhe / 2
                differenz_in_y = mitte_y - ball.y
                reduktionsfaktor = (linker_schläger.höhe / 2) / ball.geschwindigkeit
                y_geschwindigkeit = differenz_in_y / reduktionsfaktor
                ball.y_geschwindigkeit = -1 * y_geschwindigkeit

    else:
        if rechter_schläger.y <= ball.y <= rechter_schläger.y + rechter_schläger.höhe:
            if ball.x + ball.radius >= rechter_schläger.x:
                ball.x_geschwindigkeit *= -1

                mitte_y = rechter_schläger.y + rechter_schläger.höhe / 2
                differenz_in_y = mitte_y - ball.y
                reduktionsfaktor = (rechter_schläger.höhe / 2) / ball.geschwindigkeit
                y_geschwindigkeit = differenz_in_y / reduktionsfaktor
                ball.y_geschwindigkeit = -1 * y_geschwindigkeit

# Bewegung der Schläger
def schläger_bewegung(tasten, linker_schläger, rechter_schläger):
    if tasten[pygame.K_w] and linker_schläger.y - linker_schläger.geschwindigkeit >= 0:
        linker_schläger.bewegen(hoch=True)
    if tasten[pygame.K_s] and linker_schläger.y + linker_schläger.geschwindigkeit + linker_schläger.höhe <= HÖHE:
        linker_schläger.bewegen(hoch=False)

    if tasten[pygame.K_UP] and rechter_schläger.y - rechter_schläger.geschwindigkeit >= 0:
        rechter_schläger.bewegen(hoch=True)
    if tasten[pygame.K_DOWN] and rechter_schläger.y + rechter_schläger.geschwindigkeit + rechter_schläger.höhe <= HÖHE:
        rechter_schläger.bewegen(hoch=False)

# Funktion zur Eingabeaufforderung
def eingabe_aufforderung(aufforderung):
    root = tk.Tk()
    root.withdraw()
    benutzer_eingabe = simpledialog.askstring("Eingabe", aufforderung)
    root.destroy()
    return benutzer_eingabe
#########################################################################################################################################################################################################################################

# Ergänzung
# Spielhistorie anzeigen
def historie_anzeigen():
    historie_laden()
    # Erstellt einen Text, der die letzten 10 Spiele aus der Spielhistorie darstellt
    historie_text = "\n".join([f"Spiel {i + 1}: {spiel['linker_spieler']} {spiel['linker_punktestand']} - {spiel['rechter_punktestand']} {spiel['rechter_spieler']}"
                              for i, spiel in enumerate(spiel_historie[-10:])])
    
    # Erstellt ein neues Fenster für die Anzeige der Spielhistorie
    historie_fenster = tk.Tk()
    historie_fenster.title("Spielhistorie") #Title des Fensters
    historie_fenster.geometry("400x300") #Größe des Fensters

    st = scrolledtext.ScrolledText(historie_fenster, width=50, height=15)
    st.pack()
    st.insert(tk.END, historie_text)
    st.configure(state='disabled') # Deaktiviert die Bearbeitung des Textfelds

    # Erstellt einen OK-Button, der das Fenster schließt
    ok_button = tk.Button(historie_fenster, text="OK", command=historie_fenster.destroy)
    ok_button.pack(pady=10)

    historie_fenster.mainloop()

# Ergänzung
# Spielhistorie laden
def historie_laden():
    global spiel_historie
    try:
        with open(historie_datei, "r") as file: # Öffnet die Historie-Datei im Lesemodus
            lines = file.readlines() # Liest alle Zeilen der Datei in eine Liste
            spiel_historie.clear()  # Bestehende Historie löschen, um Duplikate zu vermeiden
            for line in lines:
                parts = line.strip().split(",") # Trennt die Zeile anhand des Kommas

                # Überprüft, ob die Zeile vier Teile hat (linker Spieler, rechter Spieler, Punktestand linker Spieler, Punktestand rechter Spieler)
                # Fügt ein neues Spiel zur Spielhistorie hinzu
                if len(parts) == 4: 
                    spiel_historie.append({
                        "linker_spieler": parts[0],
                        "rechter_spieler": parts[1],
                        "linker_punktestand": int(parts[2]),
                        "rechter_punktestand": int(parts[3])
                    })
    except FileNotFoundError: # Wenn die Datei nicht vorhanden ist, wird nichts unternommen (pass)
        pass

# Ergänzung
# Spielhistorie speichern
def historie_speichern():
    with open(historie_datei, "w") as file: # Öffnet die Historie-Datei im Schreibmodus
        for spiel in spiel_historie[-10:]: # Geht durch die 10 letzten Spiele und schreibt diese im richtigen Format auf.
            file.write(f"{spiel['linker_spieler']},{spiel['rechter_spieler']},{spiel['linker_punktestand']},{spiel['rechter_punktestand']}\n")

# Ergänzung
# Hauptfunktion
def hauptfunktion():
    global linker_spieler, rechter_spieler, sieg_punktestand, ball_geschwindigkeit, FENSTER

    # Ergänzung
    # Spieler initialisieren
    def spieler_initialisieren():
        global linker_spieler, rechter_spieler
        linker_spieler = eingabe_aufforderung("Gebe den Namen des linken Spielers ein:")
        rechter_spieler = eingabe_aufforderung("Gebe den Namen des rechten Spielers ein:")

    # Ergänzung
    # Spielparameter festlegen
    def spiel_parameter_setzen():
        global sieg_punktestand, ball_geschwindigkeit
        while True:
            sieg_punktestand = eingabe_aufforderung("Gebe die Gewinnpunktzahl ein:")
            try:
                sieg_punktestand = int(sieg_punktestand) # Gewinnpunktzahl eingeben und sicherstellen, dass es eine Zahl ist
                break
            except ValueError:
                pass # Wenn nicht Frage erneut stellen.
        while True:
            schwierigkeit = eingabe_aufforderung("Wähle die Ballgeschwindigkeit (leicht, mittel, schwer):").lower()
            if schwierigkeit == "leicht":
                ball_geschwindigkeit = 4
                break # Schleife wird nach richtiger Eingabe verlassen.
            elif schwierigkeit == "mittel":
                ball_geschwindigkeit = 7
                break # Schleife wird nach richtiger Eingabe verlassen.
            elif schwierigkeit == "schwer":
                ball_geschwindigkeit = 10
                break # Schleife wird nach richtiger Eingabe verlassen.
    
    # Ergänzung
    # Spiel beenden
    def spiel_beenden():
        pygame.quit() #Pygame beenden
        sys.exit() #Programm beenden

    # Ergänzung
    # Nochmals spielen
    def nochmal_spielen():
        root = tk.Tk() # Fenster erstellen
        root.withdraw() # Fenster ausblenden
        antwort = messagebox.askyesno("Nochmal spielen?", "Möchtet Ihr nochmal spielen?")
        root.destroy()
        return antwort

    #########################################################################################################################################################################################################################################
    
    # Spiel starten
    def spiel_starten():
        global FENSTER
        pygame.display.init()
        FENSTER = pygame.display.set_mode((BREITE, HÖHE))
        pygame.display.set_caption("PingPong")
        
        laufen = True
        uhr = pygame.time.Clock()  # Uhr-Objekt erstellen, um die Frame-Rate zu steuern

        # Initialisierung der Schläger und des Balls
        linker_schläger = Schläger(10, HÖHE // 2 - SCHLÄGER_HÖHE // 2, SCHLÄGER_BREITE, SCHLÄGER_HÖHE)
        rechter_schläger = Schläger(BREITE - 10 - SCHLÄGER_BREITE, HÖHE // 2 - SCHLÄGER_HÖHE // 2, SCHLÄGER_BREITE, SCHLÄGER_HÖHE)
        ball = Ball(BREITE // 2, HÖHE // 2, BALL_RADIUS, ball_geschwindigkeit)

        # Punktestände der Spieler initialisieren
        linker_punktestand = 0
        rechter_punktestand = 0

        while laufen:
            uhr.tick(FPS) # Framerate festlegen
            zeichnen(FENSTER, [linker_schläger, rechter_schläger], ball, linker_punktestand, rechter_punktestand, linker_spieler, rechter_spieler)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    laufen = False
                    break
            
            # Tasten abfragen
            tasten = pygame.key.get_pressed()
            # Tasten bewegen die Schläger
            schläger_bewegung(tasten, linker_schläger, rechter_schläger)

            # Ball bewegen
            ball.bewegen()
            # Schläger zusammentreffen mit dem Ball
            kollisionsbehandlung(ball, linker_schläger, rechter_schläger)

            # Punktestand aktualisieren und Ball zurücksetzen, wenn ein Punkt erzielt wird
            if ball.x < 0:
                rechter_punktestand += 1
                ball.zurücksetzen()
                linker_schläger.zurücksetzen()
                rechter_schläger.zurücksetzen()
            elif ball.x > BREITE:
                linker_punktestand += 1
                ball.zurücksetzen()
                linker_schläger.zurücksetzen()
                rechter_schläger.zurücksetzen()

            # Überprüfen, ob jemand gewonnen hat
            gewonnen = False
            if linker_punktestand >= sieg_punktestand:
                gewonnen = True
                sieg_text = f"{linker_spieler} hat gewonnen!"
            elif rechter_punktestand >= sieg_punktestand:
                gewonnen = True
                sieg_text = f"{rechter_spieler} hat gewonnen!"

            # Wenn das Spiel gewonnen ist, Spielhistorie aktualisieren und den Siegertext anzeigen
            if gewonnen:
                spiel_historie.append({
                    "linker_spieler": linker_spieler,
                    "rechter_spieler": rechter_spieler,
                    "linker_punktestand": linker_punktestand,
                    "rechter_punktestand": rechter_punktestand
                })
                historie_speichern()

                # Siegertext anzeigen
                text = PUNKTZAHL_SCHRIFT.render(sieg_text, 1, WEISS)
                FENSTER.blit(text, (BREITE // 2 - text.get_width() // 2, HÖHE // 2 - text.get_height() // 2))
                pygame.display.update()
                pygame.time.delay(5000) 
                
                laufen = False

        pygame.display.quit()

    #########################################################################################################################################################################################################################################

    # Ergänzung
    # Menü anzeigen
    def menü_anzeigen():
        root = tk.Tk()
        root.title("PingPong Menü")
        root.geometry("300x200")

        def start_button_clicked():
            root.destroy()
            if not (linker_spieler and rechter_spieler):  # Nur initialisieren, wenn nicht bereits gesetzt
                spieler_initialisieren()
                spiel_parameter_setzen()
            while True:
                spiel_starten()
                if not nochmal_spielen(): # Fragen ob nochmal gespielt werden soll
                    break
            menü_anzeigen()

        def history_button_clicked():
            root.destroy()  # Menüfenster schließen
            historie_anzeigen()  # Spielhistorie anzeigen
            menü_anzeigen()  # Menü erneut anzeigen

        def quit_button_clicked():
            root.destroy()  # Menüfenster schließen
            sys.exit()  # Programm beenden

        # Menü Button
        start_button = tk.Button(root, text="Spiel Starten", command=start_button_clicked, width=20)
        start_button.pack(pady=10)

        history_button = tk.Button(root, text="Historie", command=history_button_clicked, width=20)
        history_button.pack(pady=10)

        quit_button = tk.Button(root, text="Beenden", command=quit_button_clicked, width=20)
        quit_button.pack(pady=10)

        root.mainloop() # Hauptprogramm wird geladen

    # Features werden geladen
    historie_laden()
    linker_spieler = None
    rechter_spieler = None
    menü_anzeigen()

if __name__ == "__main__":
    hauptfunktion()

#########################################################################################################################################################################################################################################