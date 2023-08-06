import pandas as pd
from sklearn.preprocessing import StandardScaler


class EXDA:
    def nullreplace_mean(self, arg):
        """
        Replace the null values in the provded dataframe columns or series with the mean of that specific column or series

        Parameters
        ----------
        arg = dataframe(single column(series) or multiple columns)

        Example
        -------
        >>> df = pd.DataFrame([[np.nan, 2, np.nan, 0],
        ...                     [3, 4, 1, 1],
        ...                     [np.nan, np.nan, 5, 5],
        ...                     [np.nan, 3, 6, 4]],
        ...                       columns=list('ABCD'))

        >>> eda=EDA()
        >>> df1=eda.nullreplace_mean(df)
        >>> df1
         A    B    C  D
        0  3.0  2.0  4.0  0
        1  3.0  4.0  1.0  1
        2  3.0  3.0  5.0  5
        3  3.0  3.0  6.0  4


        """
        arg = arg.fillna(value=arg.mean())
        return arg

    def nullreplace_median(self, arg):
        """
        Replace the null values in the provded dataframe columns or series with the median of that specific column or series

        Parameters
        ----------
        arg = dataframe(single column(series) or multiple columns)

        Example
        -------
        >>> df = pd.DataFrame([[np.nan, 2, np.nan, 0],
        ...                     [3, 4, 1, 1],
        ...                     [np.nan, np.nan, 5, 5],
        ...                     [np.nan, 3, 6, 4]],
        ...                       columns=list('ABCD'))

        >>> eda=EDA()
        >>> df1=eda.nullreplace_mean(df)
        >>> df1
         A    B    C  D
        0  3.0  2.0  5.0  0
        1  3.0  4.0  1.0  1
        2  3.0  3.0  5.0  5
        3  3.0  3.0  6.0  4

        """
        arg = arg.fillna(value=arg.median())
        return arg

    def nullreplace_mode(self, arg):
        """
        Replace the null values in the provded dataframe columns or series with the mode of that specific column or series

        Parameters
        ----------
        arg = dataframe(single column(series) or multiple columns)

        Example
        -------
        >>> df = pd.DataFrame([[np.nan, 2, np.nan, 0],
        ...                     [3, 4, 1, 1],
        ...                     [np.nan, np.nan, 5, 5],
        ...                     [np.nan, 3, 6, 4]],
        ...                       columns=list('ABCD'))

        >>> eda=EDA()
        >>> df1=eda.nullreplace_mode(df)
        >>> df1
         A    B    C  D
        0  3.0  2.0  1.0  0
        1  3.0  4.0  1.0  1
        2  3.0  3.0  5.0  5
        3  3.0  3.0  6.0  4

        """
        arg = arg.fillna(value=arg.mode().iloc[0])
        return arg

    def normalize(self, arg):
        """
        Normalize or standardizing the features by removing the mean and scaling to unit variance

        Parameters
        ----------
        arg : dataframe(single column(series) or multiple columns)

        Example
        -------
        >>> df1
         A    B    C  D
        0  3.0  2.0  4.0  0
        1  3.0  4.0  1.0  1
        2  3.0  3.0  5.0  5
        3  3.0  3.0  6.0  4

        >>> scaler = StandardScaler()
        >>> df1=scaler.fit_transform(df1)
        >>> df1=pd.DataFrame(df1)
        >>> df1
             0         1         2         3
            0  0.0 -1.414214  0.000000 -1.212678
            1  0.0  1.414214 -1.603567 -0.727607
            2  0.0  0.000000  0.534522  1.212678
            3  0.0  0.000000  1.069045  0.727607


        """

        scaler = StandardScaler()
        arg = scaler.fit_transform(arg)
        arg = pd.DataFrame(arg)
        return arg
