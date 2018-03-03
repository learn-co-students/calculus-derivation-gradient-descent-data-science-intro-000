import plotly
from plotly.offline import iplot, init_notebook_mode
from plotly import tools
init_notebook_mode(connected=True)

def trace(data, mode = 'markers', name="data"):
    x_values = list(map(lambda point: point['x'],data))
    y_values = list(map(lambda point: point['y'],data))
    return {'x': x_values, 'y': y_values, 'mode': mode, 'name': name}

def line_function_trace(line_function, x_values, mode = 'line', name = 'line function'):
    values = line_function_data(line_function, x_values)
    values.update({'mode': mode, 'name': name})
    return values

def line_function_data(line_function, x_values):
    y_values = list(map(lambda x: line_function(x), x_values))
    return {'x': x_values, 'y': y_values}

def m_b_data(m, b, x_values):
    y_values = list(map(lambda x: m*x + b, x_values))
    return {'x': x_values, 'y': y_values}

# def error_line(x_values, y_values, m, b, x):
#     y_hat = m*x + b
#     x_value = point['x']
#     y = y_actual()
#     name = 'error at ' + str(x_value)
#     return {'x': [x, x], 'y': [y, y_hat], 'mode': 'line', 'marker': {'color': 'red'}, 'name': name}
#
# def error_lines(regression_line, points):
#     return list(map(lambda point: error_line(regression_line, point), points))

def plot(traces, layout = {}):
    if not isinstance(traces, list): raise TypeError('first argument must be a list.  Instead is', traces)
    plotly.offline.iplot({'data': traces, 'layout': layout})

def build_layout(x_range = None, y_range = None, options = {}):
    layout = {}
    if isinstance(x_range, list): layout.update({'xaxis': {'range': x_range}})
    if isinstance(y_range, list): layout.update({'yaxis': {'range': y_range}})
    layout.update(options)
    return layout

def squared_error(x, points, m, b):
    return (y(x, points) - (m*x + b))**2

def rss(points, m, b):
    squared_errors = list(map(lambda point: squared_error(point['x'], points, m, b), points))
    return sum(squared_errors)

def build_tangent_line(original_function, x, line_length = 5, delta = .01):
    curve_at_point = derivative_at(original_function, x, delta)
    slope = curve_at_point['slope']
    x_minus = x - line_length
    x_plus = x + line_length
    y = original_function(x)
    y_minus = y - slope * line_length
    y_plus = y + slope * line_length
    text = '    slope:' + format(slope, '.2f')
    return {'x': [x_minus, x, x_plus], 'y': [y_minus, y, y_plus], 'mode': 'lines+text', 'text': [text], 'textposition': 'right'}

def derivative_at(original_function, x, delta = .01):
    numerator = original_function(x + delta) - original_function(x)
    slope = numerator/delta
    return {'value': x, 'slope': slope}

def m_b_trace(m, b, x_values, mode = 'line', name = 'line function'):
    values = m_b_data(m, b, x_values)
    values.update({'mode': mode, 'name': name})
    return values

# def build_cost_curve_tangent_line(b, m, points, line_length = 5):
#     curve_at_point = cost_curve_at(b, m, points)
#     slope = curve_at_point['slope']
#     b_minus = b - line_length
#     b_plus = b + line_length
#     rss_exact = curve_at_point['rss']
#     rss_minus = rss_exact - slope * line_length
#     rss_plus = rss_exact + slope * line_length
#     text = '    slope:' + format(slope, '.2f')
#     return {'x': [b_minus, b, b_plus], 'y': [rss_minus, curve_at_point['rss'], rss_plus], 'mode': 'lines+text', 'text': [text], 'textposition': 'right'}

def cost_chart_b(points, m, b_values):
    rss_values = list(map(lambda b: rss(points, m, b), b_values))
    return {'b_values': b_values, 'rss_values': rss_values}

def cost_curve_at(b, m, points):
    delta = .01
    base_rss = rss(points, m, b)
    numerator = rss(points, m, b + delta) - base_rss
    slope = numerator/delta
    return {'b': b,'rss': base_rss, 'slope': slope}

def trace_values(x_values, y_values, mode = 'markers', name="data", text = []):
    return {'x': x_values, 'y': y_values, 'mode': mode, 'name': name, 'text': text}

def plot_side_by_side(left_trace, right_trace):
    fig = tools.make_subplots(rows=1, cols=2)
    fig.append_trace(left_trace, 1, 1)
    fig.append_trace(right_trace, 1, 2)
    plotly.offline.iplot(fig)
# next to build out is a cost function table
# https://plot.ly/python/table/

# followed by a cost function graph
# https://plot.ly/python/table/
