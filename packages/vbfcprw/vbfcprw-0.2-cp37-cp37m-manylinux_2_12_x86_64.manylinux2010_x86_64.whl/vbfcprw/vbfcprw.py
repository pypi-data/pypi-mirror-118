import hawkroutines
import numpy as _numpy
from pylorentz import Momentum4 as _Momentum4
from .pdf import getPDFs2 as _getPDFs2
import vbfcprw.constants as _constants


def _rapidity(lv):
    """
calculate the rapidity of the Lorentz vector lv in z direction
Args:
    lv (pylorentz.Momentum4)
Returns:
    float
"""
    return 0.5*_numpy.log((lv.e+lv.p_z)/(lv.e-lv.p_z))


class WeightDtilde:
    """object-style interface to weightdtilde function"""

    def __init__(self, flavourIn, flavourOut, pjetOut, phiggs):
        """
Args:
    flavourIn (list[int]): flavours of incoming partons in PDG ID
    flavourOut (list[int]): flavours of outgoin partons in PDG ID
    pjetIn (list[numpy.array[float]]): 4-moms of outgoing partons (E, Px, Py, Pz)
    phiggs (numpy.array[float]): 4-mom of Higgs boson (E, Px, Py, Pz)

Returns:
    None
        """
        assert len(flavourIn) == 2
        npafin = len(flavourOut)
        assert npafin == 2 or npafin == 3
        assert len(pjetOut) == npafin

        lv = _Momentum4(*phiggs)
        mH = lv.m
        for pjet in pjetOut:
            lv += _Momentum4(*pjet)
        x1 = lv.m/_constants.ecm*_numpy.exp(_rapidity(lv))
        x2 = lv.m/_constants.ecm*_numpy.exp(-1*_rapidity(lv))

        if npafin == 2:
            flavourOut += [0]
            pjetOut += [_numpy.zeros(4)]

        self.wlin, self.wquad, ierr = weightdtilde(_constants.ecm, mH, npafin,
                                                   *flavourIn,
                                                   *flavourOut,
                                                   x1, x2,
                                                   *pjetOut,
                                                   phiggs)
        if ierr:
            raise RuntimeError("Something wrong in weightdtilde: ierr = %s" % ierr)

    def eventweight(self, dtilde=0):
        return 1 + self.wlin*dtilde + self.wquad*dtilde**2


class OptimalObservable:
    """object style interfacet to optimal observable function"""

    def __init__(self, pjetOut, phiggs):
        """
Args:
    pjetOut (list[numpy.array[float]]): 4-moms of outgoin jets (E, Px, Py, Pz)
    phiggs (numpy.array[float]): 4-mom of Higgs boson (E, Px, Py, Pz)

"""
        assert len(pjetOut) == 2

        lv = _Momentum4(*phiggs)
        mH = lv.m
        if _constants.scale_Q == "mH":
            Q = mH
        else:
            Q = _constants.scale_Q
        for pjet in pjetOut:
            lv += _Momentum4(*pjet)
        x1 = lv.m/_constants.ecm*_numpy.exp(_rapidity(lv))
        x2 = lv.m/_constants.ecm*_numpy.exp(-1*_rapidity(lv))

        # pdfIn (list[_numpy.array[float]]): PDFs of incoming partons
        pdfIn = _getPDFs2(x1, x2, Q)

        # self.oo1, self.oo2, ierr = 1,1,1
        self.oo1, self.oo2, ierr = optobs(_constants.ecm, mH,
                                          x1, x2,
                                          *pdfIn,
                                          *pjetOut,
                                          phiggs)

        if ierr:
            raise RuntimeError("Something wrong in weightdtilde: ierr = %s" % ierr)


# ################################################ #
# 1-to-1 interface to hawkroutines with docstrings #
# ################################################ #

def optobs(ecm, mH, x1, x2, pdf1, pdf2, pjet1, pjet2, phiggs):
    """
wrapper for optobs subroutine in weightandoptobs.f
Args:
    ecm (float): center of mass energy in GeV
    mH (float): Higgs boson mass in GeV
    x1 (float): momentum fraction of incoming parton 1 ((finalstate_tlv.M()/ecm)*TMath::Exp(finalstate_tlv.Rapidity());)
    x2 (float): momentum fraction of incoming parton 2 ((finalstate_tlv.M()/ecm)*TMath::Exp(-1*finalstate_tlv.Rapidity());)
    pdf1 (numpy.array[float]): PDFs of incoming parton 1 from -6 to 6 reprensenting the quark flavours
    pdf2 (numpy.array[float]): PDFs of incoming parton 2 from -6 to 6 reprensenting the quark flavours
    pjet1 (numpy.array): 4-mom of outgoing jet 1 (E, Px, Py, Pz)
    pjet2 (numpy.array): 4-mom of outgoing jet 2 (E, Px, Py, Pz)
    phiggs (numpy.array): 4-mom of Higgs boson (E, Px, Py, Pz)

Returns:
    tuple: (oo1, oo2, ierr) Optimal Observable first order, second order, error code
"""
    return hawkroutines.optobs(ecm, mH,
                               x1, x2,
                               pdf1, pdf2,
                               pjet1, pjet2,
                               phiggs)


