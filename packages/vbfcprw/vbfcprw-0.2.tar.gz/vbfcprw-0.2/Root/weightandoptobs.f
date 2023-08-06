*************************************************************************
      subroutine weightdtilde(ecms,mhiggs,
     +     npafin,iflin1,iflin2,iflout1,iflout2,iflout3,  
     +     x1,x2,pjet1,pjet2,pjet3,phiggs,
     +     wedtlin,wedtquad,ierr) 
*************************************************************************
C      input: ecms proton-proton center-of mass energy in GeV 
C             mhiggs mass of Higgs boson in Gev
C
C             npafin:   number of partons in final state  either  2 or 3 
C             ifl1in:   flavour of incoming parton 1  
C             ifl2in:   flavour of incoming parton 2
C             ifl1out:  flavour of outgoing parton 1  
C             ifl2out:  flavour of outgoing parton 2
C             ifl3out:  flavour of outgoing parton 3
C
C             flavour assignment: t = 6  b = 5 c = 4, s = 3, u = 2, d = 1   
C                                 anti-qarks with negative sign
C                                 gluon = 0 
C   
C             x1, x2:   Bjorken x of incoming partons,  
C                       1 in + z , 2 in -z direction
C             pjet1(0:3):  E,px,py,pz of 1st final state parton
C             pjet2(0:3):  E,px,py,pz of 2nd final state parton 
C             pjet3(0:3):  E,px,py,pz of 3rd final state parton 
C                          if npafin=3.  gluon should be 3rd parton
C             phiggs(0:3): E,px,py,pz of Higgs boson
C             make sure that four-momentum conservation holds 
C------------------------------------------------------------------------
C     output:
C
C     wedtlin, wedtquad  (contributions to event weight) 
C     weight is decoposed as: weight = 1 + dtilde wedtline + dtilde^2 wedtquad
C     the weight is calculated under the assumption dtilde=detilde_b and
C     all other anomalous couplings/ Wilson coefficients asumed to vanish  
C
C     ierr: error flag
C     if ierr <> 0 default value of -99 will be returned
C     ierr: 0 all ok, some problem if <> 0   
C------------------------------------------------------------------------
C     author: Markus Schumacher  4. December 2016
C             based on subrotine reweight. 
C
C     modification log: 
*************************************************************************
      implicit none
      integer ihelp
      real*8 phelp(0:3)
C input variables
      real*8 rsmin,din,dbin,dtin,dtbin,lambdahvvin
      real*8 a1hwwin,a2hwwin,a3hwwin,a1haain,a2haain,a3haain
      real*8 a1hazin,a2hazin,a3hazin,a1hzzin,a2hzzin,a3hzzin
      real*8 ecms,mhiggs,x1,x2
      real*8 pjet1(0:3),pjet2(0:3),pjet3(0:3),phiggs(0:3)
      integer npafin,iflin1,iflin2,iflout1,iflout2,iflout3
C output variables
      integer ierr
      real*8 wedtlin,wedtquad
Cf2py intent(out) ierr, wedtlin, wedtquad
C some other variables for internal use
      integer ipara,i1,i2,i,j,k,l,idebug
      real*8 m2sm,m2full,m2cpo
C variables given to HAWK
      real*8 xp1,xp2,p(6,0:3)
      real*8 m2i(-5:5,-5:5),m2if(-5:5,-5:5,-5:5,-5:5)
      real*8 m2i_gluon(-5:5,-5:5),m2if_gluon(-5:5,-5:5,-5:5,-5:5)
C HAWK parameters and flags
      integer qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &     qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &     qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
      common/rcoptions/qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &     qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &     qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
C
      real*8 pi,el,alpha,alpha0,alphaz,GF,alphas
      real*8 cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2
      real*8 ml,ml2,mqp,mqp2,mqm,mqm2
C
      complex*16 v,cv
      common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &     v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &     ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
C     
      real*8 sinthetac
      real*8 ppecms
      common/ppecms/ppecms
C
      complex*16 ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
      common/cparam/ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
C
      complex*16 xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null
      complex*16 xml,xml2,xmqp,xmqp2,xmqm,xmqm2
C
      common/xparam/xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null, 
     &     xml(3),xml2(3),xmqp(3),xmqp2(3),xmqm(3),xmqm2(3) 
C
      real*8 qu,qd,ql,qn,qf,mu,mu2,md,md2,mlep,mlep2
      complex*16 guu,gdd,gnn,gll     
      common/qf/qu,qd,ql,qn,qf(4),mu,mu2,md,md2,mlep,mlep2,
     +     guu(-1:1),gdd(-1:1),gnn(-1:1),gll(-1:1)
C
      integer qhvv
C
      real*8 rsm,d,db,dt,dtb,lambdahvv
      real*8 a1hww,a2hww,a3hww,a1haa,a2haa,a3haa
      real*8 a1haz,a2haz,a3haz,a1hzz,a2hzz,a3hzz
      common/hvv/rsm,d,db,dt,dtb,lambdahvv,
     &     a1hww,a2hww,a3hww,a1haa,a2haa,a3haa,
     &     a1haz,a2haz,a3haz,a1hzz,a2hzz,a3hzz,qhvv
C
      idebug = 0
C initialise output values     
      wedtlin  = -99.0d0        ! default value if something fails
      wedtquad = -99.0d0        ! default value if something fails
      ierr   =  99
C check some conditions to avoid crashes
      if (npafin.lt.2.or.npafin.gt.3) then
         write(*,*)" Bad number of final state partons ",npafin
         return
      endif
      if (x1.gt.1.0d0.or.x1.lt.0.0d0) then
         write(*,*)" Bjporken x1 bad ",x1
         return
      endif
      if (x2.gt.1.0d0.or.x2.lt.0.0d0) then
         write(*,*)" Bjporken x2 bad ",x2
         return
      endif
      if (phiggs(0).lt.0.0d0) then
         write(*,*)" Higgs energy < 0",phiggs(0)
         return
      endif
      if (pjet1(0).lt.0.0d0) then
         write(*,*)" 1st parton energy < 0",pjet1(0)
         return
      endif
      if (pjet2(0).lt.0.0d0) then
         write(*,*)" 2nd parton energy < 0",pjet2(0)
         return
      endif
      if (pjet3(0).lt.0.0d-20.and.npafin.eq.3) then
         write(*,*)" 3rd parton energy < 0",pjet3(0)
         return
      endif
C copy c-o-m energies and Higgs boson mass
      ppecms = ecms            
      mh   = mhiggs            
C copy anamoalous couplings to Hawk couplings 
      rsm       = 1. ! rsmin
      d         = 0.0
      db        = 0.0 
      dt        = 1.0
      dtb       = 1.0
      lambdahvv = - 100. ! no form factor
      a1hww     = 0.0d0
      a2hww     = 0.0d0
      a3hww     = 0.0d0
      a1haa     = 0.0d0
      a2haa     = 0.0d0
      a3haa     = 0.0d0
      a1haz     = 0.0d0
      a2haz     = 0.0d0
      a3haz     = 0.0d0
      a1hzz     = 0.0d0
      a2hzz     = 0.0d0
      a3hzz     = 0.0d0
