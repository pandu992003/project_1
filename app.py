from flask import Flask, request, jsonify, send_file
import pandas as pd

app = Flask(__name__)

# Load datasets
student_file = r'reference.xlsx'
bus_file = r'Bus Details.xlsx'

student_df = pd.read_excel(student_file)
bus_df = pd.read_excel(bus_file)

# Serve the HTML file for the root route
@app.route('/')
def home():
    return send_file('index.html')  # Ensure the file is in the same directory

@app.route('/find-route', methods=['GET'])
def find_route():
    roll_number = request.args.get('rollNumber')

    # Validate input
    if not roll_number:
        return jsonify({'error': 'Registered number is required!'})

    # Find student details
    student = student_df[student_df['Registered Number'] == roll_number]
    if student.empty:
        return jsonify({'error': 'Registered number not found!'})

    # Match bus details based on student address
    student_address = student.iloc[0]['Student Address']
    bus_route = bus_df[bus_df['Covered Areas'].str.contains(student_address, na=False, case=False)]

    if bus_route.empty:
        return jsonify({'error': 'No bus route found for the given address!'})

    # Return route details
    route = bus_route.iloc[0]
    return jsonify({
        'routeNumber': int(route['Route Number']),
        'routeName': route['Route Name'],
        'fee': int(route['Fee'])
    })

if __name__ == '__main__':
    app.run(debug=True)