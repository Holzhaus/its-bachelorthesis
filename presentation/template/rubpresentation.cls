\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{rubpresentation}[2017/03/15 Customized RUB-themed presentation class]

\LoadClass{beamer}

\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage{pgfpages}
\RequirePackage[babel,english=american, german=quotes]{csquotes}
\RequirePackage[skip=2pt]{caption}
\RequirePackage[subpreambles,mode=buildnew]{standalone}
\RequirePackage{relsize}
\RequirePackage{listings}
\RequirePackage{droidmono}
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
        \frametitle{\iflanguage{english}{Overview}{Überblick}}%
        \tableofcontents[currentsection]%
      \end{frame}%
    }%
}

\newcommand{\presentationlanguages}{ngerman,english}
\DeclareOption{german}{\renewcommand{\presentationlanguages}{english,ngerman}}

\ExecuteOptionsX{cornerlogo, alternativetitlepage}
\ProcessOptionsX%
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}
\ProcessOptions\relax

\RequirePackage[\presentationlanguages]{babel}

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

% Add some colors
\definecolor{gray}{rgb}{0.4,0.4,0.4}
\definecolor{darkblue}{rgb}{0.0,0.0,0.6}
\definecolor{cyan}{rgb}{0.0,0.6,0.6}

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

\lstdefinelanguage{xml}
{
  morestring=[b]",
  morestring=[s]{>}{<},
  morecomment=[s]{<?}{?>},
  stringstyle=\color{black},
  identifierstyle=\color{darkblue},
  keywordstyle=\color{cyan},
  morekeywords={xmlns,version,type}% list your attributes here
}
\lstdefinelanguage{json}{
    stringstyle=\color{darkblue},
    morestring=[b]",
    literate=
     *{0}{{{\color{cyan}0}}}{1}
      {1}{{{\color{cyan}1}}}{1}
      {2}{{{\color{cyan}2}}}{1}
      {3}{{{\color{cyan}3}}}{1}
      {4}{{{\color{cyan}4}}}{1}
      {5}{{{\color{cyan}5}}}{1}
      {6}{{{\color{cyan}6}}}{1}
      {7}{{{\color{cyan}7}}}{1}
      {8}{{{\color{cyan}8}}}{1}
      {9}{{{\color{cyan}9}}}{1}
}
