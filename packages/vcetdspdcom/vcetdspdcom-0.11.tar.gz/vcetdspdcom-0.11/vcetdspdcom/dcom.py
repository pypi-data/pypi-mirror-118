import random
import math as mt
import numpy as np
def ask_modulation(fs,fc,tb,sim_t):
    sb=tb*fs
    x=[random.randint(0,1) for i in range(int(sim_t/tb))]
    print('Transmitted bits=',x)
    m=[]
    for i in range(len(x)):
        if x[i]==0:
            m.append(([0]*int(sb)))
        else:
            m.append(([1]*int(sb)))
    t=[i for i in np.arange(0,sim_t,1/fs)]
    c=[np.cos(2*np.pi*fc*i) for i in np.arange(0,sim_t,1/fs)]
    m=np.array(m)
    m=m.reshape(-1,)
    c=np.array(c)
    y=m*c 
    y_output=y
    m_message=m
    c_carrier=c
    t_time=t
    return y_output,m_message,c_carrier,t_time
def ask_demodulation(y_output,fs,c_carrier,tb):
    y=y_output
    c=c_carrier
    sb=tb*fs
    xt=y*c
    ys=[0]*len(xt)
    rec=[0]*int(len(y)/sb)
    k=0
    for i in range(0,len(y),int(sb)):
        ys[i]=np.sum(xt[i:i+int(sb)])
        rec[k]=ys[i]
        k=k+1   
    threshold= int(sb/2)-(0.1*sb) 
    rec1=np.zeros((len(xt),))
    k=0
    for i in range(int(len(y)/sb)):
        if rec[i]>threshold:
            rec[i]=1
            rec1[k:k+int(sb)]=1
            k=k+int(sb)
        else:
            rec[i]=0
            rec1[k:k+int(sb)]=0
            k=k+int(sb)
    return rec1,rec
def psk_modulation(fs,fc,tb,sim_t):
    sb=tb*fs
    x=[random.randint(0,1) for i in range(int(sim_t/tb))]
    print('Transmitted bits=',x)
    m=[]
    for i in range(len(x)):
        if x[i]==0:
            m.append(([-1]*int(sb)))
        else:
            m.append(([1]*int(sb)))
    t=[i for i in np.arange(0,sim_t,1/fs)]
    c=[np.cos(2*np.pi*fc*i) for i in np.arange(0,sim_t,1/fs)]
    m=np.array(m)
    m=m.reshape(-1,)
    c=np.array(c)
    y=m*c
    y_output=y
    m_message=m
    c_carrier=c
    t_time=t
    return y_output,m_message,c_carrier,t_time
def psk_demodulation(y_output,fs,c_carrier,tb):
    #coherent detection
    y=y_output
    c=c_carrier
    sb=tb*fs
    xt=y*c
    ys=[0]*len(xt)
    rec=[0]*int(len(y)/sb)
    k=0
    for i in range(0,len(y),int(sb)):
        ys[i]=np.sum(xt[i:i+int(sb)])
        rec[k]=ys[i]
        k=k+1
    #print(rec)     
    threshold= 0
    #print(threshold)
    rec1=np.zeros((len(xt),))
    k=0
    for i in range(int(len(y)/sb)):
        if rec[i]>threshold:
            rec[i]=1
            rec1[k:k+int(sb)]=1
            k=k+int(sb)
        else:
            rec[i]=0
            rec1[k:k+int(sb)]=-1
            k=k+int(sb)
    return rec1,rec
def fsk_modulation(fs,fc1,fc2,tb,sim_t):
    sb=tb*fs
    x=[random.randint(0,1) for i in range(int(sim_t/tb))]
    print('Transmitted bits=',x)
    m1=[]
    m2=[]
    for i in range(len(x)):
        if x[i]==0:
            m1.append(([0]*int(sb)))
            m2.append(([1]*int(sb)))
        else:
            m1.append(([1]*int(sb)))
            m2.append(([0]*int(sb)))
    t=[i for i in np.arange(0,sim_t,1/fs)]
    c1=[np.cos(2*np.pi*fc1*i) for i in np.arange(0,sim_t,1/fs)]
    c2=[np.cos(2*np.pi*fc2*i) for i in np.arange(0,sim_t,1/fs)]
    m1=np.array(m1)
    m2=np.array(m2)
    m1=m1.reshape(-1,)
    m2=m2.reshape(-1,)
    c1=np.array(c1)
    c2=np.array(c2)
    y=m1*c1+m2*c2
    y_output=y
    m_message=m1
    c_carrier1=c1
    c_carrier2=c2
    t_time=t
    return y_output,m_message,c_carrier1,c_carrier2,t_time
