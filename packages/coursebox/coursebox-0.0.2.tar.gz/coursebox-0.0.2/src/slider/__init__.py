import os
import shutil

from coursebox.thtools_base import execute_command


def latexmk(texfile,pdf_out=None,shell=False,cleanup=False, Linux=False):
    cdir = os.getcwd()
    dname = os.path.dirname(texfile)
    os.chdir(dname)
    texfile = os.path.basename(texfile)
    if Linux:
        CMD = "latexmk -f -g -pdf -interaction=nonstopmode " + texfile
        print("Running LaTeX command>> " + CMD)
        s = execute_command(CMD.split(" "), shell=True)
    else:
        CMD = "latexmk -f -g -pdf -shell-escape -interaction=nonstopmode " + texfile
        print("Running LaTeX command>> " + CMD)
        s = execute_command(CMD.split(" "),shell=True)
    # print("Result of running command: ")
    # print(s)

    if pdf_out:
        shutil.copyfile(texfile[:-4]+".pdf", pdf_out)
    else:
        pdf_out = os.path.join(os.path.dirname(texfile), texfile[:-4]+".pdf")

    if cleanup and os.path.exists(pdf_out):
        bft = ['bbl', 'blg', 'fdb_latexmk', 'fls', 'aux', 'synctex.gz', 'log']
        for ex in bft:
            import glob
            fl = glob.glob(dname + "/*."+ex)
            for f in fl:
                os.remove(f)

    os.chdir(cdir)
    return pdf_out