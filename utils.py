import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def filter_data(df: pd.DataFrame, filter_column: str, time_range_start: str, time_range_end: str):
    # Try to convert the filter_column to datetime
    try:
        df[filter_column] = pd.to_datetime(df[filter_column])
        start = pd.to_datetime(time_range_start)
        end = pd.to_datetime(time_range_end)
    except ValueError:
        # If conversion to datetime fails, try to convert the filter_column to time
        try:
            time_format = "%H:%M:%S"
            df[filter_column] = pd.to_datetime(df[filter_column], format=time_format).dt.time
            start = datetime.strptime(time_range_start, time_format).time()
            end = datetime.strptime(time_range_end, time_format).time()
        except ValueError:
            raise ValueError("Invalid format in filter_column or time_range_start/time_range_end")

    df = df[(df[filter_column] >= start) & (df[filter_column] <= end)]

    return df

def generate_chart(df: pd.DataFrame, x_column: str, y_column: str, chart_type: str):
    if chart_type == 'scatter':
        fig = px.scatter(df, x=x_column, y=y_column)
    elif chart_type == 'bar':
        fig = px.bar(df, x=x_column, y=y_column)

    # Update x and y axis labels
    fig.update_xaxes(title_text=x_column)
    fig.update_yaxes(title_text=y_column)

    return fig

def generate_insights(df: pd.DataFrame):
    insights = {}
    dataset_size = len(df)

    for column in df.columns:
        null_count = df[column].isnull().sum()

        if np.issubdtype(df[column].dtype, np.number):
            insights[column] = {
                "mean": str(round(df[column].mean(), 3)),
                "median": str(round(df[column].median(), 3)),
                "null_count": str(null_count),
            }
        else:
            insights[column] = {
                "unique_count": str(df[column].nunique()),
                "null_count": str(null_count),
            }

    return {"dataset_size": dataset_size, "column_insights": insights}


def generate_correlation_matrix(df: pd.DataFrame):
    # Calculate the correlation matrix
    corr_matrix = df.corr()

    # Create the heatmap
    fig = go.Figure(go.Heatmap(
        z=corr_matrix,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='Viridis',
        zmin=-1,
        zmax=1,
    ))

    return fig