C copy Bjorken x and construct 4-momenta of incoming partons
      xp1=x1                    
      xp2=x2                    
      p(1,0) = xp1*ppecms/2.0d0
      p(1,1) = 0.0d0
      p(1,2) = 0.0d0
      p(1,3) = xp1*ppecms/2.0d0

      p(2,0) = xp2*ppecms/2.0d0
      p(2,1) = 0.0d0
      p(2,2) = 0.0d0
      p(2,3) = -xp2*ppecms/2.0d0
C set Hawk flags and pars for reweighting
      call sethawkpars(1,1)
      if (npafin.eq.2) then
C     two parton final state
C     construct 4-momenta of Higgs bosons and outgoing partons    
         do I = 0,3
            p(3,i) = pjet1(i)
            p(4,i) = pjet2(i)
            p(5,i) = phiggs(i)
            p(6,i) = 0.0d0
         enddo
C Markus 15 July change: if q anti-q --> anti-q q + H  or c-conjugated 
C                        then reverse order of outgoging partons
C        23 July: implement missing do loop over 4 vector components
         if (iflin1*iflin2.lt.0) then
C            write (*,*)'change order'
            if (iflin1*iflout1.lt.0.or.iflin2*iflout2.lt.0) then
               ihelp = iflout2 
               iflout2= iflout1
               iflout1 = ihelp
               do I = 0,3 !new 23 July
                  p(3,i) = pjet2(i)
                  p(4,i) = pjet1(i)
               enddo ! new 23 July
            endif
         endif
C Markus 15 July change: end
C     SM maxtrix elements
         qhvv = 0 
         call Mat2born0(p,m2i,m2if,1)
         m2sm = m2if(iflin1,iflin2,iflout1,iflout2)
C         write(*,*)'msmsm test',m2if(iflin1,iflin2,iflout1,iflout2)
C     anomalous coupling matrix elements
         qhvv = 1 
         call Mat2born0(p,m2i,m2if,1)
         m2full = m2if(iflin1,iflin2,iflout1,iflout2)
C get pure CP-odd matrix elements
         qhvv  = 1
         a1hww = 0d0
         a1hzz = 0D0
         call Mat2born0(p,m2i,m2if,1)
         m2cpo = m2if(iflin1,iflin2,iflout1,iflout2)
      endif
      
C-----------------------------------------------------------------------
      if (npafin.eq.3) then
C transform bottom in strange quarks as no b-quark ME evaluetd for 
C 3 parton final state
      if (abs(iflin1).eq.5) iflin1 = 3 * iflin1/abs(iflin1)
      if (abs(iflin2).eq.5) iflin2 = 3 * iflin2/abs(iflin2)
      if (abs(iflout1).eq.5) iflout1 = 3 * iflout1/abs(iflout1)
      if (abs(iflout2).eq.5) iflout2 = 3 * iflout2/abs(iflout2)
      if (abs(iflout3).eq.5) iflout3 = 3 * iflout3/abs(iflout3)
C     three parton final state
         if (iflin1*iflin2.ne.0) then
C     no gluon in intial state
C     parton1(p1) + parton2(p2) --> f(p3) + f'(p4) + H(p5) + gluon(p6)
C     construct 4-momenta of Higgs bosons and outgoing partons    
            if (iflout3.eq.0) then
               if (iflin1*iflout1.lt.0) then
                  ihelp = iflout2 
                  iflout2= iflout1
                  iflout1 = ihelp
                  do I = 0,3
                     phelp(i) = pjet2(i)
                     pjet2(i) = pjet1(i)
                     pjet1(i) = phelp(i)
                  enddo
C                  write (*,*)'changed to  process ',iflin1,' + '
C     +                 ,iflin2,' --> ',
C     +                 iflout1,' + ',iflout2,' + ',iflout3
               endif
               do I = 0,3
                  p(3,i) = pjet1(i)
                  p(4,i) = pjet2(i)
                  p(5,i) = phiggs(i)
                  p(6,i) = pjet3(i)
               enddo
C     SM matrix elements
               qhvv = 0 
               call Mat2gluon_out(p,m2i_gluon,m2if_gluon)
C
               m2sm = m2if_gluon(iflin1,iflin2,iflout1,iflout2)
C               write(*,*)'mat2 qqgluon in SM',m2sm
C     anomalous coupling matrix elements
               qhvv = 1 
               call Mat2gluon_out(p,m2i_gluon,m2if_gluon)
               m2full = m2if_gluon(iflin1,iflin2,iflout1,iflout2)
C               write(*,*)'mat2 qqgluon in EFT',m2full
C     get pure CP-odd matrix elements
               qhvv  = 1
               a1hww = 0d0
               a1hzz = 0D0
C
               call Mat2gluon_out(p,m2i_gluon,m2if_gluon)
               m2cpo = m2if_gluon(iflin1,iflin2,iflout1,iflout2)
C
            elseif (iflout2.eq.0) then
               if (iflin1*iflout1.lt.0) then
                  ihelp = iflout3 
                  iflout3= iflout1
                  iflout1 = ihelp
                  do I = 0,3
                     phelp(i) = pjet3(i)
                     pjet3(i) = pjet1(i)
                     pjet1(i) = phelp(i)
                  enddo
C                  write (*,*)'changed to  process ',iflin1,' + '
C     +                 ,iflin2,' --> ',
C     +                 iflout1,' + ',iflout3,' + ',iflout2
               endif
               do I = 0,3
                  p(3,i) = pjet1(i)
                  p(4,i) = pjet3(i)
                  p(5,i) = phiggs(i)
                  p(6,i) = pjet2(i)
               enddo
C     SM matrix elements
              qhvv = 0 
               call Mat2gluon_out(p,m2i_gluon,m2if_gluon)
               m2sm = m2if_gluon(iflin1,iflin2,iflout1,iflout3)
C     anomalous coupling matrix elements
               qhvv = 1 
               call Mat2gluon_out(p,m2i_gluon,m2if_gluon)
               m2full = m2if_gluon(iflin1,iflin2,iflout1,iflout3)
C     get pure CP-odd matrix elements
               qhvv  = 1
               a1hww = 0d0
               a1hzz = 0D0
               call Mat2gluon_out(p,m2i_gluon,m2if_gluon)
               m2cpo = m2if_gluon(iflin1,iflin2,iflout1,iflout3)
            elseif (iflout1.eq.0) then
               if (iflin1*iflout2.lt.0) then
                  ihelp = iflout3 
                  iflout3= iflout2
                  iflout2 = ihelp
                  do I = 0,3
                     phelp(i) = pjet3(i)
                     pjet3(i) = pjet2(i)
                     pjet2(i) = phelp(i)
                  enddo
