************************************************************************
      subroutine Mat2born0(p,m2i0,m2if0,qbcalc)
************************************************************************
*     Born structures needed for subtraction function for
*     parton1(p1) + parton2(p2) --> f(p3) + f'(p4) + H(p5)
*     qbcalc = 0/1: b-quarks ex-/in-cluded in evaluation
*     
*     Note: anomalous HVV couplings for qhvv>0 included
*-----------------------------------------------------------------------
*     13.10.06 Stefan Dittmaier
************************************************************************
      implicit real*8 (a-z)
      complex*16 v,cv
      complex*16 ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2,cmh,cmh2
      complex*16 pws,pws12,pwt11,pwt22,pwt12,pwt21
      complex*16 pzs,pzs12,pzt11,pzt22,pzt12,pzt21
      real*8 p(6,0:3)
      real*8 m2aqq0ss(5,5,5,5),m2qaq0ss(5,5,5,5)
      real*8 m2qq0ss(5,5,5,5),m2aqaq0ss(5,5,5,5)
      real*8 m2aqq0tt(5,5,5,5),m2qaq0tt(5,5,5,5)
      real*8 m2qq0tt(5,5,5,5),m2aqaq0tt(5,5,5,5)
      real*8 m2aqq0st(5,5,5,5),m2qaq0st(5,5,5,5)
      real*8 m2qq0st(5,5,5,5),m2aqaq0st(5,5,5,5)
      real*8 m2i0(-5:5,-5:5)
      real*8 m2if0(-5:5,-5:5,-5:5,-5:5)
      integer i1,i2,i3,i4,i,j,qb,qbcalc
      integer qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &     qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &     qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
      integer qhvv
      
      common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &     v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &     ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
      common/cparam/ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
      common/rcoptions/qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &     qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &     qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
      common/hvv/rsm,d,db,dt,dtb,lambdahvv,
     &     a1hww,a2hww,a3hww,a1haa,a2haa,a3haa,
     &     a1haz,a2haz,a3haz,a1hzz,a2hzz,a3hzz,qhvv
      
      data m2aqq0ss/625*0/,m2aqq0st/625*0/,m2aqq0tt/625*0/
      data m2qq0ss/625*0/,m2qq0st/625*0/,m2qq0tt/625*0/
      data m2aqaq0ss/625*0/,m2aqaq0st/625*0/,m2aqaq0tt/625*0/
      data m2qaq0ss/625*0/,m2qaq0st/625*0/,m2qaq0tt/625*0/
      
c energies and angles
      eb1  = p(1,0)
      eb2  = p(2,0)
      e1   = p(3,0)
      e2   = p(4,0)
      cth1 = p(3,3)/p(3,0)
      cth2 = p(4,3)/p(4,0)
      if (p(1,3).lt.0d0) then
         cth1 = -cth1
         cth2 = -cth2
      endif
      sth1 = sqrt(p(3,1)**2+p(3,2)**2)/p(3,0)
      sth2 = sqrt(p(4,1)**2+p(4,2)**2)/p(4,0)
      if (cth1.gt.0d0) then
         c22th1 = (1d0+cth1)*.5d0
         s22th1 = sth1**2/(4d0*c22th1)
      else
         s22th1 = (1d0-cth1)*.5d0
         c22th1 = sth1**2/(4d0*s22th1)
      endif
      if (cth2.gt.0d0) then
         c22th2 = (1d0+cth2)*.5d0
         s22th2 = sth2**2/(4d0*c22th2)
      else
         s22th2 = (1d0-cth2)*.5d0
         c22th2 = sth2**2/(4d0*s22th2)
      endif

c invariants
      s    =  4d0*eb1*eb2
      t11  = -4d0*eb1*e1*s22th1
      t12  = -4d0*eb1*e2*s22th2
      t21  = -4d0*eb2*e1*c22th1
      t22  = -4d0*eb2*e2*c22th2
c     s12  = mh2-s+4d0*e1*eb1*s22th1+4d0*e1*eb2*c22th1
c     &		    +4d0*e2*eb1*s22th2+4d0*e2*eb2*c22th2
      s12  = 2d0*( p(3,0)*p(4,0)-p(3,1)*p(4,1)
     &     -p(3,2)*p(4,2)-p(3,3)*p(4,3))
      
c propagators
      if(qwidth.eq.1) then
         pws12 = 1d0/(s12-cmw2)
         pzs12 = 1d0/(s12-cmz2)
         pws = 1d0/(s-cmw2)
         pzs = 1d0/(s-cmz2)
          pwt11 = 1d0/(t11-cmw2)
          pzt11 = 1d0/(t11-cmz2)
          pwt22 = 1d0/(t22-cmw2)
          pzt22 = 1d0/(t22-cmz2)
          pwt12 = 1d0/(t12-cmw2)
          pzt12 = 1d0/(t12-cmz2)
          pwt21 = 1d0/(t21-cmw2)
          pzt21 = 1d0/(t21-cmz2)
        else

          if ((qwidth.eq.0).or.((qwidth.eq.2).and.(s12.lt.0d0))) then
            pws12 = 1d0/(s12-mw2)
            pzs12 = 1d0/(s12-mz2)
          else
            pws12 = 1d0/(s12-cmw2)
            pzs12 = 1d0/(s12-cmz2)
          endif
          
          if ((qwidth.eq.0).or.((qwidth.eq.2).and.(s.lt.0d0))) then
            pws = 1d0/(s-mw2)
            pzs = 1d0/(s-mz2)
          else
            pws = 1d0/(s-cmw2)
            pzs = 1d0/(s-cmz2)
          endif
          
          if ((qwidth.eq.0).or.((qwidth.eq.2).and.(t11.lt.0d0))) then
            pwt11 = 1d0/(t11-mw2)
            pzt11 = 1d0/(t11-mz2)
          else
            pwt11 = 1d0/(t11-cmw2)
            pzt11 = 1d0/(t11-cmz2)
          endif
          
          if ((qwidth.eq.0).or.((qwidth.eq.2).and.(t22.lt.0d0))) then
            pwt22 = 1d0/(t22-mw2)
            pzt22 = 1d0/(t22-mz2)
          else
            pwt22 = 1d0/(t22-cmw2)
            pzt22 = 1d0/(t22-cmz2)
          endif
          
          if ((qwidth.eq.0).or.((qwidth.eq.2).and.(t12.lt.0d0))) then
            pwt12 = 1d0/(t12-mw2)
            pzt12 = 1d0/(t12-mz2)
          else
            pwt12 = 1d0/(t12-cmw2)
            pzt12 = 1d0/(t12-cmz2)
          endif
          
          if ((qwidth.eq.0).or.((qwidth.eq.2).and.(t21.lt.0d0))) then
            pwt21 = 1d0/(t21-mw2)
            pzt21 = 1d0/(t21-mz2)
          else
            pwt21 = 1d0/(t21-cmw2)
            pzt21 = 1d0/(t21-cmz2)
          endif
        endif
C
	qb = qbcalc
	if ((qbini.eq.0).and.(qbfin.eq.0)) qb = 0
C
	if (qhvv.eq.0) then

c qbar-q --> qbar-q
           call Mat2aqqborn(m2aqq0ss,m2aqq0tt,m2aqq0st,
     &          s,s12,t11,t21,t12,t22,
     &          pws,pws12,pwt11,pwt22,pzs,pzs12,pzt11,pzt22,qb)
c q-q    --> q-q
           call Mat2aqqborn(m2qq0ss,m2qq0tt,m2qq0st,
     &          t21,t12,t11,s,s12,t22,
     &          pwt21,pwt12,pwt11,pwt22,pzt21,pzt12,pzt11,pzt22,qb)

c other channels from CP symmetry for qcp=1
           if (qcp.eq.0) then
c q-qbar --> q-qbar
              call Mat2aqqborn(m2qaq0ss,m2qaq0tt,m2qaq0st,
     &             s,s12,t22,t12,t21,t11,
     &             pws,pws12,pwt22,pwt11,pzs,pzs12,pzt11,pzt22,qb)
c qbar-qbar --> qbar-qbar
              call Mat2aqqborn(m2aqaq0ss,m2aqaq0tt,m2aqaq0st,
     &             t12,t21,t11,s12,s,t22,
     &             pwt12,pwt21,pwt11,pwt22,pzt21,pzt12,pzt11,pzt22,qb)
           else
              do 103 i4=1,4+qb
                 do 103 i3=1,4+qb
                    do 103 i2=1,4+qb
                       do 103 i1=1,4+qb
                          m2qaq0ss(i1,i2,i3,i4)  = m2aqq0ss(i1,i2,i3,i4) 
                          m2qaq0tt(i1,i2,i3,i4)  = m2aqq0tt(i1,i2,i3,i4) 
                          m2qaq0st(i1,i2,i3,i4)  = m2aqq0st(i1,i2,i3,i4) 
                          m2aqaq0ss(i1,i2,i3,i4) = m2qq0ss(i1,i2,i3,i4)  
                          m2aqaq0tt(i1,i2,i3,i4) = m2qq0tt(i1,i2,i3,i4)  
                          m2aqaq0st(i1,i2,i3,i4) = m2qq0st(i1,i2,i3,i4)  
 103          continue
           endif
                    
        else

	call setprods3(p)

c qbar-q --> qbar-q
        call Mat2aqqbornhvv(m2aqq0ss,m2aqq0tt,m2aqq0st,-1,-2,3,4,qb)
c q-q    --> q-q
        call Mat2aqqbornhvv(m2qq0ss,m2qq0tt,m2qq0st,3,-2,-1,4,qb)
c q-qbar --> q-qbar
        call Mat2aqqbornhvv(m2qaq0ss,m2qaq0tt,m2qaq0st,-2,-1,4,3,qb)
c qbar-qbar --> qbar-qbar
        call Mat2aqqbornhvv(m2aqaq0ss,m2aqaq0tt,m2aqaq0st,-1,4,3,-2,qb)

	endif

c add final states for fixed initial states
        do 200 i1=-4-qbini,4+qbini
        do 200 i2=-4-qbini,4+qbini
          m2i0(i1,i2) = 0d0
          if (i1*i2.eq.0) goto 200
        do 300 i3=1,4+qbfin
        do 300 i4=1,4+qbfin
          if(i1.gt.0) then
            if ((i2.gt.0)) then
              m2if0(i1,i2,i3,i4)    = m2qq0ss(i3,i2,i1,i4)*.5d0
     &           + m2qq0tt(i3,i2,i1,i4)*.5d0 + m2qq0st(i3,i2,i1,i4)*.5d0
              m2i0(i1,i2) = m2i0(i1,i2) + m2if0(i1,i2,i3,i4)
            else
              m2if0(i1,i2,i3,-i4)    = m2qaq0ss(-i2,i1,i4,i3)
     &           + m2qaq0tt(-i2,i1,i4,i3) + m2qaq0st(-i2,i1,i4,i3)
              m2i0(i1,i2) = m2i0(i1,i2) + m2if0(i1,i2,i3,-i4)
            endif
          elseif (i2.gt.0) then
            m2if0(i1,i2,-i3,i4)    = m2aqq0ss(-i1,i2,i3,i4)
     &         + m2aqq0tt(-i1,i2,i3,i4) + m2aqq0st(-i1,i2,i3,i4)
            m2i0(i1,i2) = m2i0(i1,i2) + m2if0(i1,i2,-i3,i4)
          else
            m2if0(i1,i2,-i3,-i4)    = m2aqaq0ss(-i1,i4,i3,-i2)*.5d0
     &         + m2aqaq0tt(-i1,i4,i3,-i2)*.5d0 
     &	       + m2aqaq0st(-i1,i4,i3,-i2)*.5d0
            m2i0(i1,i2) = m2i0(i1,i2) + m2if0(i1,i2,-i3,-i4)
	  endif
300     continue
200     continue

	end
************************************************************************
        subroutine Mat2born(p,m2i0,m2if0,
     &		     m2if0_22,m2if0_33,m2if0_44,m2if0_nd,qbcalc)
************************************************************************
*       Born structures needed for subtraction function for
*	    parton1(p1) + parton2(p2) --> f(p3) + f'(p4) + H(p5)
*	qbcalc = 0/1: b-quarks ex-/in-cluded in evaluation
*
*	Note: anomalous HVV couplings for qhvv>0
*	      + included in m2i0, m2if0_22, m2if0_33, m2if0_44
*	      - NOT included in m2if0, m2if0_nd
*
*-----------------------------------------------------------------------
*       13.10.06 Stefan Dittmaier
************************************************************************
        implicit real*8 (a-z)
	complex*16 v,cv
        complex*16 ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2,cmh,cmh2
	complex*16 pws,pws12,pwt11,pwt22,pwt12,pwt21
	complex*16 pzs,pzs12,pzt11,pzt22,pzt12,pzt21
        real*8 p(6,0:3)
        real*8 m2aqq0ss(5,5,5,5),m2qaq0ss(5,5,5,5)
        real*8 m2qq0ss(5,5,5,5),m2aqaq0ss(5,5,5,5)
        real*8 m2aqq0tt(5,5,5,5),m2qaq0tt(5,5,5,5)
        real*8 m2qq0tt(5,5,5,5),m2aqaq0tt(5,5,5,5)
        real*8 m2aqq0st(5,5,5,5),m2qaq0st(5,5,5,5)
        real*8 m2qq0st(5,5,5,5),m2aqaq0st(5,5,5,5)
        real*8 m2i0(-5:5,-5:5)
        real*8 m2if0(-5:5,-5:5,-5:5,-5:5)
        real*8 m2if0hvv(-5:5,-5:5,-5:5,-5:5)
        real*8 m2if0_22(-5:5,-5:5,-5:5,-5:5)
        real*8 m2if0_33(-5:5,-5:5,-5:5,-5:5)
        real*8 m2if0_44(-5:5,-5:5,-5:5,-5:5)
        real*8 m2if0_nd(-5:5,-5:5,-5:5,-5:5)
	integer i1,i2,i3,i4,i,j,qb,qbcalc
        integer qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &			 qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
	integer qhvv

        common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &         v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &         ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
        common/cparam/ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
        common/rcoptions/qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &			 qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
        common/hvv/rsm,d,db,dt,dtb,lambdahvv,
     &             a1hww,a2hww,a3hww,a1haa,a2haa,a3haa,
     &             a1haz,a2haz,a3haz,a1hzz,a2hzz,a3hzz,qhvv

        data m2aqq0ss/625*0/,m2aqq0st/625*0/,m2aqq0tt/625*0/
        data m2qq0ss/625*0/,m2qq0st/625*0/,m2qq0tt/625*0/
        data m2aqaq0ss/625*0/,m2aqaq0st/625*0/,m2aqaq0tt/625*0/
        data m2qaq0ss/625*0/,m2qaq0st/625*0/,m2qaq0tt/625*0/

c energies and angles
        eb1  = p(1,0)
        eb2  = p(2,0)
	e1   = p(3,0)
	e2   = p(4,0)
	cth1 = p(3,3)/p(3,0)
	cth2 = p(4,3)/p(4,0)
	if (p(1,3).lt.0d0) then
	  cth1 = -cth1
	  cth2 = -cth2
	endif
	sth1 = sqrt(p(3,1)**2+p(3,2)**2)/p(3,0)
	sth2 = sqrt(p(4,1)**2+p(4,2)**2)/p(4,0)
        if (cth1.gt.0d0) then
          c22th1 = (1d0+cth1)*.5d0
          s22th1 = sth1**2/(4d0*c22th1)
        else
          s22th1 = (1d0-cth1)*.5d0
          c22th1 = sth1**2/(4d0*s22th1)
        endif
        if (cth2.gt.0d0) then
          c22th2 = (1d0+cth2)*.5d0
          s22th2 = sth2**2/(4d0*c22th2)
        else
          s22th2 = (1d0-cth2)*.5d0
          c22th2 = sth2**2/(4d0*s22th2)
        endif

c invariants
        s    = 4d0*eb1*eb2
        t11  = -4d0*eb1*e1*s22th1
        t12  = -4d0*eb1*e2*s22th2
        t21  = -4d0*eb2*e1*c22th1
        t22  = -4d0*eb2*e2*c22th2
c        s12  = mh2-s+4d0*e1*eb1*s22th1+4d0*e1*eb2*c22th1
c     &		    +4d0*e2*eb1*s22th2+4d0*e2*eb2*c22th2
	s12  = 2d0*( p(3,0)*p(4,0)-p(3,1)*p(4,1)
     &	            -p(3,2)*p(4,2)-p(3,3)*p(4,3))

c propagators
        if(qwidth.eq.1) then
          pws12 = 1d0/(s12-cmw2)
          pzs12 = 1d0/(s12-cmz2)
          pws = 1d0/(s-cmw2)
          pzs = 1d0/(s-cmz2)
          pwt11 = 1d0/(t11-cmw2)
          pzt11 = 1d0/(t11-cmz2)
          pwt22 = 1d0/(t22-cmw2)
          pzt22 = 1d0/(t22-cmz2)
          pwt12 = 1d0/(t12-cmw2)
          pzt12 = 1d0/(t12-cmz2)
          pwt21 = 1d0/(t21-cmw2)
          pzt21 = 1d0/(t21-cmz2)
        else

          if ((qwidth.eq.0).or.((qwidth.eq.2).and.(s12.lt.0d0))) then
            pws12 = 1d0/(s12-mw2)
            pzs12 = 1d0/(s12-mz2)
          else
            pws12 = 1d0/(s12-cmw2)
            pzs12 = 1d0/(s12-cmz2)
          endif
          
          if ((qwidth.eq.0).or.((qwidth.eq.2).and.(s.lt.0d0))) then
            pws = 1d0/(s-mw2)
            pzs = 1d0/(s-mz2)
          else
            pws = 1d0/(s-cmw2)
            pzs = 1d0/(s-cmz2)
          endif
          
          if ((qwidth.eq.0).or.((qwidth.eq.2).and.(t11.lt.0d0))) then
            pwt11 = 1d0/(t11-mw2)
            pzt11 = 1d0/(t11-mz2)
          else
            pwt11 = 1d0/(t11-cmw2)
            pzt11 = 1d0/(t11-cmz2)
          endif
          
          if ((qwidth.eq.0).or.((qwidth.eq.2).and.(t22.lt.0d0))) then
            pwt22 = 1d0/(t22-mw2)
            pzt22 = 1d0/(t22-mz2)
          else
            pwt22 = 1d0/(t22-cmw2)
            pzt22 = 1d0/(t22-cmz2)
          endif
          
          if ((qwidth.eq.0).or.((qwidth.eq.2).and.(t12.lt.0d0))) then
            pwt12 = 1d0/(t12-mw2)
            pzt12 = 1d0/(t12-mz2)
          else
            pwt12 = 1d0/(t12-cmw2)
            pzt12 = 1d0/(t12-cmz2)
          endif
          
          if ((qwidth.eq.0).or.((qwidth.eq.2).and.(t21.lt.0d0))) then
            pwt21 = 1d0/(t21-mw2)
            pzt21 = 1d0/(t21-mz2)
          else
            pwt21 = 1d0/(t21-cmw2)
            pzt21 = 1d0/(t21-cmz2)
          endif
        endif


c*** initializations
c	do 100 i1=1,4
c	do 100 i2=1,4
c	do 100 i3=1,4
c	do 100 i4=1,4
c	  m2aqq0ss(i1,i2,i3,i4)  = 0d0
c	  m2aqq0tt(i1,i2,i3,i4)  = 0d0
c	  m2aqq0st(i1,i2,i3,i4)  = 0d0
c	  m2qaq0ss(i1,i2,i3,i4)  = 0d0
c	  m2qaq0tt(i1,i2,i3,i4)  = 0d0
c	  m2qaq0st(i1,i2,i3,i4)  = 0d0
c	  m2qq0ss(i1,i2,i3,i4)   = 0d0
c	  m2qq0tt(i1,i2,i3,i4)   = 0d0
c	  m2qq0st(i1,i2,i3,i4)   = 0d0
c	  m2aqaq0ss(i1,i2,i3,i4) = 0d0
c	  m2aqaq0tt(i1,i2,i3,i4) = 0d0
c	  m2aqaq0st(i1,i2,i3,i4) = 0d0
c100	continue

	qb = qbcalc
	if ((qbini.eq.0).and.(qbfin.eq.0)) qb = 0

c qbar-q --> qbar-q
	call Mat2aqqborn(m2aqq0ss,m2aqq0tt,m2aqq0st,
     &			 s,s12,t11,t21,t12,t22,
     &			 pws,pws12,pwt11,pwt22,pzs,pzs12,pzt11,pzt22,qb)
