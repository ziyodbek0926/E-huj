# Django Project Setup

```bash
git clone <repository-url>
cd <repository-folder>
```
# Set up a virtual environment

* ***Create a virtual environment for the project:***

```bash
python -m venv venv
```
# Activate the virtual environment

* ***Windows:***


```bash
source venv/bin/activate
```
* ***macOS/Linux:***
```bash
venv\\Scripts\\activate
```
# Activate the virtual environment
* ***Install the required dependencies using pip: ***

```bash
pip install -r requirements.txt
```

# Run the project
* ***Make sure to apply migrations first if you haven’t done that already:***

```bash
python manage.py migrate
```

* ***Then, run the server:***

```bash
python manage.py runserver
```

# Deactivate the virtual environment
* ***Once you’re done, deactivate the virtual environment with:***

```bash
deactivate
```