### This project is only compatible with Windows.
### Project is created using Python 3.12.7, and you need to have it installed on your machine.
#### Newer versions of Python might not work with dependencies. You need to check it by yourself.
#### Please run project using administrator privileges and without any virtual environments, and close all other streamlit web tabs before running the app.

## How to setup the environment
You need to have Build Tools installed on your machine. https://visualstudio.microsoft.com/pl/visual-cpp-build-tools/

#### All commands can be run without 'python -m' prefix, but it is recommended to use it to avoid any conflicts with other Python installations.

### It is recommended to update pip before installing any packages
```bash
    python -m pip install --upgrade pip
```

### scikit-surprise & data manipulation
```bash
    python -m pip install scikit-learn
    python -m pip install surprise
    python -m pip install pandas
    python -m pip install python-dotenv

    python -m pip uninstall numpy
    python -m pip install "numpy<2.0"
```

### StableDiffusion3
```bash
    python -m pip install diffusers
    python -m pip install transformers
    python -m pip install bitsandbytes
    python -m pip install accelerate
    python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
    python -m pip install protobuf
    python -m pip install sentencepiece
 ```

### Streamlit
```bash
    python -m pip install streamlit
 ```

### After installing all dependencies, you need login to Hugging Face and pass your API token
```bash
  huggingface-cli login
```

## Running app
- From inside main directory run:
```bash
    python -m streamlit run main.py
 ```

## How the data is structured
### ratings.csv
- id: ID of the rating
- userId: We assume that we can have multiple users
- categoryId: The main category of tags used to generate the picture (if multiple categories -> separated by '|')
- rating: The rating that the user gave to the picture (1-10)
- tags: The tags that model used to generate the picture (separated by '|')

In the program we should distinguish the difference between rating a category and tags, they should be treated separately!

### categories.csv
- id: ID of the category
- name: Name of the category
