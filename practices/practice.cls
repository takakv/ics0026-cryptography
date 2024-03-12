\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{practice}[2024/01/31 Practice tasks template]

\LoadClass[parskip=half]{scrartcl}

\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{amsthm}

\RequirePackage{tcolorbox}

\RequirePackage[hidelinks]{hyperref}

\RequirePackage{fontspec}
\RequirePackage{unicode-math}
\RequirePackage{microtype}

\setmainfont{Stix Two Text}
\setsansfont[BoldFont = *-Semibold]{Source Sans 3}
\setmathfont{Stix Two Math}
\setmonofont{Courier New}

\RequirePackage{bookmark}

\RequirePackage{datetime2}
\DTMsetdatestyle{ddmmyy}
\DTMsetup{datesep=.}

\makeatletter
\def\@maketitle{%
  \newpage
  \begin{center}%
    {Practice session \@title{} --- \@date\par}%
  \end{center}%
  \par}
\makeatother

\newcounter{task}[section]
\newenvironment*{task}[1]{%
  \refstepcounter{task}%
  \textbf{Task~\thetask{} --- {#1}}\par}{}

%\makeatletter
%\newcommand\task{\@startsection {task}{1}{\z@}%
%                                {0pt}%
%                                {0pt}%
%                                {\normalfont\bfseries\par}}
%\newcommand{\taskmark}[1]{}
%\newcounter{task}
%\let\l@task\l@section
