# Label A Auto Parts API

## Tech Goodies

- Python (Django Magic Wand)
- Database: SQLite (for convenience in development)
- ORM: Django ORM (Our Really Marvelous tool)

## Setup Guide - Getting the Magic Started

### Ingredients Needed

- Python (3.x for the latest enchantment)
- pip (Python potion installer)

### Casting the Spell

1. Clone the spellbook (repository):

   ```bash
   git clone <https://github.com/skb-ahmd/LableA-backend>
   cd <labela_backend_assignment>

2. Create seperate world (Docker)
   ```bash
   docker run -p 8000:80 -d autocompany

## or

2. Create and activate the mystical venv:
   ```bash
    python -m venv venv
    venv\scripts\activate  # For our wizardly Windows users
   
3. Cast the install spell to gather the magic components:
    ```bash
    pip install -r requirements. txt

4. Sprinkle some magic dust - Seed the realm with dummy data:
   ```bash
   python manage.py seed autoparts --number=15

5. Unleash the magic - Run the enchanting server:
   ```bash
   python manage.py runserver

## Postman Collection - The Magical Map
### All the secrets to reach different realms are stored in the Postman Collection. Import this mystical map into your Postman to explore the magical endpoints.

## Concluding the Spell
### And there you have it, a potion to make the Label A Auto Parts API come alive! Explore the realms, cast your spells wisely, and have a magical coding journey! 🧙‍♂️✨
