from shiny import ui, App, render
from shinywidgets import output_widget, render_widget
import plotly.express as px
import pandas as pd
import seaborn as sns

exercise_df = pd.read_csv('Habit-Data/Exercise.csv')
education_df = pd.read_csv('Habit-Data/Education.csv')
yes_or_no_df = pd.read_csv('Habit-Data/YesOrNo.csv')

exercise_df_melted = exercise_df.melt(id_vars='Date', var_name='Type', value_name='Minutes')
education_df_melted = education_df.melt(id_vars='Date', var_name='Type', value_name='Minutes')

exercise_df_melted['Date'] = exercise_df_melted['Date'].astype('category')
education_df_melted['Date'] = education_df_melted['Date'].astype('category')

color_map = {
    'Lifting': '#13538A', 'Running': '#1C88CF', 'Biking': '#5BDBFD', 'Swimming': '#86EAE9',
    'Developing Technical Skills': '#1C88CF', 'Schoolwork': '#13538A', 'Read & Write': '#5BDBFD', 'Podcasts & Audiobooks': '#86EAE9'
}
color_sequence = ['#13538A', '#1C88CF', '#5BDBFD', '#86EAE9']
color_palette = {"yes": "#13538A", "no": "#5BDBFD"}

def date_range(current_df):
    last_date = current_df['Date'].iloc[-1]
    first_date = current_df['Date'].iloc[-10]
    date_range = [first_date, last_date]
    return date_range

app_ui = ui.page_fluid(
    {"class": "app-basic"},
    ui.panel_title('Habit Analytics'),
    ui.tags.style(
        """
        .app-basic {
            padding: 10px 0 20px;
            color: black;
            background-color: #5BDBFD;
            text-align: center;
        }
        """
    ),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select(
                "data", label="Data Type",
                choices=['Exercise', 'Education']
            ),
            '',
            f'Statistics',
            ''
        ),
        ui.panel_main(
            output_widget("bar_plot"),
            output_widget("pie_plot"),
            ui.output_plot("count_plot")
        ),
    ),
)

def server(input, output, session):
    @output
    @render_widget
    def bar_plot():
        if input.data() == "Exercise":
            current_df = exercise_df_melted
        elif input.data() == "Education":
            current_df = education_df_melted
        fig = px.bar(current_df, x='Date', y='Minutes', color='Type', barmode='stack', text='Minutes', color_discrete_map=color_map, title=f'Daily {input.data()} Activity')
        xaxes_range = date_range(current_df)
        fig.update_xaxes(range=xaxes_range)
        return fig
    @output
    @render_widget
    def pie_plot():
        if input.data() == "Exercise":
            current_df = exercise_df_melted
        elif input.data() == "Education":
            current_df = education_df_melted
        fig = px.pie(current_df, values='Minutes', names='Type', color_discrete_sequence=color_sequence, title=f'Total {input.data()} Distribution')
        return fig
    @output
    @render.plot
    def count_plot():
        fig = sns.countplot(data=yes_or_no_df, x='Type', hue="Value", palette=color_palette).set(title='Countplot for Daily Habits', xlabel='Habit Type', ylabel='Number of Days')
        return fig

app = App(app_ui, server)
