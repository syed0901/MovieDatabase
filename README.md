# MovieDatabase
Requires Windows machine with MySQL setup.
This program takes Movies directory or the movie file as input.
It makes entries in the MySQL DB for the movie files or movie files in the input directories.
If whole source is passed as input Dir, Program will refresh the complete table i.e. delete and insert again.
This program internally calls the windows batch files to import data in MySQL DB.
This program will also call IMDB API to fetch the rating of the movie and will insert in DB.
PS:This program is made for learning purpose, so there can be better ways to do this.
