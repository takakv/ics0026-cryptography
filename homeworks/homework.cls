\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{homework}[2024/01/31 Homework tasks template]

\LoadClass[parskip=half]{scrartcl}

\iffalse
\RequirePackage[
  a4paper,
  top=25mm,
  bottom=25mm,
  left=30mm,
  right=30mm,
  footskip=10mm
]{geometry}
\fi

\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{amsthm}

\RequirePackage[hidelinks]{hyperref}

\RequirePackage{tcolorbox}

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
    {Homework~\@title{} --- Deadline:~\@date~23:59~EET\par}%
  \end{center}%
  \par}
\makeatother

\newcounter{task}[section]
\newenvironment*{task}[1]{%
  \refstepcounter{task}%
  \textbf{Task~\thetask{} --- {#1}}\par}{}
