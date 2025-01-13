#!/usr/bin/env python3

# This script provides a clean way of compiling a LaTeX document directly,
# and neatly stores extraneous files in the folder in the directory in which
# the main .tex and .bib files live. We rely on the following python packages:

import subprocess, sys, os, shutil


# We create a metafiles directory for the subprocess commands to draw from. This
# is not strictly necessary, but makes for a cleaner working directory.
# It does necessitate copying the bib file to the meta directory, from which we
# may run bibtex.

metafiles = "metafiles"
if not os.path.isdir(metafiles):
    os.mkdir(metafiles)


# This block generates the meta files and does the first compilation of the pdf.
# The metafiles are for bibtex to be able to append with its database
# information.

pdf1cmd1 = subprocess.run(
    ['pdflatex', '-halt-on-error','-output-directory=metafiles',
    sys.argv[1]+'.tex'],
    stdout=subprocess.PIPE
)

pdf1cmd2 = subprocess.run(
    ['grep','^!.*','-A200','--color=always'],
    input=pdf1cmd1.stdout
)


# From here we need to copy the bibliography database from the root directory
# and put it in the same directory as the auxilliary. If we do not do this,
# bibtex fails to cooperate, and the generated pdf does not come with its
# bibliography. Then we run the bibtex command, and delete the copied bib file.
# We finally change back to our main working directory.

shutil.copy2(sys.argv[1]+'.bib', "metafiles/")
os.chdir("metafiles/")
bibcmd1 = subprocess.run(
    ['bibtex','-terse',sys.argv[1]+'.aux']
)
os.remove(sys.argv[1]+'.bib')
os.chdir('../')


# This last block runs pdflatex twice, which should now be formatted correctly
# and include the bibliographical data.

pdf2cmd1 = subprocess.run(
    ['pdflatex', '-halt-on-error','-output-directory=metafiles',
     sys.argv[1]+'.tex'], stdout=subprocess.PIPE
)

pdf2cmd2 = subprocess.run(
    ['grep','^!.*','-A200','--color=always'],
    input=pdf2cmd1.stdout
)

pdf3cmd1 = subprocess.run(
    ['pdflatex', '-halt-on-error','-output-directory=metafiles',
    sys.argv[1]+'.tex'],
    stdout=subprocess.PIPE
)

pdf3cmd2 = subprocess.run(
    ['grep','^!.*','-A200','--color=always'],
    input=pdf3cmd1.stdout
)


# Finally, we move the pdf from the metafiles into the main working directory.
# We use replace instead of move because simply moving the file throws an error
# if there is already a file with that name in the working directory. Using
# replace will create the file if there is none with its name in the working
# directory, so nothing to worry about.

os.replace('metafiles/'+sys.argv[1]+'.pdf', './'+sys.argv[1]+'.pdf')