c q-q    --> q-q
	call Mat2aqqborn(m2qq0ss,m2qq0tt,m2qq0st,
     &		 t21,t12,t11,s,s12,t22,
     &		 pwt21,pwt12,pwt11,pwt22,pzt21,pzt12,pzt11,pzt22,qb)

c other channels from CP symmetry for qcp=1
	if (qcp.eq.0) then
c q-qbar --> q-qbar
	  call Mat2aqqborn(m2qaq0ss,m2qaq0tt,m2qaq0st,
     &			 s,s12,t22,t12,t21,t11,
     &	                 pws,pws12,pwt22,pwt11,pzs,pzs12,pzt11,pzt22,qb)
c qbar-qbar --> qbar-qbar
	  call Mat2aqqborn(m2aqaq0ss,m2aqaq0tt,m2aqaq0st,
     &		 t12,t21,t11,s12,s,t22,
     &		 pwt12,pwt21,pwt11,pwt22,pzt21,pzt12,pzt11,pzt22,qb)
	else
	  do 103 i4=1,4+qb
	  do 103 i3=1,4+qb
	  do 103 i2=1,4+qb
	  do 103 i1=1,4+qb
	    m2qaq0ss(i1,i2,i3,i4)  = m2aqq0ss(i1,i2,i3,i4) 
	    m2qaq0tt(i1,i2,i3,i4)  = m2aqq0tt(i1,i2,i3,i4) 
	    m2qaq0st(i1,i2,i3,i4)  = m2aqq0st(i1,i2,i3,i4) 
	    m2aqaq0ss(i1,i2,i3,i4) = m2qq0ss(i1,i2,i3,i4)  
	    m2aqaq0tt(i1,i2,i3,i4) = m2qq0tt(i1,i2,i3,i4)  
	    m2aqaq0st(i1,i2,i3,i4) = m2qq0st(i1,i2,i3,i4)  
103	  continue
	endif

c add final states for fixed initial states
        do 200 i1=-4-qbini,4+qbini
        do 200 i2=-4-qbini,4+qbini
          m2i0(i1,i2) = 0d0
          if (i1*i2.eq.0) goto 200
        do 300 i3=1,4+qbfin
        do 300 i4=1,4+qbfin
          if(i1.gt.0) then
            if ((i2.gt.0)) then
              m2if0_nd(i1,i2,i3,i4) = m2qq0st(i3,i2,i1,i4)*.5d0
              m2if0(i1,i2,i3,i4)    = m2qq0ss(i3,i2,i1,i4)*.5d0
     &           + m2qq0tt(i3,i2,i1,i4)*.5d0 + m2qq0st(i3,i2,i1,i4)*.5d0
              m2i0(i1,i2) = m2i0(i1,i2) + m2if0hvv(i1,i2,i3,i4)
            else
              m2if0_nd(i1,i2,i3,-i4) = m2qaq0st(-i2,i1,i4,i3)
              m2if0(i1,i2,i3,-i4)    = m2qaq0ss(-i2,i1,i4,i3)
     &           + m2qaq0tt(-i2,i1,i4,i3) + m2qaq0st(-i2,i1,i4,i3)
              m2i0(i1,i2) = m2i0(i1,i2) + m2if0hvv(i1,i2,i3,-i4)
            endif
          elseif (i2.gt.0) then
            m2if0_nd(i1,i2,-i3,i4) = m2aqq0st(-i1,i2,i3,i4)
            m2if0(i1,i2,-i3,i4)    = m2aqq0ss(-i1,i2,i3,i4)
     &         + m2aqq0tt(-i1,i2,i3,i4) + m2aqq0st(-i1,i2,i3,i4)
            m2i0(i1,i2) = m2i0(i1,i2) + m2if0hvv(i1,i2,-i3,i4)
          else
            m2if0_nd(i1,i2,-i3,-i4) = m2aqaq0st(-i1,i4,i3,-i2)*.5d0
            m2if0(i1,i2,-i3,-i4)    = m2aqaq0ss(-i1,i4,i3,-i2)*.5d0
     &         + m2aqaq0tt(-i1,i4,i3,-i2)*.5d0 
     &	       + m2aqaq0st(-i1,i4,i3,-i2)*.5d0
            m2i0(i1,i2) = m2i0(i1,i2) + m2if0hvv(i1,i2,-i3,-i4)
	  endif
300     continue
          if ((i1.ne.-1).or.(i2.ne.1)) m2i0(i1,i2) = 0d0
200     continue


	if (qhvv.ne.0) then

	call setprods3(p)

c qbar-q --> qbar-q
        call Mat2aqqbornhvv(m2aqq0ss,m2aqq0tt,m2aqq0st,
     &	                    -1,-2,3,4,qb)
c q-q    --> q-q
        call Mat2aqqbornhvv(m2qq0ss,m2qq0tt,m2qq0st,
     &	                    3,-2,-1,4,qb)
c q-qbar --> q-qbar
        call Mat2aqqbornhvv(m2qaq0ss,m2qaq0tt,m2qaq0st,
     &	                    -2,-1,4,3,qb)
c qbar-qbar --> qbar-qbar
        call Mat2aqqbornhvv(m2aqaq0ss,m2aqaq0tt,m2aqaq0st,
     &	                    -1,4,3,-2,qb)

	endif

c add final states for fixed initial states
        do 201 i1=-4-qbini,4+qbini
        do 201 i2=-4-qbini,4+qbini
          m2i0(i1,i2) = 0d0
          if (i1*i2.eq.0) goto 201
        do 301 i3=1,4+qbfin
        do 301 i4=1,4+qbfin
          if(i1.gt.0) then
            if ((i2.gt.0)) then
              m2if0_22(i1,i2,i3,i4) = 0d0
              m2if0_33(i1,i2,i3,i4) = m2qq0tt(i3,i2,i1,i4)*.5d0
              m2if0_44(i1,i2,i3,i4) = m2qq0ss(i3,i2,i1,i4)*.5d0
              m2if0hvv(i1,i2,i3,i4) = m2qq0ss(i3,i2,i1,i4)*.5d0
     &           + m2qq0tt(i3,i2,i1,i4)*.5d0 + m2qq0st(i3,i2,i1,i4)*.5d0
              m2i0(i1,i2) = m2i0(i1,i2) + m2if0hvv(i1,i2,i3,i4)
            else
              m2if0_22(i1,i2,i3,-i4) = m2qaq0ss(-i2,i1,i4,i3)
              m2if0_33(i1,i2,i3,-i4) = m2qaq0tt(-i2,i1,i4,i3)
              m2if0_44(i1,i2,i3,-i4) = 0d0
              m2if0hvv(i1,i2,i3,-i4) = m2qaq0ss(-i2,i1,i4,i3)
     &           + m2qaq0tt(-i2,i1,i4,i3) + m2qaq0st(-i2,i1,i4,i3)
              m2i0(i1,i2) = m2i0(i1,i2) + m2if0hvv(i1,i2,i3,-i4)
            endif
          elseif (i2.gt.0) then
            m2if0_22(i1,i2,-i3,i4) = m2aqq0ss(-i1,i2,i3,i4)
            m2if0_33(i1,i2,-i3,i4) = m2aqq0tt(-i1,i2,i3,i4)
            m2if0_44(i1,i2,-i3,i4) = 0d0
            m2if0hvv(i1,i2,-i3,i4) = m2aqq0ss(-i1,i2,i3,i4)
     &         + m2aqq0tt(-i1,i2,i3,i4) + m2aqq0st(-i1,i2,i3,i4)
            m2i0(i1,i2) = m2i0(i1,i2) + m2if0hvv(i1,i2,-i3,i4)
          else
            m2if0_22(i1,i2,-i3,-i4) = 0d0
            m2if0_33(i1,i2,-i3,-i4) = m2aqaq0tt(-i1,i4,i3,-i2)*.5d0
            m2if0_44(i1,i2,-i3,-i4) = m2aqaq0ss(-i1,i4,i3,-i2)*.5d0
            m2if0hvv(i1,i2,-i3,-i4) = m2aqaq0ss(-i1,i4,i3,-i2)*.5d0
     &         + m2aqaq0tt(-i1,i4,i3,-i2)*.5d0 
     &	       + m2aqaq0st(-i1,i4,i3,-i2)*.5d0
            m2i0(i1,i2) = m2i0(i1,i2) + m2if0hvv(i1,i2,-i3,-i4)
	  endif
301     continue
201     continue

	end
************************************************************************
      subroutine Mat2aqqborn(m2aqq0ss,m2aqq0tt,m2aqq0st,
     &     s,s12,t11,t21,t12,t22,
     &     pws,pws12,pwt11,pwt22,pzs,pzs12,pzt11,pzt22,qb)
************************************************************************
*       generic Born structures needed for subtraction function for
*	    anti-q(p1) + q(p2) --> f(p3) + f'(p4) + H(p5)
*
*       from generic amplitudes for
*	    H(p) --> fa(k1) + anti-fb(k2) + fc(k3) + anti-fd(k4)
*	         CC: f1     + anti-f2     + f3     + anti-f4     
*	         NC: f1     + anti-f1     + f3     + anti-f3     
*	             f2     + anti-f2     + f3     + anti-f3     
*	             f1     + anti-f1     + f4     + anti-f4     
*
*	fermions: f1,f4 = generic   up-type fermions
*	          f2,f3 = generic down-type fermions
*-----------------------------------------------------------------------
*       13.10.06 Stefan Dittmaier
************************************************************************
      implicit real*8 (a-z)
      complex*16 pre,pres,pret,mats0,matt0,wmats0,wmatt0
	complex*16 v,cv
	complex*16 pws,pws12,pwt11,pwt22
	complex*16 pzs,pzs12,pzt11,pzt22
        complex*16 ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2,cmh,cmh2
        complex*16 xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null
        complex*16 xml,xml2,xmqp,xmqp2,xmqm,xmqm2
	real*8 m1243sq(-1:1,-1:1),m4213sq(-1:1,-1:1)
        real*8 m2aqq0ss(5,5,5,5),m2aqq0tt(5,5,5,5),m2aqq0st(5,5,5,5)
	integer ia,ib,ic,id
	integer i1,i2,i3,i4,j,j1,j2,f1,f2,f3,f4,g1,g2,g3,g4,qb
        integer qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &			 qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
	complex*16 guu,gdd,gnn,gll     
	logical checkss12,checkt11t22

        common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &         v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &         ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
        common/rcoptions/qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &			 qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
        common/cparam/ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
        common/xparam/xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null,
     &       xml(3),xml2(3),xmqp(3),xmqp2(3),xmqm(3),xmqm2(3)
        common/qf/qu,qd,ql,qn,qf(4),mu,mu2,md,md2,mlep,mlep2,
     +       guu(-1:1),gdd(-1:1),gnn(-1:1),gll(-1:1)

	el3 = el**3

        m1243sq(1,1)   = 4D0*t12*t21
        m1243sq(-1,1)  = 4D0*t11*t22
        m1243sq(1,-1)  = m1243sq(-1,1)
        m1243sq(-1,-1) = m1243sq(1,1)

        M4213sq(1,1)   = m1243sq(1,1)
        M4213sq(-1,1)  = 4D0*s*s12
        M4213sq(1,-1)  = M4213sq(-1,1)
        M4213sq(-1,-1) = m1243sq(-1,-1)

	checkss12   = ((  s*qschan.gt.0d0).or.(  s*qtchan.lt.0d0)).and.
     &	              ((s12*qschan.gt.0d0).or.(s12*qtchan.lt.0d0))
	checkt11t22 = ((t11*qschan.gt.0d0).or.(t11*qtchan.lt.0d0)).and.
     &	              ((t22*qschan.gt.0d0).or.(t22*qtchan.lt.0d0))


c qbar-q scattering
c
c   s-channel:                             t-channel:
c
c   fa(p1) \_          / fd(p3)            fa(p1) --<--*--<-- fb(p3)
c          |\        |/                                >
c            \       /-                                >
c             *vvvvv*                                  >
c           _/       \                                 >
c           /|        \|                               >
c   fb(p2) /          -\ fc(p4)            fd(p2) -->--*-->-- fc(p4)


c Type: ubar-d -> ubar-d
c-----------------------

c*** generic amplitudes
	pres = 0d0
	pret = 0d0

c ubar-d -W-> cbar-s    (k1->-p1,k2->-p2,k3->p4,k4->p3)   
        if (checkss12) pres = qw*el3*PWS12*PWS*XMW/(2D0*XSW*XSW2)

c ubar-s -Z-> ubar-s    (k1->-p1,k2->p3,k3->p4,k4->-p2)   
        if (checkt11t22) pret = qz*el3*PZT11*PZT22/XSW/XCW2*XMW

c*** individual channels
 	do 200 g1=1,2
 	do 200 g2=1,2+qb
 	do 200 g3=1,2
 	do 200 g4=1,2+qb
 	  f1 = 2*g1
 	  f2 = 2*g2-1
 	  f3 = 2*g3
 	  f4 = 2*g4-1
 	  m2aqq0ss(f1,f2,f3,f4) = 0d0
 	  m2aqq0tt(f1,f2,f3,f4) = 0d0
 	  m2aqq0st(f1,f2,f3,f4) = 0d0

	do 200 i1=1,4

	  if (i1.eq.1) then
	    mats0  = 0d0
	    matt0  = pret*guu(-1)*gdd(+1)
	    fac    = m4213sq(-1,+1)
	  elseif (i1.eq.2) then
	    mats0  = -pres
	    matt0  = pret*guu(-1)*gdd(-1)
	    fac    = m4213sq(-1,-1)
	  elseif (i1.eq.3) then
	    mats0  = 0d0
	    matt0  = pret*guu(+1)*gdd(+1)
	    fac    = m4213sq(+1,+1)
	  elseif (i1.eq.4) then
	    mats0  = 0d0
	    matt0  = pret*guu(+1)*gdd(-1)
	    fac    = m4213sq(+1,-1)
	  endif

 	  wmats0   = cv(g1,g2)*v(g3,g4)*mats0

 	  if ((f1.eq.f3).and.(f2.eq.f4)) then
 	    m2aqq0ss(f1,f2,f3,f4) = m2aqq0ss(f1,f2,f3,f4) 
     &		         + fac*9d0*abs(wmats0)**2 *qch2
 	    m2aqq0tt(f1,f2,f3,f4) = m2aqq0tt(f1,f2,f3,f4) 
     &		         + fac*9d0*abs(matt0)**2 *qch2
 	    m2aqq0st(f1,f2,f3,f4) = m2aqq0st(f1,f2,f3,f4) 
     &	          - fac*3d0*2d0*dreal(wmats0*dconjg(matt0)) *qchint 
 	  else
 	    m2aqq0ss(f1,f2,f3,f4) = m2aqq0ss(f1,f2,f3,f4) 
     &			 + fac*9d0*abs(wmats0)**2 *qch2 
 	  endif

200	continue

c Type: dbar-u -> dbar-u
c-----------------------

c*** generic amplitudes
	pres = 0d0
	pret = 0d0

c dbar-u -W-> sbar-c    (k3->-p1,k4->-p2,k1->p4,k2->p3)   
	if (checkss12) pres = qw*el3*PWS12*PWS*XMW/(2D0*XSW*XSW2)

c dbar-c -Z-> dbar-c    (k3->-p1,k4->p3,k1->p4,k2->-p2)   
        if (checkt11t22) pret = qz*el3*PZT11*PZT22*XMW/(XSW*XCW2)

 	do 205 g1=1,2+qb
 	do 205 g2=1,2
 	do 205 g3=1,2+qb
 	do 205 g4=1,2
 	  f1 = 2*g1-1
 	  f2 = 2*g2
 	  f3 = 2*g3-1
 	  f4 = 2*g4
 	  m2aqq0ss(f1,f2,f3,f4) = 0d0
 	  m2aqq0tt(f1,f2,f3,f4) = 0d0
 	  m2aqq0st(f1,f2,f3,f4) = 0d0

	do 205 i1=1,4

	  if (i1.eq.1) then
	    mats0  = 0d0
	    matt0  = pret*guu(+1)*gdd(-1)
	    fac    = m4213sq(-1,+1)
	  elseif (i1.eq.2) then
	    mats0  = -pres
	    matt0  = pret*guu(-1)*gdd(-1)
	    fac    = m4213sq(-1,-1)
	  elseif (i1.eq.3) then
	    mats0  = 0d0
	    matt0  = pret*guu(+1)*gdd(+1)
	    fac    = m4213sq(+1,+1)
	  elseif (i1.eq.4) then
	    mats0  = 0d0
	    matt0  = pret*guu(-1)*gdd(+1)
	    fac    = m4213sq(+1,-1)
	  endif

 	  wmats0 = v(g2,g1)*cv(g4,g3)*mats0

 	  if ((f1.eq.f3).and.(f2.eq.f4)) then
 	    m2aqq0ss(f1,f2,f3,f4) = m2aqq0ss(f1,f2,f3,f4) 
     &		         + fac*9d0*abs(wmats0)**2 *qch2 
 	    m2aqq0tt(f1,f2,f3,f4) = m2aqq0tt(f1,f2,f3,f4) 
     &		         + fac*9d0*abs(matt0)**2 *qch2 
 	    m2aqq0st(f1,f2,f3,f4) = m2aqq0st(f1,f2,f3,f4) 
     &	          - fac*3d0*2d0*dreal(wmats0*dconjg(matt0)) *qchint
 	  else
 	    m2aqq0ss(f1,f2,f3,f4) = m2aqq0ss(f1,f2,f3,f4) 
     &			 + fac*9d0*abs(wmats0)**2 *qch2 
 	  endif
205	continue


c Type: ubar-u -> ubar-u
c----------------------- 

c*** generic amplitudes
	pres = 0d0
	pret = 0d0

c ubar-u -Z-> cbar-c  (k1->-p1,k2->-p2,k3->p4,k4->p3)
	if (checkss12) pres = qz*el3*PZS*PZS12*XMW/(XSW*XCW2)

c ubar-c -Z-> ubar-c  (k1->-p1,k2->p3,k3->p4,k4->-p2)
	if (checkt11t22) pret = qz*el3*PZT11*PZT22*XMW/(XSW*XCW2)

	m2aqq0ss(2,2,2,2) = 0d0
	m2aqq0tt(2,2,2,2) = 0d0
	m2aqq0st(2,2,2,2) = 0d0
	m2aqq0ss(2,2,4,4) = 0d0
	m2aqq0tt(2,2,4,4) = 0d0
	m2aqq0st(2,2,4,4) = 0d0
	m2aqq0ss(2,4,2,4) = 0d0
	m2aqq0tt(2,4,2,4) = 0d0
	m2aqq0st(2,4,2,4) = 0d0

	do 201 i1=1,6

	if (i1.eq.1) then
	  mats0  = 0d0
	  matt0  = pret*guu(+1)*guu(-1)
	  fac    = m4213sq(-1,+1)
	elseif (i1.eq.2) then
	  mats0  = -pres*guu(-1)*guu(-1)
	  matt0  =  pret*guu(-1)*guu(-1)
	  fac    = m4213sq(-1,-1)
	elseif (i1.eq.3) then
	  mats0  = -pres*guu(+1)*guu(+1)
	  matt0  =  pret*guu(+1)*guu(+1)
	  fac    = m4213sq(+1,+1)
	elseif (i1.eq.4) then
	  mats0  = 0d0
	  matt0  = pret*guu(-1)*guu(+1)
	  fac    = m4213sq(+1,-1)
	elseif (i1.eq.5) then
	  mats0  = pres*guu(-1)*guu(+1)
	  matt0  = 0d0
	  fac    = m1243sq(-1,+1)
	elseif (i1.eq.6) then
	  mats0  = pres*guu(+1)*guu(-1)
	  matt0  = 0d0
	  fac    = m1243sq(+1,-1)
	endif

c*** ubar-u -ZZ-> ubar-u    
	m2aqq0ss(2,2,2,2) = m2aqq0ss(2,2,2,2) 
     &			    + fac*9d0*abs(mats0)**2 *qch2
	m2aqq0tt(2,2,2,2) = m2aqq0tt(2,2,2,2) 
     &			    + fac*9d0*abs(matt0)**2 *qch2 
	m2aqq0st(2,2,2,2) = m2aqq0st(2,2,2,2) 
     &	      - fac*3d0*2d0*dreal(mats0*dconjg(matt0)) *qchint
c*** ubar-u -Z-> cbar-c 
	m2aqq0ss(2,2,4,4) = m2aqq0ss(2,2,4,4) 
     &			    + fac*9d0*abs(mats0)**2 *qch2 
