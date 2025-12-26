/api/models contains __init__.py and one file for each entity
-__init__.py: extensions initialization, like SQLAlchemy()
-stanza.py: defines the DB structure (columns and data types) for the room entity
-stato.py: defines the DB structure (columns and data types) for the status entity
-programma.py: defines the DB structure (columns and data types) for the schedule entity
-pianta_programma.py: defines the DB structure (columns and data types) for the plant-schedule association entity
-pianta.py: defines the DB structure (columns and data types) for the plant entity (header, detail and sensors details)
-pianta_storico.py: defines the DB structure (columns and data types) for the plants history entity