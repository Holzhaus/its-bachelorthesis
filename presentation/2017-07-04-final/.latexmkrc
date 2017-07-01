$pdf_mode = 1;                    # Use PDF output format instead of DVI/PS
$bibtex_use = 2;                  # We're using biblatex, delete *.bbl files
$latex = 'latex --shell-escape';
$pdflatex = 'pdflatex --shell-escape';

@default_files = ('presentation.tex');  # Specifies the main tex file

$jobname = '2017-07-04-holthuis-xml-json-conversion-ABSCHLUSS';

# Add template folder to the search path
$ENV{'TEXINPUTS'} = '' unless defined $ENV{'TEXINPUTS'};
$ENV{'TEXINPUTS'} = $ENV{'TEXINPUTS'} . $search_path_separator . '../template/' . $search_path_separator . './thesis/';

# Add more generated extensions
push @generated_exts, "cb";
push @generated_exts, "cb2";
push @generated_exts, "spl";
push @generated_exts, "nav";
push @generated_exts, "snm";
push @generated_exts, "sta";
push @generated_exts, "tdo";
push @generated_exts, "nmo";
push @generated_exts, "brf";
push @generated_exts, "nlg";
push @generated_exts, "nlo";
push @generated_exts, "nls";
push @generated_exts, "fls";
push @generated_exts, "vrb";
push @generated_exts, "synctex.gz";
push @generated_exts, "tex.latexmain";
push @generated_exts, "run.xml";