c*** ubar-c -Z-> ubar-c 
	m2aqq0tt(2,4,2,4) = m2aqq0tt(2,4,2,4) 
     &			    + fac*9d0*abs(matt0)**2 *qch2 
201	continue
	m2aqq0ss(4,4,4,4) = m2aqq0ss(2,2,2,2) 
	m2aqq0tt(4,4,4,4) = m2aqq0tt(2,2,2,2) 
	m2aqq0st(4,4,4,4) = m2aqq0st(2,2,2,2) 
	m2aqq0ss(4,4,2,2) = m2aqq0ss(2,2,4,4)
	m2aqq0tt(4,4,2,2) = m2aqq0tt(2,2,4,4)
	m2aqq0st(4,4,2,2) = m2aqq0st(2,2,4,4)
	m2aqq0ss(4,2,4,2) = m2aqq0ss(2,4,2,4)
	m2aqq0tt(4,2,4,2) = m2aqq0tt(2,4,2,4)
	m2aqq0st(4,2,4,2) = m2aqq0st(2,4,2,4)


c Type: ubar-u -> dbar-d
c----------------------- 

c*** generic amplitudes
	pres = 0d0
	pret = 0d0

c ubar-u -Z-> sbar-s  (k1->-p1,k2->-p2,k3->p4,k4->p3)
        if (checkss12) pres = qz*el3*PZS*PZS12*XMW/(XSW*XCW2)

c ubar-u -W-> dbar-d  (k1->-p1,k2->p3,k3->p4,k4->-p2)
	if (checkt11t22) pret = qw*el3*PWT11*PWT22*XMW/(2D0*XSW*XSW2)

 	do 202 g1=1,2
 	do 202 g2=1,2
 	do 202 g3=1,2+qb
 	do 202 g4=1,2+qb
 	  f1 = 2*g1
 	  f2 = 2*g2
 	  f3 = 2*g3-1
 	  f4 = 2*g4-1
 	  m2aqq0ss(f1,f2,f3,f4) = 0d0
 	  m2aqq0tt(f1,f2,f3,f4) = 0d0
 	  m2aqq0st(f1,f2,f3,f4) = 0d0

	do 202 i1=1,4

	  if (i1.eq.1) then
	    matt0  = 0d0
	    mats0  = pres*guu(+1)*gdd(-1)
	    fac    = m1243sq(-1,+1)
	  elseif (i1.eq.2) then
	    matt0  = -pret
	    mats0  = pres*guu(-1)*gdd(-1)
	    fac    = m1243sq(-1,-1)
	  elseif (i1.eq.3) then
	    matt0  = 0d0
	    mats0  = pres*guu(+1)*gdd(+1)
	    fac    = m1243sq(+1,+1)
	  elseif (i1.eq.4) then
	    matt0  = 0d0
	    mats0  = pres*guu(-1)*gdd(+1)
	    fac    = m1243sq(+1,-1)
	  endif

 	  wmatt0 = cv(g1,g3)*v(g2,g4)*matt0

 	  if ((f1.eq.f2).and.(f3.eq.f4)) then
 	    m2aqq0ss(f1,f2,f3,f4) = m2aqq0ss(f1,f2,f3,f4) 
     &		          + fac*9d0*abs(mats0)**2 *qch2 
 	    m2aqq0tt(f1,f2,f3,f4) = m2aqq0tt(f1,f2,f3,f4) 
     &		          + fac*9d0*abs(wmatt0)**2 *qch2
 	    m2aqq0st(f1,f2,f3,f4) = m2aqq0st(f1,f2,f3,f4) 
     &	          - fac*3d0*2d0*dreal(wmatt0*dconjg(mats0)) *qchint
 	  else
 	    m2aqq0tt(f1,f2,f3,f4) = m2aqq0tt(f1,f2,f3,f4) 
     &			 + fac*9d0*abs(wmatt0)**2 *qch2 
 	  endif
202	  continue


c Type: dbar-d -> dbar-d
c-----------------------

c*** generic amplitudes
	pres = 0d0
	pret = 0d0

c ubar-u -Z-> cbar-c  (k1->-p1,k2->-p2,k3->p4,k4->p3)
	if (checkss12) pres = qz*el3*PZS*PZS12*XMW/(XSW*XCW2)

c ubar-c -Z-> ubar-c  (k1->-p1,k2->p3,k3->p4,k4->-p2)
	if (checkt11t22) pret = qz*el3*PZT11*PZT22*XMW/(XSW*XCW2)

	m2aqq0ss(1,1,1,1) = 0d0
	m2aqq0tt(1,1,1,1) = 0d0
	m2aqq0st(1,1,1,1) = 0d0
	m2aqq0ss(1,1,3,3) = 0d0
	m2aqq0tt(1,1,3,3) = 0d0
	m2aqq0st(1,1,3,3) = 0d0
	m2aqq0ss(1,3,1,3) = 0d0
	m2aqq0tt(1,3,1,3) = 0d0
	m2aqq0st(1,3,1,3) = 0d0

	do 203 i1=1,6

	if (i1.eq.1) then
	  mats0  = 0d0
	  matt0  = pret*gdd(+1)*gdd(-1)
	  fac    = m4213sq(-1,+1)
	elseif (i1.eq.2) then
	  mats0  = -pres*gdd(-1)*gdd(-1)
	  matt0  =  pret*gdd(-1)*gdd(-1)
	  fac    = m4213sq(-1,-1)
	elseif (i1.eq.3) then
	  mats0  = -pres*gdd(+1)*gdd(+1)
	  matt0  =  pret*gdd(+1)*gdd(+1)
	  fac    = m4213sq(+1,+1)
	elseif (i1.eq.4) then
	  mats0  = 0d0
	  matt0  = pret*gdd(-1)*gdd(+1)
	  fac    = m4213sq(+1,-1)
	elseif (i1.eq.5) then
	  mats0  = pres*gdd(-1)*gdd(+1)
	  matt0  = 0d0
	  fac    = m1243sq(-1,+1)
	elseif (i1.eq.6) then
	  mats0  = pres*gdd(+1)*gdd(-1)
	  matt0  = 0d0
	  fac    = m1243sq(+1,-1)
	endif

c*** dbar-d -ZZ-> dbar-d    
	m2aqq0ss(1,1,1,1) = m2aqq0ss(1,1,1,1) 
     &			    + fac*9d0*abs(mats0)**2 *qch2
	m2aqq0tt(1,1,1,1) = m2aqq0tt(1,1,1,1) 
     &			    + fac*9d0*abs(matt0)**2 *qch2
	m2aqq0st(1,1,1,1) = m2aqq0st(1,1,1,1) 
     &	       - fac*3d0*2d0*dreal(mats0*dconjg(matt0)) *qchint
c*** dbar-d -Z-> sbar-s 
	m2aqq0ss(1,1,3,3) = m2aqq0ss(1,1,3,3) 
     &			    + fac*9d0*abs(mats0)**2 *qch2 
c*** dbar-s -Z-> dbar-s 
	m2aqq0tt(1,3,1,3) = m2aqq0tt(1,3,1,3) 
     &			    + fac*9d0*abs(matt0)**2 *qch2 
203	continue
	m2aqq0ss(3,3,3,3) = m2aqq0ss(1,1,1,1) 
	m2aqq0tt(3,3,3,3) = m2aqq0tt(1,1,1,1) 
	m2aqq0st(3,3,3,3) = m2aqq0st(1,1,1,1) 
	m2aqq0ss(3,3,1,1) = m2aqq0ss(1,1,3,3)
	m2aqq0tt(3,3,1,1) = m2aqq0tt(1,1,3,3)
	m2aqq0st(3,3,1,1) = m2aqq0st(1,1,3,3)
	m2aqq0ss(3,1,3,1) = m2aqq0ss(1,3,1,3)
	m2aqq0tt(3,1,3,1) = m2aqq0tt(1,3,1,3)
	m2aqq0st(3,1,3,1) = m2aqq0st(1,3,1,3)
	if (qb.eq.1) then
        m2aqq0ss(5,5,5,5) = m2aqq0ss(1,1,1,1)
        m2aqq0tt(5,5,5,5) = m2aqq0tt(1,1,1,1)
        m2aqq0st(5,5,5,5) = m2aqq0st(1,1,1,1)
        m2aqq0ss(1,1,5,5) = m2aqq0ss(1,1,3,3)
        m2aqq0tt(1,1,5,5) = m2aqq0tt(1,1,3,3)
        m2aqq0st(1,1,5,5) = m2aqq0st(1,1,3,3)
        m2aqq0ss(3,3,5,5) = m2aqq0ss(1,1,3,3)
        m2aqq0tt(3,3,5,5) = m2aqq0tt(1,1,3,3)
        m2aqq0st(3,3,5,5) = m2aqq0st(1,1,3,3)
        m2aqq0ss(5,5,1,1) = m2aqq0ss(1,1,3,3)
        m2aqq0tt(5,5,1,1) = m2aqq0tt(1,1,3,3)
        m2aqq0st(5,5,1,1) = m2aqq0st(1,1,3,3)
        m2aqq0ss(5,5,3,3) = m2aqq0ss(1,1,3,3)
        m2aqq0tt(5,5,3,3) = m2aqq0tt(1,1,3,3)
        m2aqq0st(5,5,3,3) = m2aqq0st(1,1,3,3)
        m2aqq0ss(1,5,1,5) = m2aqq0ss(1,3,1,3)
        m2aqq0tt(1,5,1,5) = m2aqq0tt(1,3,1,3)
        m2aqq0st(1,5,1,5) = m2aqq0st(1,3,1,3)
        m2aqq0ss(3,5,3,5) = m2aqq0ss(1,3,1,3)
        m2aqq0tt(3,5,3,5) = m2aqq0tt(1,3,1,3)
        m2aqq0st(3,5,3,5) = m2aqq0st(1,3,1,3)
        m2aqq0ss(5,1,5,1) = m2aqq0ss(1,3,1,3)
        m2aqq0tt(5,1,5,1) = m2aqq0tt(1,3,1,3)
        m2aqq0st(5,1,5,1) = m2aqq0st(1,3,1,3)
        m2aqq0ss(5,3,5,3) = m2aqq0ss(1,3,1,3)
        m2aqq0tt(5,3,5,3) = m2aqq0tt(1,3,1,3)
        m2aqq0st(5,3,5,3) = m2aqq0st(1,3,1,3)
	endif

c Type: dbar-d -> ubar-u
c-----------------------
	pres = 0d0
	pret = 0d0

c*** generic amplitudes

c dbar-d -Z-> cbar-c  (k3->-p1,k4->-p2,k1->p4,k2->p3)
        if (checkss12) pres = qz*el3*PZS*PZS12*XMW/(XSW*XCW2)

c dbar-s -W-> ubar-c  (k3->-p1,k4->p3,k1->p4,k2->-p2)
	if (checkt11t22) pret = qw*el3*PWT11*PWT22*XMW/(2D0*XSW*XSW2)

 	do 204 g1=1,2+qb
 	do 204 g2=1,2+qb
 	do 204 g3=1,2
 	do 204 g4=1,2
 	  f1 = 2*g1-1
 	  f2 = 2*g2-1
 	  f3 = 2*g3
 	  f4 = 2*g4
 	  m2aqq0ss(f1,f2,f3,f4) = 0d0
 	  m2aqq0tt(f1,f2,f3,f4) = 0d0
 	  m2aqq0st(f1,f2,f3,f4) = 0d0

	do 204 i1=1,4

	  if (i1.eq.1) then
	    matt0  = 0d0
	    mats0  = pres*guu(-1)*gdd(+1)
	    fac    = m1243sq(-1,+1)
	  elseif (i1.eq.2) then
	    matt0  = -pret
	    mats0  = pres*guu(-1)*gdd(-1)
	    fac    = m1243sq(-1,-1)
	  elseif (i1.eq.3) then
	    matt0  = 0d0
	    mats0  = pres*guu(+1)*gdd(+1)
	    fac    = m1243sq(+1,+1)
	  elseif (i1.eq.4) then
	    matt0  = 0d0
	    mats0  = pres*guu(+1)*gdd(-1)
	    fac    = m1243sq(+1,-1)
	  endif

 	  wmatt0 = v(g3,g1)*cv(g4,g2)*matt0

 	  if ((f1.eq.f2).and.(f3.eq.f4)) then
 	    m2aqq0ss(f1,f2,f3,f4) = m2aqq0ss(f1,f2,f3,f4) 
     &		         + fac*9d0*abs(mats0)**2 *qch2
 	    m2aqq0tt(f1,f2,f3,f4) = m2aqq0tt(f1,f2,f3,f4) 
     &		         + fac*9d0*abs(wmatt0)**2 *qch2
 	    m2aqq0st(f1,f2,f3,f4) = m2aqq0st(f1,f2,f3,f4) 
     &	          - fac*3d0*2d0*dreal(wmatt0*dconjg(mats0)) *qchint
 	  else
 	    m2aqq0tt(f1,f2,f3,f4) = m2aqq0tt(f1,f2,f3,f4) 
     &			 + fac*9d0*abs(wmatt0)**2 *qch2 
 	  endif
204	  continue

	end
************************************************************************
********************************************************************************
        subroutine Mat2aqqbornhvv(m2aqq0ss,m2aqq0tt,m2aqq0st,
     &	                          q1,q2,q3,q4,qb)
************************************************************************
*       generic Born structures needed for subtraction function for
*	    anti-q(p1) + q(p2) --> f(p3) + f'(p4) + H(p5)
*
*	including anomalous HVV couplings !!!
*
*       from generic amplitudes for
*	    H(p) --> fa(k1) + anti-fb(k2) + fc(k3) + anti-fd(k4)
*	         CC: f1     + anti-f2     + f3     + anti-f4     
*	         NC: f1     + anti-f1     + f3     + anti-f3     
*	             f2     + anti-f2     + f3     + anti-f3     
*	             f1     + anti-f1     + f4     + anti-f4     
*
*	fermions: f1,f4 = generic   up-type fermions
*	          f2,f3 = generic down-type fermions
*-----------------------------------------------------------------------
*       14.6.12 Stefan Dittmaier
************************************************************************
        implicit real*8 (a-z)
	complex*16 msH4f(-1:1,-1:1),mtH4f(-1:1,-1:1)
	complex*16 mats0,matt0,wmats0,wmatt0
	complex*16 sp(-4:4,-4:4),csp(-4:4,-4:4)
	complex*16 v,cv
        complex*16 ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2,cmh,cmh2
        complex*16 xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null
        complex*16 xml,xml2,xmqp,xmqp2,xmqm,xmqm2
        real*8 m2aqq0ss(5,5,5,5),m2aqq0tt(5,5,5,5),m2aqq0st(5,5,5,5)
        real*8 vp(-4:4,-4:4)
	integer ia,ib,ic,id,q1,q2,q3,q4
	integer i1,i2,i3,i4,j,j1,j2,f1,f2,f3,f4,g1,g2,g3,g4,qb
        integer qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &			 qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
	complex*16 guu,gdd,gnn,gll     
C
        common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &         v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &         ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
        common/rcoptions/qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &			 qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
        common/cparam/ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
        common/xparam/xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null,
     &       xml(3),xml2(3),xmqp(3),xmqp2(3),xmqm(3),xmqm2(3)
        common/qf/qu,qd,ql,qn,qf(4),mu,mu2,md,md2,mlep,mlep2,
     &       guu(-1:1),gdd(-1:1),gnn(-1:1),gll(-1:1)

	common/prods3/sp,csp,vp

	fac = el**6

c invariants
        s   = vp(q1,q2)
	s12 = vp(q3,q4)
	t11 = vp(q1,q3)
	t22 = vp(q2,q4)

	call fixahvv(s,s12,
     &             a1hwws,a2hwws,a3hwws,a1haas,a2haas,a3haas,
     &             a1hazs,a2hazs,a3hazs,a1hzzs,a2hzzs,a3hzzs)
	call fixahvv(t11,t22,
     &             a1hwwt,a2hwwt,a3hwwt,a1haat,a2haat,a3haat,
     &             a1hazt,a2hazt,a3hazt,a1hzzt,a2hzzt,a3hzzt)

c qbar-q scattering
c
c   s-channel:                             t-channel:
c
c   fa(p1) \_          / fd(p3)            fa(p1) --<--*--<-- fb(p3)
c          |\        |/                                >
c            \       /-                                >
c             *vvvvv*                                  >
c           _/       \                                 >
c           /|        \|                               >
c   fb(p2) /          -\ fc(p4)            fd(p2) -->--*-->-- fc(p4)


c Type: ubar-d -> ubar-d
c-----------------------

c*** generic amplitudes
	do i1=-1,1,2
	do i2=-1,1,2
	  msH4f(i1,i2) = 0d0
	  mtH4f(i1,i2) = 0d0
	enddo
	enddo

c ubar-d -W-> cbar-s    (k1->-p1,k2->-p2,k3->p4,k4->p3)   
	if (qw.eq.1) call M_WW_hvv(msH4f,q1,q2,q4,q3,
     &	                  a1hwws,a2hwws,a3hwws)

c ubar-s -Z-> ubar-s    (k1->-p1,k2->p3,k3->p4,k4->-p2)   
	if (qz.eq.1) call M_ZZ_hvv(mtH4f,guu,gdd,qu,qd,q1,q3,q4,q2,
     &	                  a1haat,a2haat,a3haat,a1hazt,a2hazt,a3hazt,
     &	                  a1hzzt,a2hzzt,a3hzzt)

c*** individual channels
 	do 200 g1=1,2
 	do 200 g2=1,2+qb
 	do 200 g3=1,2
 	do 200 g4=1,2+qb
 	  f1 = 2*g1
 	  f2 = 2*g2-1
 	  f3 = 2*g3
 	  f4 = 2*g4-1
 	  m2aqq0ss(f1,f2,f3,f4) = 0d0
 	  m2aqq0tt(f1,f2,f3,f4) = 0d0
 	  m2aqq0st(f1,f2,f3,f4) = 0d0

	do 200 i1=-1,1,2
	do 200 i2=-1,1,2
	do 200 i3=-1,1,2
	  mats0  = 0d0
	  matt0  = 0d0

          if (i1.eq.-i2) mats0  = msH4f(i2,i3)
          if (i1.eq.-i3) matt0  = mtH4f(i3,i2)

 	  wmats0 = cv(g1,g2)*v(g3,g4)*mats0

 	  if ((f1.eq.f3).and.(f2.eq.f4)) then
 	    m2aqq0ss(f1,f2,f3,f4) = m2aqq0ss(f1,f2,f3,f4) 
     &		         + fac*9d0*abs(wmats0)**2 *qch2
 	    m2aqq0tt(f1,f2,f3,f4) = m2aqq0tt(f1,f2,f3,f4) 
     &		         + fac*9d0*abs(matt0)**2 *qch2
 	    m2aqq0st(f1,f2,f3,f4) = m2aqq0st(f1,f2,f3,f4) 
     &	          - fac*3d0*2d0*dreal(wmats0*dconjg(matt0)) *qchint 
 	  else
 	    m2aqq0ss(f1,f2,f3,f4) = m2aqq0ss(f1,f2,f3,f4) 
     &			 + fac*9d0*abs(wmats0)**2 *qch2 
 	  endif

200	continue

c Type: dbar-u -> dbar-u
c-----------------------

c*** generic amplitudes
	do i1=-1,1,2
	do i2=-1,1,2
	  msH4f(i1,i2) = 0d0
	  mtH4f(i1,i2) = 0d0
	enddo
	enddo

c dbar-u -W-> sbar-c    (k3->-p1,k4->-p2,k1->p4,k2->p3)   
	if (qw.eq.1) call M_WW_hvv(msH4f,q4,q3,q1,q2,
     &	                  a1hwws,a2hwws,a3hwws)

