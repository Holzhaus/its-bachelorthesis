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

Da das [LaTeX-Paket `minted`](https://www.ctan.org/pkg/minted) für die
Einfärbung der Quelltexte eingesetzt wird, müssen zudem die dazu notwendigen
Python-Pakete installiert sein:

- [Pygments](http://pygments.org), sowie
- der Einfärbungsstil
  [pygments-style-rub](https://github.com/Holzhaus/pygments-style-rub), der
  das Farbschema der Ruhr-Uni Bochum adaptiert.

Mittels [pip](https://pip.pypa.io/) können die beiden Pakete einfach
installiert werden:

```shell-session
$ pip install pygments pygments-style-rub
```

## Test-Framework

Es wird empfohlen, das Test-Framework innerhalb eines Docker-Containers
auszuführen. Dazu kann das Dockerfile unter `code/Dockerfile` verwendet
werden.

Zunächst muss dafür das Docker-Image erstellt werden:

```shell-session
$ cd code
$ docker build -t xjcc .
```

Im Anschluss kann der Docker-Container gestartet werden. Um die Ergebnisdaten
später auf dem Host-System auswerten zu können, kann ein lokaler Ordner auf
das `/data`-Verzeichnis im Docker-Container gemappt werden. Hier ein Beispiel
für das Verzeichnis `~/mydata` auf dem Host:

```shell-session
$ docker run -v ~/mydata:/data -it xjcc
```

Im Container wird eine Shell gestartet, in der dann der Befehl `xjcc` zum
Einsatz des Test-Frameworks genutzt werden kann.

Das folgende Kommando führt alle Konverter und alle Testfälle aus und
legt die Ergebnisse in einem Ordner im aktuellen Arbeitsverzeichnis ab:

```shell-session
$ xjcc -vv test-conversion -w
```

Mit dem Argument `--help` kann die eingebaute Hilfe angezeigt werden:

```shell -session
$ xjcc --help
usage: xjcc [-h] [-v | -vv | -q]
            {convert-file,list-converters,list-testcases,test-conversion,canonicalize}
            ...
positional arguments:
  {convert-file,list-converters,list-testcases,test-conversion,canonicalize}
    convert-file        convert file
    list-converters     list available converters
    list-testcases      list available testcases
    test-conversion     test conversion
    canonicalize        canonicalize an XML document
optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         be verbose
  -vv, --debug          even show debug messages
  -q, --quiet           be quiet
```

## Testcases

Die [Sicherheits-Testdokumente](code/test-documents) in den Ordnern
"denial-of-service", "file-system-access" und "server-side-request-forgery"
basieren auf der Arbeit von
[Christopher Späth](https://www.nds.rub.de/chair/people/spaetc1k/). Die
ursprünglichen Versionen der Testdokumente befinden sich im
["DTD-Attacks"-Repository](https://github.com/RUB-NDS/DTD-Attacks) des
NDS-Lehrstuhls auf Github.
