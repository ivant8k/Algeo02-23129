import os
from mir.audio import *
from utility.input import *

def audioMain(fileTestName:str) -> dict[str,Decimal]:
    '''Main Function untuk mencari similaritas audio'''
    
    # Path ke folder yang ingin diakses
    folderDataset = "./data/dataset/"
    folderTest = "./data/test/"
    fileTest = fileTestName

    # Menyimpan similarity values
    similarityKeys = []
    similarityItems = []
    similarity = {}
    tuningValues = [20, 40, 40]
    # tuningValues = [40, 30, 30]

    # Buka file audio uji
    audioTest = Audio(folderTest+fileTest)
    windowSize = audioTest.size
    windowStep = audioTest.step

    # Sederhanakan audioTest
    temp = audioTest.beats[len(audioTest.beats)//2+1]
    audioTest.beats = [temp]
    
    # Iterasi setiap file dalam folder dataset
    for fileDataset in os.listdir(folderDataset):
        # Buka file audio dataset
        audioDataset = Audio(folderDataset+fileDataset, windowSize, windowStep)

        # Mencari similaritas
        similarityValue = audioTest.compare(audioDataset, tuningValues, False)
        if similarityItems == []:
            similarityKeys.append(fileDataset)
            similarityItems.append(similarityValue)
        else:
            i = 0
            while i < len(similarityKeys):
                if similarityItems[i] <= similarityValue:
                    similarityKeys.insert(i, fileDataset)
                    similarityItems.insert(i, similarityValue)
                    break
                elif i == len(similarityItems)-1:
                    similarityKeys.append(fileDataset)
                    similarityItems.append(similarityValue)
                    break
                i += 1

    # Ranking
    similarity = {i:j for i,j in zip(similarityKeys, similarityItems)}

    # output
    return similarity

def audioMainCLI():
    '''Main Procedure untuk mencari similaritas audio dengan I/O pada CLI'''
    os.system('cls')

    # Path ke folder yang ingin diakses
    folderDataset = "./data/dataset/"
    folderTest = "./data/test/"
    fileTest = input("\nMasukkan nama file: ")

    # Menyimpan similarity values
    similarityKeys = []
    similarityItems = []
    similarity = {}
    tuningValues = [20, 40, 40]
    # tuningValues = [40, 30, 30]

    # Buka file audio uji
    print("\nMelakukan proses audio uji.")
    audioTest = Audio(folderTest+fileTest)
    windowSize = audioTest.size
    windowStep = audioTest.step

    print("Proses audio uji berhasil.")
    print(f"# size  : {windowSize}")
    print(f"# step  : {windowStep}")
    print(f"# count : {len(audioTest.beats)}")

    # Sederhanakan audioTest
    temp = audioTest.beats[len(audioTest.beats)//2+1]
    audioTest.beats = [temp]
    print("Audio uji disederhanakan dengan diambil 1 window saja.")

    # Iterasi setiap file dalam folder dataset
    for fileDataset in os.listdir(folderDataset):
        # Buka file audio dataset
        print(f"\nMelakukan proses audio dataset: {fileDataset}")
        audioDataset = Audio(folderDataset+fileDataset, windowSize, windowStep)
        print(f"# count : {len(audioDataset.beats)}")

        # Mencari similaritas
        similarityValue = audioTest.compare(audioDataset, tuningValues, True)
        if similarityItems == []:
            similarityKeys.append(fileDataset)
            similarityItems.append(similarityValue)
        else:
            i = 0
            while i < len(similarityKeys):
                if similarityItems[i] <= similarityValue:
                    similarityKeys.insert(i, fileDataset)
                    similarityItems.insert(i, similarityValue)
                    break
                elif i == len(similarityItems)-1:
                    similarityKeys.append(fileDataset)
                    similarityItems.append(similarityValue)
                    break
                i += 1

        print("Proses audio dataset berhasil.")
        print(f"# similarity: {similarityValue*100:.2f} %")

    # Ranking
    similarity = {i:j for i,j in zip(similarityKeys, similarityItems)}

    # output
    print("\nSimilarity Results:")
    rank = 1
    for key in similarity.keys():
        print(f"{rank}. {key:12}: {(similarity.get(key)*100):.2f} %")
        rank += 1
    input()


# Run CLI program
audioMainCLI()