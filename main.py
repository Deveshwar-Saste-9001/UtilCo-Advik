from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
import json

app = Flask(__name__)


data = {
    "Date": ["1/7/2024", "2/7/2024", "3/7/2024", "4/7/2024", "5/7/2024", "6/7/2024", "7/7/2024",
             "8/7/2024", "9/7/2024", "10/7/2024", "11/7/2024", "12/7/2024", "13/7/2024", "14/7/2024", "15/7/2024"],
    "Daily_kg_CO2_6Hrs": [17, 25, 21, 29, 25, 17, 29, 25, 21, 25, 29, 21, 25, 29, 17],
    "Daily_kg_CO2_4Hrs": [11, 17, 14, 20, 17, 11, 20, 17, 14, 17, 20, 14, 17, 20, 11],
    "Daily_kg_CO2_5Hrs": [14, 21, 18, 25, 21, 14, 25, 21, 18, 21, 25, 18, 21, 25, 14]
}



year1_data = {
    'AC': [100, 150, 120, 200, 140, 160, 180, 150, 220, 190, 140, 170],
    'TV': [80, 100, 70, 150, 110, 130, 140, 120, 180, 150, 100, 120],
    'Fridge': [60, 80, 50, 100, 80, 90, 100, 90, 140, 120, 80, 100],
    'Dishwasher': [50, 60, 40, 80, 60, 70, 80, 60, 100, 80, 50, 60],
    'Geyser': [40, 50, 30, 60, 50, 60, 70, 50, 80, 70, 40, 50]
}

year2_data = {
     'AC': [120, 160, 140, 220, 160, 180, 200, 170, 240, 210, 160, 190],
    'TV': [100, 120, 90, 180, 130, 150, 160, 140, 200, 170, 120, 140],
    'Fridge': [70, 90, 60, 120, 100, 110, 120, 100, 160, 140, 90, 110],
    'Dishwasher': [60, 70, 50, 100, 80, 90, 100, 80, 120, 100, 60, 70],
    'Geyser': [50, 60, 40, 80, 60, 70, 80, 60, 100, 90, 50, 60]
}
category_colors = {
    'AC': 'rgb(55, 83, 109)',  # Blue
    'TV': 'rgb(26, 118, 255)',  # Light Blue
    'Fridge': 'rgb(255, 99, 132)',  # Red
    'Dishwasher': 'rgb(75, 192, 192)',  # Green
    'Geyser': 'rgb(153, 102, 255)',  # Purple
   
}

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
def calculate_yearly_data(data):
    total_sum = sum(sum(values) for values in data.values())
    return total_sum

df = pd.DataFrame(data)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/reward')
def reward():
    return render_template('reward.html')
@app.route('/green_audits')
def green_audit():
    return render_template('greenaudits.html')

@app.route('/update_graph', methods=['POST'])
def update_graph():
    slider_value = int(request.json['slider_value'])
    column_name = f"Daily_kg_CO2_{slider_value}Hrs"
    y_values = df[column_name].tolist()

    
    fig = go.Figure(data=[
        go.Bar(x=df["Date"], y=y_values, text=y_values, textposition='auto',  marker=dict(color='#2d4a65'))
    ])
    fig.update_layout(
        height=300,  
        width=550,   
        plot_bgcolor='rgba(0, 0, 0,0)',
        paper_bgcolor='rgba(0, 0, 0,0)',
        font=dict(color='darkblue'),
        xaxis_title="Date",
        yaxis_title="Daily kg of CO2",
        template="plotly_white",
        title=None,
        margin=dict(t=10, b=20, l=40, r=10)   
    )
    return jsonify(graph_json=fig.to_json(), config={'displayModeBar': False})


@app.route("/update_report", methods=["POST"])
def update_report():
    try:
        selected_year = request.json.get("year", "Year1")
        data = year1_data if selected_year == "Year1" else year2_data
        years_totals = calculate_yearly_data(data)
        # Create a stacked bar chart
        fig = go.Figure()

      
        for category, values in data.items():
            fig.add_trace(go.Bar(
                name=category,
                x=months,
                y=values,
                marker_color=category_colors.get(category, 'rgb(204, 204, 204)')  # Default to grey if color not found
            ))
        # Layout updates
        fig.update_layout(
            height=550,  
            width=750,   
            plot_bgcolor='rgba(0, 0, 0,0)',
            paper_bgcolor='rgba(0, 0, 0,0)',
            font=dict(color='white'),
            margin=dict(t=10, b=20, l=40, r=10), 
            barmode="stack",  # Stacked bars for each month
            xaxis_title="Months",
            yaxis_title="kWh",
            legend_title="Devices",
            title=None
        )

        # Convert the plot to JSON
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        response = {
            "graph": graph_json,
            "calculated_data": years_totals
            }
        return jsonify(response)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}, config={'displayModeBar': False}), 500
if __name__ == '__main__':
    app.run(debug=True)