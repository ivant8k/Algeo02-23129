# IMAGE & AUDIO INFORMATION RETRIEVAL
Program yang dijalankan dengan python untuk melihat hasil analisis kesamaan query dengan dataset yang diupload dengan menggunakan metode Principal Component Analysis (PCA) untuk Image Retrieval dan metode Query by Humming untuk music retrieval. 

## File Structure
```

Algeo02-23129/ (repository)
├── bin/
├── doc/
├── src/
│   ├── backend/
│   │   ├── audio/
│   │   │   ├── mir/
│   │   │   │   ├── audio.py
│   │   │   │   ├── vector.py
│   │   │   │   └── windowing.py
│   │   │   └── utility/
│   │   │       └── input.py
│   │   ├── main_audio.py
│   │   └── image/
│   │       └── imgtools.py
│   ├── frontend/
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   └── style.css
│   │   │   └── js/
│   │   │       └── script.js
│   │   └── templates/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── query.html
│   │       ├── result.html
│   │       └── upload.html
│   ├── app.py
│   └── requirements.txt
├── test/
├── uploads/
│   ├── audios/audiodata/ (tempat storage dataset yang diupload)
│   │   ├── file_dataset1.midi
│   │   └── file_dataset2.midi
│   ├── images/imgdata/ (tempat storage dataset yang diupload)
│   │   ├── file_dataset1.jpg
│   │   └── file_dataset2.jpg
│   ├── mapper/ (tempat storage mapper yang diupload, bisa json atau txt)
│   │   ├── contoh_mapper.json
│   │   └── contohLain_mapper.txt
│   └── query/(tempat storage query image atau audio yang ingin dicocokkan dengan dataset)
│       ├── dataUji_gambar.jpg
│       └── dataUji_suara.midi
└── README.md

```

## How To Run
1. Clone the Repository
3. Change directory by typing 'cd src'
5. Install Requirement by typing 'pip install -r requirement.txt'
6. Ensure Python is installed
7. type 'python main.py' in terminal






