DROP TABLE IF EXISTS country_statistics;
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS regions;
CREATE TABLE regions (
    region_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_name TEXT NOT NULL UNIQUE
);

CREATE TABLE Geography (
    geo_id INTEGER PRIMARY KEY,
    country_id INTEGER,
    land_area_km2 REAL,
    density_p_km2 REAL,
    agricultural_land REAL,
    forested_area REAL,
    population INTEGER,
    urban_population INTEGER,
    FOREIGN KEY(country_id) REFERENCES Country(country_id)
);
CREATE TABLE Economy (
    economy_id INTEGER PRIMARY KEY,
    country_id INTEGER,
    gdp REAL,
    minimum_wage REAL,
    tax_revenue REAL,
    total_tax_rate REAL,
    gasoline_price REAL,
    co2_emissions REAL,
    unemployment_rate REAL,
    population_labor_force_participation REAL,
    FOREIGN KEY(country_id) REFERENCES Country(country_id)
);
CREATE TABLE Education (
    education_id INTEGER PRIMARY KEY,
    country_id INTEGER,
    gross_primary_education_enrollment REAL,
    gross_tertiary_education_enrollment REAL,
    FOREIGN KEY(country_id) REFERENCES Country(country_id)
);
CREATE TABLE Health (
    health_id INTEGER PRIMARY KEY,
    country_id INTEGER,
    life_expectancy REAL,
    infant_mortality REAL,
    maternal_mortality_ratio REAL,
    physicians_per_thousand REAL,
    out_of_pocket_health_expenditure REAL,
    fertility_rate REAL,
    birth_rate REAL,
    FOREIGN KEY(country_id) REFERENCES Country(country_id)
);
DROP TABLE IF EXISTS countries;
CREATE TABLE countries (
    country_id INTEGER PRIMARY KEY,
    country TEXT,
    capital_major_city TEXT,
    largest_city TEXT,
    official_language TEXT,
    calling_code TEXT,
    currency_code TEXT,
    latitude REAL,
    longitude REAL
);
DROP TABLE IF EXISTS countries;
SELECT country, gdp
FROM Country
JOIN Economy USING(country_id)
ORDER BY gdp DESC
LIMIT 10;
SELECT AVG(life_expectancy)
FROM Health;
SELECT country,
       unemployment_rate
FROM Country
JOIN Economy USING(country_id)
ORDER BY unemployment_rate DESC;
SELECT country,
       gdp,
       life_expectancy
FROM Country
JOIN Economy USING(country_id)
JOIN Health USING(country_id);
SELECT SUM(population)
FROM Geography;
SELECT country,
       density_p_km2
FROM Country
JOIN Geography USING(country_id)
ORDER BY density_p_km2 DESC
LIMIT 10;
SELECT country,
       co2_emissions
FROM Country
JOIN Economy USING(country_id)
ORDER BY co2_emissions DESC;
SELECT AVG(gross_tertiary_education_enrollment)
FROM Education;
SELECT *
FROM Country;
SELECT latitude,
       longitude
FROM Country;
DROP TABLE IF EXISTS region;