def fsk_demodulation(y_output,fs,c_carrier1,c_carrier2,tb):
    y=y_output
    c1=c_carrier1
    c2=c_carrier2
    sb=(fs*tb)
    xt1=y*c1
    xt2=y*c2
    ys1=[0]*len(xt1)
    rec1=[0]*int(len(xt1)/sb)
    ys2=[0]*int(len(xt2))
    rec2=[0]*int(len(xt2)/sb)
    k=0
    for i in range(0,len(xt1),int(sb)):
        ys1[i]=np.sum(xt1[i:i+int(sb)])
        rec1[k]=ys1[i]
        ys2[i]=np.sum(xt2[i:i+int(sb)])
        rec2[k]=ys2[i]
        k=k+1
    rec1=np.array(rec1)
    rec2=np.array(rec2)
    rec=rec1-rec2  
    threshold=np.mean(rec)
    k=0
    for i in range(int(len(y)/sb)):
        if rec[i]>threshold:
            rec[i]=1
        else:
            rec[i]=0
    rec11=np.zeros((len(xt1),))
    k=0
    for i in range(int(len(y)/sb)):
        if rec[i]==1:
            rec11[k:k+int(sb)]=1
            k=k+int(sb)
        else:
            rec11[k:k+int(sb)]=0
            k=k+int(sb)
    return rec11,rec
def dpsk_modulation(fs,fc,tb,sim_t,init_bit):
    sb=tb*fs
    d=init_bit
    d1=init_bit
    b=[random.randint(0,1) for i in range(int(sim_t/tb))]
    print('transmitted bits',b)
    x=[]
    #b=np.array([1,0,1,1,0])
    m1=[]
    for i in range(len(b)):
        if b[i]==0:
            m1.append(([-1]*int(sb)))
        else:
            m1.append(([1]*int(sb)))
    m1=np.array(m1)
    m1=m1.reshape(-1,)

    for i in range(len(b)):
        re= b[i]^d
        re= not re
        x.append(int(re))
        d=re
    print('encoded bits',x)
    m=[]
    if d1==1:
        m.append(([1]*int(sb)))
    else:
        m.append(([-1]*int(sb)))
    for i in range(len(x)):
        if x[i]==0:
            m.append(([-1]*int(sb)))
        else:
            m.append(([1]*int(sb)))
    t1=[i for i in np.arange(0,sim_t+tb,1/fs)]
    c1=[np.cos(2*np.pi*fc*i) for i in np.arange(0,sim_t+tb,1/fs)]
    m=np.array(m)
    m=m.reshape(-1,)
    c1=np.array(c1)
    y=m*c1
    y_output=y
    m_message=m1
    enc_message=m
    c_carrier=c1
    t_time=t1
    return y_output,m_message,enc_message,c_carrier,t_time
def dpsk_demodulation(y_output,fs,tb):
    y=y_output
    sb=(fs*tb)
    y1=np.zeros(len(y)+int(sb))
    for i in range(len(y)):
        y1[i]=y[i]
    y11=np.zeros(len(y)+int(sb))
    for i in range(len(y)):
        y11[i+int(sb)]=y[i]
    re=y1*y11
    re1=re[int(sb):len(re)-int(sb)]
    #####
    ys=[0]*len(re1)
    rec=[0]*int((len(y)/sb)-1)
    k=0
    for i in range(0,len(re1),int(sb)):
        ys[i]=np.sum(re1[i:i+int(sb)])
        rec[k]=ys[i]
        k=k+1   
    threshold= 0
    for i in range(len(rec)):
        if rec[i]>threshold:
            rec[i]=0
        else:
            rec[i]=1
    rec11=np.zeros(len(y),)
    rec1=np.zeros((len(rec)))
    for i in range(len(rec1)):
        rec1[i]=rec[i]
    k=0
    for i in range(len(rec1)):
        if rec1[i]==1:
            rec11[k:k+int(sb)]=1
            k=k+int(sb)
        else:
            rec11[k:k+int(sb)]=-1
            k=k+int(sb)
    return rec11,rec1