C                  write (*,*)'changed to  process ',iflin1,' + '
C     +                 ,iflin2,' --> ',
C     +                 iflout1,' + ',iflout3,' + ',iflout2
               endif
               do I = 0,3
                  p(3,i) = pjet2(i)
                  p(4,i) = pjet3(i)
                  p(5,i) = phiggs(i)
                  p(6,i) = pjet1(i)
               enddo
C     SM matrix elements
               qhvv = 0 
               call Mat2gluon_out(p,m2i_gluon,m2if_gluon)
               m2sm = m2if_gluon(iflin1,iflin2,iflout2,iflout3)
C     anomalous coupling matrix elements
               qhvv = 1 
               call Mat2gluon_out(p,m2i_gluon,m2if_gluon)
               m2full = m2if_gluon(iflin1,iflin2,iflout2,iflout3)
C     get pure CP-odd matrix elements
               qhvv  = 1
               a1hww = 0d0
               a1hzz = 0D0
               call Mat2gluon_out(p,m2i_gluon,m2if_gluon)
               m2cpo = m2if_gluon(iflin1,iflin2,iflout2,iflout3)
            else
               write(*,*)" non valid flavour combination!"
               return
            endif
         endif
C     gluon in intial state 
         if (iflin1.eq.0) then
C     gluon(p1) + q(p2)    --> q'(p3)    + q''(p4) + H(p5) + q'''bar(p6)
            if (iflin2.gt.0) then
               if (iflout3.lt.0) then
                  do I = 0,3
                     p(3,i) = pjet1(i)
                     p(4,i) = pjet2(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet3(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin2,iflout1,iflout2,iflout3)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin2,iflout1,iflout2,iflout3)
C     get pure CP-odd matrix elements
                  qhvv  = 1
                  a1hww = 0d0
                  a1hzz = 0D0
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2cpo = m2if_gluon(iflin2,iflout1,iflout2,iflout3)
C
               elseif (iflout2.lt.0) then
C     gluon(p1) + qbar(p2) --> q'bar(p3) + q''bar(p4) + H(p5) + q'''(p6)
                  do I = 0,3
                     p(3,i) = pjet1(i)
                     p(4,i) = pjet3(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet2(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin2,iflout1,iflout3,iflout2)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin2,iflout1,iflout3,iflout2)
C     get pure CP-odd matrix elements
                  qhvv  = 1
                  a1hww = 0d0
                  a1hzz = 0D0
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2cpo = m2if_gluon(iflin2,iflout1,iflout3,iflout2)
               elseif (iflout1.lt.0) then
                  do I = 0,3
                     p(3,i) = pjet2(i)
                     p(4,i) = pjet3(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet1(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin2,iflout2,iflout3,iflout1)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin2,iflout2,iflout3,iflout1)
                  qhvv  = 1
                  a1hww = 0d0
                  a1hzz = 0D0
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2cpo = m2if_gluon(iflin2,iflout2,iflout3,iflout1)
               else
                  write(*,*)" non valid flavour combination!"
                  return
               endif
            else
C     gluon(p1) + qbar(p2) --> q'bar(p3) + q''bar(p4) + H(p5) + q'''(p6)
               if (iflout3.gt.0) then
                  do I = 0,3
                     p(3,i) = pjet1(i)
                     p(4,i) = pjet2(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet3(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin2,iflout1,iflout2,iflout3)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin2,iflout1,iflout2,iflout3)
                  qhvv  = 1
                  a1hww = 0d0
                  a1hzz = 0D0
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2cpo = m2if_gluon(iflin2,iflout1,iflout2,iflout3)
               elseif (iflout2.gt.0) then
                  do I = 0,3
                     p(3,i) = pjet1(i)
                     p(4,i) = pjet3(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet2(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin2,iflout1,iflout3,iflout2)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin2,iflout1,iflout3,iflout2)
C     pre CP oddd
                  qhvv  = 1
                  a1hww = 0d0
                  a1hzz = 0D0
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2cpo = m2if_gluon(iflin2,iflout1,iflout3,iflout2)
               elseif (iflout1.gt.0) then
                  do I = 0,3
                     p(3,i) = pjet2(i)
                     p(4,i) = pjet3(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet1(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin2,iflout2,iflout3,iflout1)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin2,iflout2,iflout3,iflout1)
C     pure CP odd
                  qhvv  = 1
                  a1hww = 0d0
                  a1hzz = 0D0
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2cpo = m2if_gluon(iflin2,iflout2,iflout3,iflout1)
               else
                  write(*,*)" non valid flavour combination"
                  return
               endif 
            endif ! anti-quark or quark is 2nd  incoming
         endif ! gluon is 1st  incoming
C 2nd incoming parton is gluon
         if (iflin2.eq.0) then
            if (iflin1.gt.0) then
C     q(p1)    + gluon(p2) --> q'(p3)    + q''(p4) + H(p5) + q'''bar(p6)
               if (iflout3.lt.0) then
                  do I = 0,3
                     p(3,i) = pjet1(i)
                     p(4,i) = pjet2(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet3(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin1,iflout1,iflout2,iflout3)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin1,iflout1,iflout2,iflout3)
C     pure CP odd
                  qhvv  = 1
                  a1hww = 0d0
                  a1hzz = 0D0
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2cpo = m2if_gluon(iflin1,iflout1,iflout2,iflout3)
               elseif (iflout2.lt.0) then
                  do I = 0,3
                     p(3,i) = pjet1(i)
                     p(4,i) = pjet3(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet2(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin1,iflout1,iflout3,iflout2)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin1,iflout1,iflout3,iflout2)
C     pure CP odd
                  qhvv  = 1
                  a1hww = 0d0
                  a1hzz = 0D0
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2cpo = m2if_gluon(iflin1,iflout1,iflout3,iflout2)
               elseif (iflout1.lt.0) then
                  do I = 0,3
                     p(3,i) = pjet2(i)
                     p(4,i) = pjet3(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet1(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin1,iflout2,iflout3,iflout1)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin1,iflout2,iflout3,iflout1)
C     pure CP odd
                  qhvv  = 1
                  a1hww = 0d0
                  a1hzz = 0D0
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2cpo = m2if_gluon(iflin1,iflout2,iflout3,iflout1)
               else
                  write(*,*)" non valid flavour combination!"
                  return
               endif
            else
C     qbar(p1) + gluon(p2) --> q'bar(p3) + q''bar(p4) + H(p5) + q'''(p6)
C      write(*,*)"qb(p1) + gl(p2) --> q'b(p3) + q2b(p4) + H(p5) + q3(p6)"
                 if (iflout3.gt.0) then
                  do I = 0,3
                     p(3,i) = pjet1(i)
                     p(4,i) = pjet2(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet3(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin1,iflout1,iflout2,iflout3)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin1,iflout1,iflout2,iflout3)
C     pure CP odd
                  qhvv  = 1
                  a1hww = 0d0
                  a1hzz = 0D0
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2cpo = m2if_gluon(iflin1,iflout1,iflout2,iflout3)
               elseif (iflout2.gt.0) then
