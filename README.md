# Bachelorarbeit

## Ordnerstruktur

Die Ordnerstruktur (wie im [How-To](extra/How-To-Studenten.pdf) beschrieben):

| Ordner         | Inhalt                                |
| -------------- | ------------------------------------- |
| `code`         | Quelltexte                            |
| `doku`         | Zwischenergebnisse, Stichpunkte, etc. |
| `extra`        | How-To, Vorlagen, etc.                |
| `expose`       | Exposé für die Bachelorarbeit         |
| `literatur`    | Referenzierte Paper im Volltext       |
| `presentation` | Folien für die Kolloquiums-Vorträge   |
| `thesis`       | Bachelorarbeit                        |

## Latex-Abhängigkeiten

Neben einer aktuellen TeXLive-Distribution werden benötigt:

- die Schriftarten des Corporate Designs der Ruhr-Uni für Latex in Form des
  [rubfonts2009](https://noc.rub.de/~jobsanzl/latex/)-Pakets. Für ArchLinux
  gibt es ein AUR-Paket namens
  [rubtextfonts2009](https://aur.archlinux.org/packages/rubtexfonts2009/).
- das Latex-Beamer-Template [rub-beamer](https://github.com/sjewo/rub-beamer).
  Auch hier gibt es mit
  [beamer-theme-rub-git](https://aur.archlinux.org/packages/beamer-theme-rub-git/)
  ein AUR-Paket für ArchLinux.

Zudem sollte das Tool
[Latexmk](http://personal.psu.edu/jcc8//software/latexmk-jcc/) zum Kompilieren
verwendet werden, damit sichergestellt wird, dass genügend Durchläufe zum
Auflösen aller Querverweise gemacht werden. Zudem befinden sich
`.latexmkrc`-Dateien in den jeweiligen Dokumentordnern, die sinnvolle
Einstellungen für den Kompiliervorgang enthalten.
