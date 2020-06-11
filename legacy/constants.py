def reversed_dict(d):
    """Create a reverse lookup dictionary"""
    return dict([(b, a) for a, b in d])


def choices_as_set(d):
    """Handy to check if domain is correct"""
    return set([b for a, b in d])


class Constants(object):
    """Constants for all databases, or unsorted"""

    LEVEE_MATERIAL_CHOICES =  (
        (1, 'zand'),
        (2, 'klei'),
        )

    # meaning of shape types in Import database.
    PIPE_SHAPE_TYPES = {
        '00': 'circle',
        '01': 'egg',
        '02': 'rectangle',
        '03': 'mouthshape',
        '04': 'square',
        '05': 'heul',
        '06': 'trapezium'}

    # TODO: I don't think this is correct, should probably be 00, 01, etc
    MANHOLE_SHAPE_SQUARE = '00'
    MANHOLE_SHAPE_ROUND = '01'
    MANHOLE_SHAPE_RECTANGLE = '02'

    MANHOLE_SHAPE_TYPES = {
        MANHOLE_SHAPE_SQUARE: 'vierkant',
        MANHOLE_SHAPE_ROUND: 'rond',
        MANHOLE_SHAPE_RECTANGLE: 'rechthoekig'}

    FRICTION_TYPE_CHEZY = 1
    FRICTION_TYPE_MANNING = 4
    FRICTION_TYPE_NIKURADSE = 999  # TODO: fill in real code when available

    FRICTION_TYPE_CHOICES = (
        (FRICTION_TYPE_CHEZY, 'chezy [m^(1/2)/s]'),
        (FRICTION_TYPE_MANNING, 'manning nm [s/m^(1/2)]'),
        (FRICTION_TYPE_NIKURADSE, 'nikuradse (White-Coolbrook) [mm]'),
    )

    FRICTION_AVG_CHOICES = (
        (0, 'minimum'),
        (1, 'maximum'),
    )

    FRICTION_SHALLOW_WATER_CORRECTION_CHOICES = (
        (0, 'minimum'),
        (1, 'maximum'),
    )

    LIMITER_SLOPE_CROSSSECTIONAL_AREA_CHOICES = (
        (0, 'minimum'),
        (1, 'maximum'),
    )

    LIMITER_SLOPE_FRICTION_CHOICES = (
        (0, 'minimum'),
        (1, 'maximum'),
    )

    LIMITER_GRAD_2D = (
        (0, 'minimum'),
        (1, 'maximum'),
    )

    LIMITER_GRAD_1D = (
        (0, 'minimum'),
        (1, 'maximum'),
    )

    USE_0D_INFLOW_CHOICES = (
        (0, 'no_inflow'),
        (1, 'impervious_inflow'),
        (2, 'surface_inflow'),
    )

    MATERIAL_TYPE_CONCRETE = 0
    MATERIAL_TYPE_PVC = 1
    MATERIAL_TYPE_STONEWARE = 2
    MATERIAL_TYPE_CAST_IRON = 3
    MATERIAL_TYPE_BRICKWORK = 4
    MATERIAL_TYPE_HPE = 5
    MATERIAL_TYPE_HPDE = 6
    MATERIAL_TYPE_SHEET_IRON = 7
    MATERIAL_TYPE_STEEL = 8

    MATERIAL_TYPE_CHOICES = (
        (MATERIAL_TYPE_CONCRETE, 'concrete'),
        (MATERIAL_TYPE_PVC, 'pvc'),
        (MATERIAL_TYPE_STONEWARE, 'stoneware'),
        (MATERIAL_TYPE_CAST_IRON, 'cast-iron'),
        (MATERIAL_TYPE_BRICKWORK, 'brickwork'),
        (MATERIAL_TYPE_HPE, 'hpe'),
        (MATERIAL_TYPE_HPDE, 'hpde'),
        (MATERIAL_TYPE_SHEET_IRON, 'sheet-iron'),
        (MATERIAL_TYPE_STEEL, 'steel'),
        )

    # Used in guess_pipe_friction
    MATERIAL_ROUGHNESS = {
        FRICTION_TYPE_CHEZY: {
            MATERIAL_TYPE_CONCRETE: 47,
            MATERIAL_TYPE_PVC: 62,
            MATERIAL_TYPE_STONEWARE: 60,
            MATERIAL_TYPE_CAST_IRON: 50,
            MATERIAL_TYPE_BRICKWORK: 42,
            MATERIAL_TYPE_HPE: 62,
            MATERIAL_TYPE_HPDE: 62,
            MATERIAL_TYPE_SHEET_IRON: 49,
            MATERIAL_TYPE_STEEL: 52,
        },
        FRICTION_TYPE_MANNING: {
            MATERIAL_TYPE_CONCRETE: 0.0145,
            MATERIAL_TYPE_PVC: 0.0110,
            MATERIAL_TYPE_STONEWARE: 0.0115,
            MATERIAL_TYPE_CAST_IRON: 0.0135,
            MATERIAL_TYPE_BRICKWORK: 0.0160,
            MATERIAL_TYPE_HPE: 0.0110,
            MATERIAL_TYPE_HPDE: 0.0110,
            MATERIAL_TYPE_SHEET_IRON: 0.0135,
            MATERIAL_TYPE_STEEL: 0.0130,
        },
        FRICTION_TYPE_NIKURADSE: {
            MATERIAL_TYPE_CONCRETE: 3.00,
            MATERIAL_TYPE_PVC: 0.40,
            MATERIAL_TYPE_STONEWARE: 0.50,
            MATERIAL_TYPE_CAST_IRON: 2.00,
            MATERIAL_TYPE_BRICKWORK: 5.00,
            MATERIAL_TYPE_HPE: 0.40,
            MATERIAL_TYPE_HPDE: 0.40,
            MATERIAL_TYPE_SHEET_IRON: 2.00,
            MATERIAL_TYPE_STEEL: 1.50,
        },
    }

    SRS_SRID = {'DEFAULT': 28992, 'RD_New': 28992}

    # mapping file to get srid from proj, because sometimes the epsg srid code
    # is not provided in the shapefile
    PROJ_MAPPING = (
        ('amersfoort_rd_new', 28992),
        ('amersfoort_rd', 28992),
        ('amersfoort', 28992),
    )

    # RD srid
    RD_NEW_SRID = 28992
    WGS84_SRID = 4326

    # Mapping from import to 3Di
    # Original comment: 3Di has mixed up round and rectangular!
    # Hmmm shouldn't this be the same as PIPE_SHAPE_TYPES to
    # UrbanConstants.SHAPE_MAP ?? It is not (e.g. egg-shaped)
    CULVERT_MAPPING = {
        1: 2,   # round (rond)
        2: 1,   # rectangular (rechthoekig)
        3: 3,   # egg-shaped (eivormig)
        4: 4,   # ? (muil)
        5: 5,   # ellipse (ellips)
        6: 6,   # ? (heul)
        99: 2,  # unknown (onbekend)
    }

    WEIR_TYPE_BROAD_CRESTED = 1
    WEIR_TYPE_SHARP_CRESTED = 2

    WEIR_TYPE_CHOICES = (
        (WEIR_TYPE_BROAD_CRESTED, "broad crested"),
        (WEIR_TYPE_SHARP_CRESTED, "sharp crested"),
    )

    # For orifice
    FLOW_TYPE_SEWER = 1
    FLOW_TYPE_OPEN_CHANNEL = 2

    FLOW_TYPE_CHOICES = (
        (FLOW_TYPE_SEWER, "sewer"),
        (FLOW_TYPE_OPEN_CHANNEL, "open channel"),
    )

    LEVEE_CATEGORY_PRIMARY = 1
    LEVEE_CATEGORY_REGIONAL = 2
    LEVEE_CATEGORY_CTYPE = 3
    LEVEE_CATEGORY_DRY = 4
    LEVEE_CATEGORY_OTHER = 5

    LEVEE_CATEGORY_CHOICES = (
        (LEVEE_CATEGORY_PRIMARY, 'primary'),
        (LEVEE_CATEGORY_REGIONAL, 'regional'),
        (LEVEE_CATEGORY_CTYPE, 'c-type'),
        (LEVEE_CATEGORY_DRY, 'dry'),
        (LEVEE_CATEGORY_OTHER, 'other')
        )

    MEASURING_STATION_TYPE_WEATHER = 1

    MEASURING_STATION_TYPE_CHOICES = (
        (MEASURING_STATION_TYPE_WEATHER, 'weather'),
        )

    FLOW_DIRECTION_BACKWARDS = -1
    FLOW_DIRECTION_BOTH = 0
    FLOW_DIRECTION_FORWARDS = 1
    FLOW_DIRECTION_CLOSED = 3

    FLOW_DIRECTION_CHOICES = (
        (FLOW_DIRECTION_BACKWARDS, "backwards"),
        (FLOW_DIRECTION_BOTH, "both"),
        (FLOW_DIRECTION_FORWARDS, "forwards"),
        (FLOW_DIRECTION_CLOSED, "closed"),
    )


