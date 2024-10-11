\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cryslides}[2024/09/10 LaTeX class for cryptography slides]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}
\ProcessOptions\relax
\LoadClass[aspectratio=169]{beamer}

\usetheme[numbering=fraction]{metropolis}
\metroset{block=fill}

% Cryptographic symbols
\RequirePackage{crysymb}

% Graphics and drawings
\RequirePackage{graphicx}
\RequirePackage{tikz}
\usetikzlibrary{positioning,calc}

% Typographic improvements (needs LuaLaTeX)
\RequirePackage{fontspec}
\RequirePackage{unicode-math}
\RequirePackage{microtype}

% https://tex.stackexchange.com/a/348428
\let\textttorig\texttt

\RequirePackage{csquotes}
\setquotestyle{british}

\RequirePackage[en-GB]{datetime2}
\DTMlangsetup[en-GB]{ord=omit}

% Better tables
\RequirePackage{booktabs}
\renewcommand*{\arraystretch}{1.2}