C
                  do I = 0,3
                     p(3,i) = pjet1(i)
                     p(4,i) = pjet3(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet2(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin1,iflout1,iflout3,iflout2)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin1,iflout1,iflout3,iflout2)
C     pure CP odd
                  qhvv  = 1
                  a1hww = 0d0
                  a1hzz = 0D0
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2cpo = m2if_gluon(iflin1,iflout1,iflout3,iflout2)
               elseif (iflout1.gt.0) then
                  do I = 0,3
                     p(3,i) = pjet2(i)
                     p(4,i) = pjet3(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet1(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin1,iflout2,iflout3,iflout1)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin1,iflout2,iflout3,iflout1)
C     pure CP odd
                  qhvv  = 1
                  a1hww = 0d0
                  a1hzz = 0D0
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2cpo = m2if_gluon(iflin1,iflout2,iflout3,iflout1)
               else
                  write(*,*)" non valid flavour combination"
                  return
               endif
            endif ! 1st incoming quark or antiquark
         endif !gluon is 2nd incoming
      endif  ! npafin.eq.3
C check SM matrix element 
      if (m2sm.lt.1.0d-20) then
         write(*,*)" M2SM<10-20 ",m2sm
         return
      endif
C     M2full = MSM2 + dtilde 2 RE(MSMMCP) + dtilde1^2 MCP2
C     devide by M2SM      
C     weight = 1    + dtilde wedtlin      + dtilde^2  wedtquad
C     calculate weight contributions
      wedtlin  = (M2full-m2sm-m2cpo)/m2sm
      wedtquad =  m2cpo/m2sm
C everything seems ok 
      ierr = 0 
      return
      end
*************************************************************************
      subroutine reweight(ecms,mhiggs,ipara,rsmin,
     +     din,dbin,dtin,dtbin,lambdahvvin,
     +     a1hwwin,a2hwwin,a3hwwin,a1haain,a2haain,a3haain,
     +     a1hazin,a2hazin,a3hazin,a1hzzin,a2hzzin,a3hzzin,
     +     npafin,iflin1,iflin2,iflout1,iflout2,iflout3,  
     +     x1,x2,pjet1,pjet2,pjet3,phiggs,weight,ierr) 
*************************************************************************
C      input: ecms proton-pton center-of mass energy in GeV 
C             mhiggs mass of Higgs boson in Gev
C             ipara = 1 use parametrization in terms of d, db dt, dbt etc.
C                     else use parametrization in a1, a2, a3
C             anomalous couplings: rsmin,din,dbin,dtin,dtbin, 
C             a1hwwin,a2hwwin,a3hwwin,a1haain,a2haain,a3haain,
C             a1hazin,a2hazin,a3hazin,a1hzzin,a2hzzin,a3hzzin
C             lambdahvvin for formfactor if set to positive value
C             set lambdahvvin to negative values in ordr no to use formfactors
C
C             npafin:   number of partons in final state  either  2 or 3 
C             ifl1in:   flavour of incoming parton 1  
C             ifl2in:   flavour of incoming parton 2
C             ifl1out:  flavour of outgoing parton 1  
C             ifl2out:  flavour of outgoing parton 2
C             ifl3out:  flavour of outgoing parton 3
C
C             flavour assignment: t = 6  b = 5 c = 4, s = 3, u = 2, d = 1   
C                                 anti-qarks with negative sign
C                                 gluon = 0 
C   
C             x1, x2:   Bjorken x of incoming partons,  
C                       1 in + z , 2 in -z direction
C             pjet1(0:3):  E,px,py,pz of 1st final state parton
C             pjet2(0:3):  E,px,py,pz of 2nd final state parton 
C             pjet3(0:3):  E,px,py,pz of 3rd final state parton 
C                          if npafin=3.  gluon should be 3rd parton
C             phiggs(0:3): E,px,py,pz of Higgs boson
C             make sure that for momentum conservation holds 
C------------------------------------------------------------------------
C      output: weight - weight for reweighting from SM 
C                       to anomalous coupling choice 
C                       if ierr <> 0 default value of -99 will be returned
C              ierr: 0 all ok, some problem if <> 0   
C------------------------------------------------------------------------
C     author: Markus Schumacher  22. March 2015
C  
C     modification log: 24. March 2015
C                       separate setting Hawk pars in new routine
C                       correct description of flavour assignment 
C                       clean up code and put in some comments       
C
C                       3-5 April 2015:
C                       fix bug concerning ordering of four vector 
C                       for processes with gluons in initial state.
C                       allow for arbitrary ordering of outgoing
C                       flavours in in put list. Do correct odering
C                       in this routine internally.
C
C                       15. July 2015
C                       ordering of inputs / output partons for 2-->2+H 
C                       corrected.
C                       for some combination SM matrix elements of zero
C                       23. July 2015
C                       fix small bug in the implemnetation change from 15 July
*************************************************************************
      implicit none
      integer ihelp
      real*8 phelp(0:3)
C input variables
      real*8 rsmin,din,dbin,dtin,dtbin,lambdahvvin
      real*8 a1hwwin,a2hwwin,a3hwwin,a1haain,a2haain,a3haain
      real*8 a1hazin,a2hazin,a3hazin,a1hzzin,a2hzzin,a3hzzin
      real*8 ecms,mhiggs,x1,x2
      real*8 pjet1(0:3),pjet2(0:3),pjet3(0:3),phiggs(0:3)
      integer npafin,iflin1,iflin2,iflout1,iflout2,iflout3
C output variables
      integer ierr
      real*8 weight
Cf2py intent(out) ierr, weight
C some other variables for internal use
      integer ipara,i1,i2,i,j,k,l,idebug
      real*8 m2sm,m2full
C variables given to HAWK
      real*8 xp1,xp2,p(6,0:3)
      real*8 m2i(-5:5,-5:5),m2if(-5:5,-5:5,-5:5,-5:5)
      real*8 m2i_gluon(-5:5,-5:5),m2if_gluon(-5:5,-5:5,-5:5,-5:5)
C HAWK parameters and flags
      integer qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &     qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &     qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
      common/rcoptions/qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &     qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &     qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
C
      real*8 pi,el,alpha,alpha0,alphaz,GF,alphas
      real*8 cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2
      real*8 ml,ml2,mqp,mqp2,mqm,mqm2
C
      complex*16 v,cv
      common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &     v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &     ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
C     
      real*8 sinthetac
      real*8 ppecms
      common/ppecms/ppecms
C
      complex*16 ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
      common/cparam/ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
C
      complex*16 xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null
      complex*16 xml,xml2,xmqp,xmqp2,xmqm,xmqm2
C
      common/xparam/xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null, 
     &     xml(3),xml2(3),xmqp(3),xmqp2(3),xmqm(3),xmqm2(3) 
