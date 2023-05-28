################################################################################
# Plotly basics
################################################################################

import plotly
import plotly.express as px

def main():
    # Basic figure
    fig = px.bar(x=list('abc'), y=[1,2,3])
    assert isinstance(fig, plotly.graph_objs.Figure)

    # Lots of different types of built in charts

    # Saving
    fig.write_html('first_figure.html')

if __name__ == '__main__':
    main()
