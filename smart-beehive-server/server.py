from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)

DB_HOST = "host"
DB_USER = "name"
DB_PASSWORD = "password"  
DB_NAME = "name"

def connect_db():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

@app.route('/send_data', methods=['POST'])
def save_seonsors_data():
    try:
        data = request.get_json()
        temperature = float(data.get("temperature").replace("C", "").strip()) if "C" in data.get("temperature") else None
        pressure = float(data.get("pressure").replace("hPa", "").strip()) if "hPa" in data.get("pressure") else None
        humidity = float(data.get("humidity").replace("%", "").strip()) if "%" in data.get("humidity") else None
        co2_level = float(data.get("co2_level"))
        weight = float(data.get("weight"))
        distance = float(data.get("distance"))
        rain_percentage = float(data.get("rain_percentage"))

    except:
        return jsonify({"error": str(e)}), 500 

    try:
        connection = connect_db()
        with connection.cursor() as cursor:
            sql = "INSERT INTO sensors_data (temperature, pressure, humidity, co2_level, weight, distance, rain_percentage) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (temperature, pressure, humidity, co2_level, weight, distance, rain_percentage))
        connection.commit()
        connection.close()

        return jsonify({"message": "Value saved successfully"}), 200
    except Exception as e:
        print(f"Database error: {str(e)}")

        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
