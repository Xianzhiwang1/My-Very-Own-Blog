import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
from itertools import combinations
from sklearn.linear_model import LogisticRegression
le = LabelEncoder()

class FinalProject:
    def __init__(self):
        self.qual_cols = None
        self.feature_score_pair = dict()

    def preparing_data(self, df):
        # le.fit(df["Species"])
        # df = df.drop(["studyName", "Sample Number", "Individual ID", "Date Egg", "Comments", "Region"], axis = 1)
        # df = df[df["Sex"] != "."]
        # df = df.dropna()
        # y = le.transform(df["Species"])
        # df = df.drop(["Species"], axis = 1)
        # df = pd.get_dummies(df)
        # return df, y
        pass

    def create_balanced_data(self, df) -> pd.DataFrame:
        df_inc = df.loc[df['Form'] == 1]
        df_not_inc = df.loc[df['Form'] == 0]
        print(f"df incorporated have {df_inc.shape[0]} many rows")
        df_not_inc = df_not_inc.sample(n=2393, replace=False)
        print(f"after balancing, df not incorporated have {df_not_inc.shape[0]} many rows")
        frames = [df_inc, df_not_inc]
        result = pd.concat(frames)
        result = result.sample(frac=1).reset_index(drop=True)
        return result
        

    def plot_regions(self, model, X, y):
        
        x0 = X[X.columns[0]]
        x1 = X[X.columns[1]]
        qual_features = X.columns[2:]
        
        fig, axarr = plt.subplots(1, len(qual_features), figsize = (7, 3))

        # create a grid
        grid_x = np.linspace(x0.min(),x0.max(),501)
        grid_y = np.linspace(x1.min(),x1.max(),501)
        xx, yy = np.meshgrid(grid_x, grid_y)
        
        XX = xx.ravel()
        YY = yy.ravel()

        for i in range(len(qual_features)):
            XY = pd.DataFrame({
                X.columns[0] : XX,
                X.columns[1] : YY
            })

        for j in qual_features:
            XY[j] = 0

        XY[qual_features[i]] = 1

        p = model.predict(XY)
        p = p.reshape(xx.shape)
        
        
        # use contour plot to visualize the predictions
        axarr[i].contourf(xx, yy, p, cmap = "jet", alpha = 0.2, vmin = 0, vmax = 1)
        
        ix = X[qual_features[i]] == 1
        # plot the data
        axarr[i].scatter(x0[ix], x1[ix], c = y[ix], cmap = "jet", vmin = 0, vmax = 1) 
        
        axarr[i].set(xlabel = X.columns[0], 
                ylabel  = X.columns[1])
        
        patches = []
        for color, spec in zip(["red", "blue"], ["1", "0"]):
            patches.append(Patch(color = color, label = spec))

        plt.legend(title = "Species", handles = patches, loc = "best")
        
        plt.tight_layout()

    def prepare_data(self, df):
        y = df['Form']
        X = df.drop(['Form'], axis = 1)
        return df, X, y

    def split_data(self, df):
        train, validate, test = np.split(df.sample(frac=1, random_state=42), [int(.6*len(df)), int(.8*len(df))])
        return train, validate, test  

    def feature_combo(self, all_qual_cols, all_quant_cols, df, y): 
        for qual in all_qual_cols: 
            self.qual_cols = [col for col in df.columns if qual in col ]
            for pair in combinations(all_quant_cols, 2):
                cols = self.qual_cols + list(pair) 
                # you could train models and score them here, keeping the list of 
                # columns for the model that has the best score. 
                LR = LogisticRegression()
                LR.fit(df[cols], y)
                score = LR.score(df[cols], y)
                self.feature_score_pair[tuple(cols)] = score


    def print_confusion_matrix(self, model, X, y):
        my_matr = confusion_matrix(y, model.predict(X), normalize="true")
        fig, ax = plt.subplots(figsize=(4,4))
        ax.imshow(my_matr)
        ax.xaxis.set(ticks=(0,1), ticklabels=('Predicted False', 'Predicted True'))
        ax.yaxis.set(ticks=(0,1), ticklabels=('Actually False', 'Actually True'))
        ax.set_ylim(1.5, -0.5)

        for i in range(2):
            for j in range(2):
                ax.text(j,i, my_matr[i,j].round(3), ha='center', va='center', color='black')


    






































