#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Import der notwendigen Bibliotheken
import json
import sqlite3
import os
#import MySQLdb

conn = sqlite3.connect('/home/pi/.credentials/datenbank.db')

# Zugangsdaten importieren
with open('/home/pi/.credentials/datenbank.json') as creds:    
	credentials = json.load(creds)


# Funktion Datenbank auslesen
def lesen(tabelle, feld, start=None):
	mysql = None
	try:
		mysql = sqlite3.connect('/home/pi/.credentials/datenbank.db')
		zeiger = mysql.cursor()
		if "running" in feld:
			datenbankquery = """SELECT %s FROM %s ORDER BY id DESC LIMIT 1;"""
			zeiger.execute(datenbankquery %(feld, tabelle))
			datenraw = zeiger.fetchall()
			wert = datenraw[0]
			wert = wert[0]
			return wert
		elif "timestamp" in feld:
			if start == None:
				datenbankquery = """SELECT UNIX_TIMESTAMP(%s) FROM %s WHERE running = 2 ORDER BY id LIMIT 1 ;"""
				zeiger.execute(datenbankquery %(feld, tabelle))
				datenraw = zeiger.fetchall()
				wert = datenraw[0]
				wert = wert[0]
				return wert
			elif start == 1:
				datenbankquery = """SELECT UNIX_TIMESTAMP(%s) FROM %s ORDER BY id DESC LIMIT 1;"""
				zeiger.execute(datenbankquery %(feld, tabelle))
				datenraw = zeiger.fetchall()
				wert = datenraw[0]
				wert = wert[0]
				return wert				
		else:
			datenbankquery = """SELECT %s FROM %s WHERE id = 1;"""
			zeiger.execute(datenbankquery %(feld,tabelle))
			datenraw = zeiger.fetchall()
			wert = datenraw[0]
			if "," not in feld:
				wert = wert[0]
		return wert
	except:
		wert = None
		return wert
	finally:
		if mysql:
			mysql.close()

# Funktion Datenbank schreiben
def schreiben(tabelle, feld1, wert1, feld2=None, wert2=None, feld3=None, wert3=None, feld4=None, wert4=None):
	mysql = None
	if wert1 == None:
		wert1 = "NULL"
	if wert2 == None:
		wert2 = "NULL"
	if wert3 == None:
		wert3 = "NULL"
	if wert4 == None:
		wert4 = "NULL"
	if feld4 != None:
		query = """INSERT INTO %s (%s, %s, %s, %s) VALUES (%s,%s,%s, %s);"""
		datenbankquery = query %(tabelle, feld1, feld2, feld3, feld4, wert1, wert2, wert3, wert4)
	if feld3 != None:
		query = """INSERT INTO %s (%s, %s, %s) VALUES (%s,%s,%s);"""
		datenbankquery = query %(tabelle, feld1, feld2, feld3, wert1, wert2, wert3)
	elif feld2 !=None:
		query = """INSERT INTO %s (%s, %s) VALUES (%s,%s);"""
		datenbankquery = query %(tabelle, feld1, feld2, wert1, wert2)
	else:
		query = """INSERT INTO %s (%s) VALUES (%s);"""
		datenbankquery = query %(tabelle, feld1, wert1)
	try:
		mysql = sqlite3.connect('/home/pi/.credentials/datenbank.db')
		zeiger = mysql.cursor()
		zeiger.execute(datenbankquery)
		mysql.commit()
		fehler = 0
		return fehler
	except:
		fehler = 1
		return fehler
	finally:
		if mysql:
			mysql.close()
			
			