c dbar-c -Z-> dbar-c    (k3->-p1,k4->p3,k1->p4,k2->-p2)   
	if (qz.eq.1) call M_ZZ_hvv(mtH4f,guu,gdd,qu,qd,q4,q2,q1,q3,
     &	                  a1haat,a2haat,a3haat,a1hazt,a2hazt,a3hazt,
     &	                  a1hzzt,a2hzzt,a3hzzt)

 	do 205 g1=1,2+qb
 	do 205 g2=1,2
 	do 205 g3=1,2+qb
 	do 205 g4=1,2
 	  f1 = 2*g1-1
 	  f2 = 2*g2
 	  f3 = 2*g3-1
 	  f4 = 2*g4
 	  m2aqq0ss(f1,f2,f3,f4) = 0d0
 	  m2aqq0tt(f1,f2,f3,f4) = 0d0
 	  m2aqq0st(f1,f2,f3,f4) = 0d0

	do 205 i1=-1,1,2
	do 205 i2=-1,1,2
	do 205 i3=-1,1,2
	  mats0  = 0d0
	  matt0  = 0d0

	   if (i1.eq.-i2) mats0  = msH4f(i3,i2)
	   if (i1.eq.-i3) matt0  = mtH4f(i2,i3)

 	  wmats0 = v(g2,g1)*cv(g4,g3)*mats0

 	  if ((f1.eq.f3).and.(f2.eq.f4)) then
 	    m2aqq0ss(f1,f2,f3,f4) = m2aqq0ss(f1,f2,f3,f4) 
     &		         + fac*9d0*abs(wmats0)**2 *qch2 
 	    m2aqq0tt(f1,f2,f3,f4) = m2aqq0tt(f1,f2,f3,f4) 
     &		         + fac*9d0*abs(matt0)**2 *qch2 
 	    m2aqq0st(f1,f2,f3,f4) = m2aqq0st(f1,f2,f3,f4) 
     &	          - fac*3d0*2d0*dreal(wmats0*dconjg(matt0)) *qchint
 	  else
 	    m2aqq0ss(f1,f2,f3,f4) = m2aqq0ss(f1,f2,f3,f4) 
     &			 + fac*9d0*abs(wmats0)**2 *qch2 
 	  endif
205	continue


c Type: ubar-u -> ubar-u
c----------------------- 

c*** generic amplitudes
	do i1=-1,1,2
	do i2=-1,1,2
	  msH4f(i1,i2) = 0d0
	  mtH4f(i1,i2) = 0d0
	enddo
	enddo

c ubar-u -Z-> cbar-c  (k1->-p1,k2->-p2,k3->p4,k4->p3)
	if (qz.eq.1) call M_ZZ_hvv(msH4f,guu,guu,qu,qu,q1,q2,q4,q3,
     &	                  a1haas,a2haas,a3haas,a1hazs,a2hazs,a3hazs,
     &	                  a1hzzs,a2hzzs,a3hzzs)

c ubar-c -Z-> ubar-c  (k1->-p1,k2->p3,k3->p4,k4->-p2)
	if (qz.eq.1) call M_ZZ_hvv(mtH4f,guu,guu,qu,qu,q1,q3,q4,q2,
     &	                  a1haat,a2haat,a3haat,a1hazt,a2hazt,a3hazt,
     &	                  a1hzzt,a2hzzt,a3hzzt)

	m2aqq0ss(2,2,2,2) = 0d0
	m2aqq0tt(2,2,2,2) = 0d0
	m2aqq0st(2,2,2,2) = 0d0
	m2aqq0ss(2,2,4,4) = 0d0
	m2aqq0tt(2,2,4,4) = 0d0
	m2aqq0st(2,2,4,4) = 0d0
	m2aqq0ss(2,4,2,4) = 0d0
	m2aqq0tt(2,4,2,4) = 0d0
	m2aqq0st(2,4,2,4) = 0d0

	do 201 i1=-1,1,2
	do 201 i2=-1,1,2
	do 201 i3=-1,1,2
	  mats0  = 0d0
	  matt0  = 0d0

	  if (i1.eq.-i2) mats0  = msH4f(i2,i3)
	  if (i1.eq.-i3) matt0  = mtH4f(i3,i2)

c*** ubar-u -ZZ-> ubar-u    
	m2aqq0ss(2,2,2,2) = m2aqq0ss(2,2,2,2) 
     &			    + fac*9d0*abs(mats0)**2 *qch2
	m2aqq0tt(2,2,2,2) = m2aqq0tt(2,2,2,2) 
     &			    + fac*9d0*abs(matt0)**2 *qch2 
	m2aqq0st(2,2,2,2) = m2aqq0st(2,2,2,2) 
     &	      - fac*3d0*2d0*dreal(mats0*dconjg(matt0)) *qchint
c*** ubar-u -Z-> cbar-c 
	m2aqq0ss(2,2,4,4) = m2aqq0ss(2,2,4,4) 
     &			    + fac*9d0*abs(mats0)**2 *qch2 
c*** ubar-c -Z-> ubar-c 
	m2aqq0tt(2,4,2,4) = m2aqq0tt(2,4,2,4) 
     &			    + fac*9d0*abs(matt0)**2 *qch2 
201	continue
	m2aqq0ss(4,4,4,4) = m2aqq0ss(2,2,2,2) 
	m2aqq0tt(4,4,4,4) = m2aqq0tt(2,2,2,2) 
	m2aqq0st(4,4,4,4) = m2aqq0st(2,2,2,2) 
	m2aqq0ss(4,4,2,2) = m2aqq0ss(2,2,4,4)
	m2aqq0tt(4,4,2,2) = m2aqq0tt(2,2,4,4)
	m2aqq0st(4,4,2,2) = m2aqq0st(2,2,4,4)
	m2aqq0ss(4,2,4,2) = m2aqq0ss(2,4,2,4)
	m2aqq0tt(4,2,4,2) = m2aqq0tt(2,4,2,4)
	m2aqq0st(4,2,4,2) = m2aqq0st(2,4,2,4)


c Type: ubar-u -> dbar-d
c----------------------- 

c*** generic amplitudes
	do i1=-1,1,2
	do i2=-1,1,2
	  msH4f(i1,i2) = 0d0
	  mtH4f(i1,i2) = 0d0
	enddo
	enddo

c ubar-u -Z-> sbar-s  (k1->-p1,k2->-p2,k3->p4,k4->p3)
	if (qz.eq.1) call M_ZZ_hvv(msH4f,guu,gdd,qu,qd,q1,q2,q4,q3,
     &	                  a1haas,a2haas,a3haas,a1hazs,a2hazs,a3hazs,
     &	                  a1hzzs,a2hzzs,a3hzzs)

c ubar-u -W-> dbar-d  (k1->-p1,k2->p3,k3->p4,k4->-p2)
	if (qw.eq.1) call M_WW_hvv(mtH4f,q1,q3,q4,q2,
     &	                  a1hwwt,a2hwwt,a3hwwt)

 	do 202 g1=1,2
 	do 202 g2=1,2
 	do 202 g3=1,2+qb
 	do 202 g4=1,2+qb
 	  f1 = 2*g1
 	  f2 = 2*g2
 	  f3 = 2*g3-1
 	  f4 = 2*g4-1
 	  m2aqq0ss(f1,f2,f3,f4) = 0d0
 	  m2aqq0tt(f1,f2,f3,f4) = 0d0
 	  m2aqq0st(f1,f2,f3,f4) = 0d0

	do 202 i1=-1,1,2
	do 202 i2=-1,1,2
	do 202 i3=-1,1,2
	  mats0  = 0d0
	  matt0  = 0d0

	  if (i1.eq.-i2) mats0  = msH4f(i2,i3)
	  if (i1.eq.-i3) matt0  = mtH4f(i3,i2)

 	  wmatt0 = cv(g1,g3)*v(g2,g4)*matt0

 	  if ((f1.eq.f2).and.(f3.eq.f4)) then
 	    m2aqq0ss(f1,f2,f3,f4) = m2aqq0ss(f1,f2,f3,f4) 
     &		          + fac*9d0*abs(mats0)**2 *qch2 
 	    m2aqq0tt(f1,f2,f3,f4) = m2aqq0tt(f1,f2,f3,f4) 
     &		          + fac*9d0*abs(wmatt0)**2 *qch2
 	    m2aqq0st(f1,f2,f3,f4) = m2aqq0st(f1,f2,f3,f4) 
     &	          - fac*3d0*2d0*dreal(wmatt0*dconjg(mats0)) *qchint
 	  else
 	    m2aqq0tt(f1,f2,f3,f4) = m2aqq0tt(f1,f2,f3,f4) 
     &			 + fac*9d0*abs(wmatt0)**2 *qch2 
 	  endif
202	  continue


c Type: dbar-d -> dbar-d
c-----------------------

c*** generic amplitudes
	do i1=-1,1,2
	do i2=-1,1,2
	  msH4f(i1,i2) = 0d0
	  mtH4f(i1,i2) = 0d0
	enddo
	enddo

c ubar-u -Z-> cbar-c  (k1->-p1,k2->-p2,k3->p4,k4->p3)
	if (qz.eq.1) call M_ZZ_hvv(msH4f,gdd,gdd,qd,qd,q1,q2,q4,q3,
     &	                  a1haas,a2haas,a3haas,a1hazs,a2hazs,a3hazs,
     &	                  a1hzzs,a2hzzs,a3hzzs)

c ubar-c -Z-> ubar-c  (k1->-p1,k2->p3,k3->p4,k4->-p2)
	if (qz.eq.1) call M_ZZ_hvv(mtH4f,gdd,gdd,qd,qd,q1,q3,q4,q2,
     &	                  a1haat,a2haat,a3haat,a1hazt,a2hazt,a3hazt,
     &	                  a1hzzt,a2hzzt,a3hzzt)

	m2aqq0ss(1,1,1,1) = 0d0
	m2aqq0tt(1,1,1,1) = 0d0
	m2aqq0st(1,1,1,1) = 0d0
	m2aqq0ss(1,1,3,3) = 0d0
	m2aqq0tt(1,1,3,3) = 0d0
	m2aqq0st(1,1,3,3) = 0d0
	m2aqq0ss(1,3,1,3) = 0d0
	m2aqq0tt(1,3,1,3) = 0d0
	m2aqq0st(1,3,1,3) = 0d0

	do 203 i1=-1,1,2
	do 203 i2=-1,1,2
	do 203 i3=-1,1,2
	  mats0  = 0d0
	  matt0  = 0d0

	  if (i1.eq.-i2) mats0  = msH4f(i2,i3)
	  if (i1.eq.-i3) matt0  = mtH4f(i3,i2)

c*** dbar-d -ZZ-> dbar-d    
	m2aqq0ss(1,1,1,1) = m2aqq0ss(1,1,1,1) 
     &			    + fac*9d0*abs(mats0)**2 *qch2
	m2aqq0tt(1,1,1,1) = m2aqq0tt(1,1,1,1) 
     &			    + fac*9d0*abs(matt0)**2 *qch2
	m2aqq0st(1,1,1,1) = m2aqq0st(1,1,1,1) 
     &	       - fac*3d0*2d0*dreal(mats0*dconjg(matt0)) *qchint
c*** dbar-d -Z-> sbar-s 
	m2aqq0ss(1,1,3,3) = m2aqq0ss(1,1,3,3) 
     &			    + fac*9d0*abs(mats0)**2 *qch2 
c*** dbar-s -Z-> dbar-s 
	m2aqq0tt(1,3,1,3) = m2aqq0tt(1,3,1,3) 
     &			    + fac*9d0*abs(matt0)**2 *qch2 
203	continue
	m2aqq0ss(3,3,3,3) = m2aqq0ss(1,1,1,1) 
	m2aqq0tt(3,3,3,3) = m2aqq0tt(1,1,1,1) 
	m2aqq0st(3,3,3,3) = m2aqq0st(1,1,1,1) 
	m2aqq0ss(3,3,1,1) = m2aqq0ss(1,1,3,3)
	m2aqq0tt(3,3,1,1) = m2aqq0tt(1,1,3,3)
	m2aqq0st(3,3,1,1) = m2aqq0st(1,1,3,3)
	m2aqq0ss(3,1,3,1) = m2aqq0ss(1,3,1,3)
	m2aqq0tt(3,1,3,1) = m2aqq0tt(1,3,1,3)
	m2aqq0st(3,1,3,1) = m2aqq0st(1,3,1,3)
	if (qb.eq.1) then
        m2aqq0ss(5,5,5,5) = m2aqq0ss(1,1,1,1)
        m2aqq0tt(5,5,5,5) = m2aqq0tt(1,1,1,1)
        m2aqq0st(5,5,5,5) = m2aqq0st(1,1,1,1)
        m2aqq0ss(1,1,5,5) = m2aqq0ss(1,1,3,3)
        m2aqq0tt(1,1,5,5) = m2aqq0tt(1,1,3,3)
        m2aqq0st(1,1,5,5) = m2aqq0st(1,1,3,3)
        m2aqq0ss(3,3,5,5) = m2aqq0ss(1,1,3,3)
        m2aqq0tt(3,3,5,5) = m2aqq0tt(1,1,3,3)
        m2aqq0st(3,3,5,5) = m2aqq0st(1,1,3,3)
        m2aqq0ss(5,5,1,1) = m2aqq0ss(1,1,3,3)
        m2aqq0tt(5,5,1,1) = m2aqq0tt(1,1,3,3)
        m2aqq0st(5,5,1,1) = m2aqq0st(1,1,3,3)
        m2aqq0ss(5,5,3,3) = m2aqq0ss(1,1,3,3)
        m2aqq0tt(5,5,3,3) = m2aqq0tt(1,1,3,3)
        m2aqq0st(5,5,3,3) = m2aqq0st(1,1,3,3)
        m2aqq0ss(1,5,1,5) = m2aqq0ss(1,3,1,3)
        m2aqq0tt(1,5,1,5) = m2aqq0tt(1,3,1,3)
        m2aqq0st(1,5,1,5) = m2aqq0st(1,3,1,3)
        m2aqq0ss(3,5,3,5) = m2aqq0ss(1,3,1,3)
        m2aqq0tt(3,5,3,5) = m2aqq0tt(1,3,1,3)
        m2aqq0st(3,5,3,5) = m2aqq0st(1,3,1,3)
        m2aqq0ss(5,1,5,1) = m2aqq0ss(1,3,1,3)
        m2aqq0tt(5,1,5,1) = m2aqq0tt(1,3,1,3)
        m2aqq0st(5,1,5,1) = m2aqq0st(1,3,1,3)
        m2aqq0ss(5,3,5,3) = m2aqq0ss(1,3,1,3)
        m2aqq0tt(5,3,5,3) = m2aqq0tt(1,3,1,3)
        m2aqq0st(5,3,5,3) = m2aqq0st(1,3,1,3)
	endif

c Type: dbar-d -> ubar-u
c-----------------------
	do i1=-1,1,2
	do i2=-1,1,2
	  msH4f(i1,i2) = 0d0
	  mtH4f(i1,i2) = 0d0
	enddo
	enddo

c*** generic amplitudes

c dbar-d -Z-> cbar-c  (k3->-p1,k4->-p2,k1->p4,k2->p3)
	if (qz.eq.1) call M_ZZ_hvv(msH4f,guu,gdd,qu,qd,q4,q3,q1,q2,
     &	                  a1haas,a2haas,a3haas,a1hazs,a2hazs,a3hazs,
     &	                  a1hzzs,a2hzzs,a3hzzs)

c dbar-s -W-> ubar-c  (k3->-p1,k4->p3,k1->p4,k2->-p2)
	if (qw.eq.1) call M_WW_hvv(mtH4f,q4,q2,q1,q3,
     &	                  a1hwwt,a2hwwt,a3hwwt)

 	do 204 g1=1,2+qb
 	do 204 g2=1,2+qb
 	do 204 g3=1,2
 	do 204 g4=1,2
 	  f1 = 2*g1-1
 	  f2 = 2*g2-1
 	  f3 = 2*g3
 	  f4 = 2*g4
 	  m2aqq0ss(f1,f2,f3,f4) = 0d0
 	  m2aqq0tt(f1,f2,f3,f4) = 0d0
 	  m2aqq0st(f1,f2,f3,f4) = 0d0

	do 204 i1=-1,1,2
	do 204 i2=-1,1,2
	do 204 i3=-1,1,2
	  mats0  = 0d0
	  matt0  = 0d0

	  if (i1.eq.-i2) mats0  = msH4f(i3,i2)
	  if (i1.eq.-i3) matt0  = mtH4f(i2,i3)

 	  wmatt0 = v(g3,g1)*cv(g4,g2)*matt0

 	  if ((f1.eq.f2).and.(f3.eq.f4)) then
 	    m2aqq0ss(f1,f2,f3,f4) = m2aqq0ss(f1,f2,f3,f4) 
     &		         + fac*9d0*abs(mats0)**2 *qch2
 	    m2aqq0tt(f1,f2,f3,f4) = m2aqq0tt(f1,f2,f3,f4) 
     &		         + fac*9d0*abs(wmatt0)**2 *qch2
 	    m2aqq0st(f1,f2,f3,f4) = m2aqq0st(f1,f2,f3,f4) 
     &	          - fac*3d0*2d0*dreal(wmatt0*dconjg(mats0)) *qchint
 	  else
 	    m2aqq0tt(f1,f2,f3,f4) = m2aqq0tt(f1,f2,f3,f4) 
     &			 + fac*9d0*abs(wmatt0)**2 *qch2 
 	  endif
204	  continue

	end

************************************************************************
        subroutine fixahvv(q1,q2,
     &             a1hwwf,a2hwwf,a3hwwf,a1haaf,a2haaf,a3haaf,
     &             a1hazf,a2hazf,a3hazf,a1hzzf,a2hzzf,a3hzzf)
************************************************************************
*       rescale anomalous HVV couplings by form factor
*	q1,q2 = virtualities of vector bosons
*-----------------------------------------------------------------------
*       14.6.12 Stefan Dittmaier
************************************************************************
        implicit real*8 (a-z)
	complex*16 v,cv
	integer qhvv

        common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &         v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &         ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
        common/hvv/rsm,d,db,dt,dtb,lambdahvv,
     &             a1hww,a2hww,a3hww,a1haa,a2haa,a3haa,
     &             a1haz,a2haz,a3haz,a1hzz,a2hzz,a3hzz,qhvv

	if (lambdahvv.gt.0d0) then
	  formfac_ww = lambdahvv**4/(lambdahvv**2+abs(q1))
     &	                           /(lambdahvv**2+abs(q2))
	else
	  formfac_ww = 1d0
	endif

	formfac_zz = formfac_ww
	formfac_aa = formfac_ww 
	formfac_az = formfac_ww 

	a1hwwf = a1hww 
	a2hwwf = a2hww * formfac_ww
	a3hwwf = a3hww * formfac_ww
	a1haaf = a1haa 
	a2haaf = a2haa * formfac_aa
	a3haaf = a3haa * formfac_aa
	a1hazf = a1haz 
	a2hazf = a2haz * formfac_az
	a3hazf = a3haz * formfac_az
	a1hzzf = a1hzz 
	a2hzzf = a2hzz * formfac_zz
	a3hzzf = a3hzz * formfac_zz

	end

************************************************************************
        subroutine M_WW_hvv(mH4f,fa,fb,fc,fd,a1,a2,a3)
************************************************************************
*       Helicity amplitudes for
*       H -> WW -> fa + fb-bar + fc + fd-bar 
*       with anomalous HVV couplings
*-----------------------------------------------------------------------
*       14.6.12 Stefan Dittmaier
************************************************************************
        implicit real*8 (a-z)
	complex*16 sp(-4:4,-4:4),csp(-4:4,-4:4)
        complex*16 ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2,cmh,cmh2
        complex*16 pwab,pwcd
        complex*16 Amm,mH4f(-1:1,-1:1)
        complex*16 fac
        complex*16 v,cv
        complex*16 xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null
        complex*16 xml,xml2,xmqp,xmqp2,xmqm,xmqm2
        real*8 vp(-4:4,-4:4)
        integer fa,fb,fc,fd,ia,ib,ic,id,i1,i2,i3
        integer qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &                   qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
        logical check

        common/prods3/sp,csp,vp
        common/cparam/ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
        common/xparam/xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null,
     &       xml(3),xml2(3),xmqp(3),xmqp2(3),xmqm(3),xmqm2(3)
        common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &         v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &         ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
        common/rcoptions/qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &                   qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp

	Amm(ia,ib,ic,id,a1,a2,a3) = 2d0*a1*sp(ia,ic)*csp(ib,id)
     &	  + dcmplx(a2,+a3)*sp(ic,ia)*csp(ib,ia)*sp(ia,ic)*csp(id,ic)
     &	  + dcmplx(a2,-a3)*sp(ia,ib)*csp(id,ib)*sp(ic,id)*csp(ib,id)

        sab  = vp(fa,fb)
        scd  = vp(fc,fd)

        if ((qwidth.eq.0).or.((qwidth.eq.2).and.(sab.lt.0d0))) then
          pwab = 1d0/(sab-mw2)
        else
          pwab = 1d0/(sab-cmw2)
        endif
        if ((qwidth.eq.0).or.((qwidth.eq.2).and.(scd.lt.0d0))) then
          pwcd = 1d0/(scd-mw2)
        else
          pwcd = 1d0/(scd-cmw2)
        endif

        check = ((qschan.eq.1).and.(sab.gt.0d0).and.(scd.gt.0d0))
     &     .or. ((qtchan.eq.1).and.(sab.lt.0d0).and.(scd.lt.0d0))

        if (.not.check) pwab = 0d0

	mH4f(+1,+1) = 0d0
	mH4f(+1,-1) = 0d0
	mH4f(-1,+1) = 0d0
	mH4f(-1,-1) = pwab*pwcd/2d0/xsw2*Amm(fa,fb,fc,fd,a1,a2,a3)

	end

