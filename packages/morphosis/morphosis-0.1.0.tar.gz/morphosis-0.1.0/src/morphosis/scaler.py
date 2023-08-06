import numpy as np
from sklearn.preprocessing import MinMaxScaler, MultiLabelBinarizer
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
from morphosis.utils import literal_return


class HardMinMaxScaler(MinMaxScaler):
    _capping = (-1, 1)

    @property
    def capping(self):
        return self._capping

    @capping.setter
    def capping(self, value):
        self._capping = value

    def transform(self, X: pd.DataFrame):
        """Scale features of X, capping the outputs of MinMaxScaler
        between `self.capping`.

        MinMaxScaler.transform() can return values outside of (0, 1)
        in case it transforms values outside of the seen values during
        the fit. The HardMinMaxScaler caps these outcomes.

        :param X : Input data that will be transformed.
        :type X : array-like of shape (n_samples, n_features)

        :return: Transformed data.
        :rtype: ndarray of shape (n_samples, n_features)
        """
        x = super(HardMinMaxScaler, self).transform(X)
        ones = np.ones(x.shape)
        min_values = self.capping[0] * ones
        max_values = self.capping[1] * ones
        x = np.minimum(x, max_values)
        x = np.maximum(x, min_values)
        return x


class MultiHotEncoder(BaseEstimator, TransformerMixin):
    """Wraps `MultiLabelBinarizer` in a form that can work with `ColumnTransformer`. Note
    that input X has to be a `pandas.DataFrame`.
    """

    def __init__(self):
        self.mlbs = list()
        self.classes_ = list()

    def fit(self, y: pd.DataFrame):
        """Fit the label sets binarizer, storing :term:`classes_`.

        :param y : Input data that will be fit.
        :type y: array-like of shape (n_samples, n_features) where n_samples
            are iterable or string representations of iterables

        :return: self
        """
        n_features = y.shape[1]
        for i in range(n_features):
            mlb = MultiLabelBinarizer()
            mlb.fit(y.iloc[:, i].apply(literal_return))
            self.mlbs.append(mlb)
            self.classes_.append(mlb.classes_)
        return self

    def transform(self, y: pd.DataFrame):
        if not self.mlbs:
            raise ValueError("Please fit the transformer first.")
        if len(self.mlbs) != y.shape[1]:
            raise ValueError(
                f"The fit transformer deals with {len(self.mlbs)} columns "
                f"while the input has {y.shape[1]}."
            )

        result = [
            self.mlbs[i].transform(y.iloc[:, i].apply(literal_return))
            for i in range(len(self.mlbs))
        ]
        result = np.concatenate(result, axis=1)
        return result
