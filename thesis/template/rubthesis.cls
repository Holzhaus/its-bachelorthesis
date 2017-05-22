%%% TEMPLATE-INFO
%% AUTHOR		: johannes.hoffmann@rub.de (former: vincent.immler@rub.de)
%% VERSION		: 0.03
%% Please send comments and feedback (and donations ;-)) to author, thanks!

%%% DOCUMENT-INFO
%% AUTHOR		: Dennis Felsch [dennis.felsch@ruhr-uni-bochum.de]
%% VERSION		: 0.1

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{rubthesis}[2017/03/15 Customized RUB-themed presentation class]

\RequirePackage{fix-cm,cmap}

\LoadClass[
fontsize=11pt,
paper=a4,
abstract=true,
numbers=noenddot,
listof=totoc,
bibliography=totoc,
twoside,
open=right,
cleardoublepage=plain,
parskip=half+, % comment this out if you do not want an empty half line between paragraphs, but please read the KomaScript Guide and search for parskip (around page 82): ftp://ftp.dante.de/pub/tex/macros/latex/contrib/koma-script/scrguide.pdf
BCOR=1cm, % Bindekorrektur: Change this accordingly, also read the KomaScript Guide! Make sure you read the guide.
]{scrreprt}

\setcounter{tocdepth}{3}  % Inhaltsverzeichnis bis Subsubsection
\setcounter{secnumdepth}{3} % Nummerierung bis Subsubsection

% General stuff
\RequirePackage{fixltx2e}
\RequirePackage[utf8]{inputenc} % CHANGE HERE IF NECESSARY
\RequirePackage[T1]{fontenc}