def weightdtilde(ecm, mH,
                 npafin,
                 flavour1In, flavour2In,
                 flavour1Out, flavour2Out, flavour3Out,
                 x1, x2,
                 pjet1, pjet2, pjet3, phiggs):
    """
wrapper for the weightdtilde subroutine in weightandoptobs.f

Args:
    ecm (float): center of mass energy in GeV
    mH (float): Higgs boson mass in GeV
    npafin (int): number of partons in final state, 2 or 3 (if 3, the third is gluon)
    flavour1In (int): PDG ID of incoming parton 1, i.e. t = 6  b = 5 c = 4, s = 3, u = 2, d = 1
    flavour2In (int): PDG ID of incoming parton 2
    flavour1Out (int): PDG ID of outgoing parton 1
    flavour2Out (int): PDG ID of outgoing parton 2
    flavour3Out (int): PDG ID of outgoing parton 3
    x1 (float): momentum fraction of incoming parton 1 ((finalstate_tlv.M()/ecm)*TMath::Exp(finalstate_tlv.Rapidity());)
    x2 (float): momentum fraction of incoming parton 2 ((finalstate_tlv.M()/ecm)*TMath::Exp(-1*finalstate_tlv.Rapidity());)
    pjet1 (numpy.array): 4-mom of outgoing parton 1 (E, Px, Py, Pz)
    pjet2 (numpy.array): 4-mom of outgoing parton 2 (E, Px, Py, Pz)
    pjet3 (numpy.array): 4-mom of outgoing parton 3 (E, Px, Py, Pz)
    phiggs (numpy.array): 4-mom of Higgs boson (E, Px, Py, Pz)

Returns:
    tuple: (wedtlin, wedtquad, ierr) linear weight, quadratic weight, error code
"""
    return hawkroutines.weightdtilde(ecm, mH, npafin,
                                     flavour1In,
                                     flavour2In,
                                     flavour1Out,
                                     flavour2Out,
                                     flavour3Out,
                                     x1, x2,
                                     pjet1, pjet2, pjet3,
                                     phiggs)


# TODO interface the reweight subroutines with doc
def reweight(ecm, mH,
             ipara,
             rsmin, din, dbin, dtin, dtbin, lambdahvvin,
             a1hwwin, a2hwwin, a3hwwin, a1haain, a2haain, a3haain, a1hazin, a2hazin, a3hazin, a1hzzin, a2hzzin, a3hzzin,
             npafin,
             flavour1In, flavour2In,
             flavour1Out, flavour2Out, flavour3Out,
             x1, x2,
             pjet1, pjet2, pjet3, phiggs):
    """
wrapper for the reweight subroutine in weightandoptobs.f
Args:
    ecm (float): center of mass energy in GeV
    mH (float): Higgs boson mass in GeV
    ipara = 1 use parametrization in terms of d, db dt, dbt etc. else use parametrization in a1, a2, a3
    anomalous couplings: rsmin,din,dbin,dtin,dtbin, 
        a1hwwin,a2hwwin,a3hwwin,a1haain,a2haain,a3haain,
        a1hazin,a2hazin,a3hazin,a1hzzin,a2hzzin,a3hzzin
        lambdahvvin for formfactor if set to positive value
        set lambdahvvin to negative values in order not to use formfactors
    npafin (int): number of partons in final state, 2 or 3 (if 3, the third is gluon)
    flavour1In (int): PDG ID of incoming parton 1, i.e. t = 6  b = 5 c = 4, s = 3, u = 2, d = 1
    flavour2In (int): PDG ID of incoming parton 2
    flavour1Out (int): PDG ID of outgoing parton 1
    flavour2Out (int): PDG ID of outgoing parton 2
    flavour3Out (int): PDG ID of outgoing parton 3
    x1 (float): momentum fraction of incoming parton 1 ((finalstate_tlv.M()/ecm)*TMath::Exp(finalstate_tlv.Rapidity());)
    x2 (float): momentum fraction of incoming parton 2 ((finalstate_tlv.M()/ecm)*TMath::Exp(-1*finalstate_tlv.Rapidity());)
    pjet1 (numpy.array): 4-mom of outgoing parton 1 (E, Px, Py, Pz)
    pjet2 (numpy.array): 4-mom of outgoing parton 2 (E, Px, Py, Pz)
    pjet3 (numpy.array): 4-mom of outgoing parton 3 (E, Px, Py, Pz)
    phiggs (numpy.array): 4-mom of Higgs boson (E, Px, Py, Pz)

Returns:
    tuple (weight, ierr) event weight to reweight from SM to chosen parameters, error code
"""
    return hawkroutines.reweight(ecm, mH,
                                 ipara,
                                 rsmin, din, dbin, dtin, dtbin, lambdahvvin,
                                 a1hwwin, a2hwwin, a3hwwin, a1haain, a2haain, a3haain, a1hazin, a2hazin, a3hazin, a1hzzin, a2hzzin, a3hzzin,
                                 npafin,
                                 flavour1In, flavour2In,
                                 flavour1Out, flavour2Out, flavour3Out,
                                 x1, x2,
                                 pjet1, pjet2, pjet3, phiggs)
