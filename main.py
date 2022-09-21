from kivy.properties import  ObjectProperty
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import platform
import csv
import datetime
import os
import io

class MultiButton(Button):
    pass
class MenuButton(MultiButton):
    pass
class Ueberschriften(BoxLayout):
    pass

class MenuZeile(FloatLayout):
    pass

class Zeile(BoxLayout):
    def aenderName(self,name):
        self.ids.name.vorname = name[0]
        self.ids.name.nachname = name[1]
    def getNamen(self):
        return [self.ids.name.vorname,self.ids.name.nachname]
    pass

class HaTrNaAbschr(BoxLayout):
#Diese Klasse erzeugt ein Widget, in dem vergessen Hausaufgaben (Ha)
#geschickt zum Trainingsraum, Nacharbeiten und Abschreiben
#dokumentiert wird.
    schuelerDaten = []
    schuelerWidget=[]
    tage=[]
    klasse=''
    def werteSchuelerEintraegeAus(self,zeile):
    #return {'Ha':3,'Tr':3,'Na':3,'Abschr':1}
    #Diese Funktion wertet die bekommen und erledigten Abschreibe, Trainingsraumeinheiten aus.
        if len(zeile)<3:
            return {'Ha':0, 'Tr':0,'Na':0,'Abschr':0}
        werte=[x.split('-') for x in zeile[2:]]
        ha=''.join([y for x in werte for y in x if 'Ha' in y ]).replace('m','-').replace('p','+').replace('Ha','1')
        tr=''.join([y for x in werte for y in x if 'Tr' in y ]).replace('m','-').replace('p','+').replace('Tr','1')
        na=''.join([y for x in werte for y in x if 'Na' in y ]).replace('m','-').replace('p','+').replace('Na','1')
        abschr=''.join([y for x in werte for y in x if 'Abschr' in y ]).replace('m','-').replace('p','+').replace('Abschr','1')
        werte={'Ha':eval(ha if len(ha)>0 else '0') , 'Tr':eval(tr if len(tr)>0 else '0'),'Na':eval(na if len(na)>0 else '0'),'Abschr':eval(abschr if len(abschr)>0 else '0')}
        return werte
    def fuegeWertEinUndStelleSieDar(self, instance):
        # Erstelle für jeden Schüler einen Datensatz der Form
        # daten=['vorname','nachname','mHa-pTr','mAschr-mTr',...] usw.
        heute=datetime.date.today().strftime("%Y.%m.%d")
        id=str(self.get_id(instance.parent))
        wert=('m' if instance.text=='-' else 'p')+ id
        schuelerNr=[i for i in range(len(self.schuelerDaten)) if self.schuelerDaten[i][0:2]==self.get_namen(instance.parent)][0]
        if len(self.tage)==0 or not self.tage[-1]==heute:
            self.tage.append(heute)
            self.schuelerDaten[schuelerNr].append(wert)
        elif len(self.schuelerDaten[schuelerNr])==2:
            self.schuelerDaten[schuelerNr].append(wert)
        else:
            self.schuelerDaten[schuelerNr][-1]=self.schuelerDaten[schuelerNr][-1]+'-'+wert
        werte=self.werteSchuelerEintraegeAus(self.schuelerDaten[schuelerNr])
        instance.parent.ids.ausgabe.text=str(werte[id])
    def get_id(self,  instance):
        for id, widget in instance.parent.ids.items():
            if widget.__self__ == instance:
                return id
    def get_namen(self,  instance):
        return [instance.parent.ids.name.nachname,instance.parent.ids.name.vorname]
    def leseConfigDatei(self):
        app=App.get_running_app()
        self.klasse=(app.configDatei.split('_')[1]).split('.')[0]
        with open(app.configDatei) as csvfile:
            s = csv.reader(csvfile, delimiter=',')
            for i, l in enumerate(s):
                if l[0]=='Klasse':
                    if len(l)>2:
                        self.tage=l[2:]
                else:
                    self.schuelerDaten.append(l)
    def schreibeConfigDatei(self):
        app=App.get_running_app()
        with open(app.configDatei, mode='w') as csvfile:
            file = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file.writerow(['Klasse',self.klasse]+self.tage)
            for daten in self.schuelerDaten:
                file.writerow(daten)
        self.ueberpruefeInfodatei()
    def ueberpruefeInfodatei(self):
    #Diese Funktion überprüft, ob der Inhalt der Infodatei noch aktuell ist
    #Wenn der Schüler nachgesitzt hat, wird er entfernt. Muss ein Schuler nachsitzen,
    #Wird er hinzugefügt
        app=App.get_running_app()
        inhaltInfo=[]
    #Lese Infodatei
        if os.path.isfile(os.path.join(app.grundpfad,app.infodatei)):
            with open(os.path.join(app.grundpfad,app.infodatei)) as csvfile:
                inhaltInfo = list(csv.reader(csvfile, delimiter=','))
    #Suche Schüler, die Nachsitzen müssen
        schuelerNachsitzen=[]
        for schueler in self.schuelerDaten:
            werte=self.werteSchuelerEintraegeAus(schueler)
            if werte['Na']>2:
                schuelerNachsitzen.append([self.klasse, schueler[1],schueler[0],'Nacharbeiten'])
    #Füge Infodatei dem Array schuelerNachsitzen hinzu
        for i,zeile in enumerate(inhaltInfo):
            if not zeile[0]==self.klasse:
                schuelerNachsitzen.append(zeile)
        with open(os.path.join(app.grundpfad,app.infodatei), mode='w') as csvfile:
            file = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for schueler in schuelerNachsitzen:
                file.writerow(schueler)
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        app=App.get_running_app()
        self.schuelerWidget=[]
        self.klasse = (app.configDatei.split('_')[1]).split('.')[0]
        self.orientation='vertical'
        self.schuelerDaten=[]
        self.leseConfigDatei()
        self.add_widget(Label(text=self.klasse,font_size=app.schriftgroesse))
        self.add_widget(Ueberschriften())
        vornamen=[]
        for schueler in self.schuelerDaten:
            self.schuelerWidget.append(Zeile())
            self.schuelerWidget[-1].aenderName([schueler[1],schueler[0]])
            vornamen.append(self.schuelerWidget[-1].getNamen()[1])
