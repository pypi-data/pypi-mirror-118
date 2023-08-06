from sklearn.impute import SimpleImputer
import pandas as pd

def clean_column_names(df):
    """ Removes special charectors and space
    form columns names"""
    columns = df.columns
    colupdated = []
    for col in columns:
        removespecialchars = col.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,. /<>?\|`~-=_+'"})
        colupdated.append(removespecialchars)
    df.columns = colupdated
    return df

def drop_duplicate(df, keep = 'first'):
    """ Drops duplicate rows
    keep = first - keeping the first occurrence
    keep = 'fast - keeping last occurrence
    keep = False - keeps nothing. """
    df = df.drop_duplicates(subset=None, keep= keep, inplace=False)
    return df


def remove_outlier_IQR(df, q1=0.25, q3=0.75):
    """ Removes outliers with Q1 = 0.25, Q3 = 0.75"""
    Q1 = df.quantile(q1)
    Q3 = df.quantile(q3)
    IQR = Q3 - Q1
    df_final = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR)))]
    return df_final


def drop_missing_value(df, axis=0):
    """Drops missing values rows or columns
     df - DataFrame
     axis = 1 - columns
     axis = 0 - rows """
    reduced_df = df.dropna(axis=axis)
    return reduced_df


def impute_missing_value(df):
    """make new columns indicating what will be imputed"""

    cols_with_missing = (col for col in df.columns
                         if df[col].isna().any())
    for col in cols_with_missing:
        df[col + '_was_missing'] = df[col].isnull()
    columns = df.columns
    # Imputation
    my_imputer = SimpleImputer()
    df = pd.DataFrame(my_imputer.fit_transform(df), columns=columns)
    return df

def cleandata(df):
    """ Performs, cleaning columns headers, removing outliers, imputing missed values"""
    df = clean_column_names(df)
    print("Columns headers cleaned")
    df_dup = drop_duplicate(df, keep='first')
    print("Dropped duplicate rows")
    df = remove_outlier_IQR(df_dup)
    print("Outliers removed")
    df = impute_missing_value(df)
    print("Missing Values imputed")
    return df