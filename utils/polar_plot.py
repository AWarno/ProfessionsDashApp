
import plotly.graph_objects as go

import pandas as pd
import numpy as np

from sklearn.datasets import load_iris, load_wine
from sklearn.preprocessing import MinMaxScaler

iris = load_iris()
iris_data = MinMaxScaler().fit_transform(iris.data)
iris_data = np.hstack((iris_data, iris.target.reshape(-1,1)))

iris_df = pd.DataFrame(data=iris_data, columns=[f'feature_{i}' for i in range(5)])
iris_df.head()

avg_iris  = iris_df.groupby("feature_1").mean()

def polar_plot():
    fig = go.Figure()

    colors= ["tomato", "dodgerblue"]
    names = ["average", "you"]
    for i in range(2):
        fig.add_trace(
                    go.Scatterpolar(
                                    r=avg_iris.loc[i].values.tolist() + avg_iris.loc[i].values.tolist()[:1],
                                    theta=avg_iris.columns.tolist() + avg_iris.columns.tolist()[:1],
                                    fill='toself',
                                    name=names[i],
                                    fillcolor=colors[i], line=dict(color=colors[i]),
                                    showlegend=True, opacity=0.6
                                    )
                    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                            visible=True,
                            range=[0, 1]
                        )
                ),
        title="Srenia dla wybronego zawodu vs Twój wynik"
    )
    return fig