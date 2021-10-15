# flask pokeapi

# Run Local
* pip install -r requirements.txt
* export FLASK_APP=hello
* flask run
* Open in your browser -> http://localhost:5000

# Run Docker
* Build the image -> docker build -t pokeapi .
* Run the container -> docker run -p 5001:5000 -d pokeapi
* Open in your browser -> http://localhost:5001