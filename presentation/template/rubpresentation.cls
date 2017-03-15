\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{rubpresentation}[2017/03/15 Customized RUB-themed presentation class]

\LoadClass{beamer}

\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage[ngerman]{babel}
\RequirePackage{pgfpages}
\RequirePackage[skip=2pt]{caption}
\RequirePackage[subpreambles]{standalone}
\RequirePackage{relsize}
\RequirePackage{listings}
\RequirePackage{inconsolata}
\RequirePackage{multicol}
\RequirePackage{blindtext}
\RequirePackage{xkeyval}
\RequirePackage{etoolbox}

\def\cornerlogo{}%
\define@key{rubpresentation.cls}{cornerlogo}[]{%
  \def\cornerlogo{#1}%
}
\def\alternativetitlepage{normal}%
\define@key{rubpresentation.cls}{alternativetitlepage}[normal]{%
  \def\alternativetitlepage{#1}%
}

\DeclareOption{sectionoverview}{%
    \AtBeginSection[]{%
      \begin{frame}%
        \frametitle{Überblick}%
        \tableofcontents[currentsection]%
      \end{frame}%
    }%
}

\ExecuteOptionsX{cornerlogo, alternativetitlepage}
\ProcessOptionsX%
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}
\ProcessOptions\relax

\usetheme[alternativetitlepage=\alternativetitlepage]{Rub}
%\setbeameroption{show notes}
%\setbeameroption{show notes on second screen=right}

%% Add the logo in the bottom right corner
\ifdefempty{\cornerlogo}{}{%
    \addtobeamertemplate{footline}{}{%
      \framelatex{%
        \begin{beamercolorbox}[rightskip=.3cm,wd=\paperwidth,ht=0pt,sep=0.1cm]{section in head/foot}%
          \hfill%
          \includegraphics[height=0.5cm,interpolate=true]{\cornerlogo}%
          \vspace{0.5cm}%
          \hspace{0.5cm}%
        \end{beamercolorbox}%
      }%
    }%
}

%% Add proper styling to captions
\DeclareCaptionFormat{rub}{\fontsize{5}{6}\selectfont#1#2#3}
\captionsetup{format=rub,labelformat=empty}
\setbeamercolor{caption}{fg=black}

%% Nice look for lstlistings
\lstset{
  basicstyle=\ttfamily\upshape,
  numberstyle=\tiny\color[rgb]{0.6,0.60,0.6},
  keywordstyle=\color[rgb]{0.13,0.29,0.53}\bfseries,
  stringstyle=\color[rgb]{0.31,0.60,0.02},
  commentstyle=\color[rgb]{0.56,0.35,0.01}\itshape,
  backgroundcolor=\color[RGB]{248,248,248},
  numbers=left,
  stepnumber=1,
  numbersep=5pt,
  keepspaces=true,
  showspaces=false,
  showstringspaces=false,
  showtabs=false,
  tabsize=2,
  captionpos=b,
  breaklines=true,
  breakatwhitespace=false,
  breakautoindent=true,
  postbreak=\raisebox{0ex}[0ex][0ex]{\ensuremath{\color{red}\hookrightarrow\space}},
  escapeinside={\%*}{*\%},
  linewidth=\textwidth,
  basewidth=0.5em,
  literate={Ö}{{\"O}}1{Ä}{{\"A}}1{Ü}{{\"U}}1{ß}{{\ss}}2{ü}{{\"u}}1{ä}{{\"a}}1{ö}{{\"o}}1,
}
