### This project is only compatible with Windows.

## How to setup the environment
### scikit-surprise & data manipulation
```bash
    pip3 install scikit-learn
    pip3 install surprise
    pip3 install pandas

    pip3 uninstall numpy
    pip3 install "numpy<2.0"
```

### StableDiffusion3
```bash
    pip3 install diffusers
    pip3 install transformers
    pip3 install bitsandbytes
    pip3 install accelerate
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    pip3 install protobuf
    pip3 install sentencepiece
 ```

### Streamlit
```bash
    pip3 install streamlit
 ```

## Running app
- From inside main directory run
```bash 
    streamlit run main.py
 ```

## How the data is structured
### ratings.csv
- userId: We assume that we can have multiple users
- categoryId: The main category of tags used to generate the picture (we need integer type here)
- rating: The rating that the user gave to the picture (1-10)
- tags: The tags that model used to generate the picture (separated by '|')

### categories.csv
- id: ID of the category
- name: Name of the category

## What not to forget
- The current ratings.csv and categories.csv were generated by ChatGPT - We should replace them later
- Implement adding new users (id, name)
- Implement generating e.g. 10 pictures with one click (not only one)
- Generated images should contain best rated tags and tags that are not rated yet
- Add a loading screen when the models are initialising (on the app start)
