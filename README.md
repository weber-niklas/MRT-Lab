# MRT 1 - Praktikum Versuch 1: Morsealphabet

## Aufgabenstellung
*Es ist ein Programm in Micropython für Raspberry Pi Pico W zu schreiben, welches
eine Zeichenkette als Morsecode ausgibt. Die Zeichenkette soll dabei aus den
aneinander gereihten Familiennahmen der Gruppenmitglieder bestehen.*

*Für die Ausgabe der Morsezeichen sind die vorhandenen LEDs wie folgt zu nutzen:*
- *LED rot: Darstellung eines Striches (-) (Länge: 0,5s)*
- *LED grün: Darstellung eines Punktes (.) (Länge: 0,1s)*
- *Pause: Zwischenraum zwischen Zeichen (Länge: 0,2s).*

*Die Namen sollen über die Thonny-Console mittels Tastatur eingegeben werden
können. Mittels mitgeliefertem Taster soll der Ablauf auf dem Raspberry Pi Pico
gestartet (erster Tastendruck) und wieder beendet (zweiter Tastendruck) werden.*

---

An dieser Stelle wurde die Aufgabenstellung leicht **modifiziert**. Der Pi wurde als Wireless Access Point konfiguriert und stellt eine Weboberfläche zur verfügung, die in jedem gängigen Browser geöffnet und bedient werden kann. Das ermöglicht eine kabellose und plattformunabhängige Kommunikation, für die keinerlei zusätzliche Software (Thonny oder VS-Code...) benötigt wird. Selbst mit einem Smartphone kann so gemorst werden. Inspiration bot dabei der in der Vorlesung gezeigte Quelltext.

**Hinweis:** Es wird zusätzlich ein Programm eingereicht, welches die Eingabe in der Python-REPL ermöglicht. Die nachfolgende Dokumentation bezieht sich aber auf das Programm, welches die kabellose Kommunikation über die grafische Benutzeroberfläche ermöglicht.

## Umsetzung
### Hardware
Für die Realisierung der Hardware wurden zwei LEDs mit einem Vorwiderstand auf einen Output-Pin geschaltet. Sollen die LEDs eingeschaltet werden, wird der Pin auf 1 (ca. 3 V) gesetzt. Die LED leuchtet.
Der Taster zum Sarten des Programmes wurde mit einem Pull-Down Widerstand beschaltet. Generell liegt also eine 0 (0V) am Input-Pin an. Wird der Button betätigt ändert sich das Potenzial zu einer 1 (ca. 3 V). Dafür wurde ein 10 k Widerstand verwendet, um den Pi nicht mit zu hohen Strömen zu belasten.

### Software
#### Netzwerkkommunikation

#### Morsecode / Stringmanipulation
Zum
#### Hardwaresteuerung
Zum Einen müssen die **LEDs** angesteuert werden. Dazu werden die Variablen `led_red` und `led_green` mit dem Konstruktor `Pin()` aus `machine` initialisiert. Festgelegt werden die Pins 14 und 15 als Ausgabepins. Mithilfe der Methode `value()` werden die Pins auf eine logische 1 oder 0 gesetzt (bei 1 liegt Spannung an, die LEDs leuchten).
Der Eingabepin (Pin 16) wird mit dem selben Konstruktor initialisiert, allerdings wird als Argument `Pin.IN` übergeben. Anschließend wird die Methode `irq()` auf diesem Objekt ausgeführt. Durch Übergabe der Argumente `trigger=Pin.IRQ_Rising` und `handler=handle_interrupt` wird spezifiziert, dass bei einer steigenden Flanke am Input-Pin (drücken des Buttons, beschaltet mit Pull-Down-Widerstand) die Funktion `handle_interrupt()` ausgeführt wird.
### Probleme bei der Umsetzung
Ein Problem stellte das Modul `socket` dar. Dieses ist in Micro-Python nicht in vollem Umfang implementiert. Das führte zur Verwirrung bei der Anwendung, da die falsche Dokumentation (für normales Pyhton) benutzt wurde.
Ein weiteres Problem stellte der Interrupt-Handler dar. Zunächst wurde probiert die Socket direkt aus dem interrupt zu schließen.

<details><summary> Versuchter Ansatz </summary>
  

  
</details>


