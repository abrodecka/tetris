from random import randrange as rand
import pygame
from pygame.locals import *
import sys, os
import numpy as np


if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()
    
    

# Klocki
klocki = [
	[[1, 1, 1],
	 [0, 1, 0]],
	
	[[0, 1, 1],
	 [1, 1, 0]],
	
	[[1, 1, 0],
	 [0, 1, 1]],
	
	[[1, 0, 0],
	 [1, 1, 1]],
	
	[[0, 0, 1],
	 [1, 1, 1]],
	
	[[1, 1, 1, 1]],
	
	[[1, 1],
	 [1, 1]]
]

kolorki = [
(204,  204,   204  ),
(153,  255,   255),
(51,  255,   255),
(0, 204, 204),
(0, 153, 153 ),
(255,  204, 229 ),
(255, 153, 204 ),
(255, 102, 178 ),
(204,  0,  102) ,
(153,  0,  76) 
]

poziomy = ['Cienki Bolek','Średniak', 'Mistrz']
tempo = [1000,600,300]
sciezka = os.path.dirname(os.path.realpath(__file__))
   
   
class Tetris:
   
	
    
	def __init__(self):
		pygame.mixer.init()
		pygame.init()
		pygame.key.set_repeat(250,25)
			
		self.screen = pygame.display.set_mode((324, 396))
		pygame.display.set_caption("Tetris")
		self.klocek_nowy = klocki[rand(len(klocki))]
		
		p1 = np.zeros((22,12), dtype = np.int)
		p2 = np.ones((12,), dtype=np.int)
		plansza  = p1.tolist() + [p2.tolist()] 
	
		self.plansza = plansza 
		self.nowy_klocek()
		self.poziom = 1
		self.punkty = 0
		self.linie = 0
		self.podaj_imie = False
		
		self.start_sound = pygame.mixer.Sound(os.path.join(sciezka, 'jazz.wav'))
		self.end_sound = pygame.mixer.Sound(os.path.join(sciezka, 'koniec.wav'))
					
		
	def sprawdz(self, klocek_1, p_x, p_y):
		for p_y2, wiersz in enumerate(klocek_1):
			for p_x2, wartosc in enumerate(wiersz):
				try:
					if wartosc and self.plansza[ p_y2 + p_y ][ p_x2 + p_x ]:
						return True
				except IndexError:
					return True
		return False
		
				   	
	def nowy_klocek(self):
		self.klocek = self.klocek_nowy[:]
		self.klocek_nowy = klocki[rand(len(klocki))]
		self.klocek_x = int(6 - len(self.klocek[0])/2)
		self.klocek_y = 0
		
		if self.sprawdz(self.klocek, self.klocek_x, self.klocek_y):
			self.gameover = True
	
	def poloz_klocek(self):
		for p_y2, wiersz in enumerate(self.klocek):
			for p_x2, wartosc in enumerate(wiersz):
				self.plansza[p_y2+self.klocek_y-1][p_x2+self.klocek_x] += wartosc
		n_sound = pygame.mixer.Sound(os.path.join(sciezka, 'point.wav'))
		n_sound .set_volume(0.2)
		n_sound.play()
							
		
	def usun_wiersz(self, wiersz, cols):
		nowa_plansza = self.plansza
		del nowa_plansza[wiersz]
		nowa_plansza = [np.zeros(cols, dtype = int).tolist()] + nowa_plansza
		self.plansza = nowa_plansza	

		
		
	def napis(self, msg, x, y, rozmiar):
		self.default_font = pygame.font.SysFont('Arial', rozmiar)
		self.screen.blit(self.default_font.render(msg,False,(255,255,255)),(x,y))

		
	def obroc(self):
		if not self.gameover and self.gramy:
			nowy_klocek = np.rot90(self.klocek, 1).tolist()
			if not self.sprawdz(nowy_klocek, self.klocek_x, self.klocek_y):	
				self.klocek = nowy_klocek	
	
	
	def rysuj_klocek(self, matrix, p_x, p_y):
		
		for y in range(0,4):
			kk = np.rot90(matrix,y).tolist()
			if kk in klocki: kolor = kolorki[klocki.index(kk)+1]
			
		for y, row in enumerate(matrix):
			for x, i in enumerate(row):
				if i:
					pygame.draw.rect(self.screen,kolor, pygame.Rect((p_x+x) * 18, (p_y+y) * 18, 18, 18),0)
		
	def rysuj_pole(self, matrix, p_x, p_y):
		kolor = kolorki[0]
			
		for y, row in enumerate(matrix):
			for x, i in enumerate(row):
				if i:
					pygame.draw.rect(self.screen,kolor, pygame.Rect((p_x+x) * 18, (p_y+y) * 18, 18, 18),0)
		
	def zmien_x(self, przesuniecie_x):
		if not self.gameover and self.gramy:
			nowy_x = self.klocek_x + przesuniecie_x
			if nowy_x < 0:
				nowy_x = 0
			if nowy_x > 12 - len(self.klocek[0]):
				nowy_x = 12 - len(self.klocek[0])
			if not self.sprawdz(self.klocek, nowy_x, self.klocek_y):
				self.klocek_x = nowy_x
				


	def zatrzymaj(self):
		self.gramy = not self.gramy				
			
			
	def nowa_gra(self):
		if self.gameover:
			
			p1 = np.zeros((22,12), dtype = np.int)
			p2 = np.ones((12,), dtype=np.int)
			plansza  = p1.tolist() + [p2.tolist()]
			
			self.plansza = plansza 
			self.nowy_klocek()
			self.poziom = 1
			self.punkty = 0
			self.linie = 0
			pygame.time.set_timer(pygame.USEREVENT+1, self.szybkosc)
			self.gameover = False		
		self.poczatek = False	
		self.start_sound.stop()
		self.end_sound.stop()
				     
        
	def licz_punkty(self, n):
		self.linie += n
		self.punkty += 50 * self.poziom * n
		if self.linie >= self.poziom*2:
			poziom_sound = pygame.mixer.Sound(os.path.join(sciezka, 'poziom.wav'))
			poziom_sound.set_volume(1)
			poziom_sound.play()
			self.poziom += 1
			opoznienie = self.szybkosc-50*(self.poziom-1) 
			if opoznienie < 50: opoznienie = 50
			pygame.time.set_timer(pygame.USEREVENT+1,opoznienie)
		
		
	def zmien_y(self):
		if not self.gameover and self.gramy:

			
			self.klocek_y += 1
			if self.sprawdz(self.klocek, self.klocek_x, self.klocek_y):
				self.poloz_klocek()
				self.nowy_klocek()
				zaliczone_wiersze = 0
				while True: #sprawdzamy czy nie mamy pelnego wiersza
					for i, wiersz in enumerate(self.plansza[:-1]):
						if 0 not in wiersz:
							self.usun_wiersz(i,12 )
							zaliczone_wiersze += 1
							level_sound = pygame.mixer.Sound(os.path.join(sciezka, 'level.wav'))
							level_sound.set_volume(100)
							level_sound.play()
							break
					else:
						break
					
				self.licz_punkty(zaliczone_wiersze)	
			
	def rysuj_menu(self, poz):
		pygame.draw.rect(self.screen, (153,0,76), Rect((100, 58 + poz * 23),(110, 18)))
		self.poziomy = poziomy
		self.napis('Wybierz poziom!', 100, 30, 22)
				
		for i in range(len(poziomy)):
			self.napis(poziomy[i], 105, 60 + i * 20, 18)
				
		pygame.display.update()
				
				
	def powitanie(self, imie):
		self.screen.fill((51,51,51))
		self.napis('Podaj imię! :) ', 100, 30, 22)
		pygame.draw.rect(self.screen, (153,0,76), Rect((100, 58),(90, 25)))
		self.napis(imie, 102, 60, 22)
		image = pygame.image.load(os.path.join(sciezka,'tetris.jpg'))
		self.screen.blit(image, (0, 180))
		pygame.display.flip()
		
				
	def graj(self):
		
		clock = pygame.time.Clock()
		self.gameover = False
		self.gramy = True
		self.poczatek = True
		poz = 0
		imie = ''
		self.podaj_imie = False
		
		while 1:
			self.screen.fill((51,51,51))
					
							
			if self.poczatek:
				
				self.start_sound.play()
				image = pygame.image.load(os.path.join(sciezka,'tetris.jpg'))
				self.screen.blit(image, (0, 180))
				
				
				for event in pygame.event.get():
			
					if event.type == pygame.KEYDOWN:
							if event.key == K_s:
								self.screen.fill((51,51,51))
								pygame.display.update()
								self.nowa_gra()
							if event.key == K_DOWN:
								poz = (poz + 1)%3	
							if event.key == K_UP:
								poz = (poz + 2)%3
							if event.key == K_RETURN:
								self.screen.fill((51,51,51))
								pygame.display.update()
								self.poczatek = False
								self.podaj_imie = True
								
						
					elif event.type == QUIT:
						pygame.display.quit()
						sys.exit()		
							
				
				self.rysuj_menu(poz)
			
			elif self.podaj_imie:
				
				 for event in pygame.event.get():
					 if event.type == KEYDOWN:
						 if event.unicode.isalpha():
							 imie += event.unicode
						 if event.key == K_BACKSPACE:
							 imie = imie[:-1]
						 if event.key == K_SPACE:
							 self.podaj_imie = False
							 self.szybkosc = tempo[poz]
							 pygame.time.set_timer(pygame.USEREVENT+1, self.szybkosc)
							 self.nowa_gra()

					 elif event.type == QUIT:
						 pygame.display.quit()
						 sys.exit()
										
				 self.powitanie(imie)

				
				
			elif self.podaj_imie == False:
				
		
				if self.gameover:
				
	
					self.end_sound.play()
					self.screen.fill((51,51,51))
					self.napis("Koniec gry! ", 234,252, 16)
					self.napis("Naciśnij 's' ", 234,267, 16)
					self.rysuj_pole(self.plansza, 0,0) 
								
					if event.type == pygame.KEYDOWN:
							if event.key == eval("pygame.K_" + 's'):		
								self.nowa_gra()
								
			
				pygame.draw.line(self.screen,(0,0,0),(217, 0), (217, 395))
				self.napis("Następny:", 234,2, 16)
			
				self.napis("Wynik: " , 234,127, 16)
				self.napis(str(self.punkty), 234,142, 16)
				self.napis("Etap:", 234,172, 16)
				self.napis(str(self.poziom), 234,187, 16)
				self.napis("Poziom: " , 234,87, 16)
				self.napis(self.poziomy[poz], 234,102, 16)
				self.napis("Gracz: " , 234,210, 16)
				self.napis(imie, 234,225, 16)
				
				self.rysuj_pole(self.plansza, 0,0) # rysuje pole
				self.rysuj_klocek(self.klocek, self.klocek_x, self.klocek_y) #rysuje klocek na gorze
				self.rysuj_klocek(self.klocek_nowy,13,2) #rysuje nastepny klocek
			
			
				pygame.display.update()
			
			
			
				for event in pygame.event.get():
					if event.type == pygame.USEREVENT+1: #samorzutne spadanie 
						self.zmien_y()

					if event.type == pygame.KEYDOWN:
							if event.key == K_UP: self.obroc()
							if event.key == K_LEFT: self.zmien_x(-1)
							if event.key == K_RIGHT: self.zmien_x(1)
							if event.key == K_DOWN: self.zmien_y()
							if event.key == K_p: self.zatrzymaj()
							if event.key == K_s: self.nowa_gra()
	
					elif event.type == QUIT:
						pygame.display.quit()
						sys.exit()
							
							
			clock.tick(30)





 ## uruchomienie gry:       
if __name__ == '__main__':
	import sys
	

	tetris = Tetris()
	tetris.graj()


