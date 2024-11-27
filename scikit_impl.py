import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from surprise import Dataset, Reader
from surprise import SVD
from surprise import accuracy


class ScikitImpl:

    def __init__(self, debug=False):
        self.debug = debug
        # Read the ratings data
        ratings_df = pd.read_csv("data/ratings.csv")

        if self.debug:
            # Display all columns in the output
            pd.set_option('display.max_columns', None)
            print(ratings_df)

        # Encode the userId and categoryId columns
        self.user_encoder = LabelEncoder()
        self.category_encoder = LabelEncoder()
        ratings_df['userId'] = self.user_encoder.fit_transform(ratings_df['userId'])
        ratings_df['categoryId'] = self.category_encoder.fit_transform(ratings_df['categoryId'])

        # Split the tags column into multiple columns based on the delimiter '|' - It is how the model can understand the tags
        mlb = MultiLabelBinarizer()
        self.ratings_df = ratings_df.join(pd.DataFrame(mlb.fit_transform(ratings_df.pop('tags').str.split('|')), columns=mlb.classes_, index=ratings_df.index))

        # Model based on the SVD Singular Value Decomposition algorithm
        self.model_svd = SVD()

    # This function doesn't contain final implementation of choosing categories/tags!
    def train(self):
        # 80% training, 20% testing - To learn the model and test it
        train_df, test_df = train_test_split(self.ratings_df, test_size=0.2)

        # Model must know the range of ratings in the dataset
        reader = Reader(rating_scale=(1, 10))

        # Load only the necessary columns from the training data
        data = Dataset.load_from_df(train_df[['userId', 'categoryId', 'rating']], reader)

        # Build the training set
        trainset = data.build_full_trainset()

        # Train the model
        self.model_svd.fit(trainset)

        # another model - worse RMSE
        # model_knn = KNNBasic()
        # model_knn.fit(trainset)

        if self.debug:
            # testset to test the model
            testset = [(row['userId'], row['categoryId'], row['rating']) for _, row in test_df.iterrows()]

            # Predict ratings for the testset
            predictions_test = self.model_svd.test(testset)

            # Calculate RMSE on the test set, the lower the value the better, for 1-10 rating scale, we want RMSE to be less than 1 (1 point of rating)
            accuracy.rmse(predictions_test)

    def get_top_n_recommendations(self, user_id, n=10):
        user_id = self.user_encoder.transform([user_id])[0]
        # Get all unique categories
        all_categories = self.ratings_df['categoryId'].unique()

        # Get all user-category pairs
        user_category_pairs = [(user_id, category_id, 0) for category_id in all_categories]

        # Predict ratings for all user-category pairs
        predictions_cf = self.model_svd.test(user_category_pairs)

        # Sort the predictions by estimated rating in descending order and get top n recommendations
        top_n_recommendations = sorted(predictions_cf, key=lambda x: x.est, reverse=True)[:n]

        if self.debug:
            print(top_n_recommendations)

        # Get the top n predicted ratings
        predicted_ratings = [pred.est for pred in top_n_recommendations]

        # Get the top n category ids
        top_category_ids = [pred.iid for pred in top_n_recommendations]

        # Return the top categories
        return [self.category_encoder.inverse_transform(top_category_ids), predicted_ratings]
