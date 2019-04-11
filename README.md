# Remember to use `git checkout -b <new_branch_name>` before starting work on anything. Committing directly to `master` is to invite the Gods of Chaos into our world

## Things that you'll need to do before running anything

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

4. You'll also need to have a PostgreSQL server running on your machine, since the Flask infrastructure needs it to be there. Don't forget to use `python migrate.py` to create all the required tables and fields in the DB before trying to use it.
