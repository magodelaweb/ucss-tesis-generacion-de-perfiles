from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from perfiles.models import Operacion, Cliente
from perfiles.clases import Cliente_Cubo, Funciones_Cubo
import configparser
#from pprint import pprint
#import json
#from django.core import serializers
#from django.http import JsonResponse

# Create your views here.
def perfiles(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('perfiles/perfiles.html')
    operaciones=len(getOperaciones())
    clientes=len(getClientes())
    context = {
        'menu':0,
        'clientes':clientes,
        'operaciones':operaciones,
        #'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
def ver(request):
    config = configparser.ConfigParser()
    config.read('perfiles/config.ini')
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('perfiles/ver.html')
    perfiles=generarPerfiles()
    clientes=getClientes()
    listPrev = relacionar(perfiles,clientes)
    list=etiquetado(listPrev)
    #itemTest= test.__dict__
    #data = serializers.serialize('json', itemTest)
    #data = vars(vTest)
    context = {
        'menu':1,
        'perfiles':list,
        'precision':float(config['CLUSTER']['PRECISION'])*100
        #'test':vTest
        #'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))



def print_r(the_object):
    print ("CLASS: ", the_object.__class__.__name__, " (BASE CLASS: ", the_object.__class__.__bases__,")")
    pprint(vars(the_object))

def etiquetado(perfiles):
    vPerfil=Funciones_Cubo(perfiles)
    nPerfil=vPerfil.traerCubos()
    vPerfil.actualizarPerfiles(nPerfil)
    resp=vPerfil.calcularEtiquetas()
    return resp

def relacionar(perfiles,clientes):
    list=[]
    for i in range(0,len(perfiles)):
        listCli=[]
        for j in range(0,len(perfiles[i])):
            cli=clientes.filter(id=perfiles[i][j]).values('nombre','id')[0]
            nomCli=cli['nombre'].split()[0]
            idCli=cli['id']
            listCli.append({"nombre":nomCli, "id":idCli})
        obj={"perfil":i+1,"clientes":listCli, "cubos":[], "etiquetas":[]}
        list.append(obj)
    return list

def getOperaciones():
    operaciones=Operacion.objects.all()
    return operaciones
def getClientes():
    clientes=Cliente.objects.all()
    return clientes

def modelar(data):
    config = configparser.ConfigParser()
    config.read('perfiles/config.ini')
    ldata=list(data.values('cliente_id'))

    s=set([])
    for registro in ldata:
        idCli= registro['cliente_id']
        t=set([idCli])
        s |= t
    lset=list(s)
    n=len(lset)
    dataAgrupada=[0 for x in range(0,n)]
    cont=0
    for id in lset:
        operaciones=data.filter(cliente_id=id)
        dataAgrupada[cont]={"perfil":id,"operaciones":list(operaciones)}
        cont=cont+1

    simil = [ [0 for columna in range(0,n+1)] for fila in range (0,n)]
    for i in range(0,n):
        for j in range(0,n):
            id_operaciones_i=lset[i]
            id_operaciones_j=lset[j]
            if i==j:
                simil[i][j]=1
                simil[i][n]=id_operaciones_i
            else:
                valorSimilaridad=0
                operaciones_i=data.filter(cliente_id=id_operaciones_i)
                operaciones_j=data.filter(cliente_id=id_operaciones_j)
                for p in range(0,len(operaciones_i)):
                    for q in range(0,len(operaciones_j)):
                        l= int(config['DEFAULT']['COL'])
                        sum_simil=0
                        edad_i = operaciones_i.values('cliente__edad')[p]['cliente__edad']
                        edad_j = operaciones_j.values('cliente__edad')[q]['cliente__edad']
                        sum_simil=sum_simil+((1/l) if edad_i==edad_j else 0)
                        distrito_i = operaciones_i.values('evento__distrito')[p]['evento__distrito']
                        distrito_j = operaciones_j.values('evento__distrito')[q]['evento__distrito']
                        sum_simil=sum_simil+((1/l) if distrito_i==distrito_j else 0)
                        discoteca_i = operaciones_i.values('evento__discoteca')[p]['evento__discoteca']
                        discoteca_j = operaciones_j.values('evento__discoteca')[q]['evento__discoteca']
                        sum_simil=sum_simil+((1/l) if discoteca_i==discoteca_j else 0)
                        tipoLista_i = operaciones_i.values('evento__tipoLista')[p]['evento__tipoLista']
                        tipoLista_j = operaciones_j.values('evento__tipoLista')[q]['evento__tipoLista']
                        sum_simil=sum_simil+((1/l) if tipoLista_i==tipoLista_j else 0)
                        if valorSimilaridad<sum_simil:
                            valorSimilaridad=sum_simil
                simil[i][j]=valorSimilaridad
    return simil

def corregir(simil):
    config = configparser.ConfigParser()
    config.read('perfiles/config.ini')
    n= len(simil)
    l= int(config['DEFAULT']['COL'])
    distancia = [ [0 for columna in range(0,n+1)] for fila in range (0,n)]
    for i in range(0,n):
        for j in range(0,n+1):
            vs=simil[i][j]
            if j!=n:
                distancia[i][j]=int(abs(1.0-vs)*l)
            else:
                distancia[i][j]=vs
    return distancia

def particionar(distancia,i):
    #test=9;
    config = configparser.ConfigParser()
    config.read('perfiles/config.ini')
    min= int(config['DEFAULT']['MIN_GRAFO'])
    clusteres1=[]
    clusteres0=[]
    clusteres2=[]
    clusteresParticionados=[]
    nRegistros=len(distancia)-1
    if nRegistros%2==0:
        #test #test="{0}: {1}".format(1,nRegistros)
        clusteres1=Bisecar(distancia,nRegistros/2)
        clusteres0=Bisecar(distancia,nRegistros/2-1)
        clusteres2=Bisecar(distancia,nRegistros/2+1)
    else:
        clusteres1=Bisecar(distancia,(nRegistros-1)/2)
        clusteres0=Bisecar(distancia,(nRegistros-1)/2-1)
        clusteres2=Bisecar(distancia,(nRegistros-1)/2+1)
    clusteres=ElegirEquilibrado(clusteres1,clusteres0,clusteres2)
    if clusteres!=False:
        if len(clusteres[0])>=min:
            clusteresParticionados=particionar(clusteres[0],i+1)
        else:
            clusteresParticionados=clusteres[0]
        if len(clusteres[1])>=min:
            clusteresParticionados.extend(particionar(clusteres[1],i+1))
        else:
            clusteresParticionados.extend(clusteres[1])
    else:
        clusteresParticionados=[distancia]
    return clusteresParticionados

def Bisecar(distancia,corte):
    corte=int(corte)
    grafo=[0,0]
    n=len(distancia)-1
    if (n<2) or (corte==1) or (corte==n) or (corte==0):
        return False
    else:
        grafo[0]=distancia[0:int(corte)]
        grafo[1]=distancia[int(corte):n+1]
        if len(grafo[0])==0:
            return False
        if len(grafo[1])==0:
            return False
    return grafo

def ElegirEquilibrado(clusteres1,clusteres0,clusteres2):
    if (clusteres0==False) and (clusteres1==False) and (clusteres2==False):
        return False
    e1=HallarEquilibrio(clusteres1)
    e0=HallarEquilibrio(clusteres0)
    e2=HallarEquilibrio(clusteres2)
    if e0==False:
        e0=99999;
    if e1==False:
        e1=99999;
    if e2==False:
        e2=99999;
    menor=min(e1, e0, e2)
    if e1==menor:
        return clusteres1
    elif e0==menor:
        return clusteres0
    elif e2==menor:
        return clusteres2
    else:
        return False

def HallarEquilibrio(clusteres):
    if (not clusteres):
        return False
    w1=HallarTrabajo(clusteres[0])
    w2=HallarTrabajo(clusteres[1])
    c1=HallarCosto(clusteres[0])
    c2=HallarCosto(clusteres[1])
    e=CalculaEquilibrio(w1,w2,c1,c2)
    return e

def CalculaEquilibrio(w1,w2,c1,c2):
    e = abs(1 - ((w1 * c2 + 0.5) / (w2 * c1 + 0.5)) *  (abs(w2-w1) + 0.9) *  (abs(c2-c1) + 0.1))
    return e

def HallarTrabajo(cluster):
    n=len(cluster)
    c=len(cluster[0])-1
    suma=0
    for i in range(0,n):
        for j in range(0,c):
            suma=suma+cluster[i][j]
    return suma

def HallarCosto(cluster):
    n=len(cluster)
    c=len(cluster[0])-1
    suma=0
    for i in range(0,n):
        for j in range(0,c):
            if j>i:
                suma=suma+cluster[i][j]
    return suma

def limpiar(grafo):
    grafo_limpio=[]
    flag=0
    for subgrafo in grafo:
        if type(subgrafo[0]) is list:
            grafo_limpio.extend(limpiar(subgrafo))
        else:
            grafo_limpio.append(subgrafo) #[len(subgrafo)-1]
            flag=1
    if flag==1:
        return [grafo_limpio]
    return grafo_limpio

def fusionar(grafo):
    repetir=True
    romper=False
    seg=0
    while repetir:
        seg=seg+1
        nGrafos=len(grafo)
        for i in range(0,nGrafos):
            for j in range(0,nGrafos):
                if i==j:
                    continue
                bEvaluaIR=EvaluaIR(grafo[i],grafo[j])
                if bEvaluaIR:
                    bEvaluaCR=EvaluaCR(grafo[i],grafo[j])
                    if bEvaluaCR:
                        grafo[i]=grafo[i]+grafo[j]
                        grafo.pop(j)
                        romper=True
                        break
            if romper:
                romper=False
                break
        if i==nGrafos-1:
            repetir=False
        if seg>20:
            break
    return grafo

def EvaluaIR(grafo1,grafo2):
    config = configparser.ConfigParser()
    config.read('perfiles/config.ini')
    TRI= float(config['DEFAULT']['TRI'])
    nV1=len(grafo1)
    nV2=len(grafo2)
    ECij = 0
    ECCi = 0
    ECCj = 0
    for i in range(0,nV1):
        for j in range(0,nV2):
            nCliente1=grafo1[i][len(grafo1[i])-1]
            nCliente2=grafo2[j][len(grafo2[j])-1]
            ECij = ECij + grafo1[i][nCliente2]
            nCampos=len(grafo1[i])-1;
            for k in range(0,nCampos):
                if k==nCliente1:
                    ECCi = ECCi-grafo1[i][k]/(nV1*nV2)
                elif k==nCliente2:
                    ECCj = ECCj-grafo2[j][k]/(nV1*nV2)
                else:
                    ECCi = ECCi + (grafo1[i][k])/(nV1*nV2)
                    ECCj = ECCj + (grafo2[j][k])/(nV1*nV2)
    if ECij==0:
        ECij=1
    if ECCi==0:
        ECCi=1
    if ECCj==0:
        ECCj=1
    RI = 1 - (ECij/( ECCi + ECCj))/2
    RI = abs(RI)
    return RI>=TRI

def EvaluaCR(grafo1,grafo2):
    config = configparser.ConfigParser()
    config.read('perfiles/config.ini')
    TRC= float(config['DEFAULT']['TRC'])
    nV1=len(grafo1)
    nV2=len(grafo2)
    SECij = 0
    SECCi = 0
    SECCj = 0
    for i in range(0,nV1):
        for j in range(0,nV2):
            nCliente1=grafo1[i][len(grafo1[i])-1]
            nCliente2=grafo2[j][len(grafo2[j])-1]
            SECij = SECij + grafo1[i][nCliente2]/(nV1*nV2)
            nCampos=len(grafo1[i])-1;
            for k in range(0,nCampos):
                if k==nCliente1:
                    SECCi = SECCi+grafo1[i][k]/(nV1*nV2)
                elif k==nCliente2:
                    SECCj = SECCj+grafo2[j][k]/(nV1*nV2)
    if SECij==0:
        SECij=1
    if SECCi==0:
        SECCi=1
    if SECCj==0:
        SECCj=1
    RC = SECij/( (SECCi/(SECCi+SECCj))*SECCi + (SECCj/(SECCi+SECCj))*SECCj)
    RC = abs(RC)
    return True

def perfilCliente(grafoFusionado):
    nPerfiles=len(grafoFusionado)
    for i in range(0,nPerfiles):
        nV=len(grafoFusionado[i])
        for j in range(0,nV):
            nC=len(grafoFusionado[i][j])-1
            grafoFusionado[i][j]=grafoFusionado[i][j][nC]
    return grafoFusionado

def generarPerfiles():
    data=getOperaciones()
    simil=modelar(data)
    distancia=corregir(simil)
    particionado=particionar(distancia,0)
    grafo=limpiar(particionado)
    grafoFusionado=fusionar(grafo)
    grafoPerfilCliente=perfilCliente(grafoFusionado)
    return grafoPerfilCliente