C
      real*8 qu,qd,ql,qn,qf,mu,mu2,md,md2,mlep,mlep2
      complex*16 guu,gdd,gnn,gll     
      common/qf/qu,qd,ql,qn,qf(4),mu,mu2,md,md2,mlep,mlep2,
     +     guu(-1:1),gdd(-1:1),gnn(-1:1),gll(-1:1)
C
      integer qhvv
C
      real*8 rsm,d,db,dt,dtb,lambdahvv
      real*8 a1hww,a2hww,a3hww,a1haa,a2haa,a3haa
      real*8 a1haz,a2haz,a3haz,a1hzz,a2hzz,a3hzz
      common/hvv/rsm,d,db,dt,dtb,lambdahvv,
     &     a1hww,a2hww,a3hww,a1haa,a2haa,a3haa,
     &     a1haz,a2haz,a3haz,a1hzz,a2hzz,a3hzz,qhvv
C
      idebug = 0
C initialise output values     
      weight = -99.0d0 ! default value if something fails
      ierr   =  99
C check some conditions to avoid crashes
      if (npafin.lt.2.or.npafin.gt.3) then
         write(*,*)" Bad number of final state partons ",npafin
         return
      endif
      if (x1.gt.1.0d0.or.x1.lt.0.0d0) then
         write(*,*)" Bjporken x1 bad ",x1
         return
      endif
      if (x2.gt.1.0d0.or.x2.lt.0.0d0) then
         write(*,*)" Bjporken x2 bad ",x2
         return
      endif
      if (phiggs(0).lt.0.0d0) then
         write(*,*)" Higgs energy < 0",phiggs(0)
         return
      endif
      if (pjet1(0).lt.0.0d0) then
         write(*,*)" 1st parton energy < 0",pjet1(0)
         return
      endif
      if (pjet2(0).lt.0.0d0) then
         write(*,*)" 2nd parton energy < 0",pjet2(0)
         return
      endif
      if (pjet3(0).lt.0.0d-20.and.npafin.eq.3) then
         write(*,*)" 3rd parton energy < 0",pjet3(0)
         return
      endif
C copy c-o-m energies and Higgs boson mass
      ppecms = ecms            
      mh   = mhiggs            
C copy anamoalous couplings to Hawk couplings 
      rsm       = rsmin
      d         = din
      db        = dbin
      dt        = dtin
      dtb       = dtbin
      lambdahvv = lambdahvvin
      a1hww     = a1hwwin
      a2hww     = a2hwwin
      a3hww     = a3hwwin
      a1haa     = a1haain
      a2haa     = a2haain
      a3haa     = a3haain
      a1haz     = a1hazin
      a2haz     = a2hazin
      a3haz     = a3hazin
      a1hzz     = a1hzzin
      a2hzz     = a2hzzin
      a3hzz     = a3hzzin
C copy Bjorken x and construct 4-momenta of incoming partons
      xp1=x1                    
      xp2=x2                    
      p(1,0) = xp1*ppecms/2.0d0
      p(1,1) = 0.0d0
      p(1,2) = 0.0d0
      p(1,3) = xp1*ppecms/2.0d0

      p(2,0) = xp2*ppecms/2.0d0
      p(2,1) = 0.0d0
      p(2,2) = 0.0d0
      p(2,3) = -xp2*ppecms/2.0d0
C set Hawk flags and pars for reweighting
      call sethawkpars(1,ipara)
      if (npafin.eq.2) then
C     two parton final state
C     construct 4-momenta of Higgs bosons and outgoing partons    
         do I = 0,3
            p(3,i) = pjet1(i)
            p(4,i) = pjet2(i)
            p(5,i) = phiggs(i)
            p(6,i) = 0.0d0
         enddo
C Markus 15 July change: if q anti-q --> anti-q q + H  or c-conjugated 
C                        then reverse order of outgoging partons
C        23 July: implement missing do loop over 4 vector components
         if (iflin1*iflin2.lt.0) then
C            write (*,*)'change order'
            if (iflin1*iflout1.lt.0.or.iflin2*iflout2.lt.0) then
               ihelp = iflout2 
               iflout2= iflout1
               iflout1 = ihelp
               do I = 0,3 !new 23 July
                  p(3,i) = pjet2(i)
                  p(4,i) = pjet1(i)
               enddo ! new 23 July
            endif
         endif
C Markus 15 July change: end
C     SM maxtrix elements
         qhvv = 0 
         call Mat2born0(p,m2i,m2if,1)
         m2sm = m2if(iflin1,iflin2,iflout1,iflout2)
C         write(*,*)'msmsm test',m2if(iflin1,iflin2,iflout1,iflout2)
C     anomalous coupling matrix elements
         qhvv = 1 
         call Mat2born0(p,m2i,m2if,1)
         m2full = m2if(iflin1,iflin2,iflout1,iflout2)
      endif
C-----------------------------------------------------------------------
      if (npafin.eq.3) then
C transform bottom in strange quarks as no b-quark ME evaluetd for 
C 3 parton final state
      if (abs(iflin1).eq.5) iflin1 = 3 * iflin1/abs(iflin1)
      if (abs(iflin2).eq.5) iflin2 = 3 * iflin2/abs(iflin2)
      if (abs(iflout1).eq.5) iflout1 = 3 * iflout1/abs(iflout1)
      if (abs(iflout2).eq.5) iflout2 = 3 * iflout2/abs(iflout2)
      if (abs(iflout3).eq.5) iflout3 = 3 * iflout3/abs(iflout3)
C     three parton final state
         if (iflin1*iflin2.ne.0) then
C     no gluon in intial state
C     parton1(p1) + parton2(p2) --> f(p3) + f'(p4) + H(p5) + gluon(p6)
C     construct 4-momenta of Higgs bosons and outgoing partons    
            if (iflout3.eq.0) then
               if (iflin1*iflout1.lt.0) then
                  ihelp = iflout2 
                  iflout2= iflout1
                  iflout1 = ihelp
                  do I = 0,3
                     phelp(i) = pjet2(i)
                     pjet2(i) = pjet1(i)
                     pjet1(i) = phelp(i)
                  enddo
C                  write (*,*)'changed to  process ',iflin1,' + '
C     +                 ,iflin2,' --> ',
C     +                 iflout1,' + ',iflout2,' + ',iflout3
               endif
               do I = 0,3
                  p(3,i) = pjet1(i)
                  p(4,i) = pjet2(i)
                  p(5,i) = phiggs(i)
                  p(6,i) = pjet3(i)
               enddo
C     SM matrix elements
               qhvv = 0 
               call Mat2gluon_out(p,m2i_gluon,m2if_gluon)
C
               m2sm = m2if_gluon(iflin1,iflin2,iflout1,iflout2)
C               write(*,*)'mat2 qqgluon in SM',m2sm
C     anomalous coupling matrix elements
               qhvv = 1 
               call Mat2gluon_out(p,m2i_gluon,m2if_gluon)
               m2full = m2if_gluon(iflin1,iflin2,iflout1,iflout2)
