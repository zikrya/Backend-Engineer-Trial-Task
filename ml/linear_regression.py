import numpy as np

class LinearRegression() :

    def __init__(self, learning_rate, iterations):

        self.lr = learning_rate
        self.iterations = iterations
        self.loss = []

    @staticmethod
    def mean_squared_error(y, y_hat):

        return np.square(np.subtract(np.array(y), np.array(y_hat))).mean()

    # Fit the Regression
    def fit(self, X, Y):

        # Rows and Columns
        self.m, self.n = X.shape

        # Initialize array of zeros size of X's columns
        self.W = np.zeros(self.n)
        self.b = 0
        self.X = X
        self.Y = Y

        # Learning through gradient descent
        for i in range(self.iterations):

            self.update()

        return self

    # Cleans up fit() by updating in seperate method
    def update(self):

        Y_pred = self.predict(self.X)

        # Log to be able to view later
        mse = self.mean_squared_error(self.Y, Y_pred)
        loss.append(mse)

        # Partial Derivatives (vectorized)

        dW = -(2 * (self.X.T).dot(self.Y - Y_pred)) / self.m

        db = -2 * np.sum(self.Y - Y_pred) / self.m

        # update weights

        self.W = self.W - self.lr * dW

        self.b = self.b - self.lr * db

        return self

    # Model prediction with current weights and bias
    def predict(self, X):

        return X.dot(self.W) + self.b