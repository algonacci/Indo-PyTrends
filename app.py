import os
from flask import Flask, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)

# Initialize pytrends for Indonesia (country code: ID)
pytrends = TrendReq(hl='id-ID', tz=3600, geo='ID')


@app.route("/")
def index():
    return jsonify({
        "status": {
            "code": 200,
            "message": "Success fetching the API",
        },
        "data": None,
    }), 200


@app.route('/trending', methods=['GET'])
def get_trending_queries():
    try:
        # Get currently trending search queries in Indonesia
        trending_searches_df = pytrends.trending_searches(pn='indonesia')

        if not trending_searches_df.empty:
            trending_queries = trending_searches_df[0].tolist()
            return jsonify({
                "status": {
                    "code": 200,
                    "message": "Success fetching the trending topics in Indonesia",
                },
                "data": {
                    'trending_queries': trending_queries
                }
            }), 200
        else:
            return jsonify({
                "status": {
                    "code": 404,
                    "message": "Failed fetching the trends",
                },
                "data": {
                    'error': 'No trending queries available for Indonesia.',
                }
            }), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True,
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 8080)))