************************************************************************
        subroutine M_ZZ_hvv(mH4f,gaz,gcz,qa,qc,fa,fb,fc,fd,
     &	             a1aa,a2aa,a3aa,a1az,a2az,a3az,a1zz,a2zz,a3zz)
************************************************************************
*       Helicity amplitudes for
*       H -> AA/AZ/ZZ -> fa + fb-bar + fc + fd-bar 
*       with anomalous HVV couplings
*-----------------------------------------------------------------------
*       14.6.12 Stefan Dittmaier
************************************************************************
        implicit real*8 (a-z)
	complex*16 sp(-4:4,-4:4),csp(-4:4,-4:4)
        complex*16 ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2,cmh,cmh2
        complex*16 pzab,pzcd
        complex*16 App,Apm,Amp,Amm,mH4f(-1:1,-1:1)
        complex*16 fac
        complex*16 gaz(-1:1),gcz(-1:1)
        complex*16 v,cv
        complex*16 xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null
        complex*16 xml,xml2,xmqp,xmqp2,xmqm,xmqm2
        real*8 vp(-4:4,-4:4)
        integer fa,fb,fc,fd,ia,ib,ic,id,i1,i2,i3
        integer qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &                   qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
        logical check

        common/prods3/sp,csp,vp
        common/cparam/ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
        common/xparam/xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null,
     &       xml(3),xml2(3),xmqp(3),xmqp2(3),xmqm(3),xmqm2(3)
        common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &         v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &         ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
        common/rcoptions/qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &                   qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp

	App(ia,ib,ic,id,a1,a2,a3) = 2d0*a1*csp(ia,ic)*sp(ib,id)
     &	  + dcmplx(a2,-a3)*csp(ic,ia)*sp(ib,ia)*csp(ia,ic)*sp(id,ic)
     &	  + dcmplx(a2,+a3)*csp(ia,ib)*sp(id,ib)*csp(ic,id)*sp(ib,id)

	Apm(ia,ib,ic,id,a1,a2,a3) = 2d0*a1*csp(ia,id)*sp(ib,ic)
     &	  + dcmplx(a2,-a3)*csp(id,ia)*sp(ib,ia)*csp(ia,id)*sp(ic,id)
     &	  + dcmplx(a2,+a3)*csp(ia,ib)*sp(ic,ib)*csp(id,ic)*sp(ib,ic)

	Amm(ia,ib,ic,id,a1,a2,a3) = 2d0*a1*sp(ia,ic)*csp(ib,id)
     &	  + dcmplx(a2,+a3)*sp(ic,ia)*csp(ib,ia)*sp(ia,ic)*csp(id,ic)
     &	  + dcmplx(a2,-a3)*sp(ia,ib)*csp(id,ib)*sp(ic,id)*csp(ib,id)

	Amp(ia,ib,ic,id,a1,a2,a3) = 2d0*a1*sp(ia,id)*csp(ib,ic)
     &	  + dcmplx(a2,+a3)*sp(id,ia)*csp(ib,ia)*sp(ia,id)*csp(ic,id)
     &	  + dcmplx(a2,-a3)*sp(ia,ib)*csp(ic,ib)*sp(id,ic)*csp(ib,ic)

        sab  = vp(fa,fb)
        scd  = vp(fc,fd)

        paab = 1d0/sab
        pacd = 1d0/scd
        if ((qwidth.eq.0).or.((qwidth.eq.2).and.(sab.lt.0d0))) then
          pzab = 1d0/(sab-mz2)
        else
          pzab = 1d0/(sab-cmz2)
        endif
        if ((qwidth.eq.0).or.((qwidth.eq.2).and.(scd.lt.0d0))) then
          pzcd = 1d0/(scd-mz2)
        else
          pzcd = 1d0/(scd-cmz2)
        endif

        check = ((qschan.eq.1).and.(sab.gt.0d0).and.(scd.gt.0d0))
     &     .or. ((qtchan.eq.1).and.(sab.lt.0d0).and.(scd.lt.0d0))

        if (.not.check) paab = 0d0
        if (.not.check) pzab = 0d0

	mH4f(+1,+1) = ((-qa)*(-qc)*paab*pacd)
     &	              *App(fa,fb,fc,fd,a1aa,a2aa,a3aa)
     &	             +((-qa)*gcz(+1)*paab*pzcd+gaz(+1)*(-qc)*pzab*pacd)
     &	              *App(fa,fb,fc,fd,a1az,a2az,a3az)
     &	             +gaz(+1)*gcz(+1)*pzab*pzcd
     &	              *App(fa,fb,fc,fd,a1zz,a2zz,a3zz)	

	mH4f(+1,-1) = ((-qa)*(-qc)*paab*pacd)
     &	              *Apm(fa,fb,fc,fd,a1aa,a2aa,a3aa)
     &	             +((-qa)*gcz(-1)*paab*pzcd+gaz(+1)*(-qc)*pzab*pacd)
     &	              *Apm(fa,fb,fc,fd,a1az,a2az,a3az)
     &	             +gaz(+1)*gcz(-1)*pzab*pzcd
     &	              *Apm(fa,fb,fc,fd,a1zz,a2zz,a3zz)	

	mH4f(-1,+1) = ((-qa)*(-qc)*paab*pacd)
     &	              *Amp(fa,fb,fc,fd,a1aa,a2aa,a3aa)
     &	             +((-qa)*gcz(+1)*paab*pzcd+gaz(-1)*(-qc)*pzab*pacd)
     &	              *Amp(fa,fb,fc,fd,a1az,a2az,a3az)
     &	             +gaz(-1)*gcz(+1)*pzab*pzcd
     &	              *Amp(fa,fb,fc,fd,a1zz,a2zz,a3zz)	

	mH4f(-1,-1) = ((-qa)*(-qc)*paab*pacd)
     &	              *Amm(fa,fb,fc,fd,a1aa,a2aa,a3aa)
     &	             +((-qa)*gcz(-1)*paab*pzcd+gaz(-1)*(-qc)*pzab*pacd)
     &	              *Amm(fa,fb,fc,fd,a1az,a2az,a3az)
     &	             +gaz(-1)*gcz(-1)*pzab*pzcd
     &	              *Amm(fa,fb,fc,fd,a1zz,a2zz,a3zz)	

	end
       subroutine setprods3(p)
************************************************************************                                                                                   
*       Weyl-van der Waerden and Minkowski products                                                                                                        
*-----------------------------------------------------------------------                                                                                   
*       23.8.06 Stefan Dittmaier                                                                                                                           
************************************************************************                                                                                   
        implicit real*8 (a-z)
        complex*16 eiph1,eiph2,sp(-4:4,-4:4),csp(-4:4,-4:4),v,cv
        real*8 p(6,0:3),vp(-4:4,-4:4)
        integer i,j

        common/prods3/sp,csp,vp
        common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &         v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &         ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)

c energies and angles                                                                                                                                      
        eb1  = p(1,0)
        eb2  = p(2,0)
        e1   = p(3,0)
        e2   = p(4,0)
        cth1 = p(3,3)/p(3,0)
        cth2 = p(4,3)/p(4,0)
        sth1 = sqrt(p(3,1)**2+p(3,2)**2)/p(3,0)
        sth2 = sqrt(p(4,1)**2+p(4,2)**2)/p(4,0)
        eiph1= dcmplx(p(3,1),p(3,2))/p(3,0)/sth1
        eiph2= dcmplx(p(4,1),p(4,2))/p(4,0)/sth2
        if (p(1,3).lt.0d0) then
          cth1 = -cth1
          cth2 = -cth2
          eiph1= dconjg(eiph1)
          eiph2= dconjg(eiph2)
        endif
        r2eb1= sqrt(2d0*eb1)
        r2eb2= sqrt(2d0*eb2)
        r2e1 = sqrt(2d0*e1)
        r2e2 = sqrt(2d0*e2)
        if (cth1.gt.0d0) then
          c2th1 = sqrt((1d0+cth1)/2d0)
          s2th1 = sth1/2d0/c2th1
        else
          s2th1 = sqrt((1d0-cth1)/2d0)
          c2th1 = sth1/2d0/s2th1
        endif
        if (cth2.gt.0d0) then
          c2th2 = sqrt((1d0+cth2)/2d0)
          s2th2 = sth2/2d0/c2th2
        else
          s2th2 = sqrt((1d0-cth2)/2d0)
          c2th2 = sth2/2d0/s2th2
        endif

c spinor products                                                                                                                                          
        sp(1,2) = r2eb1*r2eb2
        sp(1,3) = r2eb1*r2e1*(s2th1)
        sp(1,4) = r2eb1*r2e2*(s2th2)
        sp(2,3) = r2eb2*r2e1*(-1d0/eiph1*c2th1)
        sp(2,4) = r2eb2*r2e2*(-1d0/eiph2*c2th2)
        sp(3,4) = r2e1 *r2e2*(c2th1/eiph1*s2th2-c2th2/eiph2*s2th1)

        do 101 i=1,3
        do 101 j=i+1,4
           sp(j,i) = -sp(i,j)
101     continue

        do 100 i=1,4
        do 100 j=1,4
          csp(i,j)  = dconjg(sp(i,j))
           sp(-i, j) =  sp(i,j)
           sp( i,-j) =  sp(i,j)
           sp(-i,-j) =  sp(i,j)
          csp(-i, j) =-csp(i,j)
          csp( i,-j) =-csp(i,j)
          csp(-i,-j) = csp(i,j)
           vp( i, j) =  sp(i,j)*csp(i,j)
           vp(-i, j) = -vp(i,j)
           vp( i,-j) = -vp(i,j)
           vp(-i,-j) =  vp(i,j)
100     continue

        end
************************************************************************
        subroutine Mat2gluon_in1(p,m2i_gluon,m2if_gluon)
************************************************************************
*       squared amplitudes for 
*	gluon(p1) + q(p2)    --> q'(p3)    + q''(p4) + H(p5) + q'''bar(p6)
*	gluon(p1) + qbar(p2) --> q'bar(p3) + q''bar(p4) + H(p5) + q'''(p6)
*-----------------------------------------------------------------------
*       22.3.06 Stefan Dittmaier
************************************************************************
        implicit real*8 (a-z)
	complex*16 v,cv
	complex*16 sp(6,6),csp(6,6)
        real*8 p(6,0:3),k(6,0:3),vp(6,6)
        real*8 m2gluonq(5,5,5,5),m2gluonqbar(5,5,5,5)
        real*8 m2i_gluon(-5:5),m2if_gluon(-5:5,-5:5,-5:5,-5:5)
        integer qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &			 qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
	integer i1,i2,i3,i4,dir(6)

        common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &         v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &         ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
        common/prods4/sp,csp,vp
        common/rcoptions/qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &			 qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp

	dir(1) = +1
	dir(2) = -1
	dir(3) = +1
	dir(4) = +1
	dir(5) = +1
	dir(6) = -1

	do i1=0,3
	  k(1,i1) = p(3,i1)
	  k(2,i1) = p(2,i1)
	  k(3,i1) = p(6,i1)
	  k(4,i1) = p(4,i1)
	  k(5,i1) = p(5,i1)
	  k(6,i1) = p(1,i1)
	enddo

	call setprods4(k,dir)

c*** initializations
	do 100 i1=1,4
	do 100 i2=1,4
	do 100 i3=1,4
	do 100 i4=1,4
	  m2gluonq(i1,i2,i3,i4)    = 0d0
	  m2gluonqbar(i1,i2,i3,i4) = 0d0
100	continue

c a-q --> q-q-qbar
	call Mat2aqq_gluon(k,m2gluonq,1,2,3,4)

c other channels from CP symmetry for qcp=1
        if (qcp.eq.0) then
c a-qbar --> qbar-qbar-q
	  call Mat2aqq_gluon(k,m2gluonqbar,2,1,4,3)
        else
          do 103 i1=1,4
          do 103 i2=1,4
          do 103 i3=1,4
          do 103 i4=1,4
	    m2gluonqbar(i1,i2,i3,i4) = m2gluonq(i2,i1,i4,i3)
103       continue
        endif

c add final states for fixed initial states
        do 200 i1=1,4
          m2i_gluon( i1) = 0d0
          m2i_gluon(-i1) = 0d0
        do 300 i2=1,4
        do 300 i3=1,4
        do 300 i4=1,4
          m2if_gluon(i1,i2,i3,-i4) = m2gluonq(i2,i1,i4,i3)/2d0
          m2i_gluon(i1) = m2i_gluon(i1) + m2if_gluon(i1,i2,i3,-i4)
          m2if_gluon(-i1,-i2,-i3,i4) = m2gluonqbar(i1,i2,i3,i4)/2d0
          m2i_gluon(-i1) = m2i_gluon(-i1) + m2if_gluon(-i1,-i2,-i3,i4)
300     continue
200     continue

	end

************************************************************************
        subroutine Mat2gluon_in2(p,m2i_gluon,m2if_gluon)
************************************************************************
*       squared amplitudes for 
*	q(p1)    + gluon(p2) --> q'(p3)    + q''(p4) + H(p5) + q'''bar(p6)
*	qbar(p1) + gluon(p2) --> q'bar(p3) + q''bar(p4) + H(p5) + q'''(p6)
*-----------------------------------------------------------------------
*       22.3.06 Stefan Dittmaier
************************************************************************
        implicit real*8 (a-z)
	complex*16 v,cv
	complex*16 sp(6,6),csp(6,6)
        real*8 p(6,0:3),k(6,0:3),vp(6,6)
        real*8 m2gluonq(5,5,5,5),m2gluonqbar(5,5,5,5)
        real*8 m2i_gluon(-5:5),m2if_gluon(-5:5,-5:5,-5:5,-5:5)
        integer qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &			 qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
	integer i1,i2,i3,i4,dir(6)

        common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &         v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &         ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
        common/prods4/sp,csp,vp
        common/rcoptions/qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &			 qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp

	dir(1) = +1
	dir(2) = -1
	dir(3) = +1
	dir(4) = +1
	dir(5) = +1
	dir(6) = -1

	do i1=0,3
	  k(1,i1) = p(3,i1)
	  k(2,i1) = p(1,i1)
	  k(3,i1) = p(6,i1)
	  k(4,i1) = p(4,i1)
	  k(5,i1) = p(5,i1)
	  k(6,i1) = p(2,i1)
	enddo

	call setprods4(k,dir)

c*** initializations
	do 100 i1=1,4
	do 100 i2=1,4
	do 100 i3=1,4
	do 100 i4=1,4
	  m2gluonq(i1,i2,i3,i4)    = 0d0
	  m2gluonqbar(i1,i2,i3,i4) = 0d0
100	continue

c a-q --> q-q-qbar
	call Mat2aqq_gluon(k,m2gluonq,1,2,3,4)

c other channels from CP symmetry for qcp=1
        if (qcp.eq.0) then
c a-qbar --> qbar-qbar-q
	  call Mat2aqq_gluon(k,m2gluonqbar,2,1,4,3)
        else
          do 103 i1=1,4
          do 103 i2=1,4
          do 103 i3=1,4
          do 103 i4=1,4
	    m2gluonqbar(i1,i2,i3,i4) = m2gluonq(i2,i1,i4,i3)
103       continue
        endif

c add final states for fixed initial states
        do 200 i1=1,4
          m2i_gluon( i1) = 0d0
          m2i_gluon(-i1) = 0d0
        do 300 i2=1,4
        do 300 i3=1,4
        do 300 i4=1,4
          m2if_gluon(i1,i2,i3,-i4) = m2gluonq(i2,i1,i4,i3)/2d0
          m2i_gluon(i1) = m2i_gluon(i1) + m2if_gluon(i1,i2,i3,-i4)
          m2if_gluon(-i1,-i2,-i3,i4) = m2gluonqbar(i1,i2,i3,i4)/2d0
          m2i_gluon(-i1) = m2i_gluon(-i1) + m2if_gluon(-i1,-i2,-i3,i4)
300     continue
200     continue

	end

************************************************************************
        subroutine Mat2gluon_out(p,m2i_gluon,m2if_gluon)
************************************************************************
*       squared amplitudes for 
*	    parton1(p1) + parton2(p2) --> f(p3) + f'(p4) + H(p5) + gluon(p6)
*-----------------------------------------------------------------------
*       19.3.06 Stefan Dittmaier
************************************************************************
        implicit real*8 (a-z)
	complex*16 v,cv
	complex*16 sp(6,6),csp(6,6)
        real*8 p(6,0:3),vp(6,6)
	real*8 m2aqq_gluon(5,5,5,5),m2qaq_gluon(5,5,5,5)
        real*8 m2qq_gluon(5,5,5,5),m2aqaq_gluon(5,5,5,5)
        real*8 m2i_gluon(-5:5,-5:5),m2if_gluon(-5:5,-5:5,-5:5,-5:5)
	integer i1,i2,i3,i4,dir(6)

        common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &         v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &         ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
        common/prods4/sp,csp,vp

	dir(1) = -1
	dir(2) = -1
	dir(3) = +1
	dir(4) = +1
	dir(5) = +1
	dir(6) = +1
	call setprods4(p,dir)

c*** initializations
	do 100 i1=1,4
	do 100 i2=1,4
	do 100 i3=1,4
	do 100 i4=1,4
	  m2aqq_gluon(i1,i2,i3,i4)  = 0d0
	  m2qq_gluon(i1,i2,i3,i4)   = 0d0
	  m2qaq_gluon(i1,i2,i3,i4)  = 0d0
	  m2aqaq_gluon(i1,i2,i3,i4) = 0d0
100	continue

c qbar-q --> qbar-q
	call Mat2aqq_gluon(p,m2aqq_gluon,1,2,3,4)
c q-qbar --> q-qbar
	call Mat2aqq_gluon(p,m2qaq_gluon,2,1,4,3)
c q-q    --> q-q
	call Mat2aqq_gluon(p,m2qq_gluon,3,2,1,4)
c qbar-qbar --> qbar-qbar
	call Mat2aqq_gluon(p,m2aqaq_gluon,1,4,3,2)

c add final states for fixed initial states
        do 200 i1=-4,4
        do 200 i2=-4,4
          m2i_gluon(i1,i2) = 0d0
        do 300 i3=1,4
        do 300 i4=1,4
          if (i1*i2.eq.0) goto 200
          if ((i1.lt.0).and.(i2.gt.0)) then
            m2if_gluon(i1,i2,-i3,i4) = m2aqq_gluon(-i1,i2,i3,i4)
            m2i_gluon(i1,i2)=m2i_gluon(i1,i2)+m2if_gluon(i1,i2,-i3,i4)
	  endif
          if ((i1.gt.0).and.(i2.lt.0)) then
            m2if_gluon(i1,i2,i3,-i4) = m2qaq_gluon(-i2,i1,i4,i3)
            m2i_gluon(i1,i2)=m2i_gluon(i1,i2)+m2if_gluon(i1,i2,i3,-i4)
	  endif
          if ((i1.gt.0).and.(i2.gt.0)) then
            m2if_gluon(i1,i2,i3,i4) = m2qq_gluon(i3,i2,i1,i4)/2d0
            m2i_gluon(i1,i2)=m2i_gluon(i1,i2)+m2if_gluon(i1,i2,i3,i4)
	  endif
          if ((i1.lt.0).and.(i2.lt.0)) then
            m2if_gluon(i1,i2,-i3,-i4) = m2aqaq_gluon(-i1,i4,i3,-i2)/2d0
            m2i_gluon(i1,i2)=m2i_gluon(i1,i2)+m2if_gluon(i1,i2,-i3,-i4)
	  endif
300     continue
200     continue

	end

************************************************************************
        subroutine Mat2aqq_gluon(p,m2aqq_gluon,q1,q2,q3,q4)
