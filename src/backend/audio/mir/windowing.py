import numpy as np

#from mir.vector import *
from backend.audio.mir.vector import Vector
from decimal import Decimal
class Windowing:
    
    # ===== Atribut ===== #
    notes   : list[int] # isi note-note pitch melody dalam bentuk integer
    size    : int       # jumlah note tiap window

    # ===== Method ===== #
    def __init__(self, stream:list, size:int, start:int) -> None:
        '''Membuat objek Window'''
        self.size = size
        self.notes = stream[start : (start + size)]
        self.normalizeNotes()


    def normalizeNotes(self) -> None:
        '''Melakukan normalisasi note-note melodi pada Window'''
        for note in self.notes:
            note = (note - np.average(self.notes)) / np.std(self.notes)

    
    def vektorATB(self) -> Vector:
        '''Menghasilkan histogram ATB untuk sebuah Window'''        
        # declare
        hist = [i for i in range(0, 128)]
        sum = 0
        # algorithm
        for bin in range(0, 128):
            hist[bin] = self.notes.count(bin)
            sum += hist[bin]
        # normalize
        for i in range(0, 128):
            hist[i] /= sum
        # output
        return Vector([Decimal(i) for i in hist])


    def vektorRTB(self) -> Vector:
        '''Menghasilkan histogram RTB untuk sebuah Window'''        
        # declare
        hist = [0 for i in range(-127, 128)]
        sum = 0
        # algorithm
        for i in range(1, self.size):
            hist[self.notes[i]-self.notes[i-1]+127] += 1
            sum += 1
        # normalize
        for i in range(-127, 128):
            hist[i] /= sum
        # output        
        return Vector([Decimal(i) for i in hist])


    def vektorFTB(self) -> Vector:
        '''Menghasilkan histogram FTB untuk sebuah Window'''        
        # declare
        hist = [0 for i in range(-127, 128)]
        sum = 0
        # algorithm
        for i in range(self.size):
            hist[self.notes[i]-self.notes[0]+127] += 1
            sum += 1
        # normalize
        for i in range(-127, 128):
            hist[i] /= sum
        # output
        return Vector([Decimal(i) for i in hist])
    

    def compare(self, other, tuning:list[int]):
        '''Mencari similaritas antar dua window berdasarkan 3 jenis vektor: ATB, RTB, FTB'''
        if isinstance(other, Windowing):
            if self.size != other.size:
                raise ValueError("Hanya bisa komparasi dua window dengan size yang sama")
            
            else:
                # deklarasi
                vektor1 = None
                vektor2 = None
                atb = Decimal(0)
                rtb = Decimal(0)
                ftb = Decimal(0)
                
                # mencari similaritas dari vektor atb
                vektor1 = self.vektorATB()
                vektor2 = other.vektorATB()
                atb = vektor1.cosineSimilarity(vektor2)
                
                # mencari similaritas dari vektor rtb
                vektor1 = self.vektorRTB()
                vektor2 = other.vektorRTB()
                rtb = vektor1.cosineSimilarity(vektor2)
                
                # mencari similaritas dari vektor ftb
                vektor1 = self.vektorFTB()
                vektor2 = other.vektorFTB()
                ftb = vektor1.cosineSimilarity(vektor2)

                # pembobotan hasil
                # tuning = [bobotATB, bobotRTB, bobotFTB] dengan total bobot 100
                return Decimal(atb*tuning[0] + rtb*tuning[1] + ftb*tuning[2]) / 100
                
        else:
            raise TypeError("Hanya bisa komparasi sesama window.")