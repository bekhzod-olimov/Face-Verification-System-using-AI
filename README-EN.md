1. Open Anaconda Prompt from Search window;
2. Create a virtual environment using the following script and activate it:

`conda create -n face python=3.8`
`conda activate face`

3. Clone the following GitHub repository using this script:

`git clone https://github.com/sachadee/Dlib.git`

4. Go into the cloned repo and run the following command:

`cd Dlib`
`python -m pip install dlib-19.22.99-cp38-cp38-win_amd64.whl`

5. Go back to the root folder and install required libraries:

`cd ..`
`pip install -r requirements.txt`

6. After completing the aforementioned steps, run the code:

`python run.py`
