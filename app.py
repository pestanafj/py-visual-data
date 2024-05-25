import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc


def make_pie_charts(df):
    bins = [0, 3.5, 4, 4.5, float("inf")]
    labels = [
        "Menor que  3.5",
        "Entre 3.5 e 4",
        "Entre 4 e 4.5",
        "Maior que 4.5 ",
    ]
    colors = ["#FFD766", "#B9AC99", "#DEA68F", "#372213"]
    df["rating_category"] = pd.cut(df["average_rating"], bins=bins, labels=labels)
    ratings_counts = df["rating_category"].value_counts()
    fig_pie = px.pie(
        values=ratings_counts.values,
        names=ratings_counts.index,
        title="Distribuição das Classificações Médias dos Livros",
        color_discrete_sequence=colors,
    )
    return fig_pie


def make_line_graph(df):

    df["publication_date"] = pd.to_datetime(
        df["publication_date"], format="%m/%d/%Y", errors="coerce"
    )

    df["year"] = df["publication_date"].dt.year
    yearly_counts = df["year"].value_counts().sort_index()
    fig_line = px.line(
        yearly_counts,
        x=yearly_counts.index,
        y=yearly_counts.values,
        labels={"x": "Ano", "y": "Número de Livros"},
        title="Evolução das Publicações de Livros ao Longo do Tempo",
        template="ggplot2",
    )
    return fig_line


def make_treemap(df):
    idioma_counts = df["language_code"].value_counts()
    fig_treemap = px.treemap(
        names=idioma_counts.index,
        parents=["Livros"] * len(idioma_counts),  # Define a raiz da árvore
        values=idioma_counts.values,
        title="Distribuição de Idiomas dos Livros",
        template="ggplot2",
    )
    return fig_treemap


app = Dash(__name__)

df = pd.read_csv("data/books.csv")

app.layout = html.Div(
    [
        html.H1("Análise de Livros by GoodReads DataSet"),
        dcc.Graph(id="pie-chart", figure=make_pie_charts(df)),
        dcc.Graph(id="line-graph", figure=make_line_graph(df)),
        dcc.Graph(id="treemap", figure=make_treemap(df)),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
