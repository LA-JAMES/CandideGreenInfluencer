# CandideGreenInfluencer
A basic web app to show image recommendations.

# Build the venv
You shouldn't need to do this as the venv directory is included with this repo. But just in case...
virtualenv <env_name>
source <env_name>/bin/activate
pip install -r path/to/requirements.txt

To activate the given venv...
source venv/bin/activate

# Run the Flask app
Open a terminal window.
cd path/to/flask-backend.
python main.py (make sure you are using the venv detailed above).

# Run the React app
Open a terminal window.
cd path/to/react-frontend
npm run build

# Updates to code since Monday 29th July 2019
Timsort-based ranking algorithm (using sorted() function) added alongside the original unoptimized bubblesort implementation - you can see & use the original bubblesort implementation by passing a different value into the 'algorithm' parameter of the ranking function.
Code now aligns with Python PEP-8 Style Guide.
Added Python Docstrings to functions.
Category lists no longer display a trailing comma.
