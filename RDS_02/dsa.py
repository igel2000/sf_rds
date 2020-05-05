import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from scipy.stats import ttest_ind

empty_str_to_none = lambda x: None if type(x) == str and x.strip() == '' else x

str_with_percent_to_float = lambda x: float(x.replace('%', '')) if type(x) == str else x

def show_df_info(df):
    """
    Показать детальную информацию по датасету
    """
    display(df.head())
    print(f"Количество строк в датасете: {df.shape[0]}")
    print(f"Cтолбцы в датасете ({len(df.columns)}):")
    d = pd.DataFrame()
    d['column'] = df.columns
    d['not_null_unique_values_count'] = d.apply(lambda x: df[x.column].nunique(), axis=1)
    d['not_null_count'] = d.apply(lambda x: df[x.column].count(), axis=1)
    d['d_type'] = d.apply(lambda x: df[x.column].dtype, axis=1)
    d['percent_not_null_value'] = d['not_null_count'] / df.shape[0]
    display(d)
    print('Типы столбцов:')
    display(d[['column', 'd_type']].groupby(by='d_type').count().T)
    del d

def show_column_info(df, col, bins=20, fig_size_x=3, fig_size_y=2):
    '''
    показать детальную инфу по столбцу датасета
    df - датасет
    col - столбец
    '''
    if col in df.columns:
        type_col = df[col].dtype

        print(f"Тип поля {col}: {type_col}")
        print(f"Количество непустых значений: {df[col].count()}")
        print(f"Количество уникальных непустых значений: {df[col].nunique()}")
        df_count = pd.DataFrame(df[col].value_counts(dropna = False)).sort_values(col).reset_index()
        df_count.columns = [col, 'count']
        df_percent = pd.DataFrame(df[col].value_counts(normalize = True, dropna = False)).sort_values(col).reset_index()
        df_percent.columns = [col, 'percent']
        df_col = df_count.merge(df_percent, on = col, sort=True)

        display(df_col)
        
        if type_col == 'object':

            fig = plt.figure(figsize=(fig_size_x, fig_size_y))
            main_axes = fig.add_axes([0, 0, 1, 1], xlabel="score", ylabel='count')
            for v in df_col[col]:
                main_axes.hist(df[((df[col] == v) & (df['score'].notna()))]['score'], alpha=0.5, label=v)    
            main_axes.legend()
            
            
        elif type_col == 'int64' or type_col == 'float64':
            display(df[col].describe())
            print()
            ax3 = df[col].hist(bins = bins, figsize=(fig_size_x, fig_size_y))
            print()
        else:
            print(f"Неизветсный тип {type_col} столбца {col}")
    else:
        print(f"В датафрейме нет столбца {col}")

        
def clear_num_col(df, col, min_value, max_value, include_nan = True):
    '''
    Вернет датасет без строк, в которых столбец col выпадает за указанный диапазон
    '''
    if include_nan:
        return df.loc[(df[col].isna()) | ((df[col]>=min_value) & (df[col]<=max_value))]
    else:
        return df.loc[((df[col]>=min_value) & (df[col]<=max_value))]


def get_boxplot(df, col, col_score, top_values=10):
    """
    Визуализация распределения значений столбца cor_score в зависимости от значений столбца col
    df - датафрейм
    col - столбец с номинативными данными
    col_score - столбец с данными, чьё распределенеи изучается
    top_values - количество наиболее часто встречающихся значений столбца col, которые будут анализироваться
    """
    fig, ax = plt.subplots(figsize = (14, 4))
    sns.boxplot(x=col, y=col_score, 
                data=df.loc[df.loc[:, col].isin(df.loc[:, col].value_counts().index[:top_values])],
               ax=ax)
    plt.xticks(rotation=45)
    ax.set_title('Boxplot for ' + col)
    plt.show()


def get_stat_diff(df, col, col_score, top_values=10, alpha=0.05):
    """
    Поиск статистических различий распределения значений столбца cor_score в зависимости от значений столбца col
    df - датафрейм
    col - столбец с номинативными данными
    col_score - столбец с данными, чьё распределенеи изучается
    top_values - количество наиболее часто встречающихся значений столбца col, которые будут анализироваться
    alpha - уровень доверия
    """
    cols = df.loc[:, col].value_counts().index[:top_values]
    combinations_all = list(combinations(cols, 2))
    for comb in combinations_all:
        a = df.loc[df.loc[:, col] == comb[0], col_score]
        b = df.loc[df.loc[:, col] == comb[1], col_score]
        if ttest_ind(a, b, nan_policy = 'omit').pvalue <= alpha/len(combinations_all): # Учли поправку Бонферони
            print('Найдены статистически значимые различия для колонки', col)
            break