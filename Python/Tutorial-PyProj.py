"""Basics of using pyproj"""

"""
Concepts:
    - Spatial/Coordinate Reference System (SRS/CRS)
        - Coordinate System Type
            - Geographic/Geodetic - 2D lat/lon
            - Geocentric/ECEF - 3D
            - Projected - 2D x,y
                - Planar
                - Cylidrical
                - Conical
            - Engineering/Local/Custom
        - Horizontal Datum - convention for aligning ellipsoid with geoid
            - Ellipsoid - simplified elllipsoid model of the earth
            - Geoid - surface of constant gravitational potential
            - Types
                - Local - ellipsoid anchored to spots on geoid
                - Geocentric - ellipsoid has origin at earths center of mass and
                  then fit to geoid
        - Projection
    - CRS authorities
        - European Patroleum Survet Group (EPSG)
        - ISO
        - Open Geospatial Consortium (OGC)
        - World Geodetic System (WSG)
            - WSG 84 - standard established in 1984
Important CRS codes
- WGS 84 based
    - EPSG 4326 - lat/lon
    - EPSG 4978 - x/y/z (a.k.a. ECEF)
    - EPSG 4979 - lat/lon/alt (a.k.a. LLA)
- Mercator
    - EPSG 3395 - World Mercator
    - EPSG 3857 - Mercator projection used by google maps
- EPSG 7789 - ECEF
Acroynms:
- Spatial Reference System Identifier (SRID)
"""

import pyproj
import pyproj._crs
import pyproj.aoi

# Attributes
assert len(pyproj.pj_ellps.keys()) == 46
assert len(pyproj.pj_list) == 183


################################################################################
# Creating CRS
################################################################################
auth_name, code = 'EPSG', 4236 # WGS 84
crs = pyproj.CRS.from_authority(auth_name, code)
assert isinstance(crs, pyproj.CRS)

assert crs == pyproj.CRS.from_epsg(code)
# pyproj.CRS.from_cf()
# pyproj.CRS.from_dict()
# pyproj.CRS.from_epsg()
# pyproj.CRS.from_json()
# pyproj.CRS.from_json_dict()
# pyproj.CRS.from_proj4()
# pyproj.CRS.from_string()
# pyproj.CRS.from_user_input()
# pyproj.CRS.from_wkt()

################################################################################
# Converting CRS to other formats
################################################################################
assert crs.to_string() == f'{auth_name}:{code}'
assert crs.to_authority() == (auth_name, str(code))
# assert crs.list_authority() == 
assert crs.to_epsg() == code
# assert crs.to_cf() ==
# assert crs.to_json() ==
# assert crs.to_json_dict() ==
# assert crs.to_proj4() ==
# assert crs.to_dict() ==
# assert crs.to_wkt() ==
# assert crs.cs_to_cf() ==

# assert crs.to_2d()
# assert crs.to_3d()
# assert crs.get_geod() ==

assert crs.equals(crs)
assert crs.is_exact_same(crs)

################################################################################
# Properties of CRS
################################################################################
assert crs.area_of_use == pyproj.aoi.AreaOfUse(
    west=119.25, south=21.87, east=122.06, north=25.34, 
    name='Taiwan, Republic of China - onshore - Taiwan Island, Penghu (Pescadores) Islands.'
)
# assert crs.axis_info == [
#     pyproj.crs.crs.Axis(
#         name='Geodetic latitude', 
#         abbrev='Lat', 
#         direction='north', 
#         unit_auth_code='EPSG', 
#         unit_code=9122, 
#         unit_name='degree',
#     ), 
#     pyproj.crs.crs.Axis(
#         name='Geodetic longitude', 
#         abbrev='Lon', 
#         direction='east', 
#         unit_auth_code='EPSG', 
#         unit_code=9122, 
#         unit_name='degree',
#     ),
# ]

