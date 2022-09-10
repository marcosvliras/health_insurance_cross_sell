import pandas as pd
import numpy as np
from scipy import stats

def numeric_statistics(df):
    """Make a descriptive analysis on numeric data.
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

def cramer_v(x, y):
    
    cm   = pd.crosstab( x, y ).values
    n    = cm.sum()
    r, k = cm.shape
    
    chi2 = stats.chi2_contingency( cm )[0]
 
    chi2corr = max( 0, chi2 - (k-1)*(r-1)/(n-1) )
    kcorr    = k - (k-1)**2/(n-1)
    rcorr    = r - (r-1)**2/(n-1)
    
    return np.sqrt((chi2corr/n) / ( min(kcorr-1,rcorr-1)))


def precision_at_k(data, k):
        
    # sorte client by propensity score
    data = data.sort_values('score', ascending=False)
    data = data.reset_index(drop=True)
    
    # ranking
    data['k'] = data.index + 1

    # cols selected
    data = data[['k','id','response','score']]

    #accumulated sum
    data['cumsum'] = data['response'].cumsum()

    # precision top k
    data['precision_at_k'] = data['cumsum'] / data['k']
    
    return (data.loc[k,'precision_at_k'], data)

def recall_at_k(data, k):
    
    # sorte client by propensity score
    data = data.sort_values('score', ascending=False)
    data = data.reset_index(drop=True)
    
    # ranking
    data['k'] = data.index + 1

    # cols selected
    data = data[['k','id','response','score']]

    #accumulated sum
    data['cumsum'] = data['response'].cumsum()

    # precision top k
    data['recall_at_k'] = data['cumsum'] / data['response'].sum()
    
    return ( data.loc[k,'recall_at_k'], data)


def cross_validation(X_train, y_train, model, kfolds, cols_selected, ktop):
    
    score = []
    
    # utilizando o kfold para escolher em quantas partes quero divir meu dataset
    # e utilizando o parâmetro shuffle=True para misturar as linhas do dataset 
    kf = KFold(n_splits=kfolds, shuffle=True)
    
    # entrada dos meus dados de treino
    x_training_aux01 = X_train
    y_training_aux01 = y_train
 
    for i in kf.split(x_training_aux01):
        # atribuindo as colunas selecionadas para essa outra variável auxiliar, mas pq?
        # na função "precision_at_k" utilizamos o "id" que não está presente nas colunas selecionadas
        x_training_aux02 =  x_training_aux01[cols_selected]
        y_training_aux02 =  y_training_aux01.copy()

        # base de treino do modelo de fato
        treino_x = x_training_aux02.iloc[i[0]]
        treino_y = y_training_aux02.iloc[i[0]]

        # base de validação
        val_x = x_training_aux02.iloc[i[1]]
        val_y = y_training_aux02.iloc[i[1]]

        # fit do modelo
        md = model.fit(treino_x, treino_y)

        # predições das probabilidades
        pred = md.predict_proba(val_x)

        # concatenando as variáveis de validação para gerar o dataframe que vai entrar na "precision_at_k"
        data = pd.concat([val_x,val_y], axis=1)

        # gerando a coluna score
        data['score'] = pred[:,1].tolist()

        # fazendo um merge entre meu dataframe gerado pela união das variáveis de validação
        # com o data frame de treino antes de selecionar as colunas para poder pegar somente o "id"
        # fazendo o merge pelo index
        data = data[['score','response']].merge( x_training_aux01['id'], how='left', left_index=True, right_index=True )
        
        score.append(precision_at_k( data, k=ktop )[0])
        
    return np.mean(score)
