from scikit_impl import ScikitImpl


def main():
    print("Welcome to the program!")
    scikit = ScikitImpl(True)
    scikit.train()
    ids, ratings = scikit.get_top_n_recommendations(1, 3)
    print(f"IDs: {ids}", f"Ratings: {ratings}")


if __name__ == '__main__':
    main()