C               write(*,*)'mat2 qqgluon in EFT',m2full
C
            elseif (iflout2.eq.0) then
               if (iflin1*iflout1.lt.0) then
                  ihelp = iflout3 
                  iflout3= iflout1
                  iflout1 = ihelp
                  do I = 0,3
                     phelp(i) = pjet3(i)
                     pjet3(i) = pjet1(i)
                     pjet1(i) = phelp(i)
                  enddo
C                  write (*,*)'changed to  process ',iflin1,' + '
C     +                 ,iflin2,' --> ',
C     +                 iflout1,' + ',iflout3,' + ',iflout2
               endif
               do I = 0,3
                  p(3,i) = pjet1(i)
                  p(4,i) = pjet3(i)
                  p(5,i) = phiggs(i)
                  p(6,i) = pjet2(i)
               enddo
C     SM matrix elements
              qhvv = 0 
               call Mat2gluon_out(p,m2i_gluon,m2if_gluon)

               m2sm = m2if_gluon(iflin1,iflin2,iflout1,iflout3)
C     anomalous coupling matrix elements
               qhvv = 1 
               call Mat2gluon_out(p,m2i_gluon,m2if_gluon)
               m2full = m2if_gluon(iflin1,iflin2,iflout1,iflout3)
            elseif (iflout1.eq.0) then
               if (iflin1*iflout2.lt.0) then
                  ihelp = iflout3 
                  iflout3= iflout2
                  iflout2 = ihelp
                  do I = 0,3
                     phelp(i) = pjet3(i)
                     pjet3(i) = pjet2(i)
                     pjet2(i) = phelp(i)
                  enddo
C                  write (*,*)'changed to  process ',iflin1,' + '
C     +                 ,iflin2,' --> ',
C     +                 iflout1,' + ',iflout3,' + ',iflout2
               endif
               do I = 0,3
                  p(3,i) = pjet2(i)
                  p(4,i) = pjet3(i)
                  p(5,i) = phiggs(i)
                  p(6,i) = pjet1(i)
               enddo
C     SM matrix elements
               qhvv = 0 
               call Mat2gluon_out(p,m2i_gluon,m2if_gluon)
               m2sm = m2if_gluon(iflin1,iflin2,iflout2,iflout3)
C     anomalous coupling matrix elements
               qhvv = 1 
               call Mat2gluon_out(p,m2i_gluon,m2if_gluon)
               m2full = m2if_gluon(iflin1,iflin2,iflout2,iflout3)
            else
               write(*,*)" non valid flavour combination!"
               return
            endif
         endif
C     gluon in intial state 
         if (iflin1.eq.0) then
C     gluon(p1) + q(p2)    --> q'(p3)    + q''(p4) + H(p5) + q'''bar(p6)
            if (iflin2.gt.0) then
               if (iflout3.lt.0) then
                  do I = 0,3
                     p(3,i) = pjet1(i)
                     p(4,i) = pjet2(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet3(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin2,iflout1,iflout2,iflout3)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin2,iflout1,iflout2,iflout3)
               elseif (iflout2.lt.0) then
C     gluon(p1) + qbar(p2) --> q'bar(p3) + q''bar(p4) + H(p5) + q'''(p6)
                  do I = 0,3
                     p(3,i) = pjet1(i)
                     p(4,i) = pjet3(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet2(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin2,iflout1,iflout3,iflout2)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin2,iflout1,iflout3,iflout2)
               elseif (iflout1.lt.0) then
                  do I = 0,3
                     p(3,i) = pjet2(i)
                     p(4,i) = pjet3(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet1(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin2,iflout2,iflout3,iflout1)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin2,iflout2,iflout3,iflout1)
               else
                  write(*,*)" non valid flavour combination!"
                  return
               endif
            else
C     gluon(p1) + qbar(p2) --> q'bar(p3) + q''bar(p4) + H(p5) + q'''(p6)
               if (iflout3.gt.0) then
                  do I = 0,3
                     p(3,i) = pjet1(i)
                     p(4,i) = pjet2(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet3(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin2,iflout1,iflout2,iflout3)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin2,iflout1,iflout2,iflout3)
               elseif (iflout2.gt.0) then
                  do I = 0,3
                     p(3,i) = pjet1(i)
                     p(4,i) = pjet3(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet2(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin2,iflout1,iflout3,iflout2)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin2,iflout1,iflout3,iflout2)
               elseif (iflout1.gt.0) then
                  do I = 0,3
                     p(3,i) = pjet2(i)
                     p(4,i) = pjet3(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet1(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin2,iflout2,iflout3,iflout1)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin2,iflout2,iflout3,iflout1)
               else
                  write(*,*)" non valid flavour combination"
                  return
               endif 
            endif ! anti-quark or quark is 2nd  incoming
         endif ! gluon is 1st  incoming
C 2nd incoming parton is gluon
         if (iflin2.eq.0) then
            if (iflin1.gt.0) then
C     q(p1)    + gluon(p2) --> q'(p3)    + q''(p4) + H(p5) + q'''bar(p6)
               if (iflout3.lt.0) then
                  do I = 0,3
                     p(3,i) = pjet1(i)
                     p(4,i) = pjet2(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet3(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin1,iflout1,iflout2,iflout3)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin1,iflout1,iflout2,iflout3)
               elseif (iflout2.lt.0) then
                  do I = 0,3
                     p(3,i) = pjet1(i)
                     p(4,i) = pjet3(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet2(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin1,iflout1,iflout3,iflout2)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin1,iflout1,iflout3,iflout2)
               elseif (iflout1.lt.0) then
                  do I = 0,3
                     p(3,i) = pjet2(i)
                     p(4,i) = pjet3(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet1(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin1,iflout2,iflout3,iflout1)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin1,iflout2,iflout3,iflout1)
               else
                  write(*,*)" non valid flavour combination!"
                  return
               endif
            else
C     qbar(p1) + gluon(p2) --> q'bar(p3) + q''bar(p4) + H(p5) + q'''(p6)
C      write(*,*)"qb(p1) + gl(p2) --> q'b(p3) + q2b(p4) + H(p5) + q3(p6)"
                 if (iflout3.gt.0) then
                  do I = 0,3
                     p(3,i) = pjet1(i)
                     p(4,i) = pjet2(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet3(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin1,iflout1,iflout2,iflout3)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin1,iflout1,iflout2,iflout3)
               elseif (iflout2.gt.0) then
C
                  do I = 0,3
                     p(3,i) = pjet1(i)
                     p(4,i) = pjet3(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet2(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin1,iflout1,iflout3,iflout2)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin1,iflout1,iflout3,iflout2)
               elseif (iflout1.gt.0) then
                  do I = 0,3
                     p(3,i) = pjet2(i)
                     p(4,i) = pjet3(i)
                     p(5,i) = phiggs(i)
                     p(6,i) = pjet1(i)
                  enddo
C     SM matrix elements
                  qhvv = 0 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2sm = m2if_gluon(iflin1,iflout2,iflout3,iflout1)
