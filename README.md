# CandideGreenInfluencer
A basic web app to show image recommendations.

# Build the venv
1. virtualenv <env_name>
2. source <env_name>/bin/activate
3. pip install -r path/to/requirements.txt

# Run the Flask app
1. Open a terminal window.
2. cd path/to/flask-backend.
3. python main.py (make sure you are using the venv detailed above).

# Run the React app
1. Open a terminal window.
2. cd path/to/react-frontend
3. npm run build

# Updates to code since Monday 29th July 2019
- Timsort-based ranking algorithm (using sorted() function) added alongside the original unoptimized bubblsort implementation - you can see & use the original bubblesort implementation by passing a different value into the 'algorithm' parameter of the ranking function.
- Code now aligns with Python PEP-8 Style Guide.
- Added Python Docstrings to functions.
- Category lists no longer display a trailing comma.
