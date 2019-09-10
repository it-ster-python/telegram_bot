CREATE TABLE "weather" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"temp"	REAL NOT NULL,
	"humidity"	INTEGER NOT NULL,
	"temp_min"	INTEGER NOT NULL,
	"temp_max"	INTEGER NOT NULL,
	"sea_level"	REAL,
	"ground_level"	REAL,
	"wind"	INTEGER NOT NULL,
	"clouds"	INTEGER NOT NULL,
	"snow"	TEXT,
	"rain"	TEXT
);

CREATE TABLE "description" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"status"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	"icon"	INTEGER NOT NULL
);

CREATE TABLE "Location" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"country"	TEXT NOT NULL UNIQUE,
	"lat"	REAL NOT NULL,
	"lon"	REAL NOT NULL
);

INSERT INTO "description"
("status", "description", "icon" )
VALUES
("Clouds", "overcast clouds", "04d")

iNSERT INTO "Location"
("country", "city", "lat", "lon" )
VALUES
("BY", "Brest", 52.09, 23.69)

iNSERT INTO "weather"
("temp", "humidity", "temp_min", "temp_max", "sea_level", "ground_level", "wind", "clouds",	"snow",	"rain" )
VALUES
(14.22, 76, 14.22, 14.22, 1008.44, 991.6, "16.07.2019 19:36:00", '{'speed': 3.24, 'deg': 246.987}', 87, NULL, NULL, (SELECT id FROM "Location" WHERE "city" = ))