C     anomalous coupling matrix elements
                  qhvv = 1 
                  call Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
                  m2full = m2if_gluon(iflin1,iflout2,iflout3,iflout1)
               else
                  write(*,*)" non valid flavour combination"
                  return
               endif
            endif ! 1st incoming quark or antiquark
         endif !gluon is 2nd incoming
      endif  ! npafin.eq.3
C check SM matrix element 
      if (m2sm.lt.1.0d-20) then
         write(*,*)" M2SM<10-20 ",m2sm
         return
      endif
C calculate weight 
      weight = m2full/m2sm
C everything seems ok 
      ierr = 0 
      return
      end
*************************************************************************
      subroutine optobs(ecms,mhiggs,x1,x2,pdf1,pdf2,pjet1,pjet2,
     +                  phiggs,oo1,oo2,ierr) 
*************************************************************************
C     input: ecms proton-pton center-of mass energy in GeV 
C             mhiggs mass of Higgs boson in GeV
C            1st incoming parton in positive z direction
C            2nd incoming parton in negative z direction
C            x1, x2: Bjorken x of 1st and 2ns incoming partons
C            pdf1,pdf2 from -6 to 6: pdfs for 1st and 2nd parton
C            pjet1(0:3):  E,px,py,pz of 1st outgoing jet
C            pjet1(0:3):  E,px,py,pz of 2nd outgoing jet
C            phiggs(0:3): E,px,py,pz of Higgs boson
C -----------------------------------------------------------------------
C      output: oo1:  optimal observable 1st order
C              oo2:  optimal observable 2nd order
C              ierr: 0 all ok, some problem if <> 0   
C -----------------------------------------------------------------------
C     author: Markus Schumacher 22. March 2015
C
C     modification log: 24. March 2015
C                       separate setting Hawk pars in new routine
C                       add mhiggs as input variable to routine 
C                       clean up code and put in some comments       
*************************************************************************
      implicit none
C input variables
      real*8 ecms,mhiggs,x1,x2,pdf1(-6:6),pdf2(-6:6)
      real*8 pjet1(0:3),pjet2(0:3)
      real*8 phiggs(0:3)
C output variables
      real*8 oo1,oo2
      integer ierr
Cf2py intent(out) oo1, oo2, ierr
C loop indices
      integer i1,i2,i,j
C matrix elements 
      real*8 m2sm,m2full,m2cpo,int
C Bjorken x
      real*8 xp1,xp2
C array with 4-momenta 
      real*8 p(6,0:3)
C arrays for storing matrix elements for all initial and final states 
      real*8 m2ism(-5:5,-5:5),m2ifsm(-5:5,-5:5,-5:5,-5:5)
      real*8 m2iano(-5:5,-5:5),m2ifano(-5:5,-5:5,-5:5,-5:5)
      real*8 m2icpo(-5:5,-5:5),m2ifcpo(-5:5,-5:5,-5:5,-5:5)
C flags and parameters used by Hawk
      integer qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &     qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &     qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
      common/rcoptions/qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &     qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &     qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
C
      real*8 pi,el,alpha,alpha0,alphaz,GF,alphas
      real*8 cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2
      real*8 ml,ml2,mqp,mqp2,mqm,mqm2
C
      complex*16 v,cv
      common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &     v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &     ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
C     
      real*8 sinthetac,mfact
      real*8 ppecms
      common/ppecms/ppecms
C
      complex*16 ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
      common/cparam/ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
C
      complex*16 xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null
      complex*16 xml,xml2,xmqp,xmqp2,xmqm,xmqm2
C
      common/xparam/xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null, 
     &     xml(3),xml2(3),xmqp(3),xmqp2(3),xmqm(3),xmqm2(3) 
C
      real*8 qu,qd,ql,qn,qf,mu,mu2,md,md2,mlep,mlep2
      complex*16 guu,gdd,gnn,gll     
      common/qf/qu,qd,ql,qn,qf(4),mu,mu2,md,md2,mlep,mlep2,
     +     guu(-1:1),gdd(-1:1),gnn(-1:1),gll(-1:1)
C
      integer qhvv
      real*8 rsm,d,db,dt,dtb,lambdahvv
      real*8 a1hww,a2hww,a3hww,a1haa,a2haa,a3haa
      real*8 a1haz,a2haz,a3haz,a1hzz,a2hzz,a3hzz
C
      common/hvv/rsm,d,db,dt,dtb,lambdahvv,
     &     a1hww,a2hww,a3hww,a1haa,a2haa,a3haa,
     &     a1haz,a2haz,a3haz,a1hzz,a2hzz,a3hzz,qhvv
C copy c-o-m energy and Higgs boson mass     
      ppecms = ecms    
      mh   = mhiggs             !  mass of higgs boson
C initialite error flag and optimal observable values
      ierr = 99
      oo1  = 0.0d0
      oo2  = 0.0d0
C check several conditions to avoid crashes
      if (x1.gt.1.0d0.or.x1.lt.0.0d0) then
         write(*,*)" Bjporken x1 bad ",x1
         return
      endif
      if (x2.gt.1.0d0.or.x2.lt.0.0d0) then
         write(*,*)" Bjporken x2 bad ",x2
         return
      endif
      if (phiggs(0).lt.0.0d0) then
         write(*,*)" Higgs energy < 0",phiggs(0)
         return
      endif
      if (pjet1(0).lt.0.0d0) then
         write(*,*)" 1st parton energy < 0",pjet1(0)
         return
      endif
      if (pjet2(0).lt.0.0d0) then
         write(*,*)" 2nd parton energy < 0",pjet2(0)
         return
      endif
C set hawk parameters for optobs calculation
      call sethawkpars(0,0)
C copy Bjorken x and construct 4-momenta of incoming partons
      xp1=x1                    
      xp2=x2                    
      p(1,0) = xp1*ppecms/2.0d0
      p(1,1) = 0.0d0
      p(1,2) = 0.0d0
      p(1,3) = xp1*ppecms/2.0d0
      p(2,0) = xp2*ppecms/2.0d0
      p(2,1) = 0.0d0
      p(2,2) = 0.0d0
      p(2,3) = -xp2*ppecms/2.0d0
C construct 4-momenta of Higgs and outgoing partons
      do I = 0,3
         p(3,i) = pjet1(i)
         p(4,i) = pjet2(i)
         p(5,i) = phiggs(i)
         p(6,i) = 0.0d0
      enddo
C************************************************************************
C get SM matrix elements 
      qhvv = 0 
      call Mat2born0(p,m2ism,m2ifsm,1)
C get anomalous coupling maxtrix elements 
      qhvv = 1 
      call Mat2born0(p,m2iano,m2ifano,1)
C get pure CP-odd matrix elements
      qhvv  = 1
      a1hww = 0d0
      a1hzz = 0D0
      call Mat2born0(p,m2icpo,m2ifcpo,1)
