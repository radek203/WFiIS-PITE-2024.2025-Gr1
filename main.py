from scikit_impl import ScikitImpl


def main():
    print("Welcome to the program!")
    scikit = ScikitImpl()
    scikit.train()
    ids, ratings = scikit.get_top_n_recommendations(1, 3)
    print(f"IDs: {ids}", f"Ratings: {ratings}", sep="\n")


if __name__ == '__main__':
    main()