************************************************************************
*       squared amplitudes for 
*	    anti-q(p1) + q(p2) --> f(p3) + f'(p4) + H(p5) + gluon(p6)
*
*       from generic amplitudes for
*	    H(p) --> fa(k1) + anti-fb(k2) + fc(k3) + anti-fd(k4)
*	         CC: f1     + anti-f2     + f3     + anti-f4     
*	         NC: f1     + anti-f1     + f3     + anti-f3     
*	             f2     + anti-f2     + f3     + anti-f3     
*	             f1     + anti-f1     + f4     + anti-f4     
*
*	fermions: f1,f4 = generic   up-type fermions
*	          f2,f3 = generic down-type fermions
*-----------------------------------------------------------------------
*       13.11.05 Stefan Dittmaier
************************************************************************
        implicit real*8 (a-z)
	complex*16 mats1,matt1,wmats1,wmatt1
	complex*16 mats2,matt2,wmats2,wmatt2
	complex*16 mats1hvv,matt1hvv,wmats1hvv,wmatt1hvv
	complex*16 mats2hvv,matt2hvv,wmats2hvv,wmatt2hvv
	complex*16 v,cv
        complex*16 ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2,cmh,cmh2
        complex*16 guu,gdd,gnn,gll
        complex*16 msHWW4fg1(-1:1),msHWW4fg2(-1:1)
	complex*16 mtHWW4fg1(-1:1),mtHWW4fg2(-1:1)
	complex*16 msHZZ4fg1(-1:1,-1:1,-1:1),msHZZ4fg2(-1:1,-1:1,-1:1)
	complex*16 mtHZZ4fg1(-1:1,-1:1,-1:1),mtHZZ4fg2(-1:1,-1:1,-1:1)
        complex*16 msHWW4fg1hvv(-1:1),msHWW4fg2hvv(-1:1)
	complex*16 mtHWW4fg1hvv(-1:1),mtHWW4fg2hvv(-1:1)
	complex*16 msHZZ4fg1hvv(-1:1,-1:1,-1:1)
	complex*16 msHZZ4fg2hvv(-1:1,-1:1,-1:1)
	complex*16 mtHZZ4fg1hvv(-1:1,-1:1,-1:1)
	complex*16 mtHZZ4fg2hvv(-1:1,-1:1,-1:1)
	complex*16 sp(6,6),csp(6,6)
        real*8 p(6,0:3),vp(6,6),m2aqq_gluon(5,5,5,5)
	integer q1,q2,q3,q4
	integer ig,i1,i2,i3,i4,j,j1,j2,f1,f2,f3,f4,g1,g2,g3,g4
        integer qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &			 qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
	integer qhvv

        common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &         v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &         ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
        common/rcoptions/qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &			 qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
        common/cparam/ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
        common/qf/qu,qd,ql,qn,qf(4),mu,mu2,md,md2,mlep,mlep2,
     &            guu(-1:1),gdd(-1:1),gnn(-1:1),gll(-1:1)
        common/prods4/sp,csp,vp
        common/hvv/rsm,d,db,dt,dtb,lambdahvv,
     &             a1hww,a2hww,a3hww,a1haa,a2haa,a3haa,
     &             a1haz,a2haz,a3haz,a1hzz,a2hzz,a3hzz,qhvv

	gs2el6 = el**6*4d0*pi*alphas

c qbar-q scattering
c
c   s-channel:                             t-channel:
c
c   fa(p1) \_          / fd(p3)            fa(p1) --<--*--<-- fb(p3)
c          |\        |/                                >
c            \       /-                                >
c             *vvvvv*                                  >
c           _/       \                                 >
c           /|        \|                               >
c   fb(p2) /          -\ fc(p4)            fd(p2) -->--*-->-- fc(p4)

c Type: ubar-d -> ubar-d
c-----------------------
c ubar-d -W-> cbar-s    (k1->-p1,k2->-p2,k3->p4,k4->p3)   
	if (qw.eq.1) then
	  if ((qhvv.eq.0).or.(qqcdnondiag.eq.1)) 
     &	    call M_WW_gluon(msHWW4fg1,msHWW4fg2,q1,q2,q4,q3,0)    
	  if ((qhvv.ne.0).and.(qqcddiag.eq.1)) 
     &      call M_WW_gluon(msHWW4fg1hvv,msHWW4fg2hvv,q1,q2,q4,q3,qhvv)    
	else
	  do i1=-1,1,2
	    msHWW4fg1(i1)    = 0d0
	    msHWW4fg2(i1)    = 0d0
	    msHWW4fg1hvv(i1) = 0d0
	    msHWW4fg2hvv(i1) = 0d0
	  enddo
	endif
c ubar-s -Z-> ubar-s    (k1->-p1,k2->p3,k3->p4,k4->-p2)   
	if (qz.eq.1) then
	  if ((qhvv.eq.0).or.(qqcdnondiag.eq.1)) call M_ZZ_gluon(
     &	                mtHZZ4fg1,mtHZZ4fg2,guu,gdd,qu,qd,q1,q3,q4,q2,0)
	  if ((qhvv.ne.0).and.(qqcddiag.eq.1)) call M_ZZ_gluon(
     &	       mtHZZ4fg1hvv,mtHZZ4fg2hvv,guu,gdd,qu,qd,q1,q3,q4,q2,qhvv)
	else
	  do i1=-1,1,2
	  do i2=-1,1,2
	  do i3=-1,1,2
	    mtHZZ4fg1(i1,i2,i3)    = 0d0
	    mtHZZ4fg2(i1,i2,i3)    = 0d0
	    mtHZZ4fg1hvv(i1,i2,i3) = 0d0
	    mtHZZ4fg2hvv(i1,i2,i3) = 0d0
	  enddo
	  enddo
	  enddo
	endif

c*** individual channels
	do 200 i1=-1,1,2
	do 200 i2=-1,1,2
	do 200 i3=-1,1,2
	do 200 ig=-1,1,2
	  mats1 = 0d0
	  matt1 = 0d0
	  mats2 = 0d0
	  matt2 = 0d0
	  mats1hvv = 0d0
	  matt1hvv = 0d0
	  mats2hvv = 0d0
	  matt2hvv = 0d0
	  if ((i1.eq.1).and.(i2.eq.-1).and.(i3.eq.-1))then
      	    mats1 = mats1 + msHWW4fg1(ig)
      	    mats2 = mats2 + msHWW4fg2(ig)
            if (qhvv.ne.0) then
      	      mats1hvv = mats1hvv + msHWW4fg1hvv(ig)
      	      mats2hvv = mats2hvv + msHWW4fg2hvv(ig)
	    endif
	  endif
	  if (i1.eq.-i3) then
      	    matt1 = matt1 + mtHZZ4fg1(i3,i2,ig)
      	    matt2 = matt2 + mtHZZ4fg2(i3,i2,ig)
            if (qhvv.ne.0) then
      	      matt1hvv = matt1hvv + mtHZZ4fg1hvv(i3,i2,ig)
      	      matt2hvv = matt2hvv + mtHZZ4fg2hvv(i3,i2,ig)
	    endif
	  endif

 	do 200 g1=1,2
 	do 200 g2=1,2
 	do 200 g3=1,2
 	do 200 g4=1,2
 	  wmats1  = cv(g1,g2)*v(g3,g4)*mats1
 	  wmats2  = cv(g1,g2)*v(g3,g4)*mats2
          if (qhvv.ne.0) then
 	    wmats1hvv  = cv(g1,g2)*v(g3,g4)*mats1hvv
 	    wmats2hvv  = cv(g1,g2)*v(g3,g4)*mats2hvv
	  endif
 	  f1 = 2*g1
 	  f2 = 2*g2-1
 	  f3 = 2*g3
 	  f4 = 2*g4-1
 	  if ((f1.eq.f3).and.(f2.eq.f4)) then
	    if ((qhvv.eq.0).and.(qqcddiag.eq.1)) then
 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*qch2*12d0*( abs(wmats1)**2+abs(wmats2)**2
     &		                    +abs(matt1)**2 +abs(matt2)**2 )
	    elseif ((qhvv.ne.0).and.(qqcddiag.eq.1)) then
 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*qch2*12d0*( abs(wmats1hvv)**2+abs(wmats2hvv)**2
     &	  	                    +abs(matt1hvv)**2 +abs(matt2hvv)**2)  
	    endif
	    if (qqcdnondiag.eq.1)
     &	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*(-qchint*8d0*dreal( wmats1*dconjg(matt1)
     &		                            +wmats1*dconjg(matt2)
     &		                            +wmats2*dconjg(matt1)
     &		                            +wmats2*dconjg(matt2) ) )
 	  else
	    if ((qhvv.eq.0).and.(qqcddiag.eq.1)) then
 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*qch2*12d0*(abs(wmats1)**2+abs(wmats2)**2)
	    elseif ((qhvv.ne.0).and.(qqcddiag.eq.1)) then
 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*qch2*12d0*(abs(wmats1hvv)**2+abs(wmats2hvv)**2)
 	    endif
 	  endif
200	continue


c Type: dbar-u -> dbar-u
c-----------------------

c dbar-u -W-> sbar-c    (k3->-p1,k4->-p2,k1->p4,k2->p3)   
	if (qw.eq.1) then
	  if ((qhvv.eq.0).or.(qqcdnondiag.eq.1)) 
     &	    call M_WW_gluon(msHWW4fg1,msHWW4fg2,q4,q3,q1,q2,0)    
	  if ((qhvv.ne.0).and.(qqcddiag.eq.1)) 
     &	    call M_WW_gluon(msHWW4fg1hvv,msHWW4fg2hvv,q4,q3,q1,q2,qhvv)    
	else
	  do i1=-1,1,2
	    msHWW4fg1(i1)    = 0d0
	    msHWW4fg2(i1)    = 0d0
	    msHWW4fg1hvv(i1) = 0d0
	    msHWW4fg2hvv(i1) = 0d0
	  enddo
	endif

c dbar-c -Z-> dbar-c    (k3->-p1,k4->p3,k1->p4,k2->-p2)   
	if (qz.eq.1) then
	  if ((qhvv.eq.0).or.(qqcdnondiag.eq.1)) call M_ZZ_gluon(
     &	     mtHZZ4fg1,mtHZZ4fg2,guu,gdd,qu,qd,q4,q2,q1,q3,0)
	  if ((qhvv.ne.0).and.(qqcddiag.eq.1)) call M_ZZ_gluon(
     &       mtHZZ4fg1hvv,mtHZZ4fg2hvv,guu,gdd,qu,qd,q4,q2,q1,q3,qhvv)
	else
	  do i1=-1,1,2
	  do i2=-1,1,2
	  do i3=-1,1,2
	    mtHZZ4fg1(i1,i2,i3)    = 0d0
	    mtHZZ4fg2(i1,i2,i3)    = 0d0
	    mtHZZ4fg1hvv(i1,i2,i3) = 0d0
	    mtHZZ4fg2hvv(i1,i2,i3) = 0d0
	  enddo
	  enddo
	  enddo
	endif

	do 205 i1=-1,1,2
	do 205 i2=-1,1,2
	do 205 i3=-1,1,2
	do 205 ig=-1,1,2
	  mats1   = 0d0
	  matt1   = 0d0
	  mats2   = 0d0
	  matt2   = 0d0
	  mats1hvv = 0d0
	  matt1hvv = 0d0
	  mats2hvv = 0d0
	  matt2hvv = 0d0
	  if ((i1.eq.1).and.(i2.eq.-1).and.(i3.eq.-1)) then
      	    mats1  = mats1 + msHWW4fg1(ig)
      	    mats2  = mats2 + msHWW4fg2(ig)
            if (qhvv.ne.0) then
      	      mats1hvv  = mats1hvv + msHWW4fg1hvv(ig)
      	      mats2hvv  = mats2hvv + msHWW4fg2hvv(ig)
	    endif
	  endif
	  if (i1.eq.-i3) then
      	    matt1 = matt1 + mtHZZ4fg1(i3,i2,ig)
      	    matt2 = matt2 + mtHZZ4fg2(i3,i2,ig)
            if (qhvv.ne.0) then
      	      matt1hvv  = matt1hvv + mtHZZ4fg1hvv(i3,i2,ig)
      	      matt2hvv  = matt2hvv + mtHZZ4fg2hvv(i3,i2,ig)
	    endif
	  endif

 	do 205 g1=1,2
 	do 205 g2=1,2
 	do 205 g3=1,2
 	do 205 g4=1,2
 	  wmats1 = v(g2,g1)*cv(g4,g3)*mats1
 	  wmats2 = v(g2,g1)*cv(g4,g3)*mats2
          if (qhvv.ne.0) then
 	    wmats1hvv = v(g2,g1)*cv(g4,g3)*mats1hvv
 	    wmats2hvv = v(g2,g1)*cv(g4,g3)*mats2hvv
	  endif
 	  f1 = 2*g1-1
 	  f2 = 2*g2
 	  f3 = 2*g3-1
 	  f4 = 2*g4
 	  if ((f1.eq.f3).and.(f2.eq.f4)) then
	    if ((qhvv.eq.0).and.(qqcddiag.eq.1)) then
 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*qch2*12d0*( abs(wmats1)**2+abs(wmats2)**2 
     &		                    +abs(matt1)**2 +abs(matt2)**2 )
	    elseif ((qhvv.ne.0).and.(qqcddiag.eq.1)) then
 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*qch2*12d0*( abs(wmats1hvv)**2+abs(wmats2hvv)**2 
     &		                    +abs(matt1hvv)**2 +abs(matt2hvv)**2)
	    endif
	    if (qqcdnondiag.eq.1)
     &	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*(-qchint*8d0*dreal( wmats1*dconjg(matt1)
     &		                            +wmats1*dconjg(matt2)
     &		                            +wmats2*dconjg(matt1)
     &		                            +wmats2*dconjg(matt2) ))
 	  else
	    if ((qhvv.eq.0).and.(qqcddiag.eq.1)) then
 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*qch2*12d0*(abs(wmats1)**2+abs(wmats2)**2)
	    elseif ((qhvv.ne.0).and.(qqcddiag.eq.1)) then
 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*qch2*12d0*(abs(wmats1hvv)**2+abs(wmats2hvv)**2)
 	    endif
 	  endif
205	continue


c Type: ubar-u -> ubar-u
c----------------------- 

	if (qz.eq.1) then

c ubar-u -Z-> cbar-c  (k1->-p1,k2->-p2,k3->p4,k4->p3)
	  if ((qhvv.eq.0).or.(qqcdnondiag.eq.1)) call M_ZZ_gluon(
     &	      msHZZ4fg1,msHZZ4fg2,guu,guu,qu,qu,q1,q2,q4,q3,0)
	  if ((qhvv.ne.0).and.(qqcddiag.eq.1)) call M_ZZ_gluon(
     &	      msHZZ4fg1hvv,msHZZ4fg2hvv,guu,guu,qu,qu,q1,q2,q4,q3,qhvv)

c ubar-c -Z-> ubar-c  (k1->-p1,k2->p3,k3->p4,k4->-p2)
	  if ((qhvv.eq.0).or.(qqcdnondiag.eq.1)) call M_ZZ_gluon(
     &	     mtHZZ4fg1,mtHZZ4fg2,guu,guu,qu,qu,q1,q3,q4,q2,0)
	  if ((qhvv.ne.0).and.(qqcddiag.eq.1)) call M_ZZ_gluon(
     &	     mtHZZ4fg1hvv,mtHZZ4fg2hvv,guu,guu,qu,qu,q1,q3,q4,q2,qhvv)

	  do 201 i1=-1,1,2
	  do 201 i2=-1,1,2
	  do 201 i3=-1,1,2
	  do 201 ig=-1,1,2
	    mats1   = 0d0
	    matt1   = 0d0
	    mats2   = 0d0
	    matt2   = 0d0
	    mats1hvv = 0d0
	    matt1hvv = 0d0
	    mats2hvv = 0d0
	    matt2hvv = 0d0
	    if (i1.eq.-i2) then
      	      mats1 = mats1 + msHZZ4fg1(i2,i3,ig)
      	      mats2 = mats2 + msHZZ4fg2(i2,i3,ig)
              if (qhvv.ne.0) then
      	        mats1hvv = mats1hvv + msHZZ4fg1hvv(i2,i3,ig)
      	        mats2hvv = mats2hvv + msHZZ4fg2hvv(i2,i3,ig)
	      endif
	    endif
	    if (i1.eq.-i3) then
      	      matt1 = matt1 + mtHZZ4fg1(i3,i2,ig)
      	      matt2 = matt2 + mtHZZ4fg2(i3,i2,ig)
              if (qhvv.ne.0) then
      	        matt1hvv = matt1hvv + mtHZZ4fg1hvv(i3,i2,ig)
      	        matt2hvv = matt2hvv + mtHZZ4fg2hvv(i3,i2,ig)
	      endif
	    endif
c*** ubar-u -ZZ-> ubar-u    
	    if ((qhvv.eq.0).and.(qqcddiag.eq.1)) then
	      m2aqq_gluon(2,2,2,2) = m2aqq_gluon(2,2,2,2) 
     &	        + gs2el6*qch2*12d0*( abs(mats1)**2+abs(mats2)**2 
     &		                    +abs(matt1)**2+abs(matt2)**2 ) 
	    elseif ((qhvv.ne.0).and.(qqcddiag.eq.1)) then
	      m2aqq_gluon(2,2,2,2) = m2aqq_gluon(2,2,2,2) 
     &	        + gs2el6*qch2*12d0*( abs(mats1hvv)**2+abs(mats2hvv)**2 
     &		                    +abs(matt1hvv)**2+abs(matt2hvv)**2 ) 
	    endif
	    if (qqcdnondiag.eq.1)
     &	       m2aqq_gluon(2,2,2,2) = m2aqq_gluon(2,2,2,2) 
     &	         + gs2el6*(-qchint*8d0*dreal( mats1*dconjg(matt1)
     &		                             +mats1*dconjg(matt2)
     &		                             +mats2*dconjg(matt1)
     &		                             +mats2*dconjg(matt2) ))
c*** ubar-u -Z-> cbar-c 
	    if ((qhvv.eq.0).and.(qqcddiag.eq.1)) then
	      m2aqq_gluon(2,2,4,4) = m2aqq_gluon(2,2,4,4) 
     &	        + gs2el6*qch2*12d0*(abs(mats1)**2+abs(mats2)**2) 
	    elseif ((qhvv.ne.0).and.(qqcddiag.eq.1)) then
	      m2aqq_gluon(2,2,4,4) = m2aqq_gluon(2,2,4,4) 
     &	        + gs2el6*qch2*12d0*(abs(mats1hvv)**2+abs(mats2hvv)**2) 
	    endif
c*** ubar-c -Z-> ubar-c 
	    if ((qhvv.eq.0).and.(qqcddiag.eq.1)) then
	      m2aqq_gluon(2,4,2,4) = m2aqq_gluon(2,4,2,4) 
     &	        + gs2el6*qch2*12d0*(abs(matt1)**2+abs(matt2)**2)
	    elseif ((qhvv.ne.0).and.(qqcddiag.eq.1)) then
	      m2aqq_gluon(2,4,2,4) = m2aqq_gluon(2,4,2,4) 
     &	        + gs2el6*qch2*12d0*(abs(matt1hvv)**2+abs(matt2hvv)**2)
	    endif
201	  continue
	  m2aqq_gluon(4,4,4,4) = m2aqq_gluon(2,2,2,2) 
	  m2aqq_gluon(4,4,2,2) = m2aqq_gluon(2,2,4,4)
	  m2aqq_gluon(4,2,4,2) = m2aqq_gluon(2,4,2,4)
	endif


c Type: ubar-u -> dbar-d
c----------------------- 

c ubar-u -Z-> sbar-s  (k1->-p1,k2->-p2,k3->p4,k4->p3)
	if (qz.eq.1) then
	  if ((qhvv.eq.0).or.(qqcdnondiag.eq.1)) call M_ZZ_gluon(
     &       msHZZ4fg1,msHZZ4fg2,guu,gdd,qu,qd,q1,q2,q4,q3,0)
	  if ((qhvv.ne.0).and.(qqcddiag.eq.1)) call M_ZZ_gluon(
     &       msHZZ4fg1hvv,msHZZ4fg2hvv,guu,gdd,qu,qd,q1,q2,q4,q3,qhvv)
	else
	  do i1=-1,1,2
	  do i2=-1,1,2
	  do i3=-1,1,2
	    msHZZ4fg1(i1,i2,i3)    = 0d0
	    msHZZ4fg2(i1,i2,i3)    = 0d0
	    msHZZ4fg1hvv(i1,i2,i3) = 0d0
	    msHZZ4fg2hvv(i1,i2,i3) = 0d0
	  enddo
	  enddo
	  enddo
	endif