c determine interference, sm and cp weighted by pdfs
      int   = 0.0d0      
      m2sm  = 0.0d0
      m2cpo = 0.0d0
      do 100 i1 = -4,4
         do 100 i2 = -4,4
            if (i1*i2.eq.0) goto 100
            int = int + pdf1(i1)*pdf2(i2)/2.0d0*
     +           (m2iano(i1,i2)-m2ism(i1,i2)-m2icpo(i1,i2))
            m2sm  = m2sm  + pdf1(i1)*pdf2(i2)*m2ism(i1,i2)
            m2cpo = m2cpo + pdf1(i1)*pdf2(i2)*m2icpo(i1,i2)
 100  continue
C check SM matrix elements 
      if (m2sm.lt.1d-20) then
         write(*,*)" m2sm < 0",m2sm
         return
      endif
C determine optimal observable value of 1st and 2nd order
      oo1 = int/m2sm
      oo2 = m2cpo/m2sm
C everything seems ok
      ierr = 0 
      return
      end
*************************************************************************
*************************************************************************
      subroutine sethawkpars(iopt,ipara)
C     author: Markus Schumacher  24. March 2015
*************************************************************************
      implicit none 
      integer iopt,ipara,i,j
      integer qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &     qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &     qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
      common/rcoptions/qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &     qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &     qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
C
      real*8 pi,el,alpha,alpha0,alphaz,GF,alphas
      real*8 cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2
      real*8 ml,ml2,mqp,mqp2,mqm,mqm2

      complex*16 v,cv
      common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &     v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &     ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
C     
      real*8 sinthetac,mfact
      real*8 ppecms
      common/ppecms/ppecms
C
      complex*16 ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
      common/cparam/ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
C
      complex*16 xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null
      complex*16 xml,xml2,xmqp,xmqp2,xmqm,xmqm2
C
      common/xparam/xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null, 
     &     xml(3),xml2(3),xmqp(3),xmqp2(3),xmqm(3),xmqm2(3) 
C
      real*8 qu,qd,ql,qn,qf,mu,mu2,md,md2,mlep,mlep2
      complex*16 guu,gdd,gnn,gll     
      common/qf/qu,qd,ql,qn,qf(4),mu,mu2,md,md2,mlep,mlep2,
     +     guu(-1:1),gdd(-1:1),gnn(-1:1),gll(-1:1)
C
      integer qhvv
      real*8 rsm,d,db,dt,dtb,lambdahvv
      real*8 a1hww,a2hww,a3hww,a1haa,a2haa,a3haa
      real*8 a1haz,a2haz,a3haz,a1hzz,a2hzz,a3hzz

      common/hvv/rsm,d,db,dt,dtb,lambdahvv,
     &     a1hww,a2hww,a3hww,a1haa,a2haa,a3haa,
     &     a1haz,a2haz,a3haz,a1hzz,a2hzz,a3hzz,qhvv

C set HAWK "constants" 
      alpha = 1.0d0/137.0d0
      pi = 4d0*datan(1d0)
      el = sqrt(4d0*pi*alpha)   ! alpha, alpha0 oder alphaz
      alphas =0.112d0
C
      mz   = 91.1876d0
      cmz = mz
      xmz = mz
      mz2 = mz*mz
      xmz2 = mz2 
      cmz2  = mz2
C
      mw   = 80.425d0
      xmw  = mw
      cmw  = mw
      mw2  = mw*mw
      xmw2 = mw2
      cmw2 = mw2
C
      mh2  = mh*mh
C
      xmh   = mh
      xmh2  = mh2
C 
      cw  = mw/mz
      xcw = cw
      ccw = cw 
      cw2 = cw*cw
      xcw2 = cw2
      ccw2 = cw2
      sw2  = 1d0-cw2
      csw2 = sw2
      xsw2 = sw2
      sw  = sqrt(sw2)
      xsw  = sw 
      csw  = sw 
C fermion el-mag charges
      qu =  2d0/3d0
      qd =  -1d0/3d0
      qn =   0d0
      ql =   -1d0
C fermion couplings 
      guu(+1) = -qu*xsw/xcw
      guu(-1) = -qu*xsw/xcw+1d0/2d0/xsw/xcw
      gdd(+1) = -qd*xsw/xcw
      gdd(-1) = -qd*xsw/xcw-1d0/2d0/xsw/xcw
      gnn(+1) = -qn*xsw/xcw
      gnn(-1) = -qn*xsw/xcw+1d0/2d0/xsw/xcw
      gll(+1) = -ql*xsw/xcw
      gll(-1) = -ql*xsw/xcw-1d0/2d0/xsw/xcw
C CKM matrix and its conjugated
      sinthetac = 0.226548d0
      v(1,2) = sinthetac
      v(1,1) = sqrt(1d0-v(1,2)*v(1,2)) ! bug v(1,1)
      v(2,1) = -v(1,2)
      v(2,2) = v(1,1)
      v(1,3) = 0d0
      v(2,3) = 0d0
      v(3,1) = 0d0
      v(3,2) = 0d0
      v(3,3) = 1.0d0
      do I =1,3
         do J = 1,3
            cv(i,j) = dconjg(v(i,j))
         enddo
      enddo
C set HAWK flags
      qw     = 1 
      qz     = 1 
C
      qschan = 0 
      qtchan = 1 
      qch2   = 1
      qchint = 0 

      qqcddiag = 1 
      qqcdnondiag = 0
      qqcdgsplit = 0 
      qqcdggfus= 0 

C     
      qbini       = 1
      qbfin       = 1 
      qwidth      = 0 
      qcp         = 0 

      if (iopt.eq.1) then ! for reweighting
         if (ipara.eq.1) then  
            a1hww = mw/sw*rsm
            a2hww = 2d0*d /sw/mw
            a3hww = 2d0*dt/sw/mw
            a1haa = 0d0
            a2haa = 4d0*(d *sw2+db *cw2)/2d0/sw/mw
            a3haa = 4d0*(dt*sw2+dtb*cw2)/2d0/sw/mw
            a1haz = 0d0
            a2haz = -2d0*cw*(d -db )/mw ! sign change due to BHS convention
            a3haz = -2d0*cw*(dt-dtb)/mw ! sign change due to BHS convention
            a1hzz = mw/sw/cw2*rsm
            a2hzz = 4d0*(d *cw2+db *sw2)/2d0/sw/mw
            a3hzz = 4d0*(dt*cw2+dtb*sw2)/2d0/sw/mw
         endif
      else ! for optimal observables for dtilde dt 
C anomalous couplings: dt = dtb = 1,0 rest=0
         a1hww = mw/sw
         a2hww = 0.0d0
         a3hww = 2d0/sw/mw
         a1haa = 0d0
         a2haa = 0d0
Cold         a3haa = 0d0
         a3haa = 2d0/sw/mw
         a1haz = 0d0
         a2haz = 0d0
         a3haz = 0d0
         a1hzz = mw/sw/cw2
         a2hzz = 0d0
         a3hzz = 2d0/sw/mw
         lambdahvv = -100.0d0   ! no form factors
      endif
      return
      end
*************************************************************************
*************************************************************************
