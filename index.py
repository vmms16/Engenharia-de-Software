print "Content-Type: text/html\n"
print "<html>"
print "<body>"
print "<h1>Lamina Liquida para Irrigacao</h1>"

from google.appengine.ext import db

import os
def qs(x):
    if os.environ['QUERY_STRING']:
        for t in os.environ['QUERY_STRING'].split("&"):
            if t.split("=")[0]==x:return t.split("=")[1]
    return ''

import cgi
POST=cgi.FieldStorage()
def pv(x):
    if(POST.getvalue(x)):return POST.getvalue(x)
    return ''

def calculo(x):
	x.ll=float(x.f)*float(x.z)*((float(x.cc)-float(x.pmp))*float(x.densidade)/10)

class Medicao(db.Model):
	cod=db.StringProperty(default='')
	cc=db.StringProperty(default='')
	pmp=db.StringProperty(default='')
	densidade=db.StringProperty(default='')
	f=db.StringProperty(default='')
	z=db.StringProperty(default='')
	ll=db.StringProperty(default='')

if pv('cod'):
    if qs('id'):
        reg=db.get(qs('id'))
        reg.cod=pv('cod')
        reg.cc=pv('cc')
	reg.pmp=pv('pmp')
	reg.densidade=pv('densidade')
	reg.f=pv('f')
	reg.z=pv('z')
	reg.ll=pv('ll')
        reg.put()
    else:
	Medicao(cod=pv('cod'),cc=pv('cc'),pmp=pv('pmp'),densidade=pv('densidade'),f=pv('f'),z=pv('z'),ll=pv('ll')).put()

if qs('del'):
	db.delete(qs('del'))
if (pv('cod')or qs('del')):
	print "<a href=index.py>voltar pra listagem</a>"
else:
	print "<table border=1>";
	print "<tr><td colspan=3>Dados das Areas Cadastrados</td></tr>";
	print "<tr><td>Codigo</td><td>CC(%)</td><td>PMP(%)</td><td>Densidade(g/cm3)</td><td>f(0-1)</td><td>Z(cm)</td><td>Lamina Liquida(mm)</td></tr>"
	for reg in Medicao.all().order('cod'):
		x=float(reg.f)*float(reg.z)*((float(reg.cc)-float(reg.pmp))*float(reg.densidade)/10)
    		print "<tr><td>"+str(reg.cod)+"</td><td>"+str(reg.cc)+"</td><td>"+str(reg.pmp)+"</td><td>"+str(reg.densidade)+"</td><td>"+str(reg.f)+"</td><td>"+str(reg.z)+"</td><td>"+str(x)+"<td><input type=button value=Alterar onclick=\"location.href='index.py?id="+str(reg.key())+"';\"> <input type=button value=Excluir onclick=\"if(confirm('Tem Certeza ?'))location.href='index.py?del="+str(reg.key())+"';\"></td></tr>"
	print "</table>";

if (qs('cal') and not pv('cod')) :
	reg=db.get(qs('cal'))
	x=str(float(reg.cod)+float(reg.cc))
	print "<hr><form action=index.py?cal="+qs('cal')+" method=post>"
	print "<input type=submit name=ll value='"+str(x)+"' onclick=\"location.href='index.py';\"><br>"
	

if (qs('id') and not pv('cod')):
	reg=db.get(qs('id'))
	print "<hr><form action=index.py?id="+qs('id')+" method=post>"
    	print "Codigo <input name=cod value='"+str(reg.cod)+"'><br>"
	print "Capacidade de Campo (%) <input name=cc value='"+str(reg.cc)+"'><br>"
	print "Ponto de Murcha Permanente (%) <input name=pmp value='"+str(reg.pmp)+"'><br>"
	print "Densidade (g/cm3) <input name=densidade value='"+str(reg.densidade)+"'><br>"
	print "Coeficiente de Disponibilidade (0-1) <input name=f value='"+str(reg.f)+"'><br>"
    	print "Profundidade Efetiva do Sistema Raticular (cm) <input name=z value='"+str(reg.z)+"'><br>"
    	print "<input type=submit value=Salvar> <input type=button value=Novo onclick=\"location.href='index.py';\">"
else:
    	print "<hr><form method=post>"
    	print "Codigo <input name=cod value=0><br>"
	print "Capacidade de Campo(%) <input name=cc value=0><br>"
	print "Ponto de Murcha Permanente(%) <input name=pmp value=0><br>"
	print "Densidade (g/cm3) <input name=densidade value=0><br>"
	print "Coeficiente de Disponibilidade(0-1) <input name=f value=0><br>"
	print "Profundidade efetiva do sistema Raticular (cm) <input name=z value=0><br>"
    	print "<input type=submit value=Salvar>"

	

print "</form><hr>"
print "</body>"
print "</html>"
