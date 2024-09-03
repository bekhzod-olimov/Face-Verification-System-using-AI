1. Search dan Anaconda prompt ochiladi;
2. Virtual environment yaratilib, aktivlashtiriladi:

`conda create -n face python=3.8`

`conda activate face`

3. GitHubdan quyidagi repo clone qilib olinadi:

`git clone https://github.com/sachadee/Dlib.git`

4. Dlib bilan papka ichiga kirib, quyidagi buyruq amalga oshiriladi:

`cd Dlib`

`python -m pip install dlib-19.22.99-cp38-cp38-win_amd64.whl`

5. Asosiy papkaga o'tib quyidagi buyruq yordamida kerakli kutubxonalar o'rnatiladi:

`cd ..`

`pip install -r requirements.txt`

6. Hammasi muvafaqqiyatli yakunlangach kod yurgiziladi:

`python run.py`
