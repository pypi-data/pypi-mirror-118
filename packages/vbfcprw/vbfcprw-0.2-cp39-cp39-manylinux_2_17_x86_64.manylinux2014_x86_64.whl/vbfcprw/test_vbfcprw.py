from vbfcprw import weightdtilde, reweight
from vbfcprw import WeightDtilde, OptimalObservable
import numpy
import hawkroutines

pjet1 = numpy.array([438.019730, -24.873165, -94.306022, 427.023386])               # E,px,py,pz of nth final state parton
pjet2 = numpy.array([656.475632, -55.150478, 66.466227, -650.769506])
pjet3 = numpy.array([51.082110, 25.871174, 3.770224, 43.884504])
phiggs= numpy.array([177.080599, 54.152473, 24.069573, -110.547404])            # E,px,py,pz of Higgs boson make sure that four-momentum conservation holds 
ecm = 13000.;                           #proton-proton center-of mass energy in GeV
mH = 124.999901;                       #mass of Higgs boson in Gev
npafin = 3;                            #number of partons in final state  either  2 or 3
x1 = 0.072082;                  #Bjorken x of incoming partons, 1 in + z , 2 in -z direction
x2 = 0.123500;
Q = 84000;
flavour1In = -2;                          #flavour of incoming/outgoing parton n
flavour2In = 2;                           #flavour assignment: t = 6  b = 5 c = 4, s = 3, u = 2, d = 1   
flavour1Out = -2;                         #anti-qarks with negative sign
flavour2Out = 2;                          #gluon = 0 
flavour3Out = 0;
eventNumber = 1234;

# Only used when ran without the Event-store:
pdf1 = numpy.array([0, 0.0391232, 0.0541232, 0.0845228, 0.105186,  0.129429,  0.86471,  0.345418, 0.561297, 0.0845228, 0.0541232, 0.0391232, 0])  #from -6 to 6: pdfs for 1st parton
pdf2 = numpy.array([0, 0.0143834, 0.0205766, 0.0334123, 0.0462144, 0.0601489, 0.345621, 0.246406, 0.468401, 0.0334123, 0.0205766, 0.0143834, 0])  #from -6 to 6: pdfs for 2nd parton


def test_hawkroutines():
    wdt = hawkroutines.weightdtilde(ecm, mH,
                                    npafin,
                                    flavour1In, flavour2In,
                                    flavour1Out, flavour2Out, flavour3Out,
                                    x1, x2,
                                    pjet1, pjet2, pjet3, phiggs)
    assert wdt == (4.054467923118412, 32.29038008003971, 0)


def test_weightdtilde():
    wdt = weightdtilde(ecm, mH,
                       npafin,
                       flavour1In, flavour2In,
                       flavour1Out, flavour2Out, flavour3Out,
                       x1, x2,
                       pjet1, pjet2, pjet3, phiggs)
    assert wdt == (4.054467923118412, 32.29038008003971, 0)


def test_WeightDtilde():
    w = WeightDtilde([flavour1In, flavour2In],
                     [flavour1Out, flavour2Out, flavour3Out],
                     [pjet1, pjet2, pjet3],
                     phiggs)
    assert (w.wlin, w.wquad) == (4.3491101342370975, 33.902164911953044)


def test_OptimalObservable():
    oo = OptimalObservable([pjet1, pjet2], phiggs)
    assert (oo.oo1, oo.oo2) == (2.49182772173305, 10.750636222825886)


def test_reweight():
    w = reweight(ecm, mH,
                 1,                        # ipara: 1 for parametrisation in d and dt, else a1, a2, a3
                 0.5, 0.5, 0.5, 0.5, 0.5,  # rsmin,din,dbin,dtin,dtbin 
                 0.5,                      # lambdahvvin for formfactor if set to positive value 
                 0.5, 0.5, 0.5,            # a1hwwin,a2hwwin,a3hwwin 
                 0.5, 0.5, 0.5,            # a1haain,a2haain,a3haain 
                 0.5, 0.5, 0.5,            # a1hazin,a2hazin,a3hazin 
                 0.5, 0.5, 0.5,            # a1hzzin,a2hzzin,a3hzzin 
                 npafin,
                 flavour1In, flavour2In,
                 flavour1Out, flavour2Out, flavour3Out,
                 x1, x2,
                 pjet1, pjet2, pjet3, phiggs)
    assert w == (0.24999999978856272, 0)
