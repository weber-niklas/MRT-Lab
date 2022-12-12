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

## Umsetzung
### Hardware
Für die Realisierung der Hardware wurden zwei LEDs mit einem Vorwiderstand auf einen Output-Pin geschaltet. Sollen die LEDs eingeschaltet werden, wird der Pin auf 1 (ca. 3 V) gesetzt. Die LED leuchtet.
Der Taster zum Sarten des Programmes wurde mit einem Pull-Down Widerstand beschaltet. Generell liegt also eine 0 (0V) am Input-Pin an. Wird der Button betätigt ändert sich das Potenzial zu einer 1 (ca. 3 V).

### Software
#### Netzwerkkommunikation
Henning
#### Morsecode / Stringmanipulation
Louis / Magda
#### Hardwaresteuerung
Niklas/ Henning

