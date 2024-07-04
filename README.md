# 🏓 TT - PingPong (Tischtennis)

---

### 🎮 Aufbau des Spiels

- 🟢 Beim Starten des Spiels werden die Namen der beiden Spieler abgefragt.
- 🟢 Danach können die Gewinnpunktzahl und die Ballgeschwindigkeit gewählt werden.
- 🟢 Geschwindigkeiten: leicht, mittel, schwer

### 🎲 Spielablauf

- 🕹️ Das Spiel wird im Pygame-Fenster angezeigt.
- 🕹️ Spieler 1 (linkes Paddle) wird mit den Tasten W (hoch) und S (runter) gesteuert.
- 🕹️ Spieler 2 (rechtes Paddle) wird mit den Pfeiltasten ↑ (hoch) und ↓ (runter) gesteuert.
- 🏐 Der Ball bewegt sich automatisch, und das Ziel ist es, den Ball am Gegner vorbeizuspielen, um Punkte zu erzielen.

### 📊 Punktestand

- 🏆 Der Punktestand beider Spieler wird oben im Fenster angezeigt.
- 🏆 Wenn ein Spieler die festgelegte Punktzahl erreicht, gewinnt dieser Spieler das Spiel.

### 🔁 Spielende und Neustart

- 🏅 Nach dem Spielende wird der Gewinner angezeigt und die Möglichkeit gegeben, ein neues Spiel zu starten oder das Programm zu beenden.

### 🗂️ Historie

- 📝 Die letzten 10 Spiele werden in einer Historie gespeichert.
- 📝 Diese Historie kann über das Menü eingesehen werden.

---

### ✨ Features

- 👥 Mehrspieler-Unterstützung: Zwei Spieler können gegeneinander antreten.
- ⚙️ Anpassbare Spielparameter: Spielernamen, Gewinnpunktzahl und Ballgeschwindigkeit können vor Spielbeginn festgelegt werden.
- 📜 Spielhistorie: Die Ergebnisse der letzten 10 Spiele werden gespeichert und können eingesehen werden.
- 🖥️ Grafische Benutzeroberfläche: Einfache Menüführung und Eingabeaufforderungen mittels tkinter.

### 🖥️ Systemanforderungen

- 🐍 Python
- 🕹️ Pygame (pip install pygame)
