Tai Thurber
Music App Project

- Required libraries: spotipy, matplotlib, numpy, python-dateutil

- export SPOTIPY_CLIENT_ID='0e74cbd0f44c483ebaa65da4d27df74e'
- export SPOTIPY_REDIRECT_URI='http://localhost:3000'

Goal:
- Graph a user's changing music taste over time

Structure:
- List of "liked song" objects
    - Attributes
        - Date added
        - Name
        - Features
    - Can return a "data point"
        - x: date added
        - y: feature
- Features that can be graphed:
    - Scatterplot
        - Acousticness
        - Danceability
        - Duration (milliseconds)
        - Energy
        - Instrumentalness
        - Liveness
        - Loudness (decibels, between 0 and -60)
        - Speechiness
        - Tempo (beats per minute)
        - Valence
    - Bar graph
        - Key (pitch class notation)