assert crs.name           == 'Hu Tzu Shan 1950'
assert crs.srs            == 'EPSG:4236'
assert crs.prime_meridian == 'Greenwich'
assert crs.type_name      == 'Geographic 2D CRS'
assert crs.scope          == 'Geodesy.'
assert crs.is_bound       is False
assert crs.is_compound    is False
assert crs.is_derived     is False
assert crs.is_engineering is False
assert crs.is_geocentric  is False
assert crs.is_geographic  is True
assert crs.is_projected   is False
assert crs.is_vertical    is False
assert crs.sub_crs_list == []
assert crs.coordinate_operation is None
assert crs.remarks    is None
assert crs.source_crs is None
assert crs.target_crs is None
assert crs.utm_zone   is None

datum = crs.datum
assert isinstance(datum, pyproj._crs.Datum)
assert datum.scope          == 'Topographic mapping.'
assert datum.type_name      == 'Geodetic Reference Frame'
assert datum.name           == crs.name
assert datum.prime_meridian == crs.prime_meridian
assert datum.remarks        == crs.remarks
assert datum.ellipsoid      == crs.ellipsoid

ellipsoid = crs.ellipsoid
assert isinstance(ellipsoid, pyproj._crs.Ellipsoid)
assert ellipsoid.name                   == 'International 1924'
assert ellipsoid.inverse_flattening     == 297.0
assert ellipsoid.is_semi_minor_computed is True
assert ellipsoid.semi_major_metre       == 6378388.0
assert ellipsoid.semi_minor_metre       == 6356911.9461279465
assert ellipsoid.remarks                == crs.remarks
assert ellipsoid.scope                  is None

assert isinstance(crs.geodetic_crs, pyproj.CRS)
assert crs.geodetic_crs.name      == "Hu Tzu Shan 1950"

assert isinstance(crs.coordinate_system, pyproj._crs.CoordinateSystem)
assert crs.coordinate_system.name == 'ellipsoidal'

################################################################################
# Transforming between coordinates within one datum
################################################################################

crs_latlon = pyproj.CRS.from_epsg(4326)
crs_ecef = pyproj.CRS.from_epsg(4978)
crs_lla = pyproj.CRS.from_epsg(4979)

lla = 0,0,0

# Convert LLA to ECEF
transformer = pyproj.Transformer.from_crs(crs_lla, crs_ecef)
ecef_xyz = transformer.transform(*lla, radians=False)
assert ecef_xyz == (crs_ecef.ellipsoid.semi_major_metre, 0, 0)

transformer = pyproj.Transformer.from_crs(crs_ecef, crs_lla)
assert lla == transformer.transform(*ecef_xyz)

# Convert LatLon to LLA 
# transformer = pyproj.Transformer.from_crs(crs_latlon, crs_lla)

# Convert from LLA to local ENU

# Use np arrays and xarrays as inputs

# Find length of line 
lats = [0,45,-45,0]
lons = [0,90,-90,0]
dist = crs_lla.get_geod().line_length(lats,lons)
assert dist > 0

# Find area of polygon
area, perimeter = crs_lla.get_geod().polygon_area_perimeter(lats,lons)

################################################################################
# Transforming from CRS to CRS
################################################################################

################################################################################
# OTHER stuff
################################################################################
# Modules
 # pyproj.aoi
 # pyproj.crs
 # pyproj.database
 # pyproj.datadir
 # pyproj.enums
 # pyproj.exceptions
 # pyproj.geod
 # pyproj.list
 # pyproj.network
 # pyproj.proj
 # pyproj.pyproj
 # pyproj.sync
 # pyproj.transformer
 # pyproj.utils

# Classes
# pyproj.Geod()
# pyproj.Proj()
# pyproj.Transformer()

# Functions
# pyproj.show_versions()
# pyproj.get_authorities()
# pyproj.get_codes()
# pyproj.get_ellps_map()
# pyproj.get_prime_meridians_map()
# pyproj.get_proj_operations_map()
# pyproj.get_units_map()
# pyproj.set_use_global_context()
