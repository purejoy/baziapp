# -*- coding: utf-8 -*-

import datetime, ast, SolarTerms, JDatetime
from django.utils.safestring import mark_safe


class bazi:
    BaseYear = 1601
    LunarMonthTerms = ("*","正","二","三","四","五","六", "七","八","九","十","冬","腊")
    LunarDayTerms = ("*","初一","初二","初三","初四","初五",
	             "初六","初七","初八","初九","初十",
	             "十一","十二","十三","十四","十五",
	             "十六","十七","十八","十九","二十",
	             "廿一","廿二","廿三","廿四","廿五",       
	             "廿六","廿七","廿八","廿九","三十")

    Jieqi = ("大雪","小寒","立春","惊蛰","清明","立夏","芒种","小暑","立秋","白露","寒露","立冬","大雪")
    Tiangan = ("甲","乙","丙","丁","戊","己","庚","辛","壬","癸","")
    Dizhi = ("子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥")
    Canggan = ((9,10,10),(5,7,9),(0,2,4),(1,10,10),(1,4,9),(2,4,6),
               (3,5,10),(1,3,5),(4,6,8),(7,10,10),(3,4,7),(0,8,10))

    Shengxiao = ("鼠","牛","虎","兔","龙","蛇","马","羊","猴","鸡","狗","猪")
    Shishen = ("比肩","劫财","食神","伤官","偏财","正财","七杀","正官","偏印","正印","")
    Gender = ("乾造","坤造")
    ShizhuList =( #甲己   乙庚   丙辛   丁壬   戊癸   
                 ("甲子","丙子","戊子","庚子","壬子"),
                 ("乙丑","丁丑","己丑","辛丑","癸丑"),
                 ("丙寅","戊寅","庚寅","壬寅","甲寅"),
                 ("丁卯","己卯","辛卯","癸卯","乙卯"),
                 ("戊辰","庚辰","壬辰","甲辰","丙辰"),
                 ("己巳","辛巳","癸巳","乙巳","丁巳"),
                 ("庚午","壬午","甲午","丙午","戊午"),
                 ("辛未","癸未","乙未","丁未","己未"),
                 ("壬申","甲申","丙申","戊申","庚申"),
                 ("癸酉","乙酉","丁酉","己酉","辛酉"),
                 ("甲戌","丙戌","戊戌","庚戌","壬戌"),
                 ("乙亥","丁亥","己亥","辛亥","癸亥") )

    lifalst = ("太初历","四分历","大明历","戊寅元历","麟德历","正元历","应天历","崇天历","淳祐历","授时历")
    
    pqargs = ((1683430.515601,15.218750011),(1752157.640664,15.218749978),
              (1907369.128100,15.218449176),(1947180.798300,15.218524844),
              (1964362.041824,15.218533526),(2007445.469786,15.218535181),
              (2073204.872850,15.218515221),(2111190.300888,15.218425000),
              (2178485.706538,15.218425000),(2188621.191481,15.218437484))

    def __init__(self,bd,gender,ast=0,lon=120,lifa=0):
        self.bd = bd
        self.isFemale = gender
        self.AST = ast
        self.L = lon
        self.lifa = lifa
        self.bazi = [-1]*8
        self.shishen = [-1]*10
        self.bjq = bd
        self.fjq = bd
        self.qyspan = [0]*4
        self.jydt = bd

    def IsLeapYear(self,year):
        return (year%4 == 0) and (year%100 != 0) or (year%400 == 0)

    def SolarDaysFromBaseYear(self,date):
        pd = (0,31,59,90,120,151,181,212,243,273,304,334)
        delta = date.year - bazi.BaseYear
        offset = 365*delta + delta/4 - delta/100 + delta/400
        offset += pd[date.month-1]
        if date.month > 2 and self.IsLeapYear(date.year):
            offset += 1
        offset += date.day
        return offset-1


    def Solar2Lunar(self,bd):
        Y = bd.year
        M = bd.month
        D = bd.day
  
        jdate = JDatetime.JDatetime(bd)
        t1 = 365.2422*(Y - 1999) - 50
        zq = []
        hs = []
        dongzhi = SolarTerms.jiaoCal(t1,-90,0)
        jdate.setFromJD(dongzhi+jdate.J2000 + 8/(24-0.0),1)
        if jdate.cmp_date([Y,M,D]) == 0:
            t1 =  365.2422*(Y - 2000) - 50
        for i in range(14):
            zq.append(SolarTerms.jiaoCal(t1 + i * 30.4, i * 30 - 90, 0))  # 中气计算,冬至的太阳黄经是270度(或-90度)
        dongZhiJia1 = zq[0] + 1 - jdate.Dint_dec(zq[0], 8, 0)# 冬至过后的第一天0点的儒略日数
        hs.append(SolarTerms.jiaoCal(dongZhiJia1, 0, 1))  # 首月结束的日月合朔时刻
        for i in range(1,14): 
            hs.append(SolarTerms.jiaoCal(hs[i-1] + 25, 0, 1))
        hs.append(SolarTerms.jiaoCal(hs[0] - 35, 0, 1))
    
        A = []
        C = []
        for i in range(14):
            A.append(jdate.Dint_dec(zq[i],8,1))
            C.append(jdate.Dint_dec(hs[i],8,1))
        C.append(jdate.Dint_dec(hs[14],8,1))


        tot = 12
        nun = -5
        yn = [11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10]
        if (C[12] <= A[12]):  # 闰月分析
            yn[12] = 10
            tot = 13  
            for i in range(1, 13):
                if (C[i] <= A[i]):
                    break
            nun = i - 1
            for j in range(i, 13):
                yn[j-1] += 11 
                yn[j-1] %= 12
        j = 0
        jdate.setFromJD(C[0] + jdate.J2000 + 8/(24 - 0.0), 1)
        while jdate.cmp_date([Y,M,D]):
            j += 1
            jdate.setFromJD(C[j] + jdate.J2000 + 8/(24 - 0.0), 1)

        if j == (nun+1):
            isLeapMonth = 1
        else:
            isLeapMonth = 0
        
        if j == 0:
            jdate.setFromJD(C[14] + jdate.J2000 + 8/(24 - 0.0), 1)
        else:
            jdate.setFromJD(C[j-1] + jdate.J2000 + 8/(24- 0.0), 1)
        BD = datetime.date(Y,M,D)
        l_day = 1 + (BD - jdate.GetDate()).days
      
        j = (j+tot-1)%tot   
        l_month = yn[j]+1

        if l_month >= 9 and M <= 3:
            l_year = Y - 1
        else:
            l_year = Y
   
        return (l_year,l_month,l_day,isLeapMonth)
        
    
        

    def Get_PQ_SolarTerm(self):
        
        if self.lifa > 0:
            lfindx = self.lifa - 1
        else:
            lfindx = 9
            
        mindx = self.bd.month
        bd = JDatetime.JDatetime(self.bd)
        bjq = JDatetime.JDatetime(self.bjq)
        fjq = JDatetime.JDatetime(self.fjq)
        b = bazi.pqargs[lfindx][0]+bazi.pqargs[lfindx][1]
        k = 2*(bazi.pqargs[lfindx][1])

        if self.AST:
            BD = bd.toJD(0)
            JD = ast.mst_ast((bd.toJD(1) - 8/24.0 - bd.J2000)/36525) + BD + (self.L - 120.0)/360.0
            n = round((BD - self.bd.day + 6 - b)/k)
            tmp = k*n + b - 8/24.0 - bd.J2000
            TD = tmp + SolarTerms.dt_T2(tmp)
            D = tmp + ast.mst_ast(TD/36525) + self.L/360.0 + bd.J2000

            if JD < D:
                mindx -= 2
                tmp -= k
                TD = tmp + SolarTerms.dt_T2(tmp)
                Q = tmp + ast.mst_ast(TD/36525) + self.L/360.0 + bd.J2000
                bjq.setFromJD(Q,0)
                fjq.setFromJD(D,0)
            else:
                mindx -= 1
                tmp += k
                TD = tmp + SolarTerms.dt_T2(tmp)
                Q = tmp + ast.mst_ast(TD/36525) + self.L/360.0 + bd.J2000
                bjq.setFromJD(D,0)
                fjq.setFromJD(Q,0)

        else:
            JD = bd.toJD(0)
            n = round((JD - self.bd.day + 6 - b)/k)
            D = k*n + b

            if JD < D:
                mindx -= 2
                bjq.setFromJD(D-k,0)
                fjq.setFromJD(D,0)
            else:
                mindx -= 1
                bjq.setFromJD(D,0)
                fjq.setFromJD(D+k,0)

        return (mindx,bjq.GetDatetime(),fjq.GetDatetime())

    def Get_DQ_SolarTerm(self):
        
        mindx = self.bd.month
        bd = JDatetime.JDatetime(self.bd)
        bjq = JDatetime.JDatetime(self.bjq)
        fjq = JDatetime.JDatetime(self.fjq)

        if self.AST:
            BD = bd.toJD(0)
            JD = ast.mst_ast((bd.toJD(1) - 8/24.0 - bd.J2000)/36525) + BD + (self.L - 120.0)/360.0
            tmp = BD - self.bd.day + 5 - bd.J2000
            D = SolarTerms.qi_accurate2(tmp,1,self.L) + bd.J2000
            #D = SolarTerms.qi_accurate2(tmp,1)
            #D += ast.mst_ast(D/36525) - SolarTerms.dt_T2(D) + self.L/360.0 + bd.J2000

            if JD < D:
                mindx -= 2
                tmp -= 30
                Q = SolarTerms.qi_accurate2(tmp,1,self.L) + bd.J2000
                #Q += ast.mst_ast(Q/36535) - SolarTerms.dt_T2(Q) + self.L/360.0 + bd.J2000
                bjq.setFromJD(Q,0)
                fjq.setFromJD(D,0)
            else:
                mindx -= 1
                tmp += 30
                Q = SolarTerms.qi_accurate2(tmp,1,self.L) + bd.J2000
                #Q += ast.mst_ast(Q/36535) - SolarTerms.dt_T2(Q) + self.L/360.0 + bd.J2000
                bjq.setFromJD(D,0)
                fjq.setFromJD(Q,0)
                
        else:
            JD = bd.toJD(0)
            tmp = JD - self.bd.day + 5 - bd.J2000
            D = SolarTerms.qi_accurate2(tmp,0,120) + bd.J2000

            if JD < D:
                mindx -= 2
                tmp -= 30
                Q = SolarTerms.qi_accurate2(tmp,0,120) + bd.J2000
                bjq.setFromJD(Q,0)
                fjq.setFromJD(D,0)

            else:
                mindx -= 1
                tmp += 30
                Q = SolarTerms.qi_accurate2(tmp,0,120) + bd.J2000
                bjq.setFromJD(D,0)
                fjq.setFromJD(Q,0)

        return (mindx,bjq.GetDatetime(),fjq.GetDatetime())

    def GetSpanDays(self,tflag):

        if self.AST:
            bd = ast.calc_AST(self.bd,self.L)
        else:
            bd = self.bd
    
        if tflag:
            dt1 = self.bjq
            dt2 = bd
        else:
            dt1 = bd
            dt2 = self.fjq

        days = (dt2-dt1).days
        minutes = ((dt2-dt1).seconds)/60

        deltaH = ((minutes%60)*2)%24
        deltaD = (minutes/60)*5 + ((minutes%60)*2)/24
        deltaM = (days%3)*4 + deltaD/30
        deltaD %= 30
        deltaY = (days/3) + deltaM/12
        deltaM %= 12

        return (deltaY,deltaM,deltaD,deltaH)

    def GetJiaoYunDate(self):
        days = self.qyspan[0]*365.2422 + self.qyspan[1]*30.44 + self.qyspan[2]
        hours = self.qyspan[3]
        deltadate =  datetime.timedelta(days=days,hours=hours)
        try:
            JYdate = self.bd + deltadate
        except OverflowError:
            JYdate = datetime.datetime(1,1,1)
            return JYdate
        else:
            return JYdate
        
    def Paipan(self):
        
        if self.AST:
            bd = ast.calc_AST(self.bd,self.L)
        else:
            bd = self.bd

        Y = bd.year
        M = bd.month
        D = bd.day
        h = bd.hour
        m = bd.minute

        Nianzhu = ((Y - bazi.BaseYear) + 37)%60

        if self.lifa:
            mindx,self.bjq,self.fjq = self.Get_PQ_SolarTerm()
        else:
            mindx,self.bjq,self.fjq = self.Get_DQ_SolarTerm()

        YFlag = 0
        if mindx <= 0:
            YFlag = 1
            mindx += 12
        if YFlag == 1:
            Nianzhu += 59
            Nianzhu %= 60

        Yuezhu = (((Nianzhu%5)*12)+(mindx-1)+2)%60

        self.bazi[0] = Nianzhu%10
        self.bazi[1] = Nianzhu%12
        self.bazi[2] = Yuezhu%10
        self.bazi[3] = Yuezhu%12

        offset = self.SolarDaysFromBaseYear(bd)
        Rizhu = (offset+3)%60
        time = h/2
        Dflag = 0
        if h%2 == 1:
            time += 1
        if time == 12:
            Dflag = 1
            time = 0
        if Dflag == 1:
            Rizhu += 1
            Rizhu %= 60

        Shizhu = (Rizhu%5)*12+time

        self.bazi[4] = Rizhu%10
        self.bazi[5] = Rizhu%12
        self.bazi[6] = Shizhu%10
        self.bazi[7] = Shizhu%12

        j = self.bazi[4]
        if j%2 == 0:
            for i in range(10):
                self.shishen[j] = i
                j += 1
                j %= 10
        else:
            for k in range(0,9,2):
                self.shishen[j] = k
                self.shishen[j-1] = k+1
                j += 2
                j %= 10
        self.shishen.append(10)

        self.qyspan = self.GetSpanDays((self.bazi[0]%2)^(self.isFemale))
        self.jydt = self.GetJiaoYunDate()

        

    
    def Get8zi(self):
        output = []
        opt = "%s:%s%s %s%s %s%s %s%s" %(bazi.Gender[self.isFemale],bazi.Tiangan[self.bazi[0]],\
                                         bazi.Dizhi[self.bazi[1]],bazi.Tiangan[self.bazi[2]],\
                                         bazi.Dizhi[self.bazi[3]],bazi.Tiangan[self.bazi[4]],\
                                         bazi.Dizhi[self.bazi[5]],bazi.Tiangan[self.bazi[6]],\
                                         bazi.Dizhi[self.bazi[7]])
        output.append(opt)

        if ((self.bazi[0]%2)^(self.isFemale)):
            offsets = [9,11]
        else:
            offsets = [1,1]
            
        opt = "大运:"
        j = self.bazi[2]
        k = self.bazi[3]
        for i in range(8):
            j += offsets[0]
            j %= 10
            k += offsets[1]
            k %= 12
            opt += "%s%s " %(bazi.Tiangan[j],bazi.Dizhi[k])
        output.append(opt)
        jydt = self.jydt		
        output.append("  %s年%s月%s日交运" %(jydt.year,jydt.month,jydt.day))
        
        return "   ".join(output)

    def GetMeridiem(self,hour,minute):
        
        hm = hour*100 + minute     
        if (hm < 600):
            return "凌晨"
        elif (hm < 900):
            return "早上"
        elif (hm < 1130):
            return "上午"
        elif (hm < 1230):
            return "中午"
        elif (hm < 1800):
            return "下午"
        else:
            return "晚上"


    def print_mst(self):
        bd = self.bd
        md = self.GetMeridiem(bd.hour,bd.minute)
        tmp = bd.hour
        if bd.hour >= 13:
            tmp = bd.hour-12
        st = datetime.time(bd.hour, bd.minute).strftime('%M')
        return "%s年%s月%s日 %s%s点%s" %(bd.year,bd.month,bd.day,md,tmp,st)

    def print_lunar(self):
        
        bd = self.bd
        h = bd.hour
        time = h/2
        DFlag = 0
        if h%2 == 1:
            time += 1
        if time == 12:
            DFlag = 1
            time = 0
        if DFlag == 1:
            dt = datetime.timedelta(days=1)
            try:
                bd += dt
            except OverflowError:
                bd = datetime.datetime(1,1,1)
                return ""

        l_y,l_m,l_d,isLeap = self.Solar2Lunar(bd)
        
        ytmp = ((l_y - bazi.BaseYear) + 37)%60
        x = ytmp%12
        y = ytmp/12

        leapstr = ""
        if isLeap:
            leapstr = "闰"

        return "%s%s年%s%s月%s %s时" %(bazi.ShizhuList[x][y],bazi.Shengxiao[x],leapstr, 
                                      bazi.LunarMonthTerms[l_m],bazi.LunarDayTerms[l_d], 
                                      bazi.Dizhi[time])

    def render_ast(self):
        output = []
        opt = "<p>出生地经度 %s&deg; </p>" %(self.L)
        output.append(opt)
        
        bd = ast.calc_AST(self.bd,self.L)
        bdlst = bd.isoformat().split("T")
        dt = bdlst[0].split("-")
        tt = bdlst[1].split(":")
        dt.append(tt[0])
        dt.append(tt[1])
        opt = "<p>生日&#91;出生地真太阳时&#93;  %s年%s月%s日 %s时%s分  </p>" %tuple(dt)
        output.append(opt)

        return mark_safe("\n".join(output))

    def print_age(self):
        return "今年虚岁%d" %((datetime.datetime.now().year-self.bd.year + 1))

    def print_lifa(self):
        if self.lifa >= 1:
            return "依据 %s 数据拟合 " %(bazi.lifalst[self.lifa-1])
        else:
            return "未选择平气历法"

    def render_solarterms(self):
        output = []
        if self.AST:
            aststr = "&#91;出生地真太阳时&#93;"
        else:
            aststr = ""
            
        opt = "<p>%s%s   " %(bazi.Jieqi[self.bazi[3]], aststr)
        output.append(opt)
        
        bflist = self.bjq.isoformat().split("T")
        dt = bflist[0].split("-")
        tt = bflist[1].split(":")
        dt.append(tt[0])
        dt.append(tt[1])
        opt = " %s年%s月%s日 %s时%s分  </p>" %tuple(dt)
        output.append(opt)

        opt = "<p>%s%s  " %(bazi.Jieqi[self.bazi[3]+1],aststr)
        output.append(opt)
        
        fflist = self.fjq.isoformat().split("T")
        dt = fflist[0].split("-")
        tt = fflist[1].split(":")
        dt.append(tt[0])
        dt.append(tt[1])
        opt = " %s年%s月%s日 %s时%s分 </p>" %tuple(dt)
        output.append(opt)
        
        return mark_safe('\n'.join(output))


    def render_bazi(self):
        row_rets = ["<br/>","<br/>","<br/><br/>","<br/>","<br/>",""]
        htmsp1 = "&nbsp"
        htmsp3 = "&nbsp;&nbsp;&nbsp"
        htmsp4 = "&nbsp;&nbsp;&nbsp;&nbsp"
        output = ['<td>']
        output.append('%s %s %s' %(htmsp1,htmsp3,row_rets[0]))
        output.append('%s %s %s' %(bazi.Gender[self.isFemale],htmsp3,row_rets[1]))
        output.append('%s %s %s' %(htmsp1,htmsp1,row_rets[2]))
        output.append('%s %s %s' %("藏干",htmsp4,row_rets[3]))
        output.append('%s %s %s' %(htmsp1,htmsp3,row_rets[4]))
        output.append('%s %s %s' %(htmsp1,htmsp3,row_rets[5]))
        output.append('</td>')
        
        for i in range(4):
            output.append('<td>')
            j = i+i
            p = j+1
            if i == 2:
                output.append('%s %s %s %s' %(htmsp1,"日元",htmsp4,row_rets[0]))
            else:
            	output.append('%s %s %s %s' %(htmsp1,bazi.Shishen[self.shishen[self.bazi[j]]],htmsp4,row_rets[0]))
            output.append('%s %s %s %s' %(htmsp3,bazi.Tiangan[self.bazi[j]],htmsp3,row_rets[1]))
            output.append('%s %s %s %s' %(htmsp3,bazi.Dizhi[self.bazi[p]],htmsp3,row_rets[2]))
            for q in range(3):
                k = bazi.Canggan[self.bazi[p]][q]
                opt = "%s %s"  %(bazi.Tiangan[k],bazi.Shishen[self.shishen[k]])
                output.append('%s %s %s %s' %(htmsp1,opt,htmsp4,row_rets[q+3]))
            output.append('</td>')

        return mark_safe('\n'.join(output))
    
    
    
    def render_dayun(self):
        
        row_rets = ["<br/>","<br/><br/>","<br/><br/>","<br/>","<br/>","<br/>","<br/>",
                    "<br/><br/>","<br/>","<br/>","<br/>","<br/>","<br/><br/>",""]
        htmsp1 = "&nbsp"
        htmsp3 = "&nbsp;&nbsp;&nbsp"
        output = []

        if ((self.bazi[0]%2)^(self.isFemale)):
            offsets = [9,11]
        else:
            offsets = [1,1]

        qyspan = self.qyspan
        jydt = self.jydt
        output.append('<p>命主于出生后%d年%d个月%d天%d小时后起运</p>' %(qyspan[0],qyspan[1],qyspan[2],qyspan[3]))
        output.append('<p>命主于公历%d年%d月%d日%d时交运</p><br/>' %(jydt.year,jydt.month,jydt.day,jydt.hour))
            
            
        j = self.bazi[2]
        k = self.bazi[3]
        s = self.bazi[2]
        now = datetime.datetime.now()

        output.append('<td>')
        #output.append('%s %s %s' %(htmsp1,htmsp3,row_rets[0]))
        output.append('%s %s' %("大运",row_rets[1]))
        output.append('%s %s' %("起于",row_rets[2]))
        output.append('%s %s' %("流年",row_rets[3]))
        output.append('%s %s' %(htmsp1,row_rets[4]))
        output.append('%s %s' %(htmsp1,row_rets[5]))
        output.append('%s %s' %(htmsp1,row_rets[6]))
        output.append('%s %s' %(htmsp1,row_rets[7]))
        output.append('%s %s' %(htmsp1,row_rets[8]))
        output.append('%s %s' %(htmsp1,row_rets[9]))
        output.append('%s %s' %(htmsp1,row_rets[10]))
        output.append('%s %s' %(htmsp1,row_rets[11]))
        output.append('%s %s' %(htmsp1,row_rets[12]))
        output.append('%s %s' %("止于",row_rets[13]))
        output.append('</td>')
        
        tmp = jydt.year
        for i in range(8):
            output.append('<td>')
            #s += offsets[0]
            #s %= 10
            #opt = "%s" %(Shishen[self.shishen[s]])
            #output.append('%s %s %s' %(opt,htmsp3,row_rets[0]))
                
            j += offsets[0]
            j %= 10
            k += offsets[1]
            k %= 12
            #if now.year < tmp or now.year > (tmp + 9):
            try:
                fdt = jydt.replace(year=tmp+10)
                
            except ValueError:
                jydt = jydt.replace(month=3,day=1)
                fdt = jydt.replace(year=tmp+10)
   
            if now < jydt.replace(year=tmp) or now >= fdt :
                opt = "%s%s" %(bazi.Tiangan[j],bazi.Dizhi[k])
                output.append('%s %s %s' %(htmsp3,opt,row_rets[1]))
            else:
                opt = "<i class=\"fa fa-play\"></i>&nbsp;%s%s" %(bazi.Tiangan[j],bazi.Dizhi[k])
                output.append('%s %s' %(opt,row_rets[1]))
                
            opt = "%d" %(tmp)
            output.append('%s %s %s' %(htmsp3,opt,row_rets[2]))

            p = (tmp+6)%10
            q = (tmp+8)%12

            for n in range(10):
                if (now.year - tmp) != n:
                    opt = "%s%s" %(bazi.Tiangan[p],bazi.Dizhi[q])
                    output.append('%s %s %s' %(htmsp3,opt,row_rets[n+3]))
                else:
                    opt = "<i class=\"fa fa-play\"></i>&nbsp;%s%s" %(bazi.Tiangan[p],bazi.Dizhi[q])
                    output.append('%s %s' %(opt,row_rets[n+3]))
                  
                p += 1
                p %= 10
                q += 1
                q %= 12

            tmp += 9
            opt = "%d" %(tmp)
            output.append('%s %s %s' %(htmsp3,opt,row_rets[13]))
            output.append('</td>')
            tmp += 1

        return mark_safe('\n'.join(output))



'''
xjpdt = datetime.datetime(1953,6,15,2,30)
xjpbz = bazi(xjpdt,1,1,108,9)
xjpbz.Paipan()
print xjpbz.Solar2Lunar(xjpdt)
'''

