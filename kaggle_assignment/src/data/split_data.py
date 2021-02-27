from sklearn.model_selection import train_test_split
def split_data(df,target):
    """
    Splits data into Train, Valdiation and Test set.
    It returns all splits.
    
    Parameters
    ----------
    file : input csv file with the path
    """
    
    df_cleaned = df.copy()          
    x=df_cleaned.drop([target],axis=1)
    y=df_cleaned[target]
    x_data , x_test ,y_data,  y_test = train_test_split(x, y, test_size=0.2, random_state = 8, stratify=y)
    x_train , x_val , y_train, y_val = train_test_split(x_data, y_data, test_size=0.2, random_state = 8, stratify=y_data)
    print('x.shape',x.shape,' y.shape' , y.shape)
    print('y\n',y.value_counts(normalize=True))
    print('y_data\n',y_train.value_counts(normalize=True))
    print('y_train\n',y_train.value_counts(normalize=True))
    print('y_val\n', y_val.value_counts(normalize=True))
    print('y_test\n',y_test.value_counts(normalize=True))
    return x_data, x_train, x_val, x_test, y_data , y_train, y_val,  y_test