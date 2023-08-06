import pandas as pd
from sklearn.linear_model import LinearRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import StandardScaler
from pandas_profiling import ProfileReport
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge,Lasso,RidgeCV,LassoCV,ElasticNet,ElasticNetCV,LinearRegression
import numpy as np
import pickle

class FirstLinearModel:
    def __init__(self,link):
        self.link =link

    def Dataframe(self):
        self.df = pd.read_csv(self.link)
        return self.df

    def X(self,columns):
        obj = FirstLinearModel(self.link)
        self.columns = columns
        self.x = obj.Dataframe().drop(self.columns,axis=1)
        return self.x

    def Y(self,column):
        obj = FirstLinearModel(self.link)
        self.column = column
        self.y = obj.Dataframe()[column]
        return self.y

    def standardization(self):
        scaler = StandardScaler()
        obj = FirstLinearModel(self.link)
        x = obj.X(self.columns)
        std = scaler.fit_transform(x)
        return std

    def Report(self):

        obj = FirstLinearModel(self.link)
        x = obj.X(self.columns)
        std = obj.standardization()
        std_df = pd.DataFrame(std, columns=x.columns)
        pdf = ProfileReport(std_df)
        pdf.to_widgets()
        return pdf

    def Multicolinearity(self):
        obj = FirstLinearModel(self.link)
        x = obj.X(self.columns)
        std = obj.standardization()
        vif_df = pd.DataFrame()
        vif_df['vif'] = [variance_inflation_factor(std, i) for i in range(std.shape[1])]
        vif_df['features'] = x.columns
        return vif_df

    def x_train(self):
        obj = FirstLinearModel(self.link)
        x = obj.X(self.columns)
        y = obj.Y(self.column)
        std = obj.standardization()
        self.x_train = x
        x,x_test,y_train,y_test = train_test_split(std,y,test_size=0.25,random_state=True)
        return x

    def y_train(self):
        obj = FirstLinearModel(self.link)
        x = obj.X(self.columns)
        y = obj.Y(self.column)
        std = obj.standardization()
        self.y_train = y
        self.x_train, self.x_test, y, self.y_test = train_test_split(std, y, test_size=0.25,
                                                                                random_state=True)
        return y

    def x_test(self):
        obj = FirstLinearModel(self.link)
        x = obj.X(self.columns)
        y = obj.Y(self.column)
        std = obj.standardization()
        self.x_test = x
        x_train, x, y_train, y_test = train_test_split(std, y, test_size=0.25,random_state=True)
        return x

    def y_test(self):
        obj = FirstLinearModel(self.link)
        x = obj.X(self.columns)
        y = obj.Y(self.column)
        std = obj.standardization()
        self.y_test = y
        x_train, x_test, y_train, y = train_test_split(std, y, test_size=0.25,
                                                                                random_state=True)
        return y

    def linearModel(self):
        obj = FirstLinearModel(self.link)
        x = obj.X(self.columns)
        y = obj.Y(self.column)
        x_t = obj.x_train()
        y_t = obj.y_train()
        lr=LinearRegression()
        lr.fit(x_t,y_t)
        return lr

    def test_transform(self,values):
        obj = FirstLinearModel(self.link)
        x = obj.X(self.columns)
        scaler = StandardScaler()
        scaler.fit_transform(x)
        self.values = values
        test = scaler.transform(values)
        return test

    def predict(self,value):
        obj = FirstLinearModel(self.link)
        obj.X(self.columns)
        obj.Y(self.column)
        obj.standardization()
        self.value = value
        value = obj.test_transform(self.values)
        lr = obj.linearModel()
        return lr.predict(value)

    def score(self):
        obj = FirstLinearModel(self.link)
        obj.X(self.columns)
        obj.Y(self.column)
        y = obj.y_test()
        return obj.linearModel().score(obj.x_test(),y)

    def Lasso(self):
        lassocv = LassoCV(cv = 10,max_iter=2000000,normalize = True)
        obj = FirstLinearModel(self.link)
        obj.X(self.columns)
        obj.Y(self.column)
        x = obj.x_train()
        y = obj.y_train()
        lassocv.fit(x,y)
        lasso = Lasso(alpha = lassocv.alpha_)
        return lasso.fit(x,y)

    def lasso_score(self):
        obj = FirstLinearModel(self.link)
        obj.X(self.columns)
        obj.Y(self.column)
        y = obj.y_test()
        lasso = obj.Lasso()
        return lasso.score(obj.x_test(),y)

    def Ridge(self):
        ridgecv = RidgeCV(alphas = np.random.uniform(0,10,15),cv=10,normalize=True)
        obj = FirstLinearModel(self.link)
        obj.X(self.columns)
        obj.Y(self.column)
        x = obj.x_train()
        y = obj.y_train()
        ridgecv.fit(x, y)
        ridge = Ridge(alpha = ridgecv.alpha_)
        return ridge.fit(x,y)

    def Ridge_score(self):
        obj = FirstLinearModel(self.link)
        obj.X(self.columns)
        obj.Y(self.column)
        y = obj.y_test()
        ridge = obj.Ridge()
        return ridge.score(obj.x_test(), y)

    def ElasticNEt(self):
        elasticcv =ElasticNetCV(alphas = None,cv=10)
        obj = FirstLinearModel(self.link)
        obj.X(self.columns)
        obj.Y(self.column)
        x = obj.x_train()
        y = obj.y_train()
        elasticcv.fit(x,y)
        elastic = ElasticNet(alpha = elasticcv.alpha_,l1_ratio=elasticcv.l1_ratio)
        return elastic.fit(x,y)

    def ElasticNEt_score(self):
        obj = FirstLinearModel(self.link)
        obj.X(self.columns)
        obj.Y(self.column)
        y = obj.y_test()
        elas = obj.ElasticNEt()
        return elas.score(obj.x_test(),y)

    def dump_model(self):
        obj = FirstLinearModel(self.link)
        obj.X(self.columns)
        obj.Y(self.column)
        lr = obj.linearModel()
        #pickle.dump(lr,open('predictive_maintenance_lr_model.pickle','wb'))

    def load_model(self):
        model = pickle.load(open('predictive_maintenance_lr_model.pickle','rb'))
        return model

    def adjusted_r_square(self,x,y):
        obj = FirstLinearModel(self.link)
        obj.X(self.columns)
        obj.Y(self.column)
        r2 = obj.load_model().score(x, y)
        n = x.shape[0]
        p = x.shape[1]
        adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
        return adjusted_r2


