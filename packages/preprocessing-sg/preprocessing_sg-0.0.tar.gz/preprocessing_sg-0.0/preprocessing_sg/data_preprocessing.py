from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer


class Preprocessing:

    @staticmethod
    def standard_scaler(X, columns=None):
        if columns is not None:
            col_tf = ColumnTransformer([
                ("one_hot", StandardScaler(), columns)
            ])
            return col_tf.fit_transform(X)
        else:
            std_scaler = StandardScaler()
            return std_scaler.fit_transform(X)

    @staticmethod
    def one_hot_encoder(X, columns=None):
        if columns is not None:
            col_tf = ColumnTransformer([
                ("one_hot", OneHotEncoder(), columns)
            ])
            return col_tf.fit_transform(X)
        else:
            one_hot = OneHotEncoder()
            return one_hot.fit_transform(X)

    @staticmethod
    def imputer(X, columns=None, strategy='mean'):
        if columns is not None:
            col_tf = ColumnTransformer([
                ("one_hot", SimpleImputer(strategy=strategy), columns)
            ])
            return col_tf.fit_transform(X)
        else:
            impute = SimpleImputer()
            return impute.fit_transform(X)



