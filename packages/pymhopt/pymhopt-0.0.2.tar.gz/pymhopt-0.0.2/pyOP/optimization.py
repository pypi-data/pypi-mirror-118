class Optimization():
    
    NUM_FEATURES = globals()
    SELECTED_FEATURES = globals()
    OPTIMIZATION_TARGET = globals()
    CATEGORICAL_SELECT = globals()
    NUM_GENERATIONS = globals()
    
    def read_data(data):
        """
        Data ingestion : Function to read and formulate the data with no missing values
        """
        df = data.copy()
        df.fillna(0, inplace=True)
        data.fillna(0, inplace=True)
        return data, df
 
    def set_config(**kwargs):
        """
        Select the configuration parameters
        """
        for key, value in kwargs.items():
            print("{0} = {1}".format(key, value))

        NUM_FEATURES = list(kwargs.values())[0]
        SELECTED_FEATURES = list(kwargs.values())[1]
        OPTIMIZATION_TARGET = list(kwargs.values())[2]
        CATEGORICAL_SELECT = list(kwargs.values())[3]
        NUM_GENERATIONS = list(kwargs.values())[4]

        return NUM_FEATURES, SELECTED_FEATURES, OPTIMIZATION_TARGET, CATEGORICAL_SELECT, NUM_GENERATIONS # kwargs


    assert NUM_FEATURES == NUM_FEATURES
    assert SELECTED_FEATURES == SELECTED_FEATURES
    assert OPTIMIZATION_TARGET == OPTIMIZATION_TARGET
    assert CATEGORICAL_SELECT == CATEGORICAL_SELECT
    assert NUM_GENERATIONS == NUM_GENERATIONS
       
    # algorithms
    
    def symbolic(df, selected_features=SELECTED_FEATURES, target=OPTIMIZATION_TARGET, categorical_cols = None, generations=NUM_GENERATIONS):
        """
        Finding symbolic expression with genetic programming
        Once fitted one can inspect the best solution via the attribute '_program'.
        """
        # import libraries
        from gplearn.genetic import SymbolicRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import RidgeCV
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import make_pipeline
        from sklearn.metrics import mean_absolute_error, mean_squared_error
        import graphviz
        from collections import OrderedDict
        import pandas as pd
        
        #selected_features = ['Category', 'Type', 'Post Month', 'Post Weekday', 'Post Hour', 'Paid']
        #target = 'Total Interactions'
        X = df[selected_features]
        y =  df[target]
        '''
        def category_col_names(X):
            cat_cols = X.dtypes=='object'
            X.select_dtypes(['object'])
            return list(cat_cols)
        '''
        
        if categorical_cols is not None:
            #assert categorical_cols == CATEGORICAL_SELECT
            categorical_cols == categorical_cols
        
            # manually pick categorical variables
            #categorical_cols = ['Category', 'Type', 'Paid']
            X.loc[:, categorical_cols] = X[categorical_cols].astype('object')
            X = pd.get_dummies(X)
        else:
            pass
        
        # Split train-test
        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, random_state=142)
        
        #applying learning algorithms
        models = {'sr': SymbolicRegressor(generations=generations, verbose=4, max_samples=0.7, random_state=42),
                  'lm': make_pipeline(StandardScaler(), RidgeCV()),
                  'rf': RandomForestRegressor()}
        
        for model_name, model_instance in models.items():
            print('Training Model {}'.format(model_name))
            model_instance.fit(X_train, y_train)
            
        # Evaluation
        for model_name, model_instance in models.items():
            y_test_pred = model_instance.predict(X_test)
            mae = mean_absolute_error(y_test, y_test_pred)
            mse = mean_squared_error(y_test, y_test_pred)
            print('Model {}: \n MAE: {} \n MSE: {} \n'.format(model_name, mae, mse))
        print(models['sr']._program) 
        # Export to a graph
        graph = models['sr']._program.export_graphviz()
        graph_str = str(graph)
        program_str = str(models['sr']._program)

        # Replace X{} with actual feature names
        mapping_dict = {'X{}'.format(i): X.columns[i] for i in reversed(range(X.shape[1]))}

        for old_value, new_value in mapping_dict.items():
            graph_str = graph_str.replace(old_value, new_value)
            program_str = program_str.replace(old_value, new_value)
                
        print(f'FITTEST SOLUTION WITH FEATURES: {program_str}')
    
        # Save on disk
        src = graphviz.Source(graph_str)
        src.render('./result.gv', view=True)
    
    def nsgaII(df, selected_features=SELECTED_FEATURES, target=OPTIMIZATION_TARGET, categorical_cols = None, max_generations=NUM_GENERATIONS):
        # Libraries
        import numpy as np 
        import pandas as pd
        import sklearn.datasets
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import scale
        from copy import deepcopy

        # Internal imports
        from pyOP.Nodes.BaseNode import Node
        from pyOP.Nodes.SymbolicRegressionNodes import AddNode, SubNode, DivNode, MulNode, LogNode, SinNode, CosNode
        from pyOP.Fitness.FitnessFunction import SymbolicRegressionFitness
        from pyOP.Evolution.Evolution import pyNSGP

        from pyOP.SKLearnInterface import pyNSGPEstimator as NSGP

        np.random.seed(42)
        
        X = df[selected_features]
        y =  df[target]
        '''
        def category_col_names(X):
            cat_cols = X.dtypes=='object'
            X.select_dtypes(['object'])
            return list(cat_cols)
        '''
        if categorical_cols is not None:
            #assert categorical_cols == CATEGORICAL_SELECT
            categorical_cols == categorical_cols
            # manually pick categorical variables
            #categorical_cols = ['Category', 'Type', 'Paid']
            X.loc[:, categorical_cols] = X[categorical_cols].astype('object')
            X = pd.get_dummies(X)
        else:
            pass
        
        # Split train-test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, shuffle=True, random_state=142)
        
        # Prepare NSGA-II settings
        nsga = NSGP(pop_size=512, max_generations=max_generations, verbose=True, max_tree_size=50, 
            crossover_rate=0.8, mutation_rate=0.1, op_mutation_rate=0.1, min_depth=2, initialization_max_tree_height=6, 
            tournament_size=2, use_linear_scaling=True, use_erc=True, use_interpretability_model=True,
            functions = [ AddNode(), SubNode(), MulNode(), DivNode(), LogNode(), SinNode(), CosNode() ])

        # Fit like any sklearn estimator
        nsga.fit(X_train,y_train)

        # Obtain the front of non-dominated solutions (according to the training set)
        front = nsga.get_front()
        print('len front:',len(front))
        for solution in front:
            print(solution.GetHumanExpression())
            
        # You can also use sympy to simplify the formulas :) (if you use PowNode, replace ^ to ** before use)
        '''
        from sympy import simplify
        for solution in front:
            simplified = simplify(solution.GetHumanExpression())
            print(simplified)
        '''

        # You can use cross-validation, hyper-parameter tuning, anything a sklearn estimator can normally do
        from sklearn.model_selection import cross_validate

        cv_result = cross_validate(nsga, X, y, scoring='neg_mean_squared_error', cv=5)

        print(f'Cross Validation Result: {cv_result}')
        

    
    