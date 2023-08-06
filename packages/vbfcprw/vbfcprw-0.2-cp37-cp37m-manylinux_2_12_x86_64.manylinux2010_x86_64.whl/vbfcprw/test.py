import hawkroutines
import numpy


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
# pdf1 = array.array('d',[0, 0.0391232, 0.0541232, 0.0845228, 0.105186,  0.129429,  0.86471,  0.345418, 0.561297, 0.0845228, 0.0541232, 0.0391232, 0])  #from -6 to 6: pdfs for 1st parton
# pdf2 = array.array('d',[0, 0.0143834, 0.0205766, 0.0334123, 0.0462144, 0.0601489, 0.345621, 0.246406, 0.468401, 0.0334123, 0.0205766, 0.0143834, 0])  #from -6 to 6: pdfs for 2nd parton

wedtlin = numpy.array(0.0)
wedtquad = numpy.array(0.0)
ierr = numpy.array(0)

def test():
    hawkroutines.weightdtilde(ecm, mH , npafin,flavour1In,flavour2In,flavour1Out,flavour2Out,flavour3Out,x1,x2,pjet1,pjet2,pjet3,phiggs)
                    # wedtlin,wedtquad,ierr);

    # print(wedtlin, wedtquad, ierr)
