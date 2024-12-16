import mido

# from mir.windowing import *
from decimal import Decimal
from backend.audio.mir.windowing import Windowing

class Audio:

    # ===== Atribut ===== #
    beats   : list[Windowing]
    size    : int
    step    : int

    # ===== Method ===== #
    def __init__(self, file:str, size:int=None, step:int=6) -> None:
        '''Membuat objek Audio, membaca dari file MIDI'''
        # declare
        self.step = step
        self.beats = []
        
        # baca file MIDI
        beat = self.readMIDI(file)

        # menentukan size
        if size == None:
            self.size = self.findWindowingSize(beat)
        else:
            self.size = size
        
        # windowing
        for i in range(0, len(beat), step):
            if i + self.size <= len(beat):
                self.beats.append(Windowing(stream=beat, size=self.size, start=i))


    def readMIDI(self, file:str) -> list[int]:
        '''Membaca file MIDI dan mengekstrak notenya'''
        # declare
        beat = []
        midi = mido.MidiFile(file)
        # mengambil note_on pada channel utama
        for track in midi.tracks:
            for msg in track :
                if msg.type=="note_on" and msg.channel==0:
                    beat.append(msg.note)
        # output
        return beat
    

    def compare(self, other, tuning:list[int], cli:bool) -> Decimal:
        if cli: print("Memulai melakukan komparasi.")
        if isinstance(other, Audio):
            if self.size != other.size:
                raise ValueError("Hanya bisa komparasi similaritas audio dengan windowing size yang sama.")

            else:
                # algorithm
                tabelKomparasi = []
                mostSimilar = Decimal(0)
                # mostSimilarRow = 0
                # mostSimilarCol = 0
                for i in range(len(self.beats)):
                    row = []
                    for j in range(len(other.beats)):
                        # print(f"[-] compare window{i} -> window{j}")
                        row.append(self.beats[i].compare(other.beats[j], tuning))
                        if mostSimilar < row[-1]:
                            mostSimilar = row[-1]
                            # mostSimilarRow = i
                            # mostSimilarCol = j
                    tabelKomparasi.append(row)
                # terbentuk matriks yang merupakan tabel hasil komparasi
                # matriks tersebut seharusnya menggambarkan bahwa hasil komparasi tinggi saling membentuk diagonal

                # validasi hasil similaritas
                # ini nanti dulu, lihat nanti
                return mostSimilar
        
        else:
            raise TypeError("Hanya bisa komparasi similaritas dengan sesama audio.")


    def findWindowingSize(self, beat:list) -> int:
        '''Mencari ukuran terbaik per segmennya untuk windowing'''
        if len(beat) >= 40:
            size = 40
        elif len(beat) >= 20:
            size = len(beat)
        else:
            raise ValueError("Audio uji terlalu singkat!\nAudio uji yang terlalu singkat lebih membutuhkan banyak resource dan komputasi yang berat.")
        # output
        return size