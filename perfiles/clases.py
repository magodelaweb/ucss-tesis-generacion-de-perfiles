from perfiles.models import Operacion, Cliente, Evento
import configparser
import itertools

class Test:
    def __init__(self, clientes, eventos, operaciones):
        self.clientes=clientes
        self.eventos=eventos
        self.operaciones=operaciones

class Funciones_Cubo:

    def __init__(self, perfiles):
        self.perfiles=perfiles

    def traerCubos(self):
        for perfil in self.perfiles:
            for cliente in perfil["clientes"]:
                vCliente=Cliente_Cubo(cliente["id"])
                cubo=vCliente.getCubo()
                perfil["cubos"].extend(list([cubo]))
        return self.perfiles

    def actualizarPerfiles(self,nPerfiles):
        self.perfiles=nPerfiles

    def calcularEtiquetas(self):
        for perfil in self.perfiles:
            cubos = perfil["cubos"]
            etiquetas=self.generaEtiquetas(cubos)
            listObj=[]
            for etq in etiquetas:
                lsEtiqueta=etq.split("-")
                obj={
                    "etq":lsEtiqueta[0],
                    "pres":lsEtiqueta[1]
                }
                listObj.append(obj);
            perfil["etiquetas"]=listObj
        return self.perfiles

    def generaEtiquetas(self,cubos):
        config = configparser.ConfigParser()
        config.read('perfiles/config.ini')
        precision= float(config['CLUSTER']['PRECISION'])
        etiquetas=[]

        sEdad=set([])
        sTiposLista=set([])
        sDiscotecas=set([])
        sDistritos=set([])

        listaEdades=[(lambda cubo: cubo["edad"])(cubo) for cubo in cubos]
        listaTiposLista=[(lambda cubo: ','.join(cubo["tiposLista"]))(cubo) for cubo in cubos]
        listaDiscotecas=[(lambda cubo: [(lambda disco: disco)(disco) for disco in cubo["discotecas"]])(cubo) for cubo in cubos]
        listaDiscotecas=list(itertools.chain.from_iterable(listaDiscotecas))
        listaDistritos=[(lambda cubo: ','.join(cubo["distritos"]))(cubo) for cubo in cubos]

        nCli=len(listaEdades)
        for cubo in cubos:

            rEdad = listaEdades.count(cubo["edad"])
            for tl in cubo["tiposLista"]:
                rTiposLista = listaTiposLista.count(tl)
                f_tl=rTiposLista/nCli
                mTiposLista=(f_tl)>precision
                if mTiposLista:
                    pe=self.precision_etiqueta(f_tl)
                    tTiposLista=set(["Tipo de lista "+tl+"-"+pe])
                    sTiposLista |= tTiposLista
            for disc in cubo["discotecas"]:
                rDiscotecas = listaDiscotecas.count(disc)
                f_disc=rDiscotecas/nCli
                mDiscotecas=(f_disc)>precision
                if mDiscotecas:
                    pe=self.precision_etiqueta(f_disc)
                    tDiscotecas=set(["Discoteca "+disc+"-"+pe])
                    sDiscotecas |= tDiscotecas
            for dist in cubo["distritos"]:
                rDistritos = listaDistritos.count(dist)
                f_dist=rDistritos/nCli
                mDistritos=(f_dist)>precision
                if mDistritos:
                    pe=self.precision_etiqueta(f_dist)
                    tDistritos=set(["Distrito "+dist+"-"+pe])
                    sDistritos |= tDistritos

            f_edad=rEdad/nCli
            mEdad=(f_edad)>precision
            if mEdad:
                pe=self.precision_etiqueta(f_edad)
                tEdad=set([str(cubo["edad"])+" años"+"-"+pe])
                sEdad |= tEdad

        etiquetas.extend(list(sEdad))
        etiquetas.extend(list(sTiposLista))
        etiquetas.extend(list(sDiscotecas))
        etiquetas.extend(list(sDistritos))

        return etiquetas
    def precision_etiqueta(self, f):
        f=round(f,2)*100
        p=str(f)+"%"
        return p

class Cliente_Cubo:
    def __init__(self, id):
        self.idCliente=id
        self.edad=0
        self.tiposLista=[]
        self.discotecas=[]
        self.distritos=[]
    def getCubo(self):
        operaciones = (Operacion.objects.
                       filter(cliente_id=self.idCliente).
                       select_related().
                       values("id","cliente__edad","evento__tipoLista",
                               "evento__discoteca","evento__distrito")
                      )
        self.edad=operaciones[0]["cliente__edad"]
        stiposLista=set([])
        sdiscotecas=set([])
        sdistritos=set([])
        for o in operaciones:
            tiposLista=o["evento__tipoLista"]
            ttiposLista=set([tiposLista])
            stiposLista |= ttiposLista

            discotecas=o["evento__discoteca"]
            tdiscotecas=set([discotecas])
            sdiscotecas |= tdiscotecas

            distritos=o["evento__distrito"]
            tdistritos=set([distritos])
            sdistritos |= tdistritos

        #resp=Test("null","null",operaciones)
        self.tiposLista=list(stiposLista)
        self.discotecas=list(sdiscotecas)
        self.distritos=list(sdistritos)
        resp={
            "idCliente":self.idCliente,
            "edad":self.edad,
            "tiposLista":self.tiposLista,
            "discotecas":self.discotecas,
            "distritos":self.distritos,
        }
        return resp
