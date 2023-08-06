import parton as _parton
import numpy as _numpy
import pkg_resources as _pkg_resources

pdfdir = _pkg_resources.resource_filename(__name__, "data")
# pdfdir = "."

# TODO try this and print error when not available
# pdf = parton.mkPDF(name='CT10', member=0, pdfdir=pdfdir)

PDF = None


def init_PDF():
    global PDF
    PDF = _parton.mkPDF(name='CT10', member=0, pdfdir=pdfdir)
    return PDF


try:
    PDF = init_PDF()
except ValueError as e:
    print(f"{e}")
    print("Install the CT10 PDF set in your working dir or specify in vbfcprw.pdf.pdfdir e.g. by:")
    print("wget -qO- http://lhapdfsets.web.cern.ch/lhapdfsets/current/CT10.tar.gz| tar xvz -C .")
    print("and call vbfcprw.pdf.init_PDF() again yourself.")


def getPDFs(x1, x2, Q):
    # pre- and appending 0s for top quarks
    pdf1 = _numpy.array([0]+[PDF.xfxQ(flavor, x1, Q) for flavor in range(-5, 6)]+[0])
    pdf2 = _numpy.array([0]+[PDF.xfxQ(flavor, x2, Q) for flavor in range(-5, 6)]+[0])
    pdfIn = [pdf1, pdf2]
    return pdfIn


def getPDFs2(x1, x2, Q):
    """
this function is 30% faster than the one above
    """
    x = _numpy.array([x1, x2])
    flavors = _numpy.arange(-6, 7)

    def protect_top(f):
        if abs(f) == 6:
            return _numpy.zeros(2).reshape(2, 1)
        else:
            return PDF.xfxQ(f, x, Q)

    pdfOut = _numpy.concatenate([protect_top(f) for f in flavors], axis=1)
    return pdfOut
