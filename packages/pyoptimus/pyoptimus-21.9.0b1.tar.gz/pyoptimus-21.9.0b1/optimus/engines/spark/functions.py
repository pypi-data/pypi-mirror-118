import numpy as np
from databricks import koalas

from optimus.engines.base.commons.functions import word_tokenize
from optimus.engines.base.dataframe.functions import DataFrameBaseFunctions
from optimus.engines.base.spark.functions import SparkBaseFunctions


# These function can return a Column Expression or a list of columns expression
# Must return None if the data type can not be handle


class SparkFunctions(SparkBaseFunctions, DataFrameBaseFunctions):

    @property
    def _engine(self):
        return koalas

    def word_tokenize(self, series):
        return self.to_string(series).map(word_tokenize, na_action=None)

    def count_zeros(self, series, *args):
        return int((self.to_float(series).values == 0).sum())

    def kurtosis(self, series):
        return self.to_float(series).kurtosis()

    def skew(self, series):
        return self.to_float(series).skew()

    def exp(self, series):
        return np.exp(self.to_float(series))

    def sqrt(self, series):
        return np.sqrt(self.to_float(series))

    def reciprocal(self, series):
        return np.reciprocal(self.to_float(series))

    def radians(self, series):
        return np.radians(self.to_float(series))

    def degrees(self, series):
        return np.degrees(self.to_float(series))

    def ln(self, series):
        return np.log(self.to_float(series))

    def log(self, series, base=10):
        return np.log(self.to_float(series)) / np.log(base)

    def sin(self, series):
        return np.sin(self.to_float(series))

    def cos(self, series):
        return np.cos(self.to_float(series))

    def tan(self, series):
        return np.tan(self.to_float(series))

    def asin(self, series):
        return np.arcsin(self.to_float(series))

    def acos(self, series):
        return np.arccos(self.to_float(series))

    def atan(self, series):
        return np.arctan(self.to_float(series))

    def sinh(self, series):
        return np.arcsinh(self.to_float(series))

    def cosh(self, series):
        return np.cosh(self.to_float(series))

    def tanh(self, series):
        return np.tanh(self.to_float(series))

    def asinh(self, series):
        return np.arcsinh(self.to_float(series))

    def acosh(self, series):
        return np.arccosh(self.to_float(series))

    def atanh(self, series):
        return np.arctanh(self.to_float(series))

    def floor(self, series):
        return np.floor(self.to_float(series))

    def ceil(self, series):
        return np.ceil(self.to_float(series))

    def normalize_chars(self, series):
        return series.str.normalize("NFKD").str.encode('ascii', errors='ignore').str.decode('utf8')

    def format_date(self, series, current_format=None, output_format=None):
        return pd.to_datetime(series, format=current_format, errors="coerce").dt.strftime(output_format).reset_index(
            drop=True)

    def td_between(self, series, value=None, date_format=None):

        value_date_format = date_format

        if is_list_or_tuple(date_format) and len(date_format) == 2:
            date_format, value_date_format = date_format

        if is_list_or_tuple(value) and len(value) == 2:
            value, value_date_format = value

        date = pd.to_datetime(series, format=date_format, errors="coerce")
        value = pd.Timestamp.now() if value is None else pd.to_datetime(value, format=value_date_format,
                                                                        errors="coerce")

        return (value - date)
