# api
import requests
response = requests.get("https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults=100&compact=true&verbose=false&key=93b912b5-9d70-4b1f-960b-fb80a4c9c017")
responsejson  = response.json()

# import modules

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
#from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np
import plotly.express as px
#import plotly.graph_objects as go
import streamlit as st

cars = pd.read_pickle('cars.pkl')


def carsy():
    # df <
    
    # Eerst numerieke kolommen schoonmaken
    cars2 = cars.copy()
    cars2['catalogusprijs'] = pd.to_numeric(cars2['catalogusprijs'], errors='coerce')
    cars2['massa_ledig_voertuig'] = pd.to_numeric(cars2['massa_ledig_voertuig'], errors='coerce')
    cars2['vermogen_massarijklaar'] = pd.to_numeric(cars2['vermogen_massarijklaar'], errors='coerce')
    cars2['lengte'] = pd.to_numeric(cars2['lengte'], errors='coerce')
    cars2['breedte'] = pd.to_numeric(cars2['breedte'], errors='coerce')
    cars2['hoogte_voertuig'] = pd.to_numeric(cars2['hoogte_voertuig'], errors='coerce')
    
    # Verwijder rijen zonder prijs of met veel missende waarden
    cars2 = cars2.dropna(subset=['catalogusprijs', 'massa_ledig_voertuig', 'vermogen_massarijklaar'])
    
    # Feature selectie
    X = cars2[['massa_ledig_voertuig', 'vermogen_massarijklaar', 'lengte', 'breedte', 'hoogte_voertuig']]
    y = cars2['catalogusprijs']
    
    X = X.dropna()
    y = y.loc[X.index]
    
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # model --> andere models laten hetzelfde zien
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # prediction
    y_pred = model.predict(X_test)
    
    # Evaluatie
    #print("R²:", r2_score(y_test, y_pred))
    #print("MAE:", mean_absolute_error(y_test, y_pred))
    
    # Coëfficiënten
    coef_df = pd.DataFrame({
        "Feature": X.columns,
        "Coefficient": model.coef_
    })
    
    # plot
    plot_df = pd.DataFrame({
        "Actual Price": y_test,
        "Predicted Price": y_pred
    })
    
    plot_df["Error Value"] = np.abs(plot_df["Predicted Price"] - plot_df["Actual Price"])
    
    fig = px.scatter(
        plot_df,
        x="Actual Price",
        y="Predicted Price",    
        color="Error Value", 
        color_continuous_scale="RdYlGn_r", 
        opacity=0.6,
        title="Predicted vs. Actual Car Prices"
    )
    
    fig.add_scatter(
        x=[y_test.min(), y_test.max()],
        y=[y_test.min(), y_test.max()],
        mode="lines",
        name="Regression Line",
        line=dict(dash="dot")
    )
    
    fig.update_layout(
        xaxis_title="Actual Price (in €)",
        yaxis_title="Predicted Price (in €)",
        legend_title=None
    )

    fig.update_yaxes(range=[0,150000])
    

    return st.plotly_chart(fig, use_container_width=True)