#Sortiere die Eintraege nach dem Vornamen
        for i in [ii[0] for ii in sorted(enumerate(vornamen), key=lambda x:x[1])]:
            self.add_widget(self.schuelerWidget[i])
            werte = self.werteSchuelerEintraegeAus(self.schuelerDaten[i])
            for id in ['Ha','Tr','Na','Abschr']:
                exec("self.schuelerWidget[i].ids."+id+".ids.ausgabe.text=str(werte['"+id+"'])")
        self.add_widget(MenuZeile())

class StelleMenueDar(Widget):
    def __init__(self):
        super().__init__()
        root=BoxLayout()
        root.orientation='vertical'
        app=App.get_running_app()
        l=Label(text='Übersicht',font_size=app.schriftgroesse,size_hint=[None,None],size=[app.breite, 2*app.schriftgroesse])
        root.add_widget(l)
        g=GridLayout(rows= 3,cols= 5,padding= 20,spacing= 20)
        bten=[]
        for i,file in enumerate(app.configDateien):
            klasse=(file.split('_')[1]).split('.')[0]
            bten.append(MenuButton(text=klasse))
            g.add_widget(bten[-1])
        root.add_widget(g)
        root.pos=[0,app.hoehe-self.size[1]]
        self.add_widget(root)
        exit=MultiButton(text='Exit')
        exit.pos=[0,0]
        exit.bind(on_press=lambda  x:app.stop())
        self.add_widget(exit)
        infobox=BoxLayout(orientation='vertical')
        infobox.pos=[0,exit.size[1]+infobox.size[1]]
        if os.path.isfile(os.path.join(app.grundpfad,app.infodatei)):
            with open(os.path.join(app.grundpfad,app.infodatei)) as csvfile:
                s = csv.reader(csvfile, delimiter=',')
                for zeile in s:
                    if len(zeile)>1:
                        infobox.add_widget(Label(text=zeile[0]+': '+' '.join(zeile[1:]),font_size=app.schriftgroesse))
                    else:
                        infobox.add_widget(
                            Label(text=str(zeile), font_size=app.schriftgroesse))
        infobox.pos=[0,exit.size[1]]
        infobox.center_x=app.breite/2
        self.add_widget(infobox)

class mainApp(App):
    breite=Window.size[0]
    hoehe=Window.size[1]
#Bei 800 Pixel, Schriftgröße 20, bei 1080 Pixel Schriftgröße 35. Dazwischen lineare interpolieren
#Die Felder sind Breit: Name: 5*SG, Vier Zaehler: 4*3.5*2*SG
#  -->   Breite=6*SG+4*3.5*2*SG=(5+28)*SG
#  -->
    schriftgroesse=int(breite/33)
    grundpfad='.' if platform != 'android' else os.path.join(os.getenv('EXTERNAL_STORAGE'),'sitzplanNoten')
    configDatei=''
    infodatei='infoDateiListeAusrutcher.csv'
    configDateien=[x for x in os.listdir(grundpfad) if x.startswith('ListeAusrutscher')]
    aktuell=None
    root=None
    def entferneSitzplanLadeMenu(self):
        self.root.remove_widget(self.aktuell)
        self.aktuell=StelleMenueDar()
        self.root.add_widget(self.aktuell)
    def entferneMenuLadeSitzplan(self,klasse):
        self.configDatei=os.path.join(self.grundpfad,[x for x in self.configDateien if (x.split('_')[1]).split('.')[0]==klasse][0])
        self.root.remove_widget(self.aktuell)
        self.aktuell=HaTrNaAbschr()
        self.root.add_widget(self.aktuell)
    def build(self):
        self.configDatei=self.configDateien[0]
        self.root=BoxLayout()
        self.aktuell=StelleMenueDar()
        self.root.add_widget(self.aktuell)
        return self.root
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mainApp().run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