def qpsk_modulation(fs,fc,tb,sim_t):
    sb=tb*fs
    x=[random.randint(0,1) for i in range(int(sim_t/tb))]
    if len(x)%2!=0:
        x.append(0)
        sim_t+=tb  
    print('transmitted bits',x)
    msg=[]
    for i in range(len(x)):
        if x[i]==0:
            msg.append(([-1]*int(sb)))
        else:
            msg.append(([1]*int(sb)))
    msg=np.array(msg)
    msg=msg.reshape(-1,)
    ev_bit=[]
    od_bit=[]
    for i in range(0,int(len(x)),2):
        ev_bit.append(x[i])
        od_bit.append(x[i+1])
    print('even bits',ev_bit)
    print('odd bits',od_bit)
    m1=[]
    for i in range(len(ev_bit)):
        if ev_bit[i]==0:
            m1.append(([-1]*int(2*sb)))
        else:
            m1.append(([1]*int(2*sb)))
    m1=np.array(m1)
    m1=m1.reshape(-1,)
    m2=[]
    for i in range(len(od_bit)):
        if od_bit[i]==0:
            m2.append(([-1]*int(2*sb)))
        else:
            m2.append(([1]*int(2*sb)))
    m2=np.array(m2)
    m2=m2.reshape(-1,)
    t1=[i for i in np.arange(0,sim_t,1/fs)]
    c1=[np.cos(2*np.pi*fc*i) for i in np.arange(0,sim_t,1/fs)]
    c2=[np.sin(2*np.pi*fc*i) for i in np.arange(0,sim_t,1/fs)]
    y=m1*c1+m2*c2
    y_output=y
    c_carrier=c1
    t_time=t1
    ev_signal=m1
    od_signal=m2
    return y_output,msg,ev_signal,od_signal,c_carrier,t_time
def qpsk_demodulation(y_output,fs,fc,tb):
    xt=y_output
    sb=fs*tb
    sim_t=len(y_output)/fs
    c1=[np.cos(2*np.pi*fc*i) for i in np.arange(0,sim_t,1/fs)]
    c2=[np.sin(2*np.pi*fc*i) for i in np.arange(0,sim_t,1/fs)]
    yt1=c1*xt
    yt2=c2*xt
    ys1=[0]*len(yt1)
    rec1=[0]*int((sim_t/tb)*0.5)
    k=0
    for i in range(0,len(yt1),int(2*sb)):
        ys1[i]=np.sum(yt1[i:i+int(2*sb)])
        rec1[k]=ys1[i]
        k=k+1
    threshold1=0
    for i in range(len(rec1)):
        if rec1[i]>threshold1:
            rec1[i]=1
        else:
            rec1[i]=0
    ys2=[0]*len(yt2)
    rec2=[0]*int((sim_t/tb)*0.5)
    k=0
    for i in range(0,len(yt2),int(2*sb)):
        ys2[i]=np.sum(yt2[i:i+int(2*sb)])
        rec2[k]=ys2[i]
        k=k+1
    threshold2=0
    for i in range(len(rec2)):
        if rec2[i]>threshold2:
            rec2[i]=1
        else:
            rec2[i]=0
    recd=np.zeros(2*len(rec2))
    for i in range(0,len(recd)-1,2):
        recd[i]=rec1[int(i/2)]
        recd[i+1]=rec2[int(i/2)]
    dmsg=[]
    for i in range(len(recd)):
        if recd[i]==0:
            dmsg.append(([-1]*int(sb)))
        else:
            dmsg.append(([1]*int(sb)))
    dmsg=np.array(dmsg)
    dmsg=dmsg.reshape(-1,)
    return dmsg,recd

def qam_modulation(fs,fc,tb,sim_t):
    sb=tb*fs
    x=[random.randint(0,1) for i in range(int(sim_t/tb))]
    if len(x)%4 != 0:
        re=len(x)%4
        for i in range(4-re):
            x.append(0)
            sim_t+=tb
    print('transmitted bits',x)
    msg=[]
    for i in range(len(x)):
        if x[i]==0:
            msg.append(([-1]*int(sb)))
        else:
            msg.append(([1]*int(sb)))
    msg=np.array(msg)
    msg=msg.reshape(-1,)
    t1=[i for i in np.arange(0,sim_t,1/fs)]
    a=[]
    b=[]
    for i in range(0,len(x)-3,4):
        if x[i]==0 and x[i+1]==0:
            a.append(-0.22)
        elif x[i]==0 and x[i+1]==1:
            a.append(-0.82)
        elif x[i]==1 and x[i+1]==0:
            a.append(0.22)
        elif x[i]==1 and x[i+1]==1:
            a.append(0.82)
        if x[i+2]==0 and x[i+3]==0:
            b.append(-0.22)
        elif x[i+2]==0 and x[i+3]==1:
            b.append(-0.82)
        elif x[i+2]==1 and x[i+3]==0:
            b.append(0.22)
        elif x[i+2]==1 and x[i+3]==1:
            b.append(0.82)
    a=np.array(a)
    b=np.array(b)
    m1=list()
    st=0
    so=sim_t/len(a)
    carrier1=[np.sin((2*np.pi*fc*i)) for i in np.arange(0,sim_t,1/fs)]
    carrier2=[np.cos((2*np.pi*fc*i)) for i in np.arange(0,sim_t,1/fs)]
    for t in range(len(a)):
        c1=[a[t]*np.cos((2*np.pi*fc*i))+ b[t]*np.sin((2*np.pi*fc*i)) for i in np.arange(st,so,1/fs)]
        m1=m1+c1
        st=so
        so+=sim_t/len(a)
    if (len(m1)!=len(t1)):
        tr=min(len(m1),len(t1))
        if len(m1)>len(t1):
            m1=m1[:tr]
        else:
            t1=t1[:tr]
            carrier1=carrier1[:tr]
            carrier2=carrier2[:tr]
            
    m1=np.array(m1)
    m1=m1.reshape(-1,)
    y_output=m1
    m_message=msg
    c_carrier1=carrier1
    c_carrier2=carrier2
    t_time=t1
    return y_output,m_message,c_carrier1,t_time
