CREATE TABLE "location" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"country"	TEXT NOT NULL UNIQUE,
	"city"	TEXT NOT NULL,
	"lat"	REAL NOT NULL,
	"lon"	REAL NOT NULL
);
CREATE TABLE "description" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"status"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	"icon"	TEXT NOT NULL
);
CREATE TABLE "weather" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"temp"	REAL NOT NULL,
	"pressure"	REAL NOT NULL,
	"humidity"	INTEGER NOT NULL,
	"temp_min"	REAL NOT NULL,
	"temp_max"	REAL NOT NULL,
	"sea_level"	REAL,
	"grnd_level"	REAL,
	"date_time"	TEXT NOT NULL,
	"wind"	TEXT NOT NULL,
	"clouds"	INTEGER NOT NULL,
	"snow"	TEXT,
	"rain"	TEXT,
	"location_id"	INTEGER NOT NULL,
	"description_id"	INTEGER,
	FOREIGN KEY("location_id") REFERENCES "location"("id") ON DELETE CASCADE,
	FOREIGN KEY("description_id") REFERENCES "description"("id")
);


INSERT INTO "description"
("status", "description", "icon" )
VALUES
("Clouds", "overcast clouds", "04d" );

INSERT INTO "location"
("country", "city", "lat", "lon")
VALUES
("BY", "Brest", 52.09, 23.69);

INSERT INTO "weather"
(
	"temp", "pressure", "humidity",
	"temp_min", "temp_max", "sea_level",
	"grnd_level", "date_time", "wind",
	"clouds", "snow", "rain", "location_id",
	"description_id"
)
VALUES
(
	14.22, 1008.44, 76, 14.22, 14.22,
	1008.44, 991.6, "16.07.2019 19:36:00",
	'{"speed": 3.24, "deg": 246.987}',
	87, NULL, NULL, (SELECT id FROM "location" WHERE "city"="London", "country"="UK"), (SELECT id FROM "location" WHERE "status"="Clouds")
);
