import pandas as pd

def calculate_vif_rsquare(dataset_without_dependent_col):
    
    """[This function will use to calculate VIF and adjusted
    rsquare within featue columns or indipendent variables. it will
    return dataFrame containing VIF value and adjusted rsquare.]

    Args:
        dataset_without_dependent_col ([type]): [dataFrame without_dependent_col
        dependent or target column]
    """

    dataset = dataset_without_dependent_col
    if isinstance(dataset, pd.DataFrame):
        
        cat_data = dataset.dtypes[dataset.dtypes=='object'].index
        if cat_data.any:
            dataset = dataset.drop(columns=cat_data)
        output = pd.DataFrame(columns=['Feature Name', 'VIF', 'adj_rsquared'])
        for i in dataset.columns:
            x = dataset.drop([i], axis=1)
            y = dataset[i]
            import statsmodels.api as sm
            model = sm.OLS(y,x)
            model = model.fit()
            adj_rsquare_value = model.rsquared_adj
            rsquare_value = model.rsquared
            vif = round(1 / (1-rsquare_value),2)
            lst = [i,vif, adj_rsquare_value]
            df_tmp = pd.DataFrame(data=[lst], columns=['Feature Name', 'VIF', 'adj_rsquared'])
            output = pd.concat([output, df_tmp], ignore_index=True)
        return(output)
    else:
        print('This is not valid DataFrame, kindly provide valid DataFrame')



