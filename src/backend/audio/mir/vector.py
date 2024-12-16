from decimal import Decimal

class Vector:
    
    # ===== Atribut ===== #
    values      : list[Decimal] # besar vektor

    # ===== Methods ===== #
    def __init__(self, values:list[Decimal]):
        '''Inisiasi objek Vector'''
        self.values = values
    
    
    def dot(self, other):
        if isinstance(other, Vector):
            if len(self.values) != len(other.values):
                raise ValueError("Hanya dapat dilakukan pada vektor dengan dimensi yang sama.")
        
            else:
                # algorithm
                hasil = Decimal(0)
                for i in range(len(self.values)):
                    hasil += Decimal(self.values[i] * other.values[i])
                # output
                return hasil
        
        else:
            raise TypeError("Hanya dapat dilakukan pada sesama vektor.")


    def norm(self) -> Decimal:
        '''Mencari panjang vektor'''
        hasil = Decimal(0)
        for value in self.values:
            hasil += Decimal(value**2)
        return hasil.sqrt()


    def cosineSimilarity(self, other) -> Decimal:
        if isinstance(other, Vector):
            if len(self.values) != len(other.values):
                raise ValueError("Hanya dapat dilakukan pada vektor dengan dimensi yang sama.")
        
            else:
                return self.dot(other) / (self.norm() * other.norm())
        
        else:
            raise TypeError("Hanya dapat dilakukan pada sesama vektor.")