# Funktion Datenbankupdate
def update(tabelle, feld1, wert1, feld2=None, wert2=None, feld3=None, wert3=None, feld4=None, wert4=None):
	mysql = None
	if wert1 == None:
		wert1 = "NULL"
	if wert2 == None:
		wert2 = "NULL"
	if wert3 == None:
		wert3 = "NULL"
	if wert4 == None:
		wert4 = "NULL"
	if feld4 !=None:
		query = """UPDATE %s SET %s = %s, %s = %s, %s = %s, %s = %s ORDER BY id DESC LIMIT 1;"""
		datenbankquery = query %(tabelle, feld1, wert1, feld2, wert2, feld3, wert3, feld4, wert4)	
	if feld3 !=None:
		query = """UPDATE %s SET %s = %s, %s = %s, %s = %s ORDER BY id DESC LIMIT 1;"""
		datenbankquery = query %(tabelle, feld1, wert1, feld2, wert2, feld3, wert3)	
	if feld2 != None:
		query = """UPDATE %s SET %s = %s, %s = %s ORDER BY id DESC LIMIT 1;"""
		datenbankquery = query %(tabelle, feld1, wert1, feld2, wert2)
	else:
		query = """UPDATE %s SET %s = %s ORDER BY id DESC LIMIT 1;"""
		datenbankquery = query %(tabelle, feld1, wert1)
	try:
		mysql = sqlite3.connect('/home/pi/.credentials/datenbank.db')
		zeiger = mysql.cursor()
		zeiger.execute(datenbankquery)
		mysql.commit()
		fehler = 0
		return fehler
	except:
		fehler = 1
		return fehler
	finally:
		if mysql:
			mysql.close()
			
# Funktion Datenbank löschen
def loeschen(tabelle):	
	mysql = None
	query = """DELETE FROM %s ORDER BY id DESC LIMIT 1;"""
	datenbankquery = query %(tabelle)
	try:
		mysql = sqlite3.connect('/home/pi/.credentials/datenbank.db')
		zeiger = mysql.cursor()
		zeiger.execute(datenbankquery)
		mysql.commit()
		fehler = 0
		return fehler
	except:
		fehler = 1
		return fehler
	finally:
		if mysql:
			mysql.close()

# Funktion temporäre Datenbank erstellen
def erstelletemp():
	mysql = None
	query = """CREATE TABLE temp (id INT AUTO_INCREMENT PRIMARY KEY, strom INT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, verbrauch INT);"""
	datenbankquery = query
	try:
		mysql = sqlite3.connect('/home/pi/.credentials/datenbank.db')
		zeiger = mysql.cursor()
		zeiger.execute(datenbankquery)
		mysql.commit()
		fehler = 0
		return fehler
	except:
		fehler = 1
		return fehler
	finally:
		if mysql:
			mysql.close()
			
# Funktion temporäre Datenbank exportieren
def exporttemp():
	mysql = None
	query = """SELECT * FROM temp INTO OUTFILE '/tmp/aufzeichnung.txt' LINES TERMINATED BY '\n';"""
	datenbankquery = query
	try:	
		mysql = sqlite3.connect('/home/pi/.credentials/datenbank.db')
		zeiger = mysql.cursor()
		zeiger.execute(datenbankquery)
		mysql.commit()
		fehler = 0
		return fehler
	except:
		fehler = 1
		return fehler
	finally:
		if mysql:
			mysql.close()

# Funktion temporäre Datenbank löschen
def loeschetemp():
	if os.path.isfile('/home/pi/.credentials/datenbank.db'):
    # alte Datenbank sichern
		if os.path.isfile('/home/pi/.credentials/datenbank.db.bak'):
			os.remove('/home/pi/.credentials/datenbank.db.bak')
		os.rename('/home/pi/.credentials/datenbank.db','/home/pi/.credentials/datenbank.db.bak')
	mysql = None
	query = """SET sql_notes = 0; DROP TABLE IF EXISTS temp; SET sql_notes = 1;"""
	datenbankquery = query
	try:	
		mysql = sqlite3.connect('/home/pi/.credentials/datenbank.db')
		zeiger = mysql.cursor()
		zeiger.execute(datenbankquery)
		fehler = 0
		return fehler
	except:
		fehler = 1
		return fehler
	finally:
		if mysql:
			mysql.close()