c ubar-u -W-> dbar-d  (k1->-p1,k2->p3,k3->p4,k4->-p2)
	if (qw.eq.1) then
          if ((qhvv.eq.0).or.(qqcdnondiag.eq.1)) 
     &	    call M_WW_gluon(mtHWW4fg1,mtHWW4fg2,q1,q3,q4,q2,0)    
	  if ((qhvv.ne.0).and.(qqcddiag.eq.1)) 
     &	    call M_WW_gluon(mtHWW4fg1hvv,mtHWW4fg2hvv,q1,q3,q4,q2,qhvv)    
	else
	  do i1=-1,1,2
	    mtHWW4fg1(i1)    = 0d0
	    mtHWW4fg2(i1)    = 0d0
	    mtHWW4fg1hvv(i1) = 0d0
	    mtHWW4fg2hvv(i1) = 0d0
	  enddo
	endif

	do 202 i1=-1,1,2
	do 202 i2=-1,1,2
	do 202 i3=-1,1,2
	do 202 ig=-1,1,2
	  mats1   = 0d0
	  matt1   = 0d0
	  mats2   = 0d0
	  matt2   = 0d0
	  mats1hvv = 0d0
	  matt1hvv = 0d0
	  mats2hvv = 0d0
	  matt2hvv = 0d0
	  if (i1.eq.-i2) then
      	    mats1 = mats1 + msHZZ4fg1(i2,i3,ig)
      	    mats2 = mats2 + msHZZ4fg2(i2,i3,ig)
            if (qhvv.ne.0) then
      	      mats1hvv = mats1hvv + msHZZ4fg1hvv(i2,i3,ig)
      	      mats2hvv = mats2hvv + msHZZ4fg2hvv(i2,i3,ig)
	    endif
	  endif
	  if ((i1.eq.1).and.(i2.eq.-1).and.(i3.eq.-1))then
      	    matt1  = matt1 + mtHWW4fg1(ig)
      	    matt2  = matt2 + mtHWW4fg2(ig)
            if (qhvv.ne.0) then
      	      matt1hvv  = matt1hvv + mtHWW4fg1hvv(ig)
      	      matt2hvv  = matt2hvv + mtHWW4fg2hvv(ig)
	    endif
	  endif

 	do 202 g1=1,2
 	do 202 g2=1,2
 	do 202 g3=1,2
 	do 202 g4=1,2
 	  wmatt1 = cv(g1,g3)*v(g2,g4)*matt1
 	  wmatt2 = cv(g1,g3)*v(g2,g4)*matt2
          if (qhvv.ne.0) then
 	    wmatt1hvv = cv(g1,g3)*v(g2,g4)*matt1hvv
 	    wmatt2hvv = cv(g1,g3)*v(g2,g4)*matt2hvv
 	  endif
 	  f1 = 2*g1
 	  f2 = 2*g2
 	  f3 = 2*g3-1
 	  f4 = 2*g4-1
 	  if ((f1.eq.f2).and.(f3.eq.f4)) then
	    if ((qhvv.eq.0).and.(qqcddiag.eq.1)) then
 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*(+qch2*12d0*( abs(wmatt1)**2+abs(wmatt2)**2 
     &		                      +abs(mats1)**2 +abs(mats2)**2 )) 
	    elseif ((qhvv.ne.0).and.(qqcddiag.eq.1)) then
 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*qch2*12d0*( abs(wmatt1hvv)**2+abs(wmatt2hvv)**2 
     &		                    +abs(mats1hvv)**2 +abs(mats2hvv)**2)
	    endif
	    if (qqcdnondiag.eq.1)
     &	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	         + gs2el6*(-qchint*8d0*dreal( mats1*dconjg(wmatt1)
     &		                             +mats1*dconjg(wmatt2)
     &		                             +mats2*dconjg(wmatt1)
     &		                             +mats2*dconjg(wmatt2) ))
 	  else
	    if ((qhvv.eq.0).and.(qqcddiag.eq.1)) then
 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4)
     &	        + gs2el6*qch2*12d0*(abs(wmatt1)**2+abs(wmatt2)**2)
	    elseif ((qhvv.ne.0).and.(qqcddiag.eq.1)) then
 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4)
     &	        + gs2el6*qch2*12d0*(abs(wmatt1hvv)**2+abs(wmatt2hvv)**2)
 	    endif
 	  endif
202	  continue


c Type: dbar-d -> dbar-d
c-----------------------

	if (qz.eq.1) then

c dbar-d -Z-> sbar-s  (k1->-p1,k2->-p2,k3->p4,k4->p3)
          if ((qhvv.eq.0).or.(qqcdnondiag.eq.1)) call M_ZZ_gluon(
     &	     msHZZ4fg1,msHZZ4fg2,gdd,gdd,qd,qd,q1,q2,q4,q3,0)
	  if ((qhvv.ne.0).and.(qqcddiag.eq.1)) call M_ZZ_gluon(
     &	     msHZZ4fg1hvv,msHZZ4fg2hvv,gdd,gdd,qd,qd,q1,q2,q4,q3,qhvv)

c dbar-s -Z-> dbar-s  (k1->-p1,k2->p3,k3->p4,k4->-p2)
          if ((qhvv.eq.0).or.(qqcdnondiag.eq.1)) call M_ZZ_gluon(
     &       mtHZZ4fg1,mtHZZ4fg2,gdd,gdd,qd,qd,q1,q3,q4,q2,0)
	  if ((qhvv.ne.0).and.(qqcddiag.eq.1)) call M_ZZ_gluon(
     &       mtHZZ4fg1hvv,mtHZZ4fg2hvv,gdd,gdd,qd,qd,q1,q3,q4,q2,qhvv)

	  do 203 i1=-1,1,2
	  do 203 i2=-1,1,2
	  do 203 i3=-1,1,2
	  do 203 ig=-1,1,2
	    mats1   = 0d0
	    matt1   = 0d0
	    mats2   = 0d0
	    matt2   = 0d0
	    mats1hvv = 0d0
	    matt1hvv = 0d0
	    mats2hvv = 0d0
	    matt2hvv = 0d0
	    if (i1.eq.-i2) then
      	      mats1 = mats1 + msHZZ4fg1(i2,i3,ig)
      	      mats2 = mats2 + msHZZ4fg2(i2,i3,ig)
              if (qhvv.ne.0) then
      	        mats1hvv = mats1hvv + msHZZ4fg1hvv(i2,i3,ig)
      	        mats2hvv = mats2hvv + msHZZ4fg2hvv(i2,i3,ig)
	      endif
	    endif
	    if (i1.eq.-i3) then
      	      matt1 = matt1 + mtHZZ4fg1(i3,i2,ig)
      	      matt2 = matt2 + mtHZZ4fg2(i3,i2,ig)
              if (qhvv.ne.0) then
      	        matt1hvv = matt1hvv + mtHZZ4fg1hvv(i3,i2,ig)
      	        matt2hvv = matt2hvv + mtHZZ4fg2hvv(i3,i2,ig)
	      endif
	    endif
c*** dbar-d -ZZ-> dbar-d    
	    if ((qhvv.eq.0).and.(qqcddiag.eq.1)) then
	      m2aqq_gluon(1,1,1,1) = m2aqq_gluon(1,1,1,1) 
     &	        + gs2el6*qch2*12d0*( abs(mats1)**2+abs(mats2)**2 
     &		                    +abs(matt1)**2+abs(matt2)**2) 
	    elseif ((qhvv.ne.0).and.(qqcddiag.eq.1)) then
	      m2aqq_gluon(1,1,1,1) = m2aqq_gluon(1,1,1,1) 
     &	        + gs2el6*qch2*12d0*( abs(mats1hvv)**2+abs(mats2hvv)**2 
     &		                    +abs(matt1hvv)**2+abs(matt2hvv)**2) 
	    endif
	    if (qqcdnondiag.eq.1)
     &	      m2aqq_gluon(1,1,1,1) = m2aqq_gluon(1,1,1,1) 
     &	        + gs2el6*(-qchint*8d0*dreal( mats1*dconjg(matt1)
     &		                            +mats1*dconjg(matt2)
     &		                            +mats2*dconjg(matt1)
     &		                            +mats2*dconjg(matt2) ))
c*** dbar-d -Z-> sbar-s 
	    if ((qhvv.eq.0).and.(qqcddiag.eq.1)) then
	      m2aqq_gluon(1,1,3,3) = m2aqq_gluon(1,1,3,3) 
     &	        + gs2el6*qch2*12d0*(abs(mats1)**2+abs(mats2)**2) 
	    elseif ((qhvv.ne.0).and.(qqcddiag.eq.1)) then
	      m2aqq_gluon(1,1,3,3) = m2aqq_gluon(1,1,3,3) 
     &	        + gs2el6*qch2*12d0*(abs(mats1hvv)**2+abs(mats2hvv)**2) 
	    endif
c*** dbar-s -Z-> dbar-s 
	    if ((qhvv.eq.0).and.(qqcddiag.eq.1)) then
	      m2aqq_gluon(1,3,1,3) = m2aqq_gluon(1,3,1,3) 
     &	        + gs2el6*qch2*12d0*(abs(matt1)**2+abs(matt2)**2) 
	    elseif ((qhvv.ne.0).and.(qqcddiag.eq.1)) then
	      m2aqq_gluon(1,3,1,3) = m2aqq_gluon(1,3,1,3) 
     &	        + gs2el6*qch2*12d0*(abs(matt1hvv)**2+abs(matt2hvv)**2) 
	    endif
203	  continue
	  m2aqq_gluon(3,3,3,3) = m2aqq_gluon(1,1,1,1) 
	  m2aqq_gluon(3,3,1,1) = m2aqq_gluon(1,1,3,3)
	  m2aqq_gluon(3,1,3,1) = m2aqq_gluon(1,3,1,3)
	endif


c Type: dbar-d -> ubar-u
c-----------------------

c dbar-d -Z-> cbar-c  (k3->-p1,k4->-p2,k1->p4,k2->p3)
	if (qz.eq.1) then
          if ((qhvv.eq.0).or.(qqcdnondiag.eq.1)) call M_ZZ_gluon(
     &	     msHZZ4fg1,msHZZ4fg2,guu,gdd,qu,qd,q4,q3,q1,q2,0)
	  if ((qhvv.ne.0).and.(qqcddiag.eq.1)) call M_ZZ_gluon(
     &	     msHZZ4fg1hvv,msHZZ4fg2hvv,guu,gdd,qu,qd,q4,q3,q1,q2,qhvv)
	else
	  do i1=-1,1,2
	  do i2=-1,1,2
	  do i3=-1,1,2
	    msHZZ4fg1(i1,i2,i3)    = 0d0
	    msHZZ4fg2(i1,i2,i3)    = 0d0
	    msHZZ4fg1hvv(i1,i2,i3) = 0d0
	    msHZZ4fg2hvv(i1,i2,i3) = 0d0
	  enddo
	  enddo
	  enddo
	endif

c dbar-s -W-> ubar-c  (k3->-p1,k4->p3,k1->p4,k2->-p2)
	if (qw.eq.1) then
          if ((qhvv.eq.0).or.(qqcdnondiag.eq.1)) 
     &	     call M_WW_gluon(mtHWW4fg1,mtHWW4fg2,q4,q2,q1,q3,0)    
	  if ((qhvv.ne.0).and.(qqcddiag.eq.1)) 
     &	     call M_WW_gluon(mtHWW4fg1hvv,mtHWW4fg2hvv,q4,q2,q1,q3,qhvv)    
	else
	  do i1=-1,1,2
	    mtHWW4fg1(i1)    = 0d0
	    mtHWW4fg2(i1)    = 0d0
	    mtHWW4fg1hvv(i1) = 0d0
	    mtHWW4fg2hvv(i1) = 0d0
	  enddo
	endif

	do 204 i1=-1,1,2
	do 204 i2=-1,1,2
	do 204 i3=-1,1,2
	do 204 ig=-1,1,2
	  mats1   = 0d0
	  matt1   = 0d0
	  mats2   = 0d0
	  matt2   = 0d0
	  mats1hvv = 0d0
	  matt1hvv = 0d0
	  mats2hvv = 0d0
	  matt2hvv = 0d0
	  if (i1.eq.-i2) then
      	    mats1 = mats1 + msHZZ4fg1(i2,i3,ig)
      	    mats2 = mats2 + msHZZ4fg2(i2,i3,ig)
            if (qhvv.ne.0) then
      	      mats1hvv = mats1hvv + msHZZ4fg1hvv(i2,i3,ig)
      	      mats2hvv = mats2hvv + msHZZ4fg2hvv(i2,i3,ig)
	    endif
	  endif
	  if ((i1.eq.1).and.(i2.eq.-1).and.(i3.eq.-1)) then
      	    matt1  = matt1 + mtHWW4fg1(ig)
      	    matt2  = matt2 + mtHWW4fg2(ig)
            if (qhvv.ne.0) then
      	      matt1hvv  = matt1hvv + mtHWW4fg1hvv(ig)
      	      matt2hvv  = matt2hvv + mtHWW4fg2hvv(ig)
	    endif
	  endif

 	do 204 g1=1,2
 	do 204 g2=1,2
 	do 204 g3=1,2
 	do 204 g4=1,2
 	  wmatt1 = v(g3,g1)*cv(g4,g2)*matt1
 	  wmatt2 = v(g3,g1)*cv(g4,g2)*matt2
          if (qhvv.ne.0) then
 	    wmatt1hvv = v(g3,g1)*cv(g4,g2)*matt1hvv
 	    wmatt2hvv = v(g3,g1)*cv(g4,g2)*matt2hvv
	  endif
 	  f1 = 2*g1-1
 	  f2 = 2*g2-1
 	  f3 = 2*g3
 	  f4 = 2*g4
 	  if ((f1.eq.f2).and.(f3.eq.f4)) then
	    if ((qhvv.eq.0).and.(qqcddiag.eq.1)) then
 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*qch2*12d0*( abs(wmatt1)**2+abs(wmatt2)**2 
     &		                    +abs(mats1)**2 +abs(mats2)**2 ) 
	    elseif ((qhvv.ne.0).and.(qqcddiag.eq.1)) then
 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*qch2*12d0*( abs(wmatt1hvv)**2+abs(wmatt2hvv)**2 
     &		                    +abs(mats1hvv)**2 +abs(mats2hvv)**2) 
	    endif
	    if (qqcdnondiag.eq.1)
     & 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*(-qchint*8d0*dreal( mats1*dconjg(wmatt1)
     &		                            +mats1*dconjg(wmatt2)
     &		                            +mats2*dconjg(wmatt1)
     &		                            +mats2*dconjg(wmatt2) ))
 	  else
	    if ((qhvv.eq.0).and.(qqcddiag.eq.1)) then
 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*qch2*12d0*(abs(wmatt1)**2+abs(wmatt2)**2)
	    elseif ((qhvv.ne.0).and.(qqcddiag.eq.1)) then
 	      m2aqq_gluon(f1,f2,f3,f4) = m2aqq_gluon(f1,f2,f3,f4) 
     &	        + gs2el6*qch2*12d0*(abs(wmatt1hvv)**2+abs(wmatt2hvv)**2)
 	    endif
 	  endif
204	  continue

	end

************************************************************************
        subroutine M_WW_gluon(mH4fg1,mH4fg2,fa,fb,fc,fd,qqhvv)
************************************************************************
*       Helicity amplitudes for 
*	H -> WW -> fa + fb-bar + fc + fd-bar + gluon
*
*	qqhvv = 0/1: without/with anomalous HVV couplings
*-----------------------------------------------------------------------
*       19.3.06 Stefan Dittmaier
************************************************************************
        implicit real*8 (a-z)
        complex*16 sp(6,6),csp(6,6)
        complex*16 ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2,cmh,cmh2
        complex*16 pwab,pwcd,pwabp,pwcdp,cpwab,cpwcd,cpwabp,cpwcdp
        complex*16 A10m,A01m,Aab(-1:1),Acd(-1:1)
        complex*16 A10mhvv,A10phvv
	complex*16 mH4fg1(-1:1),mH4fg2(-1:1)
        complex*16 fac
        complex*16 v,cv
        complex*16 xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null
        complex*16 xml,xml2,xmqp,xmqp2,xmqm,xmqm2
        real*8 vp(6,6)
        integer fa,fb,fc,fd,ia,ib,ic,id,i1,i2,i3
        integer qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &			 qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
	logical checkab,checkcd
        integer qqhvv

        common/prods4/sp,csp,vp
        common/cparam/ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
        common/xparam/xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null,
     &                xml(3),xml2(3),xmqp(3),xmqp2(3),xmqm(3),xmqm2(3)
        common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &         v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &         ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
        common/rcoptions/qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &			 qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp

	A10m(ia,ib,ic,id,pwab,pwcd,pwabp,pwcdp) = csp(ib,id)*
     &	   pwabp*pwcd*(csp(ia,ib)*sp(ia,ic)+csp(6,ib)*sp(6,ic))
     &	      /csp(6,ia)/csp(6,ib)

	A10mhvv(ia,ib,ic,id,pwab,pwcd,pwabp,pwcdp,a1,a2,a3) = 
     &	  pwabp*pwcd/csp(6,ia)/csp(6,ib)
     &	  *( a1*csp(ib,id)*(csp(ib,ia)*sp(ia,ic)+csp(ib,6)*sp(6,ic))
     &	    +dcmplx(a2,-a3)/2d0*csp(ib,id)*sp(ic,id)
     &	     *( csp(ib,ia)*(sp(ia,ib)*csp(id,ib)+sp(ia,6)*csp(id,6))
     &	       +csp(ib,6)*(csp(id,ia)*sp(6,ia)+csp(id,ib)*sp(6,ib)) )
     &	    -dcmplx(a2,+a3)/2d0*csp(id,ic)
     &	     *( csp(ib,ia)*sp(ic,ia)+csp(ib,6)*sp(ic,6) )**2 )

	A10phvv(ia,ib,ic,id,pwab,pwcd,pwabp,pwcdp,a1,a2,a3) = 
     &	  -pwabp*pwcd/sp(6,ia)/sp(6,ib) 	
     &	  *( a1*sp(ia,ic)*(sp(ia,ib)*csp(ib,id)+sp(ia,6)*csp(6,id))
     &	    -dcmplx(a2,-a3)/2d0*sp(ic,id)
     &	     *( sp(ia,ib)*csp(ib,id)+sp(ia,6)*csp(6,id) )**2 
     &	    +dcmplx(a2,+a3)/2d0*sp(ia,ic)*csp(id,ic)
     &	     *( sp(ia,ib)*(csp(ib,ia)*sp(ic,ia)+csp(ib,6)*sp(ic,6))
     &	       +sp(ia,6)*(csp(6,ia)*sp(ic,ia)+csp(6,ib)*sp(ic,ib)) ) )

c	A01m(ia,ib,ic,id,pwab,pwcd,pwabp,pwcdp) = -csp(ib,id)*
c     &	   pwab*pwcdp*(csp(ic,id)*sp(ic,ia)+csp(6,id)*sp(6,ia))
c     &	      /csp(6,ic)/csp(6,id) 	

	sab  = vp(fa,fb)
	scd  = vp(fc,fd)
	sabp = vp(fa,fb) + vp(fa,6) + vp(fb,6)
	scdp = vp(fc,fd) + vp(fc,6) + vp(fd,6)

        if ((qwidth.eq.0).or.((qwidth.eq.2).and.(sab.lt.0d0))) then
          pwab = 1d0/(sab-mw2)
        else
          pwab = 1d0/(sab-cmw2)
        endif
        if ((qwidth.eq.0).or.((qwidth.eq.2).and.(scd.lt.0d0))) then
          pwcd = 1d0/(scd-mw2)
        else
          pwcd = 1d0/(scd-cmw2)
        endif
        if ((qwidth.eq.0).or.((qwidth.eq.2).and.(sabp.lt.0d0))) then
          pwabp = 1d0/(sabp-mw2)
        else
          pwabp = 1d0/(sabp-cmw2)
        endif
        if ((qwidth.eq.0).or.((qwidth.eq.2).and.(scdp.lt.0d0))) then
          pwcdp = 1d0/(scdp-mw2)
        else
          pwcdp = 1d0/(scdp-cmw2)
        endif

	checkab = ((qschan.eq.1).and.(sab.gt.0d0).and.(scdp.gt.0d0))
     &	     .or. ((qtchan.eq.1).and.(sab.lt.0d0).and.(scdp.lt.0d0))
	checkcd = ((qschan.eq.1).and.(scd.gt.0d0).and.(sabp.gt.0d0))
     &	     .or. ((qtchan.eq.1).and.(scd.lt.0d0).and.(sabp.lt.0d0))

	if (.not.checkab) pwab = 0d0
	if (.not.checkcd) pwcd = 0d0

	cpwab  = dconjg(pwab)
	cpwabp = dconjg(pwabp)
	cpwcd  = dconjg(pwcd)
	cpwcdp = dconjg(pwcdp)

	if (qqhvv.eq.0) then
	  fac = sqrt(2d0)*xmw/xsw**3
	  Aab(-1) = A10m(fa,fb,fc,fd,pwab,pwcd,pwabp,pwcdp)
