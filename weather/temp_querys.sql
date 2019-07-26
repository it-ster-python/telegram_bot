CREATE TABLE "location" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"contry_name"	TEXT NOT NULL UNIQUE,
	"city_name"	TEXT NOT NULL,
	"contry_code"	TEXT NOT NULL UNIQUE,
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
	"grand_level"	REAL,
	"date_time"	TEXT NOT NULL,
	"wind"	TEXT NOT NULL,
	"clouds"	INTEGER NOT NULL,
	"snow"	TEXT,
	"rain"	TEXT
"location_id" INTEGER,
 "description_id" INTEGER NOT NULL,
 FOREIGN KEY("location_id") REFERENCES "location"("id") ON DELETE CASCADE,
 FOREIGN KEY("description_id") REFERENCES "description"("id"),
);


INSERT INTO "description" (
"status",
"description",
"icon"
) VALUE ("Clouds", "overcast cluds", "04d");
INSERT INTO "location" (
"contry",
"city",
"lat",
"lon",)
VALUE ("BY", "Brest", 52.09, 23.69);
INSERT INTO "weather" ("temp","pressure","humidity","temp_min","temp_max","sea_level","grand_level","date_time","wind","clouds","snow","rain")
VALUES (14.22, 1008/44, 76, 14.22, 14.22, 1008.44, 991.6, "16.07.2019 19:36:00" '{"speed" : 3.24, "deg": 246.987}', 87, NULL, NULL, (SELECT id FROM location where "city" = "London", country = "UK"), (SELECT id FROM location where "status" = "clouds)
