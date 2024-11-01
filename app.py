import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
#from weather import get_weather
from testApi.test_api import test_get_weather # ТЕСТЫ ТЕСТЫ

app = dash.Dash(__name__)
cities = []

app.layout = html.Div([
    html.H1("Прогноз погоды"),
    html.Div(id='error-message', style={'color': 'red', 'font-weight': 'bold'}),
    html.Div([
        dcc.Input(id='city-input', type='text', placeholder='Введите название города'),
        html.Button('Добавить город', id='add-city-button', n_clicks=0),
        html.Button('Очистить города', id='clear-cities-button', n_clicks=0)
    ]),
    html.Div(id='city-list'),

    dcc.Slider(
        id='days-slider',
        min=2,
        max=5,
        value=5,
        marks={i: str(i) for i in range(2, 6)},
        step=1,
        tooltip={"placement": "bottom", "always_visible": True},
        included=False,
    ),

    dcc.Dropdown(id='variable-dropdown', options=[
        {'label': 'Температура', 'value': 'temperature'},
        {'label': 'Скорость ветра', 'value': 'windSpeed'},
        {'label': 'Влажность', 'value': 'humidityAg'},
    ], placeholder='Выберите переменную для графика'),
    dcc.Graph(id='weather-graph'),
    html.Div(id='weather-table')
])

@app.callback(
    Output('city-list', 'children'),
    Output('weather-graph', 'figure'),
    Output('weather-table', 'children'),
    Output('city-input', 'value'),
    Output('error-message', 'children'),
    Input('add-city-button', 'n_clicks'),
    Input('clear-cities-button', 'n_clicks'),
    Input('variable-dropdown', 'value'),
    Input('days-slider', 'value'),
    State('city-input', 'value')
)

def update_cities(add_clicks, clear_clicks, variable, days, city_input):
    global cities
    ctx = dash.callback_context
    error_message = ""

    if ctx.triggered and 'add-city-button' in ctx.triggered[0]['prop_id']:
        if city_input and city_input not in cities:
            cities.append(city_input)
        city_input = ''

    if ctx.triggered and 'clear-cities-button' in ctx.triggered[0]['prop_id']:
        cities = []

    figure = {}
    weather_table = ''

    if cities:
        weather_data = []
        for city in cities:
#            data = get_weather(city, days)
            data = test_get_weather(city, days) # ТЕСТЫ ТЕСТЫ ТЕСТЫ 
            if data == "error_city" or data == "error_weather": # Для test_get_api не работает 
                error_message = f"Ошибка: Не удалось получить данные для города '{city}'."
                cities.remove(city)
                continue
            weather_data.append((city, data))

        if weather_data:
            yaxis_title = ''
            if variable == 'temperature':
                yaxis_title = 'Температура (°C)'
            elif variable == 'windSpeed':
                yaxis_title = 'Скорость ветра (м/с)'
            elif variable == 'humidityAg':
                yaxis_title = 'Влажность (%)'

            traces = []
            for i, (city, data) in enumerate(weather_data):
                dates = [day['date'] for day in data]
                values = [
                    (day['temperature']['min'] + day['temperature']['max']) / 2 if variable == 'temperature'
                    else day['windSpeed'][0] if variable == 'windSpeed'
                    else day['humidityAg']
                    for day in data
                ]

                traces.append(go.Scatter(
                    x=dates,
                    y=values,
                    mode='lines+markers',
                    name=city,
                    line=dict(color=f'rgba({i * 50}, {i * 100}, {i * 150}, 1)')
                ))

            figure = {
                'data': traces,
                'layout': go.Layout(
                    title='Прогноз погоды',
                    xaxis={'title': 'Дата'},
                    yaxis={'title': yaxis_title}
                )
            }

            table_rows = [
                html.Tr([
                    html.Td(city),
                    html.Td(day['date']),
                    html.Td(day['text'][0]),
                    html.Td(f"{day['temperature']['min']} - {day['temperature']['max']} °C"),
                    html.Td(day['humidityAg']),
                    html.Td(day['windSpeed'][0]),
                ]) for city, data in weather_data for day in data
            ]

            weather_table = html.Div(
                style={'display': 'flex', 'justify-content': 'center', 'padding': '20px'},
                children=[
                    html.Table(
                        style={'borderCollapse': 'collapse', 'width': '80%', 'border': '1px solid #ddd'},
                        children=[
                            html.Thead(html.Tr([
                                html.Th("Город"), html.Th("Дата"), html.Th("Прогноз"),
                                html.Th("Температура"), html.Th("Влажность"), html.Th("Скорость ветра")
                            ])),
                            html.Tbody(table_rows)
                        ]
                    )
                ]
            )

    return ', '.join(cities), figure, weather_table, city_input, error_message


if __name__ == '__main__':
    app.run_server()
