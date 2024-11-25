from scikit_impl import ScikitImpl
from stablediffusion import StableDiffusion


def main():
    print("Welcome to the program!")
    scikit = ScikitImpl(True)
    scikit.train()
    ids, ratings = scikit.get_top_n_recommendations(1, 3)
    print(f"IDs: {ids}", f"Ratings: {ratings}")

    image_generator = StableDiffusion()
    image_generator.generate_image("dachshund in the santa claus hat writing a python code on the computer", "dachshund")


if __name__ == '__main__':
    main()