class UrbanConstants(object):
    """Constants for urban objects. """
    # manhole
    MANHOLE_INDICATOR_MANHOLE = 0
    MANHOLE_INDICATOR_OUTLET = 1
    MANHOLE_INDICATOR_PUMPSTATION = 2

    MANHOLE_INDICATOR_CHOICES = (
        (MANHOLE_INDICATOR_MANHOLE, 'manhole'),
        (MANHOLE_INDICATOR_OUTLET, 'outlet'),
        (MANHOLE_INDICATOR_PUMPSTATION, 'pumpstation'),
        )

    MANHOLE_INDICATOR_LOOKUP = reversed_dict(MANHOLE_INDICATOR_CHOICES)

    MANHOLE_CALCULATION_TYPE_EMBEDDED = 0
    MANHOLE_CALCULATION_TYPE_ISOLATED = 1
    MANHOLE_CALCULATION_TYPE_CONNECTED = 2

    MANHOLE_CALCULATION_TYPE_CHOICES = (
        (MANHOLE_CALCULATION_TYPE_EMBEDDED, 'embedded'),
        (MANHOLE_CALCULATION_TYPE_ISOLATED, 'isolated'),
        (MANHOLE_CALCULATION_TYPE_CONNECTED, 'connected'),
        )

    MANHOLE_CALCULATION_TYPE_LOOKUP = reversed_dict(
        MANHOLE_CALCULATION_TYPE_CHOICES)

    ZOOM_CATEGORY_CHOICES = (
        (1, 'zoom 1'),
        (2, 'zoom 2'),
        (3, 'zoom 3'),
        (4, 'zoom 4'),
        (5, 'zoom 5'),
        )

    PIPE_SEWERAGE_TYPE_COMBINED = 0
    PIPE_SEWERAGE_TYPE_STORMWATER = 1
    PIPE_SEWERAGE_TYPE_WASTEWATER = 2
    PIPE_SEWERAGE_TYPE_TRANSPORT = 3
    PIPE_SEWERAGE_TYPE_OVERFLOW = 4
    PIPE_SEWERAGE_TYPE_SINKER = 5
    PIPE_SEWERAGE_TYPE_STORAGE = 6
    PIPE_SEWERAGE_TYPE_STORAGE_SETTLING_TANK = 7

    PIPE_SEWERAGE_TYPE_CHOICES = (
        (PIPE_SEWERAGE_TYPE_COMBINED, 'combined'),
        (PIPE_SEWERAGE_TYPE_STORMWATER, 'stormwater'),  # RWA
        (PIPE_SEWERAGE_TYPE_WASTEWATER, 'wastewater'),  # DWA
        (PIPE_SEWERAGE_TYPE_TRANSPORT, 'transport'),
        (PIPE_SEWERAGE_TYPE_OVERFLOW, 'overflow'),
        (PIPE_SEWERAGE_TYPE_SINKER, 'sinker'),
        (PIPE_SEWERAGE_TYPE_STORAGE, 'storage'),
        (PIPE_SEWERAGE_TYPE_STORAGE_SETTLING_TANK, 'storage-settling-tank'),
        )

    # TODO: make calculation type the same as manhole calculation type
    PIPE_CALCULATION_TYPE_EMBEDDED = 0
    PIPE_CALCULATION_TYPE_ISOLATED = 1
    PIPE_CALCULATION_TYPE_CONNECTED = 2

    PIPE_CALCULATION_TYPE_CHOICES = (
        (PIPE_CALCULATION_TYPE_EMBEDDED, 'embedded'),
        (PIPE_CALCULATION_TYPE_ISOLATED, 'isolated'),
        (PIPE_CALCULATION_TYPE_CONNECTED, 'connected'),
        )

    # 1 = rectangle; 2 = circle; 3= egg; 4=yz;  5: tabulated (rectangle);
    # 6 = tabulated (trapezium)
    # Commented out types are not yet used, but may be used in the future.
    SHAPE_TYPE_RECTANGLE = 1
    SHAPE_TYPE_CIRCLE = 2
    SHAPE_TYPE_EGG = 3
    SHAPE_TYPE_YZ = 4
    #SHAPE_TYPE_TABULATED_RECTANGLE = 5
    SHAPE_TYPE_TABULATED_TRAPEZIUM = 6
    #SHAPE_MOUTHSHAPE = 7  # is not used yet

    SHAPE_TYPE_CHOICES = (
        (SHAPE_TYPE_RECTANGLE, 'rectangle'),
        (SHAPE_TYPE_CIRCLE, 'circle'),
        (SHAPE_TYPE_EGG, 'egg'),
        (SHAPE_TYPE_YZ, 'yz'),
        #(SHAPE_TYPE_TABULATED_RECTANGLE, 'tabulated-rectangle'),
        (SHAPE_TYPE_TABULATED_TRAPEZIUM, 'tabulated_trapezium'),
        #(SHAPE_MOUTHSHAPE, 'mouthshape'),
        )

    SHAPE_MAP = dict(SHAPE_TYPE_CHOICES)
    # Reverse lookup
    SHAPE_MAP_LOOKUP = reversed_dict(SHAPE_MAP.items())

    # 0 = round; 2= rectangle. TODO, merge with SHAPE_TYPE?
    ORIFICE_SHAPE_TYPE_ROUND = 0
    ORIFICE_SHAPE_TYPE_RECTANGLE = 2

    ORIFICE_SHAPE_TYPE_CHOICES = (
        (ORIFICE_SHAPE_TYPE_ROUND, 'round'),
        (ORIFICE_SHAPE_TYPE_RECTANGLE, 'rectangle'),
        )

    PUMPSTATION_CLASSIFICATION_CHOICES = (
        (1, 'class 1'),
        )

    PUMPSTATION_TYPE_CHOICES = (
        (1, 'type suction side'),
        (2, 'type delivery side'),
        )

    # 1 = waterlevel; 2 = velocity; 3 = discharge
    BOUNDARY_TYPE_WATERLEVEL = 1
    BOUNDARY_TYPE_VELOCITY = 2
    BOUNDARY_TYPE_DISCHARGE = 3

    BOUNDARY_TYPE_CHOICES = (
        (BOUNDARY_TYPE_WATERLEVEL, 'waterlevel'),
        (BOUNDARY_TYPE_VELOCITY, 'velocity'),
        (BOUNDARY_TYPE_DISCHARGE, 'discharge'),
        )

    # Global settings
    # 0: Euler implicit; 1: Carlson implicit 2: Silecki explicit
    INTEGRATION_METHOD_EULER_IMPLICIT = 0
    INTEGRATION_METHOD_CARLSON_IMPLICIT = 1
    INTEGRATION_METHOD_SILECKI_EXPLICIT = 2

    INTEGRATION_METHOD_CHOICES = (
        (INTEGRATION_METHOD_EULER_IMPLICIT, 'euler-implicit'),
        (INTEGRATION_METHOD_CARLSON_IMPLICIT, 'carlson-implicit'),
        (INTEGRATION_METHOD_SILECKI_EXPLICIT, 'silecki-explicit'),
        )

    # SURFACE_CLASS SURFACE_INCLINATION RIONED
    # gesloten verharding hellend gvh_hel
    # gesloten verharding vlak gvh_vla
    # gesloten verharding uitgestrekt gvh_vlu
    # open verharding hellend ovh_hel
    # open verharding vlak ovh_vla
    # open verharding uitgestrekt ovh_vlu
    # onverhard hellend onv_hel
    # onverhard vlak onv_vla
    # onverhard uitgestrekt onv_vlu
    # half verhard hellend onv_hel
    # half verhard vlak onv_vla
    # half verhard uitgestrekt onv_vlu
    # pand hellend dak_hel
    # pand vlak dak_vla
    # pand uitgestrekt dak_vlu
    SURFACE_CLASS_GESLOTEN_VERHARDING = 'gesloten verharding'
    SURFACE_CLASS_OPEN_VERHARDING = 'open verharding'
    SURFACE_CLASS_ONVERHARD = 'onverhard'
    SURFACE_CLASS_HALF_VERHARD = 'half verhard'
    SURFACE_CLASS_PAND = 'pand'

    SURFACE_CLASS_CHOICES = (
        (SURFACE_CLASS_GESLOTEN_VERHARDING, 'gesloten verharding'),
        (SURFACE_CLASS_OPEN_VERHARDING, 'open verharding'),
        (SURFACE_CLASS_ONVERHARD, 'onverhard'),
        (SURFACE_CLASS_HALF_VERHARD, 'half verhard'),
        (SURFACE_CLASS_PAND, 'pand'),
        )

    SURFACE_INCLINATION_HELLEND = 'hellend'
    SURFACE_INCLINATION_VLAK = 'vlak'
    SURFACE_INCLINATION_UITGESTREKT = 'uitgestrekt'

    SURFACE_INCLINATION_CHOICES = (
        (SURFACE_INCLINATION_HELLEND, 'hellend'),
        (SURFACE_INCLINATION_VLAK, 'vlak'),
        (SURFACE_INCLINATION_UITGESTREKT, 'uitgestrekt'),
        )

    SURFACE_CLASSES_BUILDING = {
        SURFACE_CLASS_PAND
    }

    SURFACE_CLASSES_ROAD = {
        SURFACE_CLASS_GESLOTEN_VERHARDING,
        SURFACE_CLASS_OPEN_VERHARDING,
        SURFACE_CLASS_ONVERHARD,
        SURFACE_CLASS_HALF_VERHARD
    }


class QualityCheckResult(object):

    RELIABLE = 0
    UNCERTAIN = 1
    UNRELIABLE = 2
