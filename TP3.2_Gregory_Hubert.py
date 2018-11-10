from tkinter import *
from random import *
from math import *
from threading import *
import time

colors = ['red','blue','green']
h = 400
l = 400


class main(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.fenetre = Tk()
        self.score = 0
        self.pause = 1
        self.t = 0
        self.scoring = Label(self.fenetre, text = 'Score {}'.format(self.score))
        self.scoring.pack()
        self.t_temps = Label(self.fenetre, text = 'Temps {}'.format(self.t))
        self.t_temps.pack()
        self.canvas = Canvas(self.fenetre, width = h, height = l, bg = 'black')
        self.canvas.pack()
        self.ajout = Button(self.fenetre, text = '+', command = self.ajout)
        self.ajout.pack(side = LEFT)
        self.effacer = Button(self.fenetre, text = '-', command = self.effacer)
        self.effacer.pack(side = RIGHT)
        self.p = Button(self.fenetre, text = 'Pause', command = self.pau)
        self.p.pack(side = TOP)
        self.s = Button(self.fenetre, text = 'Start', command = self.star)

    def run(self):
        pass

    def ajout(self):
        rayon = randint(10,30)
        x = randint(rayon, h-rayon)
        y = randint(rayon, l-rayon)
        color = choice(colors)
        rond = self.canvas.create_oval(x,y,x+rayon,y+rayon, fill = color)
        boule(rond,self.canvas,self.fenetre,x,y,color)
        self.pause = 1
        self.star()

    def effacer(self):
        if boule.ronds != []:
            lcanvas = self.canvas.find_all()
            self.canvas.delete(lcanvas[len(lcanvas)-1])
            boule.ronds.pop(len(boule.ronds)-1)

    def pau(self):
            if self.pause:
                for i in boule.ronds:
                    boule.stop(i)
                    self.pause = 0
                    self.p.pack_forget()
                    self.s.pack(side = TOP)
    def star(self):
        for i in boule.ronds:
            while i.dx == 0 and i.dy == 0:
                i.dx=randint(-5,5)
                i.dy=randint(-5,5)
            self.canvas.move(i.rond,i.dx,i.dy)
            i.x += i.dx
            i.y += i.dy
            if(i.x>h or i.x<0):
                i.dx=-i.dx
            if(i.y>l or i.y<0):
                i.dy=-i.dy
            self.pause = 1
            self.s.pack_forget()
            self.p.pack(side = TOP)


class boule():
    ronds = list()

    def __init__(self,rond,canvas,fenetre,x,y,color = choice(colors)):
        boule.ronds.append(self)
        self.fenetre=fenetre
        self.canvas=canvas
        self.rond = rond
        self.rayon=randint(10,20)
        self.x=x
        self.y=y
        self.dx=randint(-5,5)
        self.dy=randint(-5,5)
        while self.dx == 0 and self.dy == 0:
            self.dx=randint(-5,5)
            self.dy=randint(-5,5)
        self.move()

    def collision(self, other, fenetre):
        if (self.x+self.rayon>other.x-other.rayon and self.x-self.rayon<other.x+other.rayon and self.y+self.rayon>other.y-other.rayon and self.y-self.rayon<other.y+other.rayon ):
            fenetre.score += 1
            fenetre.scoring['text'] = ('Score: {}'.format(fenetre.score))
            self.canvas.delete(self.fenetre,self.rond)
            boule.ronds.remove(self)
            self.canvas.delete(self.fenetre,other.rond)
            boule.ronds.remove(other)

    def move(self):
        self.canvas.move(self.rond,self.dx,self.dy)
        self.x += self.dx
        self.y += self.dy
        if(self.x>h or self.x<0):
            self.dx=-self.dx
        if(self.y>l or self.y<0):
            self.dy=-self.dy
        self.fenetre.after(10,self.move)

    def stop(self):
        self.dx = 0
        self.dy = 0

class chrono():
    def __init__(self,t,fenetre):
        self.t = t
        self.fenetre = fenetre
        self.affiche()

    def affiche(self):
        if f.pause:
            f.t_temps['text'] = ('Temps: {}'.format(self.t))
            self.t += 1
            self.fenetre.after(1000, self.affiche)
        if f.pause == 0:
            self.t = self.t
            self.fenetre.after(1000, self.affiche)


class calcul(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.pause = True
        self.t = 0

    def run(self):
        while 1:
            if self.pause:
                for i in boule.ronds:
                    for j in boule.ronds:
                        if j != i:
                            i.collision(j,f)
            time.sleep(0.01)

f = main()
f.start()
c = chrono(f.t,f.fenetre)
calcul_f = calcul()
calcul_f.start()
f.fenetre.mainloop()
