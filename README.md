# Things that you'll need to do before running anything

1. Set up your Anaconda environment with `conda create -n Travola_Flask python=3.7`.

2. Install all the required packages using `pip install -r requirements.txt`. Make sure you've navigated your terminal to the repository directory first.

3. You'll need to configure your own Environment Variables in a  `.env` file. Variables currently required:

#### Flask
- `FLASK_APP='start'`
- `FLASK_ENV='development'`
- `FLASK_DEBUG=1`

#### PostgreSQL Database
- DATABASE_URL='postgres://localhost:5432/Travola_DB' 
- DB_TIMEOUT=300
- DB_POOL=5

4. You'll also need to have a PostgreSQL server running on your machine, since the Flask infrastructure needs it to be there.
