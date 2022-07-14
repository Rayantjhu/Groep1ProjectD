# Project D

The project is prototype of a simple dashboard website that is commissioned by Alten for Chengeta Wildlife.
Rangers from the Chengeta Wildlife may use the dashboard to view various statistics and information about collected data from Raspberry Pi's, such as sounds and what the sound might be.

The goal of Project D is to look for multiple solutions to create a dashboard as efficient as possible. The chosen stack is Python with the library Streamlit. 

# Commands for running the application

### Docker command for running the containers

```
docker compose up -d
```

### Docker command for stopping the containers

```
docker compose down
```

### installation

```
pip install -r requirements.txt
conda install -c conda-forge geckodriver
```

### Running the streamlit app

```
streamlit run main.py
```

### Running the middleware

```
python middleware.py
```

### Running the tests
```
python -m unittest
```
