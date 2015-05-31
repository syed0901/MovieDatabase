@ECHO OFF
SET MYSQL_EXE="C:\xampp\mysql\bin\mysql.exe"
SET DB_USER=ROOT here
SET DB_PWD=PASSWORD here
SET DB_DATABASE=DB name here

CALL %MYSQL_EXE% --user=%DB_USER% --password=%DB_PWD% --database=%DB_DATABASE% < C:\Users\srizvi\Projects\MovieDatabase\movie_delete.sql
IF %ERRORLEVEL% NEQ 0 ECHO Error executing SQL file
