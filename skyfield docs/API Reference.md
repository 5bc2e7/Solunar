# API Reference

Quick links to the sections below:
*   [Version](#version)
*   [Opening files](#opening-files)
*   [Time scales](#time-scales)
*   [Time objects](#time-objects)
*   [Time utilities](#time-utilities)
*   [Vector functions](#vector-functions)
*   [Planetary ephemerides](#planetary-ephemerides)
*   [Planetary magnitudes](#planetary-magnitudes)
*   [Planetary reference frames](#planetary-reference-frames)
*   [Almanac](#almanac)
*   [Geographic locations](#geographic-locations)
*   [Kepler orbits](#kepler-orbits)
*   [Kepler orbit data](#kepler-orbit-data)
*   [Earth satellites](#earth-satellites)
*   [Stars and other distant objects](#stars-and-other-distant-objects)
*   [Astronomical positions](#astronomical-positions)
*   [Reference frames](#reference-frames)
*   [Constellations](#constellations)
*   [Searching](#searching)
*   [Osculating orbital elements](#osculating-orbital-elements)
*   [Units](#units)
*   [Trigonometry](#trigonometry)

## Version

Skyfield offers a tuple `skyfield.VERSION` that lets your code determine the installed version of Skyfield.

```python
import skyfield
print(skyfield.VERSION)
```

See [Checking your Skyfield version](https://rhodesmill.org/skyfield/checking-version.html).

## Opening files

```python
# File you already have.
from skyfield.api import load_file
planets = load_file('~/Downloads/de405.bsp')
```

| `load_file`(path) | Open a file on your local drive, using its extension to guess its type. |
|---|---|

```python
# File you want Skyfield to download automatically.
from skyfield.api import load
ts = load.timescale()
planets = load('de405.bsp')
```

| `Loader`(directory[, verbose, expire]) | A tool for downloading and opening astronomical data files. |
|---|---|
| `Loader.build_url`(filename) | Return the URL Skyfield will try downloading for a given filename. |
| `Loader.days_old`(filename) | Return how recently `filename` was modified, measured in days. |
| `Loader.download`(url[, filename, backup]) | Download a file, even if it’s already on disk; return its path. |
| `Loader.path_to`(filename) | Return the path to `filename` in this loader’s directory. |
| `Loader.timescale`([delta_t, builtin]) | Return a `Timescale` built using official Earth rotation data. |
| `Loader.tle_file`(url[, reload, filename, ts, …]) | Load and parse a TLE file, returning a list of Earth satellites. |

## Time scales

A script will typically start by building a single Skyfield `Timescale` to use for all date and time conversions:

```python
from skyfield import api
ts = api.load.timescale()
```

Its methods are:

| `Timescale.now`() | Return the current date and time as a `Time` object. |
|---|---|
| `Timescale.from_datetime`(datetime) | Return a `Time` for a Python `datetime`. |
| `Timescale.from_datetimes`(datetime_list) | Return a `Time` for a list of Python `datetime` objects. |
| `Timescale.utc`(year[, month, day, hour, …]) | Build a `Time` from a UTC Calendar date. |
| `Timescale.tai`([year, month, day, hour, …]) | Build a `Time` from an International Atomic Time Calendar date. |
| `Timescale.tai_jd`(jd[, fraction]) | Build a `Time` from an International Atomic Time Julian date. |
| `Timescale.tt`([year, month, day, hour, …]) | Build a `Time` from a Terrestrial Time Calendar date. |
| `Timescale.tt_jd`(jd[, fraction]) | Build a `Time` from a Terrestrial Time Julian date. |
| `Timescale.J`(year) | Build a `Time` from a Terrestrial Time Julian year or array. |
| `Timescale.tdb`([year, month, day, hour, …]) | Build a `Time` from a Barycentric Dynamical Time Calendar date. |
| `Timescale.tdb_jd`(jd[, fraction]) | Build a `Time` from a Barycentric Dynamical Time Julian date. |
| `Timescale.ut1`([year, month, day, hour, …]) | Build a `Time` from a UT1 Universal Time Calendar date. |
| `Timescale.ut1_jd`(jd) | Build a `Time` from a UT1 Universal Time Julian date. |
| `Timescale.from_astropy`(t) | Build a Skyfield `Time` from an AstroPy time object. |
| `Timescale.linspace`(t0, t1[, num]) | Return `num` times spaced uniformly between `t0` to `t1`. |

## Time objects

The `Time` class is Skyfield’s way of representing either a single time, or a whole array of times. The same time can be represented in several different time scales.

| `t.tai` | International Atomic Time (TAI) as a Julian date. |
|---|---|
| `t.tt` | Terrestrial Time (TT) as a Julian date. |
| `t.J` | Terrestrial Time (TT) as floating point Julian years. |
| `t.tdb` | Barycentric Dynamical Time (TDB) as a Julian date. |
| `t.ut1` | Universal Time (UT1) as a Julian date. |

A couple of offsets between time scales are also available.

| `t.delta_t` | Difference TT − UT1 in seconds. |
|---|---|
| `t.dut1` | Difference UT1 − UTC in seconds. |

Other time scales and conversions are available through its methods.

| `Time.utc_jpl`() | Convert to a string like `A.D.2014-Jan-18 01:35:37.5000 UTC`. |
|---|---|
| `Time.utc_iso`([delimiter, places]) | Convert to an ISO 8601 string like `2014-01-18T01:35:38Z` in UTC. |
| `Time.utc_strftime`([format]) | Format the UTC time using a Python datetime formatting string. |
| `Time.utc_datetime`() | Convert to a Python `datetime` in UTC. |
| `Time.utc_datetime_and_leap_second`() | Convert to a Python `datetime` in UTC, plus a leap second value. |
| `Time.astimezone`(tz) | Convert to a Python `datetime` in a particular timezone `tz`. |
| `Time.astimezone_and_leap_second`(tz) | Convert to a Python `datetime` and leap second in a timezone. |
| `Time.toordinal`() | Return the proleptic Gregorian ordinal of the UTC date. |
| `Time.tai_calendar`() | TAI as a (year, month, day, hour, minute, second) Calendar date. |
| `Time.tt_calendar`() | TT as a (year, month, day, hour, minute, second) Calendar date. |
| `Time.tdb_calendar`() | TDB as a (year, month, day, hour, minute, second) Calendar date. |
| `Time.ut1_calendar`() | UT1 as a (year, month, day, hour, minute, second) Calendar date. |
| `Time.tai_strftime`([format]) | Format TAI with a datetime strftime() format string. |
| `Time.tt_strftime`([format]) | Format TT with a datetime strftime() format string. |
| `Time.tdb_strftime`([format]) | Format TDB with a datetime strftime() format string. |
| `Time.ut1_strftime`([format]) | Format UT1 with a datetime strftime() format string. |
| `Time.M` | 3×3 rotation matrix: ICRS → equinox of this date. |
| `Time.MT` | 3×3 rotation matrix: equinox of this date → ICRS. |
| `Time.gmst` | Greenwich Mean Sidereal Time (GMST) in hours. |
| `Time.gast` | Greenwich Apparent Sidereal Time (GAST) in hours. |
| `Time.nutation_matrix`() | Compute the 3×3 nutation matrix N for this date. |
| `Time.precession_matrix`() | Compute the 3×3 precession matrix P for this date. |
| `Time.to_astropy`() | Return an AstroPy object representing this time. |

## Time utilities

| `compute_calendar_date`(jd_integer[, …]) | Convert Julian day `jd_integer` into a calendar (year, month, day). |
|---|---|

## Vector functions

The common API shared by planets, Earth locations, and Earth satellites.

| `VectorFunction` | Given a time, computes a corresponding position. |
|---|---|
| `VectorFunction.at`(t) | At time `t`, compute the target’s position relative to the center. |

Either adding two vector functions `v1 + v2` or subtracting them `v1 - v2` produces a new function of time that, when invoked with `.at(t)`, returns the sum or difference of the vectors returned by the two functions.

## Planetary ephemerides

By downloading a `SpiceKernel` file, Skyfield users can build vector functions predicting the positions of the Moon, Sun, and planets. See [Planets and their moons: JPL ephemeris files](https://rhodesmill.org/skyfield/planets.html).

| `SpiceKernel`(path) | Ephemeris file in NASA .bsp format. |
|---|---|
| `SpiceKernel.close`() | Close this ephemeris file. |
| `SpiceKernel.names`() | Return all target names that are valid with this kernel. |
| `SpiceKernel.decode`(name) | Translate a target name into its integer code. |

Kernels also support lookup using the Python `kernel['Mars']` syntax, in which case they return a function of time that returns vectors from the Solar System barycenter to the named body.

## Planetary magnitudes

`skyfield.magnitudelib.planetary_magnitude`(_position_)
Given the position of a planet, return its visual magnitude.

```python
>>> from skyfield.api import load
>>> from skyfield.magnitudelib import planetary_magnitude
>>> ts = load.timescale()
>>> t = ts.utc(2020, 7, 31)
>>> eph = load('de421.bsp')
>>> astrometric = eph['earth'].at(t).observe(eph['jupiter barycenter'])
>>> print('%.2f' % planetary_magnitude(astrometric))
-2.73
```

The formulae are from Mallama and Hilton “Computing Apparent Planetary Magnitude for the Astronomical Almanac” (2018). Two of the formulae have inherent limits:
*   Saturn’s magnitude is unknown and the function will return `nan` (the floating-point value “Not a Number”) if the “illumination phase angle” — the angle of the vertex observer-Saturn-Sun — exceeds 6.5°.
*   Neptune’s magnitude is unknown and will return `nan` if the illumination phase angle exceeds 1.9° and the position’s date is before the year 2000.

And one formula is not fully implemented (though contributions are welcome!):
*   Skyfield does not compute which features on Mars are facing the observer, which can introduce an error of ±0.06 magnitude.

## Planetary reference frames

| `PlanetaryConstants` | Planetary constants manager. |
|---|---|
| `Frame` | Planetary constants frame, for building rotation matrices. |

## Almanac

Routines to search for events like sunrise, sunset, and Moon phase.

| `find_risings`(observer, target, start_time, …) | Return the times at which a target rises above the eastern horizon. |
|---|---|
| `find_settings`(observer, target, start_time, …) | Return the times at which a target sets below the western horizon. |
| `find_transits`(observer, target, start_time, …) | Return the times at which a target transits across the meridian. |
| `seasons`(ephemeris) | Build a function of time that returns the quarter of the year. |
| `moon_phase`(ephemeris, t) | Return the Moon phase 0°–360° at time `t`, where 180° is Full Moon. |
| `moon_phases`(ephemeris) | Build a function of time that returns the moon phase 0 through 3. |
| `moon_nodes`(ephemeris) | Build a function of time that identifies lunar nodes. |
| `oppositions_conjunctions`(ephemeris, target) | Build a function to find oppositions and conjunctions with the Sun. |
| `meridian_transits`(ephemeris, target, topos) | Build a function of time for finding when a body transits the meridian. |
| `sunrise_sunset`(ephemeris, topos) | Build a function of time that returns whether the Sun is up. |
| `dark_twilight_day`(ephemeris, topos) | Build a function of time returning whether it is dark, twilight, or day. |
| `risings_and_settings`(ephemeris, target, topos) | Build a function of time that returns whether a body is up. |

| `lunar_eclipses`(start_time, end_time, eph) | Return the lunar eclipses between `start_time` and `end_time`. |
|---|---|

## Geographic locations

Skyfield supports two Earth datums for translating between latitude/longitude and Cartesian coordinates. They each use a slightly different estimate of the Earth’s oblateness. The most popular is WGS84, which is used by the world’s GPS devices:
*   `wgs84`
*   `iers2010`

Each datum offers a method for taking a latitude and longitude and returning a `GeographicPosition` that knows its position in space:

| `Geoid.latlon`(latitude_degrees, longitude_degrees) | Return a `GeographicPosition` for a given latitude and longitude. |
|---|---|

Going in the other direction, there are several methods for converting an existing Skyfield position into latitude, longitude, and height:

| `Geoid.latlon_of`(position) | Return the latitude and longitude of a `position`. |
|---|---|
| `Geoid.height_of`(position) | Return the height above the Earth’s ellipsoid of a `position`. |
| `Geoid.geographic_position_of`(position) | Return the `GeographicPosition` of a `position`. |
| `Geoid.subpoint_of`(position) | Return the point on the ellipsoid directly below a `position`. |

Once you have used either of the above approaches to build a `GeographicPosition`, it offers several methods:

| `GeographicPosition.at`(t) | At time `t`, compute the target’s position relative to the center. |
|---|---|
| `GeographicPosition.lst_hours_at`(t) | Return the Local Apparent Sidereal Time, in hours, at time `t`. |
| `GeographicPosition.refract`(altitude_degrees, …) | Predict how the atmosphere will refract a position. |
| `GeographicPosition.rotation_at`(t) | Compute rotation from GCRS to this location’s altazimuth system. |

## Kepler orbits

See [Kepler Orbits](https://rhodesmill.org/skyfield/kepler-orbits.html) for computing the positions of comets, asteroids, and other minor planets.

## Kepler orbit data

| `load_mpcorb_dataframe`(fobj) | Parse a Minor Planet Center orbits file into a Pandas dataframe. |
|---|---|
| `load_comets_dataframe`(fobj) | Parse a Minor Planet Center comets file into a Pandas dataframe. |
| `load_comets_dataframe_slow`(fobj) | Parse a Minor Planet Center comets file into a Pandas dataframe. |

## Earth satellites

By downloading TLE satellite element sets, Skyfield users can build vector functions that predict their positions. See [Earth Satellites](https://rhodesmill.org/skyfield/earth-satellites.html).

| `EarthSatellite`(line1, line2[, name, ts]) | An Earth satellite loaded from a TLE file and propagated with SGP4. |
|---|---|
| `EarthSatellite.from_omm`(ts, element_dict) | Build an EarthSatellite from OMM text fields. |
| `EarthSatellite.from_satrec`(satrec, ts) | Build an EarthSatellite from a raw sgp4 Satrec object. |
| `TEME` | The satellite-specific True Equator Mean Equinox frame of reference. |

## Stars and other distant objects

| `Star` | The position in the sky of a star or other fixed object. |
|---|---|

## Astronomical positions

The `ICRF` three-dimensional position vector serves as the base class for all of the following position classes. Each class represents an (_x,y,z_) `.xyz` and `.velocity` vector oriented to the axes of the International Celestial Reference System (ICRS), an inertial system that’s an update to J2000 and that does not rotate with respect to the universe.

| `ICRF` | An (_x,y,z_) position and velocity oriented to the ICRF axes. |
|---|---|
| `Barycentric` | An (_x,y,z_) position measured from the Solar System barycenter. |
| `Astrometric` | An astrometric (_x,y,z_) position relative to a particular observer. |
| `Apparent` | An apparent (_x,y,z_) position relative to a particular observer. |
| `Geocentric` | An (_x,y,z_) position measured from the center of the Earth. |

You can also generate a position at the Solar System Barycenter.

| `SSB` | The Solar System Barycenter. |
|---|---|

Positions are usually generated by the `at(t)` method of a vector function, rather than being constructed manually. But you can also build a position directly from a raw vector, or from right ascension and declination coordinates with `position_of_radec()`.

| `position_of_radec`(ra_hours, dec_degrees[, …]) | Build a position object from a right ascension and declination. |
|---|---|

All position objects offer five basic attributes:

| `.xyz` | An (_x,y,z_) `Distance`. |
|---|---|
| `.velocity` | An (_x,y,z_) `Velocity`, or `None`. |
| `.t` | The `Time` of the position, or `None`. |
| `.center` | Body the vector is measured from. |
| `.target` | Body the vector is measured to. |

The `.xyz` attribute used to be named `.position`. To support older code, Skyfield will always recognize the original name as an alias.

All positions support these methods:

| `ICRF.distance`() | Compute the distance from the origin to this position. |
|---|---|
| `ICRF.speed`() | Compute the magnitude of the velocity vector. |
| `ICRF.radec`([epoch]) | Compute equatorial RA, declination, and distance. |
| `ICRF.hadec`() | Compute hour angle, declination, and distance. |
| `ICRF.altaz`([temperature_C, pressure_mbar]) | Compute (alt, az, distance) relative to the observer’s horizon |
| `ICRF.from_altaz`([alt, az, alt_degrees, …]) | Generate an Apparent position from an altitude and azimuth. |
| `ICRF.separation_from`(another_icrf) | Return the angle between this position and another. |
| `ICRF.frame_xyz`(frame) | Return this position as an (_x,y,z_) vector in a reference frame. |
| `ICRF.frame_xyz_and_velocity`(frame) | Return (_x,y,z_) position and velocity vectors in a reference frame. |
| `ICRF.frame_latlon`(frame) | Return latitude, longitude, and distance in the given frame. |
| `ICRF.frame_latlon_and_rates`(frame) | Return a reference frame latitude, longitude, range, and rates. |
| `ICRF.from_time_and_frame_vectors`(t, frame, …) | Constructor: build a position from two vectors in a reference frame. |
| `ICRF.to_skycoord`([unit]) | Convert this distance to an AstroPy `SkyCoord` object. |
| `ICRF.phase_angle`(sun) | Return this position’s phase angle: the angle Sun-target-observer. |
| `ICRF.fraction_illuminated`(sun) | Return the fraction of the target’s disc that is illuminated. |
| `ICRF.is_sunlit`(ephemeris) | Return whether a position in Earth orbit is in sunlight. |

In addition to the methods above, several subclasses of the base position class provide unique methods of their own:

| `Barycentric.observe`(body) | Compute the `Astrometric` position of a body from this location. |
|---|---|
| `Astrometric.apparent`() | Compute an `Apparent` position for this body. |

## Reference frames

| `skyfield.framelib.true_equator_and_equinox_of_date` | The dynamical frame of Earth’s true equator and true equinox of date. |
|---|---|
| `skyfield.framelib.itrs` | The International Terrestrial Reference System (ITRS). |
| `skyfield.framelib.ecliptic_frame` | Reference frame of the true ecliptic and equinox of date. |
| `skyfield.framelib.ecliptic_J2000_frame` | Reference frame of the true ecliptic and equinox at J2000. |
| `skyfield.framelib.galactic_frame` | Galactic System II reference frame. |
| `skyfield.sgp4lib.TEME` | The satellite-specific True Equator Mean Equinox frame of reference. |

## Constellations

`skyfield.api.load_constellation_map`()
Load Skyfield’s constellation boundaries and return a lookup function.
Skyfield carries an internal map of constellation boundaries that is optimized for quick position lookup. Call this function to load the map and return a function mapping position to constellation name.

```python
>>> from skyfield.api import position_of_radec, load_constellation_map
>>> constellation_at = load_constellation_map()
>>> north_pole = position_of_radec(0, 90)
>>> constellation_at(north_pole)
'UMi'
```

If you pass an array of positions, you’ll receive an array of names.

`skyfield.api.load_constellation_names`()
Return a list of abbreviation-name tuples, like `('Aql', 'Aquila')`.
You can pass the list to Python’s `dict()` to build a dictionary that turns a constellation abbreviation into a full name:

```python
>>> from skyfield.api import load_constellation_names
>>> d = dict(load_constellation_names())
>>> d['UMa']
'Ursa Major'
```

By swapping the order of the two items, you can map the other way, from a full name back to an abbreviation:

```python
>>> f = dict(reversed(item) for item in load_constellation_names())
>>> f['Ursa Major']
'UMa'
```

`skyfield.data.stellarium.parse_constellations`(_lines_)
Return a list of constellation outlines.
Each constellation outline is a list of edges, each of which is drawn between a pair of specific stars:

```
[
    (name, [(star1, star2), (star3, star4), ...]),
    (name, [(star1, star2), (star3, star4), ...]),
    ...
]
```

Each name is a 3-letter constellation abbreviation; each star is an integer Hipparcos catalog number. See [Drawing a finder chart for comet NEOWISE](https://rhodesmill.org/skyfield/neowise.html) for an example of how to combine this data with the Hipparcos star catalog to draw constellation lines on a chart.

`skyfield.data.stellarium.parse_star_names`(_lines_)
Return the names in a Stellarium `star_names.fab` file.
Returns a list of named tuples, each of which offers a `.hip` attribute with a Hipparcos catalog number and a `.name` attribute with the star name. Do not depend on the tuple having only length two; additional fields may be added in the future.

## Searching

`skyfield.searchlib.find_discrete`()
Find the times at which a discrete function of time changes value.
This routine is used to find instantaneous events like sunrise, transits, and the seasons. See [Searching for the dates of astronomical events](https://rhodesmill.org/skyfield/searching.html) for how to use it yourself.

`skyfield.searchlib.find_maxima`()
Find the local maxima in the values returned by a function of time.
This routine is used to find events like highest altitude and maximum elongation. See [Searching for the dates of astronomical events](https://rhodesmill.org/skyfield/searching.html) for how to use it yourself.

`skyfield.searchlib.find_minima`()
Find the local minima in the values returned by a function of time.
This routine is used to find events like minimum elongation. See [Searching for the dates of astronomical events](https://rhodesmill.org/skyfield/searching.html) for how to use it yourself.

## Osculating orbital elements

This routine returns osculating orbital elements for an object’s instantaneous position and velocity.

| `osculating_elements_of`(position[, …]) | Produce the osculating orbital elements for a position. |
|---|---|

| `OsculatingElements.apoapsis_distance` | Distance object |
|---|---|
| `OsculatingElements.argument_of_latitude` | Angle object |
| `OsculatingElements.argument_of_periapsis` | Angle object |
| `OsculatingElements.eccentric_anomaly` | Angle object |
| `OsculatingElements.eccentricity` | numpy.ndarray |
| `OsculatingElements.inclination` | Angle object |
| `OsculatingElements.longitude_of_ascending_node` | Angle object |
| `OsculatingElements.longitude_of_periapsis` | Angle object |
| `OsculatingElements.mean_anomaly` | Angle object |
| `OsculatingElements.mean_longitude` | Angle object |
| `OsculatingElements.mean_motion_per_day` | Angle object |
| `OsculatingElements.periapsis_distance` | Distance object |
| `OsculatingElements.periapsis_time` | Time object |
| `OsculatingElements.period_in_days` | numpy.ndarray |
| `OsculatingElements.semi_latus_rectum` | Distance object |
| `OsculatingElements.semi_major_axis` | Distance object |
| `OsculatingElements.semi_minor_axis` | Distance object |
| `OsculatingElements.time` | Time object |
| `OsculatingElements.true_anomaly` | Angle object |
| `OsculatingElements.true_longitude` | Angle object |

## Units

| `Distance` | Distance |
|---|---|
| `Velocity` | Velocity |
| `Angle` | Angle |
| `AngleRate` | Rate at which an angle is changing |

All three kinds of quantity support one or more methods.

| `Distance.au`(value) | Astronomical units (the Earth-Sun distance of 149,597,870,700 m). |
|---|---|
| `Distance.km`(value) | Kilometers (1,000 meters). |
| `Distance.m`(value) | Meters. |
| `Distance.length`() | Compute the length when this is an (_x,y,z_) vector. |
| `Distance.light_seconds`() | Return the length of this vector in light seconds. |
| `Distance.to`(unit) | Convert this distance to the given AstroPy unit. |
| `Velocity.au_per_d`(value) | Astronomical units per day. |
| `Velocity.km_per_s`(value) | Kilometers per second. |
| `Velocity.m_per_s`(value) | Meters per second. |
| `Velocity.to`(unit) | Convert this velocity to the given AstroPy unit. |
| `Angle.radians`(value) | Radians (𝜏 = 2𝜋 in a circle). |
| `Angle.hours` | Hours (24h in a circle). |
| `Angle.degrees` | Degrees (360° in a circle). |
| `Angle.arcminutes`() | Return the angle in arcminutes. |
| `Angle.arcseconds`() | Return the angle in arcseconds. |
| `Angle.mas`() | Return the angle in milliarcseconds. |
| `Angle.to`(unit) | Convert this angle to the given AstroPy unit. |
| `Angle.hms`([warn]) | Convert to a tuple (hours, minutes, seconds). |
| `Angle.signed_hms`([warn]) | Convert to a tuple (sign, hours, minutes, seconds). |
| `Angle.hstr`([places, warn, format]) | Return a string like `12h 07m 30.00s`; see [Formatting angles](https://rhodesmill.org/skyfield/angles.html#formatting-angles). |
| `Angle.dms`([warn]) | Convert to a tuple (degrees, minutes, seconds). |
| `Angle.signed_dms`([warn]) | Convert to a tuple (sign, degrees, minutes, seconds). |
| `Angle.dstr`([places, warn, format]) | Return a string like `181deg 52' 30.0"`; see [Formatting angles](https://rhodesmill.org/skyfield/angles.html#formatting-angles). |
| `AngleRate.radians` | `Rate` of change in radians. |
| `AngleRate.degrees` | `Rate` of change in degrees. |
| `AngleRate.arcminutes` | `Rate` of change in arcminutes. |
| `AngleRate.arcseconds` | `Rate` of change in arcseconds. |
| `AngleRate.mas` | `Rate` of change in milliarcseconds. |
| `Rate.per_day` | Units per day of Terrestrial Time. |
| `Rate.per_hour` | Units per hour of Terrestrial Time. |
| `Rate.per_minute` | Units per minute of Terrestrial Time. |
| `Rate.per_second` | Units per second of Terrestrial Time. |

## Trigonometry

| `position_angle_of`(anglepair1, anglepair2) | Return the position angle of one position with respect to another. |
|---|---|