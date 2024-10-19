import numpy as np

class LinearRegression() :

    def __init__(self, learning_rate, iterations):

        self.lr = learning_rate
        self.iterations = iterations
        self.loss = []

    @staticmethod
    def mean_squared_error(y, y_hat):

        return np.square(np.subtract(np.array(y), np.array(y_hat))).mean()

    def fit(self, X, Y):

        self.m, self.n = X.shape

        self.W = np.zeros(self.n)
        self.b = 0
        self.X = X
        self.Y = Y

        for i in range(self.iterations):

            self.update()

        return self

    def update(self):

        Y_pred = self.predict(self.X)

        mse = self.mean_squared_error(self.Y, Y_pred)
        self.loss.append(mse)


        dW = -(2 * (self.X.T).dot(self.Y - Y_pred)) / self.m

        db = -2 * np.sum(self.Y - Y_pred) / self.m


        self.W = self.W - self.lr * dW

        self.b = self.b - self.lr * db

        return self

    def predict(self, X):

        return X.dot(self.W) + self.b
