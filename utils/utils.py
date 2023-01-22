"""Utils."""
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.model_selection import KFold
from typing import Union, List


def numeric_statistics(df: pd.DataFrame = None) -> pd.DataFrame:
    """Make a descriptive analysis on numeric data.

    Parameters
    ----------
    df: pd.DataFrame, default=None.
    """
    dic = {
        "type": df.dtypes.values,
        "Unique_Values": df.nunique().values,
        "Mean": df.mean(),
        "Median": df.median(),
        "Std": df.std(),
        "Min": df.min(),
        "Max": df.max(),
        "Range": df.max() - df.min(),
        "Skew": df.skew(),
        "Kurtosis": df.kurtosis()
    }

    return pd.DataFrame(dic, index=df.columns)


def cramer_v(x: Union[List, np.array], y: Union[List, np.array]) -> float:
    """Return the cramer v beetwen two categorical variables.

    Parameters
    ----------
    x: list or numpy array, default=None
    y: list or numpy array, default=None
    """
    cm = pd.crosstab(x, y).values
    n = cm.sum()
    r, k = cm.shape

    chi2 = stats.chi2_contingency(cm)[0]

    chi2corr = max(0, chi2 - (k-1)*(r-1) / (n-1))
    kcorr = k - (k-1)**2 / (n-1)
    rcorr = r - (r-1)**2 / (n-1)

    return np.sqrt((chi2corr / n) / (min(kcorr-1, rcorr-1)))


def precision_at_k(
    data: pd.DataFrame, k: int, id_column: str = 'id',
        response_column: str = 'response', score_column: str = 'score'):
    """Return precision at k.

    Parameters
    ----------
    data: pd.DataFrame
    k: int
        top k
    id_column: str, default='id'
    response_column: str, default='id'
    score_column: str, default='score'
    """
    # sorte client by propensity score
    data = data.sort_values(score_column, ascending=False)
    data = data.reset_index(drop=True)

    # ranking
    data['k'] = data.index + 1

    # cols selected
    data = data[['k', id_column, response_column, score_column]]

    # accumulated sum
    data['cumsum'] = data[response_column].cumsum()

    # precision top k
    data['precision_at_k'] = data['cumsum'] / data['k']

    return (data.loc[k, 'precision_at_k'], data)


def recall_at_k(
    data: pd.DataFrame, k: int, id_column: str = 'id',
        response_column: str = 'response', score_column: str = 'score'):
    """Return recall at k.

    Parameters
    ----------
    data: pd.DataFrame
    k: int
        top k
    id_column: str, default='id'
    response_column: str, default='id'
    score_column: str, default='score'
    """
    # sorte client by propensity score
    data = data.sort_values(score_column, ascending=False)
    data = data.reset_index(drop=True)

    # ranking
    data['k'] = data.index + 1

    # cols selected
    data = data[['k', id_column, response_column, score_column]]

    # accumulated sum
    data['cumsum'] = data[response_column].cumsum()

    # precision top k
    data['recall_at_k'] = data['cumsum'] / data[response_column].sum()

    return (data.loc[k, 'recall_at_k'], data)


def cross_validation(
                     X_train, y_train, model, kfolds, cols_selected, ktop,
                     shuffle=True):
    """Cros validation function."""
    score = []
    kf = KFold(n_splits=kfolds, shuffle=shuffle)

    x_training_aux01 = X_train
    y_training_aux01 = y_train

    for i in kf.split(x_training_aux01):
        x_training_aux02 = x_training_aux01[cols_selected]
        y_training_aux02 = y_training_aux01.copy()

        # base de treino do modelo de fato
        treino_x = x_training_aux02.iloc[i[0]]
        treino_y = y_training_aux02.iloc[i[0]]

        # base de validação
        val_x = x_training_aux02.iloc[i[1]]
        val_y = y_training_aux02.iloc[i[1]]

        md = model.fit(treino_x, treino_y)

        pred = md.predict_proba(val_x)

        data = pd.concat([val_x, val_y], axis=1)
        data['score'] = pred[:, 1].tolist()
        data = data[['score', 'response']].merge(
                                                x_training_aux01['id'],
                                                how='left',
                                                left_index=True,
                                                right_index=True)

        score.append(precision_at_k(
            data,
            k=ktop,
            id_column='id',
            response_column='response',
            score_column='score')[0])

    return np.mean(score)