\newcommand{\thesislanguages}{ngerman,english} % last language given is used (here: english)
\newcommand{\thesistype}{Master's Thesis}
\newcommand{\thesischair}{Chair for Network and Data Security.}
\newcommand{\thesissupervisortitle}{Supervisor}
\newcommand{\thesissupervisor}{Prof.~Dr.~J\"{o}rg~Schwenk}
\newcommand{\thesisadvisortitle}{Advisor}
\newcommand{\thesisadvisor}{Dipl.-Ing.~Christopher Meyer}
\newcommand{\thesiskeywords}{SAML, add more}

\newcommand{\proposititontitle}{Proposition}
\newcommand{\corollarytitle}{Corollary}
\newcommand{\algorithmtitle}{Algorithm}
\newcommand{\exampletitle}{Example}

\DeclareOption{german}{
  \renewcommand{\thesislanguages}{english,ngerman}
  \renewcommand{\thesischair}{Lehrstuhl für Netz- und Datensicherheit.}
  \renewcommand{\thesissupervisortitle}{Betreuer}
  \renewcommand{\thesisadvisortitle}{Berater}

  \renewcommand{\proposititontitle}{Satz}
  \renewcommand{\corollarytitle}{Korollar}
  \renewcommand{\algorithmtitle}{Algorithmus}
  \renewcommand{\exampletitle}{Beispiel}
}
\ExecuteOptions{german}
\ProcessOptions\relax

\RequirePackage[\thesislanguages]{babel}

%\RequirePackage{microtype}
\RequirePackage{ifpdf}
\RequirePackage{ifthen}
\RequirePackage{authoraftertitle}

%%%%%% MACROS %%%%%%
\RequirePackage{xspace} % Nur dann ein Leerzeichen, wenn das nächste Zeichen kein Satzzeichen ist.
\newcommand{\SecII}{Sec\textsuperscript{2}\xspace}
\newcommand{\SAML}{\acr{SAML}\xspace}
\newcommand{\XML}{\acr{XML}\xspace}


%%%%%% %%%%%%

% Load packages ...

% Corporate Design
\RequirePackage{eso-pic}
\RequirePackage{color}
\RequirePackage{rubfonts2009}
\newcommand{\setrubfontnormal}[1]{\fontfamily{rubscala}\fontsize{#1}{1}\selectfont}
\newcommand{\setrubfontextra}[1]{\fontfamily{rubflama}\fontsize{#1}{1}\selectfont}
\definecolor{rubgreen}{cmyk}{0.5,0,1,0}
\definecolor{rubblue}{cmyk}{1,0.5,0,0.6}

% Figures
\RequirePackage{graphicx}
\RequirePackage{subfig}
\RequirePackage{placeins}

% Tables
\RequirePackage{booktabs}
\RequirePackage{marvosym}
\RequirePackage{multirow}

% Math stuff and units
\RequirePackage{latexsym,amsmath, amssymb, amsfonts, upgreek}
\RequirePackage{siunitx}
\newcommand{\mathup}{\mathrm}

% Acronyms
\RequirePackage[abbreviations,stylemods=longbooktabs,xindy]{glossaries-extra}
\makeglossaries{}
% \glscurrentfieldvalue only works with glossaries v4.23 (and above)
\renewcommand{\glsxtrpostdescacronym}{%
 \ifglshasfield{\glsxtruserfield}{\glscurrententrylabel}%
 { (\glscurrentfieldvalue)}%
 {}%
}
\setabbreviationstyle[acronym]{long-short-user}

\RequirePackage[url=true,backend=biber,style=alphabetic,maxalphanames=1]{biblatex}
\renewcommand*{\labelalphaothers}{}

% Make bibliography titles clickable if URL is given
\newbibmacro{string+url}[1]{%
  \iffieldundef{url}{%
    #1%
  }{%
    \href{\thefield{url}}{#1}%
  }%
}
\DeclareFieldFormat{title}{\usebibmacro{string+url}{\mkbibemph{#1}}}
\DeclareFieldFormat[article,incollection,inproceedings,report]{title}%
    {\usebibmacro{string+url}{\mkbibquote{#1}}}
\DefineBibliographyStrings{ngerman}{%
   andothers = {{et\,al\adddot}},%
}

\makeatletter
\newcommand{\acr}{\protect\@acr}%
\newcommand{\@acr}[1]{%
	\expandafter\ifx\csname ac@#1\endcsname\AC@used % chktex 1
		\acs{#1}%
	\else
		\acs{#1} (\acl{#1})%
		\global\expandafter\let\csname ac@#1\endcsname\AC@used % chktex 1
		\AC@addtoAC@clearlist{#1}
		\AC@logged{#1}
	\fi
}
\makeatother

% Enable quotes by \enquote{}
\RequirePackage[babel,english=american, german=quotes]{csquotes}

% Necessary for frontpage, allows to create automata and fancy graphics
\RequirePackage{tikz}

% Protocols and bytefields
\RequirePackage{protocol}
\RequirePackage{bytefield}

% Source code listings
\newcommand{\code}[1]{\texttt{#1}}

\RequirePackage{caption}
\RequirePackage{morewrites}
\RequirePackage{inconsolata}
\RequirePackage[chapter]{minted}
\usemintedstyle{autumn}
% Customize line numbers
\renewcommand{\theFancyVerbLine}{\ttfamily\textcolor{black!50}{\scriptsize{\arabic{FancyVerbLine}}}}
\setminted{
   breaklines=true,
   mathescape=false,
   linenos=true,
   xleftmargin=2em,
   numbersep=5pt,
   frame=leftline,
   framerule=2pt,
   framesep=2mm,
   rulecolor=\color{black!50},
}


% Algorithms
\RequirePackage[ruled, vlined, linesnumbered,algochapter,algo2e]{algorithm2e}

% Format page foot and header
\RequirePackage{scrpage2}
\clearscrheadings{}
\clearscrheadfoot{}
\automark[section]{chapter}
\ohead{\pagemark}
\ihead{\headmark}
\pagestyle{scrheadings}

% Nicer Theorems
\RequirePackage{mdframed}
\RequirePackage{amsthm}

%% use some standards for mathematical expressions:
\definecolor{light-gray}{gray}{0.9}

\newcommand{\red}{{\rm red}}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{\propositiontitle}
\newtheorem{corollary}[theorem]{\corollarytitle}
% \newtheorem{definition}[theorem]{Definition}
\newtheorem{algorithm}[theorem]{\algorithmtitle}
%\newenvironment{example}{\begin{quote}{\textbf \exampletitle:}}{\end{quote}}
\theoremstyle{definition}
\newtheorem{mdexample}[theorem]{\exampletitle}
\newenvironment{example}%
  {\begin{mdframed}[hidealllines=true,backgroundcolor=light-gray]\begin{mdexample}}%
  {\end{mdexample}\end{mdframed}}

% gray definition boxes, that whay you'll find them in the text
\newtheorem{mddefinition}[figure]{Definition}
\newenvironment{definition}%
  {\begin{mdframed}[hidealllines=true,backgroundcolor=light-gray]\begin{mddefinition}}%
  {\end{mddefinition}\end{mdframed}}


% BIBTEX, http://merkel.zoneo.net/Latex/natbib.php
% if you uncomment this block, you'll get an english bibliography with alphanumerical references
%\RequirePackage{bibgerm} % u. a. statt et al
%\RequirePackage[square,numbers]{natbib} % eckige klammern, natbib-package
% \setbibpreamble{{\large Seitenzahlen, auf denen ein Eintrag referenziert wird, werden am Ende eines jeden Eintrags angegeben.}\newline} % Wegen der pagebackref-Option des hyperref-Packets, wird vielen nicht direkt klar was das soll http://projekte.dante.de/DanteFAQ/Verzeichnisse#16

% experimental
%\RequirePackage{scrhack}

% Hyperlinks and menu for your document
\RequirePackage[breaklinks,hyperindex,colorlinks,anchorcolor=black,citecolor=black,filecolor=black,linkcolor=black,menucolor=black,urlcolor=black,pdftex]{hyperref} % pagebackref: Add page number to the references where they can be found
% DO NOT LOAD ANY OF YOUR PACKAGES BEYOND THIS PACKAGE

\makeatletter
\AtBeginDocument{
 \hypersetup{
   pdftitle = {\MyTitle},
   pdfauthor = {\MyAuthor},
   pdfsubject={\MyTitle},
   pdfkeywords={\thesiskeywords},
%    unicode={true},
 }
}
\makeatother

% Use the same counter for tables and figures
\makeatletter
\AtBeginDocument{
\let\c@table\c@figure{}
\let\c@lstlisting\c@table{}
\let\c@algocf\c@lstlisting{}
}
\makeatother

\ifpdf % chktex 1
	\hypersetup{linktocpage=false} 	% false=links are section names, true=links are page numbers, IMPORTANT: in dvi2ps mode, 'true' is required!
\else
	\hypersetup{linktocpage=true} 		% false=links are section names, true=links are page numbers, IMPORTANT: in dvi2ps mode, 'true' is required!
	\RequirePackage[hyphenbreaks]{breakurl}
\fi

%%%%%% FRONTPAGE %%%%%%

% Hintergrund-Makro
\newcommand\BackgroundPic{
\put(0,0){
\parbox[b][\paperheight]{\paperwidth}{%
\vfill
\centering
\includegraphics[width=\paperwidth,height=\paperheight]{images/front.png}%
\vfill
}}}

\newcommand{\frontpage}{
    \AddToShipoutPicture*{\BackgroundPic}
    \begin{titlepage}
    \makeatletter

    \enlargethispage{3cm}

    \begin{tikzpicture}[remember picture,overlay]
    \node[shift={(10cm,-23.5cm)},opacity=1] {\includegraphics[scale=0.625]{images/hgi_nds_2.pdf}};
    \end{tikzpicture}

    \vspace*{10cm}
    \begin{minipage}[b]{1\linewidth}
        \sffamily
        \hspace{-17.2mm}\includegraphics[scale=1.0]{images/rub_slogan}\\

        \textbf{\LARGE {\MyTitle}}\\

        \Large{\MyAuthor}\\

        \vspace{4cm}
        \normalsize{
        \thesistype\hspace{0.2cm}--\hspace{0.2cm}\MyDate.\\ % lacheck 246
          \thesischair\\
        }
        \newline
        \normalsize{
        \begin{tabular}{@{}ll@{}}
        \thesissupervisortitle: & \thesissupervisor\\
        \thesisadvisortitle: & \thesisadvisor\\
        \end{tabular}
        }
    \end{minipage}


    \makeatother%
    \end{titlepage}%
    \ClearShipoutPicture{}%
}