c	  Aab(+1) = -dconjg(A01m(fd,fc,fb,fa,cpwcd,cpwab,cpwcdp,cpwabp))
	  Aab(+1) = -dconjg(A10m(fb,fa,fd,fc,cpwab,cpwcd,cpwabp,cpwcdp))
c	  Acd(-1) = A01m(fa,fb,fc,fd,pwab,pwcd,pwabp,pwcdp)
c	  Acd(+1) = -dconjg(A01m(fb,fa,fd,fc,cpwab,cpwcd,cpwabp,cpwcdp))
	  Acd(-1) = A10m(fc,fd,fa,fb,pwcd,pwab,pwcdp,pwabp)
	  Acd(+1) = -dconjg(A10m(fd,fc,fb,fa,cpwcd,cpwab,cpwcdp,cpwabp))
	else
	  fac     = sqrt(2d0)/xsw2
          call fixahvv(sabp,scd,
     &             a1hww,a2hww,a3hww,a1haa,a2haa,a3haa,
     &             a1haz,a2haz,a3haz,a1hzz,a2hzz,a3hzz)
	  Aab(-1) = A10mhvv(fa,fb,fc,fd,pwab,pwcd,pwabp,pwcdp,
     &			a1hww,a2hww,a3hww)
	  Aab(+1) = A10phvv(fa,fb,fc,fd,pwab,pwcd,pwabp,pwcdp,
     &			a1hww,a2hww,a3hww)
          call fixahvv(sab,scdp,
     &             a1hww,a2hww,a3hww,a1haa,a2haa,a3haa,
     &             a1haz,a2haz,a3haz,a1hzz,a2hzz,a3hzz)
	  Acd(-1) = A10mhvv(fc,fd,fa,fb,pwcd,pwab,pwcdp,pwabp,
     &			a1hww,a2hww,a3hww)
	  Acd(+1) = A10phvv(fc,fd,fa,fb,pwcd,pwab,pwcdp,pwabp,
     &			a1hww,a2hww,a3hww)
	endif

	do i1=-1,1,2
	  mH4fg1(i1) = fac*Aab(i1)
	  mH4fg2(i1) = fac*Acd(i1)
	enddo

	end

************************************************************************
        subroutine M_ZZ_gluon(mH4fg1,mH4fg2,gaz,gcz,qa,qc,fa,fb,fc,fd,
     &	                      qqhvv)
************************************************************************
*       Helicity amplitudes for 
*	H -> ZZ -> fa + fb-bar + fc + fd-bar + gluon
*
*	qqhvv = 0/1: without/with anomalous HVV couplings
*-----------------------------------------------------------------------
*       19.3.06 Stefan Dittmaier
************************************************************************
        implicit real*8 (a-z)
        complex*16 sp(6,6),csp(6,6)
        complex*16 ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2,cmh,cmh2
        complex*16 pzab,pzcd,pzabp,pzcdp
        complex*16 paab,pacd,paabp,pacdp
        complex*16 pvab,pvcd,pvabp,pvcdp
        complex*16 A10mmm,A01mmm
        complex*16 A10mmmhvv,A10mmphvv,A10mpmhvv,A10mpphvv
        complex*16 Aab(-1:1,-1:1,-1:1),Acd(-1:1,-1:1,-1:1)
	complex*16 mH4fg1(-1:1,-1:1,-1:1),mH4fg2(-1:1,-1:1,-1:1)
        complex*16 gaz(-1:1),gcz(-1:1),fac,fac1,fac2
        complex*16 v,cv
        complex*16 xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null
        complex*16 xml,xml2,xmqp,xmqp2,xmqm,xmqm2
        real*8 vp(6,6)
        integer fa,fb,fc,fd,ia,ib,ic,id,i1,i2,i3,j
        integer qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &			 qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp
	logical checkab,checkcd
        integer qqhvv

        common/prods4/sp,csp,vp
        common/cparam/ccw,ccw2,csw,csw2,cmw,cmw2,cmz,cmz2
        common/xparam/xcw,xcw2,xsw,xsw2,xmw,xmw2,xmz,xmz2,xmh,xmh2,null,
     &                xml(3),xml2(3),xmqp(3),xmqp2(3),xmqm(3),xmqm2(3)
        common/param/pi,el,alpha,alpha0,alphaz,GF,alphas,
     &         v(3,3),cv(3,3),cw,cw2,sw,sw2,mw,mw2,gw,mz,mz2,gz,mh,mh2,
     &         ml(3),ml2(3),mqp(3),mqp2(3),mqm(3),mqm2(3)
        common/rcoptions/qborn,qw,qz,qschan,qtchan,qch2,qchint,
     &                   qbini,qbfin,qwidth,qfact,qbos,qferm,qsoft,qhh2,
     &			 qqcddiag,qqcdnondiag,qqcdgsplit,qqcdggfus,qcp

	A10mmm(ia,ib,ic,id) = csp(ib,id)*
     &	  (csp(ia,ib)*sp(ia,ic)+csp(6,ib)*sp(6,ic))/csp(6,ia)/csp(6,ib)

c	A01mmm(ia,ib,ic,id) = -csp(ib,id)*
c     &	  (csp(ic,id)*sp(ic,ia)+csp(6,id)*sp(6,ia))/csp(6,ic)/csp(6,id) 

	A10mmmhvv(ia,ib,ic,id,a1,a2,a3) = 1d0/csp(6,ia)/csp(6,ib)
     &    *( a1*csp(ib,id)*(csp(ib,ia)*sp(ia,ic)+csp(ib,6)*sp(6,ic))
     &      +dcmplx(a2,-a3)/2d0*csp(ib,id)*sp(ic,id)
     &       *( csp(ib,ia)*(sp(ia,ib)*csp(id,ib)+sp(ia,6)*csp(id,6))
     &         +csp(ib,6)*(csp(id,ia)*sp(6,ia)+csp(id,ib)*sp(6,ib)) )
     &      -dcmplx(a2,+a3)/2d0*csp(id,ic)
     &       *( csp(ib,ia)*sp(ic,ia)+csp(ib,6)*sp(ic,6) )**2 )

	A10mpmhvv(ia,ib,ic,id,a1,a2,a3) = 1d0/csp(6,ia)/csp(6,ib)
     &	  *( a1*csp(ib,ic)*(csp(ib,ia)*sp(ia,id)+csp(ib,6)*sp(6,id))
     &	    +dcmplx(a2,-a3)/2d0*csp(ib,ic)*sp(id,ic)
     &	     *( csp(ib,ia)*(sp(ia,ib)*csp(ic,ib)+sp(ia,6)*csp(ic,6))
     &	       +csp(ib,6)*(csp(ic,ia)*sp(6,ia)+csp(ic,ib)*sp(6,ib)) )
     &	    -dcmplx(a2,+a3)/2d0*csp(ic,id)
     &	     *( csp(ib,ia)*sp(ia,id)+csp(ib,6)*sp(6,id) )**2 )

	A10mmphvv(ia,ib,ic,id,a1,a2,a3) = -1d0/sp(6,ia)/sp(6,ib) 	
     &    *( a1*sp(ia,ic)*(sp(ia,ib)*csp(ib,id)+sp(ia,6)*csp(6,id))
     &      -dcmplx(a2,-a3)/2d0*sp(ic,id)
     &       *( sp(ia,ib)*csp(ib,id)+sp(ia,6)*csp(6,id) )**2
     &      +dcmplx(a2,+a3)/2d0*sp(ia,ic)*csp(id,ic)
     &       *( sp(ia,ib)*(csp(ib,ia)*sp(ic,ia)+csp(ib,6)*sp(ic,6))
     &         +sp(ia,6)*(csp(6,ia)*sp(ic,ia)+csp(6,ib)*sp(ic,ib)) ) )

	A10mpphvv(ia,ib,ic,id,a1,a2,a3) = -1d0/sp(6,ia)/sp(6,ib) 	
     &	  *( a1*sp(ia,id)*(sp(ia,ib)*csp(ib,ic)+sp(ia,6)*csp(6,ic))
     &	    -dcmplx(a2,-a3)/2d0*sp(id,ic)
     &	     *( sp(ia,ib)*csp(ib,ic)+sp(ia,6)*csp(6,ic) )**2 
     &	    +dcmplx(a2,+a3)/2d0*sp(ia,id)*csp(ic,id)
     &	     *( sp(ia,ib)*(csp(ib,ia)*sp(id,ia)+csp(ib,6)*sp(id,6))
     &	       +sp(ia,6)*(csp(6,ia)*sp(id,ia)+csp(6,ib)*sp(id,ib)) ) )

	sab  = vp(fa,fb)
	scd  = vp(fc,fd)
	sabp = vp(fa,fb) + vp(fa,6) + vp(fb,6)
	scdp = vp(fc,fd) + vp(fc,6) + vp(fd,6)

        paab  = 1d0/sab
        pacd  = 1d0/scd
        paabp = 1d0/sabp
        pacdp = 1d0/scdp

        if ((qwidth.eq.0).or.((qwidth.eq.2).and.(sab.lt.0d0))) then
          pzab = 1d0/(sab-mz2)
        else
          pzab = 1d0/(sab-cmz2)
        endif
        if ((qwidth.eq.0).or.((qwidth.eq.2).and.(scd.lt.0d0))) then
          pzcd = 1d0/(scd-mz2)
        else
          pzcd = 1d0/(scd-cmz2)
        endif
        if ((qwidth.eq.0).or.((qwidth.eq.2).and.(sabp.lt.0d0))) then
          pzabp = 1d0/(sabp-mz2)
        else
          pzabp = 1d0/(sabp-cmz2)
        endif
        if ((qwidth.eq.0).or.((qwidth.eq.2).and.(scdp.lt.0d0))) then
          pzcdp = 1d0/(scdp-mz2)
        else
          pzcdp = 1d0/(scdp-cmz2)
        endif

	checkab = ((qschan.eq.1).and.(sab.gt.0d0).and.(scdp.gt.0d0))
     &	     .or. ((qtchan.eq.1).and.(sab.lt.0d0).and.(scdp.lt.0d0))
	checkcd = ((qschan.eq.1).and.(scd.gt.0d0).and.(sabp.gt.0d0))
     &	     .or. ((qtchan.eq.1).and.(scd.lt.0d0).and.(sabp.lt.0d0))

	if (.not.checkab) then
	  paab = 0d0
	  pzab = 0d0
	endif
	if (.not.checkcd) then
	  pacd = 0d0
	  pzcd = 0d0
	endif

	if (qqhvv.eq.0) then

	fac1 = 2d0*sqrt(2d0)*xmw/xcw2/xsw * pzabp*pzcd
	fac2 = 2d0*sqrt(2d0)*xmw/xcw2/xsw * pzab *pzcdp

	Aab(-1,-1,-1) = A10mmm(fa,fb,fc,fd)
	Aab(+1,-1,-1) =-A10mmm(fb,fa,fc,fd)
	Aab(-1,+1,-1) = A10mmm(fa,fb,fd,fc)
	Aab(+1,+1,-1) =-A10mmm(fb,fa,fd,fc)
	Aab(+1,+1,+1) = dconjg(A10mmm(fa,fb,fc,fd))
	Aab(-1,+1,+1) =-dconjg(A10mmm(fb,fa,fc,fd))
	Aab(+1,-1,+1) = dconjg(A10mmm(fa,fb,fd,fc))
	Aab(-1,-1,+1) =-dconjg(A10mmm(fb,fa,fd,fc))

c	Acd(-1,-1,-1) = A01mmm(fa,fb,fc,fd)
c	Acd(+1,-1,-1) = A01mmm(fb,fa,fc,fd)
c	Acd(-1,+1,-1) =-A01mmm(fa,fb,fd,fc)
c	Acd(+1,+1,-1) =-A01mmm(fb,fa,fd,fc)
c	Acd(+1,+1,+1) = dconjg(A01mmm(fa,fb,fc,fd))
c	Acd(-1,+1,+1) = dconjg(A01mmm(fb,fa,fc,fd))
c	Acd(+1,-1,+1) =-dconjg(A01mmm(fa,fb,fd,fc))
c	Acd(-1,-1,+1) =-dconjg(A01mmm(fb,fa,fd,fc))

	Acd(-1,-1,-1) = A10mmm(fc,fd,fa,fb)
	Acd(+1,-1,-1) = A10mmm(fc,fd,fb,fa)
	Acd(-1,+1,-1) =-A10mmm(fd,fc,fa,fb)
	Acd(+1,+1,-1) =-A10mmm(fd,fc,fb,fa)
	Acd(+1,+1,+1) = dconjg(A10mmm(fc,fd,fa,fb))
	Acd(-1,+1,+1) = dconjg(A10mmm(fc,fd,fb,fa))
	Acd(+1,-1,+1) =-dconjg(A10mmm(fd,fc,fa,fb))
	Acd(-1,-1,+1) =-dconjg(A10mmm(fd,fc,fb,fa))

	do i1=-1,1,2
	do i2=-1,1,2
	do i3=-1,1,2
	  mH4fg1(i1,i2,i3) = fac1*gaz(i1)*gcz(i2)*Aab(i1,i2,i3)
	  mH4fg2(i1,i2,i3) = fac2*gaz(i1)*gcz(i2)*Acd(i1,i2,i3)
	enddo
	enddo
	enddo

	else

	do i1=-1,1,2
	do i2=-1,1,2
	do i3=-1,1,2
	  mH4fg1(i1,i2,i3) = 0d0
	  mH4fg2(i1,i2,i3) = 0d0
	enddo
	enddo
	enddo

        call fixahvv(sabp,scd,
     &             a1hww,a2hww,a3hww,a1haa,a2haa,a3haa,
     &             a1haz,a2haz,a3haz,a1hzz,a2hzz,a3hzz)
        call fixahvv(sab,scdp,
     &             xa1hww,xa2hww,xa3hww,xa1haa,xa2haa,xa3haa,
     &             xa1haz,xa2haz,xa3haz,xa1hzz,xa2hzz,xa3hzz)

	do 100 j=1,3

	if (j.eq.1) then
	  a1  = a1haa
	  a2  = a2haa
	  a3  = a3haa
	  xa1 = xa1haa
	  xa2 = xa2haa
	  xa3 = xa3haa
	elseif (j.eq.2) then
	  a1  = a1haz
	  a2  = a2haz
	  a3  = a3haz
	  xa1 = xa1haz
	  xa2 = xa2haz
	  xa3 = xa3haz
	elseif (j.eq.3) then
	  a1  = a1hzz
	  a2  = a2hzz
	  a3  = a3hzz
	  xa1 = xa1hzz
	  xa2 = xa2hzz
	  xa3 = xa3hzz
	endif

	Aab(-1,-1,-1) = A10mmmhvv(fa,fb,fc,fd,a1,a2,a3)
	Aab(-1,+1,-1) = A10mpmhvv(fa,fb,fc,fd,a1,a2,a3)
	Aab(-1,-1,+1) = A10mmphvv(fa,fb,fc,fd,a1,a2,a3)
	Aab(-1,+1,+1) = A10mpphvv(fa,fb,fc,fd,a1,a2,a3)
	Aab(+1,+1,+1) = dconjg(A10mmmhvv(fa,fb,fc,fd,a1,a2,a3))
	Aab(+1,-1,+1) = dconjg(A10mpmhvv(fa,fb,fc,fd,a1,a2,a3))
	Aab(+1,+1,-1) = dconjg(A10mmphvv(fa,fb,fc,fd,a1,a2,a3))
	Aab(+1,-1,-1) = dconjg(A10mpphvv(fa,fb,fc,fd,a1,a2,a3))

	Acd(-1,-1,-1) = A10mmmhvv(fc,fd,fa,fb,xa1,xa2,xa3)
	Acd(+1,-1,-1) = A10mpmhvv(fc,fd,fa,fb,xa1,xa2,xa3)
	Acd(-1,-1,+1) = A10mmphvv(fc,fd,fa,fb,xa1,xa2,xa3)
	Acd(+1,-1,+1) = A10mpphvv(fc,fd,fa,fb,xa1,xa2,xa3)
	Acd(+1,+1,+1) = dconjg(A10mmmhvv(fc,fd,fa,fb,xa1,xa2,xa3))
	Acd(-1,+1,+1) = dconjg(A10mpmhvv(fc,fd,fa,fb,xa1,xa2,xa3))
	Acd(+1,+1,-1) = dconjg(A10mmphvv(fc,fd,fa,fb,xa1,xa2,xa3))
	Acd(-1,+1,-1) = dconjg(A10mpphvv(fc,fd,fa,fb,xa1,xa2,xa3))

	do i1=-1,1,2
	do i2=-1,1,2
	do i3=-1,1,2
	  if (j.eq.1) then
	    fac1 = 2d0*sqrt(2d0)*(-qa)*(-qc) * paabp*pacd
	    fac2 = 2d0*sqrt(2d0)*(-qa)*(-qc) * paab *pacdp
	  elseif (j.eq.2) then
	    fac1 = 2d0*sqrt(2d0)*( (-qa)*gcz(i2)*paabp*pzcd
     &	                          +gaz(i1)*(-qc)*pzabp*pacd )
	    fac2 = 2d0*sqrt(2d0)*( (-qa)*gcz(i2)* paab*pzcdp
     &	                          +gaz(i1)*(-qc)* pzab*pacdp )
	  elseif (j.eq.3) then
	    fac1 = 2d0*sqrt(2d0)*gaz(i1)*gcz(i2) * pzabp*pzcd
	    fac2 = 2d0*sqrt(2d0)*gaz(i1)*gcz(i2) * pzab *pzcdp
	  endif
	  mH4fg1(i1,i2,i3) = mH4fg1(i1,i2,i3) + fac1*Aab(i1,i2,i3)
	  mH4fg2(i1,i2,i3) = mH4fg2(i1,i2,i3) + fac2*Acd(i1,i2,i3)
	enddo
	enddo
	enddo

100	continue

	endif

	end
************************************************************************
        subroutine setprods4(p,dir)
************************************************************************
*       Weyl-van der Waerden and Minkowski products
*-----------------------------------------------------------------------
*       14.3.2001 Stefan Dittmaier
************************************************************************
        implicit real*8 (a-z)
        complex*16 eiph(6),sp(6,6),csp(6,6)
        real*8 e(6),th(6),re(6),cth2(6),sth2(6),vp(6,6),p(6,0:3)
        integer i,j,k,dir(6)

        common/prods4/sp,csp,vp

        range(y) = max(min(y,1d0),-1d0)

        do 100 i=1,6
          e(i)    = p(i,0)
          re(i)   = sqrt(e(i))
          vect    = sqrt(p(i,1)**2+p(i,2)**2)
          vec     = sqrt(p(i,1)**2+p(i,2)**2+p(i,3)**2)
	  cth     = range( p(i,3)/vec )
	  sth     = vect/vec
	  if (cth.gt.0d0) then
            cth2(i) = sqrt((1d0+cth)/2d0)
	    sth2(i) = sth/2d0/cth2(i)
	  else
            sth2(i) = sqrt((1d0-cth)/2d0)
	    cth2(i) = sth/2d0/sth2(i)
	  endif
          if (abs(sth).lt.1d-10) then
            eiph(i) = 1d0
          else
            eiph(i) = dcmplx(p(i,1),p(i,2))/vec/sth
          endif
100     continue
        do 200 i=2,6
        do 200 j=1,i-1
           sp(i,j) = 2d0*re(i)*re(j)
     &               *(cth2(i)/eiph(i)*sth2(j)-sth2(i)*cth2(j)/eiph(j))
          csp(i,j) = dconjg(sp(i,j))*dir(i)*dir(j)
           vp(i,j) = sp(i,j)*csp(i,j)
           sp(j,i) = - sp(i,j)
          csp(j,i) = -csp(i,j)
           vp(j,i) =   vp(i,j)
200     continue

        end
