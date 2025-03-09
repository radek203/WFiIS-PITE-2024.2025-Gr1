## Project Goal
The goal of the project is to create an application that uses artificial intelligence models, such as Stable Diffusion, to generate images and implement a personalization mechanism using the scikit-surprise library. The application allows users to rate the generated images, enabling subsequent image generations to align with their individual preferences. Data related to ratings and image generations is managed using the NumPy library, which ensures efficient storage and retrieval of information, facilitating the smooth operation of the application. Additionally, to provide an intuitive and convenient user interaction experience, the graphical interface was developed using the Streamlit library. The combination of these technologies delivers personalized visual experiences in a user-friendly environment.

![image8](https://github.com/user-attachments/assets/9e83d303-9a6e-4d01-b73c-239728419f74)


### This project is only compatible with Windows and graphics card with CUDA support.
### Recommended minimum specs: 32GB RAM, 8GB VRAM
#### Tested on NVIDIA GeForce RTX 4070, 64GB RAM, using SD35LT model (and 35 steps (10 should be enough)) - average time of generating 1 image is around 30 seconds.
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
