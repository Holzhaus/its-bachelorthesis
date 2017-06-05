\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{flowchart}[2017/06/92 Customized Standalone TIKZ flowchart class]
\LoadClass[tikz]{standalone}
\RequirePackage[T1]{fontenc}
\RequirePackage{rubfonts2009}
% FIXME: Blue should be #003560, but that'd conflict with the front page colors
\definecolor{rubblue}{HTML}{003660}
\definecolor{rubgreen}{HTML}{8dae10}
\definecolor{rubgray}{HTML}{e7e7e7}
\usetikzlibrary{%
    shadows.blur,
    shapes.geometric,
    shapes.multipart,
    arrows,
    positioning,
    quotes,
    fit,
}
\tikzset{%
    every label/.style={
        text=rubblue,
        font=\fontfamily{rubflama}\selectfont\bfseries,
    },
    flowchartbase/.style = {
        minimum width=4cm,
        minimum height=1cm,
        text centered,
        text width=3cm,
        font=\fontfamily{rubflama}\selectfont,
        %draw=black!60,
        line width=0.1mm,
        %shading=axis,
        %shading angle=135,
        %rounded corners,
        %top color=white,
        %blur shadow={
        %    shadow opacity=25,
        %    shadow blur radius=2mm,
        %    shadow blur steps=5,
        %},
    },
    flowchartterminal/.style = {
        flowchartbase,
        rectangle,
        rounded corners=0.5cm,
        fill=rubgray,
    },
    flowchartio/.style = {
        flowchartbase,
        trapezium,
        trapezium left angle=70,
        trapezium right angle=110,
        text width=2.75cm,
        fill=rubgreen!40,
    },
    flowchartprocess/.style = {
        flowchartbase,
        rectangle,
        fill=rubblue!20,
    },
    flowchartsubroutine/.style = {
        flowchartbase,
        rectangle split,
        rectangle split horizontal,
        rectangle split parts=3,
        fill=rubblue,
        draw=white,
        text=white,
        text width=0,
        every two node part/.style={
            text width=3cm,
        },
    },
    flowchartdecision/.style = {
        flowchartbase,
        diamond,
        aspect=2,
        text badly centered,
        text width=2cm,
        minimum width=4cm,
        minimum height=2cm,
        inner sep=0.5ex,
        fill=rubgreen,
    },
    flowchartarrow/.style = {
        thick,
        ->,
        >=stealth,
        nodes={
            font=\fontfamily{rubscala}\selectfont,
        },
    },
}
