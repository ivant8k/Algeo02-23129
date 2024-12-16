# IMAGE & AUDIO INFORMATION RETRIEVAL
Program yang dijalankan dengan python untuk melihat hasil analisis kesamaan query dengan dataset yang diupload dengan menggunakan metode Principal Component Analysis (PCA) untuk Image Retrieval dan metode Query by Humming untuk music retrieval. 

## File Structure
```
Algeo02-23129
│   README.md
│
├───.vscode
│       settings.json
│
├───doc
│       dummy.txt
│
├───src
│   │   app.py
│   │   main.py
│   │   requirement.txt
│   │
│   ├───backend
│   │   │   generate_mapper.py
│   │   │
│   │   ├───audio
│   │   │   │   main_audio.py
│   │   │   │
│   │   │   ├───mir
│   │   │   │       audio.py
│   │   │   │       vector.py
│   │   │   │       windowing.py
│   │   │   │
│   │   │   └───utility
│   │   │           input.py
│   │   │
│   │   └───image
│   │           imgtools.py
│   │           tes.py
│   │
│   └───frontend
│       ├───static
│       │   ├───css
│       │   │       styles.css
│       │   │
│       │   ├───js
│       │   │       script.js
│       │   │
│       │   └───uploads
│       │       ├───audios
│       │       ├───images
│       │       ├───mapper
│       │       └───query
│       └───templates
│               base.html
│               home.html
│               query.html
│               result.html
│               upload.html
│
└───test
    │   audiodata.rar
    │   audiodata.zip
    │   imgdata.rar
    │   imgdata.zip
    │   mapper.json
    │   mapper.txt
    │   mapper_test.json
    │   mapper_test.txt
    │
    ├───audiodata
    │       file1.midi
    │       file2.midi
    │       file3.midi
    │       file4.midi
    │       file5.midi
    │       file6.midi
    │       file7.midi
    │
    └───imgdata
            ame.jpg
            asuna.jpg
            chisato.jpg
            mashiron.jpg
            megumin.jpg
            tomoyo.jpg
            tomoyo2.jpg

```

## How To Run
1. Clone the Repository
3. Change directory by typing 'cd src'
5. Install Requirement by typing 'pip install -r requirement.txt'
6. Ensure Python is installed
7. type 'python main.py' in terminal