def qam_demodulation(y_output,fs,fc,tb):
    y=y_output
    sb=fs*tb
    sim_t=len(y_output)/fs
    nb=int(sim_t/tb)
    carrier1=[np.cos(2*np.pi*fc*i) for i in np.arange(0,sim_t,1/fs)]
    carrier2=[np.sin(2*np.pi*fc*i) for i in np.arange(0,sim_t,1/fs)]
    yt1=y*carrier1
    yt2=y*carrier2
    ys1=[0]*len(yt1)
    rec1=[0]*round((sim_t/tb)*0.25)
    k=0
    for i in range(0,len(yt1)-1,int(4*sb)):
        ys1[i]=np.sum(yt1[i:i+int(4*sb)])
        rec1[k]=ys1[i]
        k=k+1
    ys2=[0]*len(yt2)
    rec2=[0]*round((sim_t/tb)*0.25)
    k=0
    for i in range(0,len(yt2)-1,int(4*sb)):
        ys2[i]=np.sum(yt2[i:i+int(4*sb)])
        rec2[k]=ys2[i]
        k=k+1
    rec=np.zeros(2*len(rec1))
    k=0
    for i in range(len(rec1)):
        rec[k]=rec1[i]
        rec[k+1]=rec2[i]
        k+=2
    th=max(abs(rec))
    tl=min(abs(rec))
    th1=abs(th)
    tl1=abs(tl)
    received=np.zeros(2*len(rec))
    k=0
    for i in range(len(rec)):
        if (int(rec[i])<= int(-th1)+10):
            received[k]=0
            received[k+1]=1
        elif (int(rec[i])>= int(-th1)+10) and (int(rec[i])< int(-tl1)+2):
            received[k]=0
            received[k+1]=0
        elif (int(rec[i])>= int(-tl1)+2) and (int(rec[i])< int(tl1)+22):
            received[k]=1
            received[k+1]=0
        elif(int(rec[i])>= int(th1)-10):
            received[k]=1
            received[k+1]=1
        k+=2
    dmsg=[]
    for i in range(len(received)):
        if received[i]==0:
            dmsg.append(([-1]*int(sb)))
        else:
            dmsg.append(([1]*int(sb)))
    dmsg=np.array(dmsg)
    dmsg=dmsg.reshape(-1,)
    return dmsg,received

def tdm_modulation(fs,fc1,fc2,tcb,sim_t):
    sc=fs*tcb
    x=np.zeros(round(sim_t/tcb))
    for i in range(len(x)):
        if i%2==0:
            x[i]=1
        else:
            x[i]=0
    t=[i for i in np.arange(0,sim_t,1/fs)]
    c1=[np.cos(2*np.pi*fc1*i) for i in np.arange(0,sim_t,1/fs)]
    c2=[np.cos(2*np.pi*fc2*i) for i in np.arange(0,sim_t,1/fs)]
    m1=[]
    m2=[]
    for i in range(len(x)):
        if x[i]==1:
            m1.append(([1]*int(sc)))
            m2.append(([0]*int(sc)))
        else:
            m1.append(([0]*int(sc)))
            m2.append(([1]*int(sc)))
    m2=np.array(m2)
    m1=np.array(m1)
    m1=m1.reshape(-1,)
    m2=m2.reshape(-1,)
    y=m1*c1 + m2*c2
    t_time=t
    msg1=c1
    msg2=c2
    control_signal=m1
    y_output=y
    return y_output,msg1,msg2,control_signal,t_time
def tdm_demodulation(y_output,fs,tcb):
    sc=tcb*fs
    sim_t=len(y_output)/fs
    x=np.zeros(round(sim_t/tcb))
    for i in range(len(x)):
        if i%2==0:
            x[i]=1
        else:
            x[i]=0
    m1=[]
    for i in range(int(sim_t/tcb)):
        if x[i]==1:
            m1.append(([1]*int(sc)))
        else:
            m1.append(([0]*int(sc)))
    m1=np.array(m1)
    m1=m1.reshape(-1,)
    control_signal=m1
    control_signal1=np.zeros(len(control_signal))
    for i in range(len(control_signal)):
        if control_signal[i]==0:
            control_signal1[i]=1
        else:
            control_signal1[i]=0
    d1=control_signal*y_output
    d2=control_signal1*y_output
    return d1, d2