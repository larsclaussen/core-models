"""All django models for a work database."""

from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager
from django.utils.translation import ugettext_lazy as _

from .constants import Constants, UrbanConstants

WORK_SRID = 4326


class V2ControlTable(models.Model):
    """
    Model for table control.

    **action types**

    *for weirs and orifices*
    - set_crest_level (less relevant for orifice)
    - set_discharge_coefficients: to close/open or partially close/open the
    structure; action value = (left fraction 0-1, right fraction 0-1);
    values can be NODATA (-9999)
    - set_cross_section_definition

    *for culverts, channels and pipes*
    - set_discharge_coefficients: to close/open or partially close/open the
    structure; action value = (left fraction 0-1, right fraction 0-1);
    values can be NODATA (-9999)

    *for pumps*
    - set_capacity (L/s)
    - set_levels: to set start and stop levels; action value = (start level,
    stop level, upper stop level); values can be NODATA (-9999)

    **action table**

    The action table consists of one or more threshold, action_value pairs
    separated by a comma.
    E.g. action_table with value 1.2, 4.5, 2.3, 5.6, 3.5, 7.0 has
    3 threshold, action_value pairs: (1.2, 4,5), (2.3, 5.6) and (3.5, 7.0)

    N.B. fields are nullable on purpose to allow an instance to be created in
    several separate steps (which is a likely use-case).

    """
    # variables for evaluating the measure group in v2_control
    measure_variable = models.CharField(
        help_text="e.g. s1/vol", max_length=50, blank=True, null=True)
    measure_operator = models.CharField(
        help_text="e.g. >, <, >=, <=", max_length=2, blank=True, null=True)

    # action_type: e.g. set_crest_level, set_discharge_coefficients (see
    # docstring for more details), to be applied to the target structure (see
    # below)
    action_type = models.CharField(
        help_text="e.g. set_crest_level, set_discharge_coefficients, set_capacity (L/s)",
        max_length=50, blank=True, null=True)
    # one or more thresholds and action values
    action_table = models.TextField(blank=True, null=True)

    # target structure
    target_type = models.CharField(
        help_text="e.g pumpstation, culvert (refers to the related table)",
        max_length=100, blank=True, null=True)
    target_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'v2_control_table'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __str__(self):
        return "v2_control_table: {} {} |{}| - target: {} ({}) - action: {}".\
            format(
                self.measure_variable, self.measure_operator,
                self.action_table, self.target_type, self.target_id,
                self.action_type)


class V2ControlPID(models.Model):
    """
    Model for PID control.
    Kp is the proportional gain, a tuning parameter,
    Ki is the integral gain, a tuning parameter,
    Kd is the derivative gain, a tuning parameter,
    """
    # variables for evaluating the measure group in v2_control
    measure_variable = models.CharField(
        help_text="e.g. s1/vol", max_length=50, blank=True, null=True)
    setpoint = models.FloatField(blank=True, null=True)

    kp = models.FloatField(blank=True, null=True)
    ki = models.FloatField(blank=True, null=True)
    kd = models.FloatField(blank=True, null=True)

    action_type = models.CharField(
        help_text="e.g. set_crest_level, set_discharge_coefficients, set_capacity (L/s)",
        max_length=50, blank=True, null=True)

    # target structure
    target_type = models.CharField(
        help_text="e.g pumpstation, culvert (refers to the related table)",
        max_length=100, blank=True, null=True)
    target_id = models.IntegerField(blank=True, null=True)

    # one if action_type expects one value, e.g. set_crest_level
    # two separated by semi-colon if action_type expects two values, e.g.
    # set_discharge_coefficients
    target_upper_limit = models.CharField(
        help_text="one or two (semi-colon separated) upper limit values",
        max_length=50, blank=True, null=True)
    target_lower_limit = models.CharField(
        help_text="one or two (semi-colon separated) lower limit values",
        max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'v2_control_pid'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __str__(self):
        return (
            "v2_control_pid: {measure_variable} |kp{kp}-ki{ki}-kd{kd} - "
            "target: {target_type} ({target_id}) - action: {action_type} - "
            "upper limit: {upper_limit} - lower limit: {lower_limit}".format(
                measure_variable=self.measure_variable,
                kp=self.kp, ki=self.ki, kd=self.kd,
                target_type=self.target_type, target_id=self.target_id,
                action_type=self.action_type,
                upper_limit=self.target_upper_limit,
                lower_limit=self.target_lower_limit
            )
        )


class V2ControlDelta(models.Model):
    """Model for delta control."""
    measure_variable = models.CharField(
        help_text="e.g. s1/vol", max_length=50, blank=True, null=True)
    measure_delta = models.FloatField(blank=True, null=True)
    measure_dt = models.FloatField(
        blank=True, null=True, help_text='e.g. 120.0 (seconds)'
    )

    action_type = models.CharField(
        help_text="e.g. set_crest_level, set_discharge_coefficients, set_capacity (L/s)",
        max_length=50, blank=True, null=True)
    action_value = models.CharField(
        help_text="e.g. (0.35,-9999.0)",
        max_length=50, blank=True, null=True)
    action_time = models.FloatField(
        help_text="e.g. 120 (time in seconds after which to revert to the "
                  "original value)", blank=True, null=True)

    # target structure
    target_type = models.CharField(
        help_text="e.g pumpstation, culvert (refers to the related table)",
        max_length=100, blank=True, null=True)
    target_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'v2_control_delta'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __str__(self):
        return (
            "v2_control_delta: {} {} {} - target: {} ({}) - action: {} {} {}".
            format(
                self.measure_variable, self.measure_delta, self.measure_dt,
                self.target_type, self.target_id,
                self.action_type, self.action_value, self.action_time)
        )


class V2ControlMemory(models.Model):
    """Model for memory control."""
    measure_variable = models.CharField(
        help_text="e.g. s1/vol", max_length=50, blank=True, null=True)
    upper_threshold = models.FloatField(
        blank=True, null=True, help_text='e.g. 1.85'
    )
    lower_threshold = models.FloatField(
        blank=True, null=True, help_text='e.g. 0.3'
    )

    action_type = models.CharField(
        help_text="e.g. set_crest_level, set_discharge_coefficients, set_capacity (L/s)",
        max_length=50, blank=True, null=True
    )
    action_value = models.CharField(
        help_text="e.g. (0.35,-9999.0)",
        max_length=50, blank=True, null=True
    )

    # target structure
    target_type = models.CharField(
        help_text="e.g pumpstation, culvert (refers to the related table)",
        max_length=100, blank=True, null=True)
    target_id = models.IntegerField(blank=True, null=True)

    # target configuration
    is_active = models.BooleanField(
        default=True,
        help_text="when True the initial state of the target is active"
    )
    is_inverse = models.BooleanField(
        default=False,
        help_text="when True the target will become active when the "
                  "lower threshold has been reached"
    )

    class Meta:
        db_table = 'v2_control_memory'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __str__(self):
        return """v2_control_memory: {} upper {} lower {} - target: {} ({})
        - action: {} {}""".format(
            self.measure_variable, self.upper_threshold,
            self.lower_threshold, self.target_type, self.target_id,
            self.action_type, self.action_value
        )


class V2ControlTimed(models.Model):
    """Model for timed control."""
    action_type = models.CharField(
        help_text="e.g. set_crest_level, set_discharge_coefficients, set_capacity (L/s)",
        max_length=50, blank=True, null=True)
    # one or more start, end and action values rows
    # example:
    # --01-01;--04-04;0.2;1.0#--04-04;--08-09;0.4;0.5#--08-09;--31-12;0.4;0.3
    action_table = models.TextField(blank=True, null=True)

    # target structure
    target_type = models.CharField(
        help_text="e.g pumpstation, culvert (refers to the related table)",
        max_length=100, blank=True, null=True)
    target_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'v2_control_timed'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __str__(self):
        return """v2_control_timed: action {} ({}) - target: {} ({})""".format(
            self.action_type, self.action_table, self.target_type,
            self.target_id)


class V2ControlMeasureGroup(models.Model):
    """
    Just a placeholder with a primary key. To be used to group measure
    objects and weights.
    """
    class Meta:
        db_table = 'v2_control_measure_group'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __str__(self):
        return "v2_control_measure_group: {}".format(self.id)


class V2ControlMeasureMap(models.Model):
    """
    The measure_group field is used to combine one or more object-weight
    combinations. The sum of the weight for one measure_group must be 1.0.

    """
    measure_group = models.ForeignKey(
        'threedi_tools.V2ControlMeasureGroup', blank=True, null=True,
        on_delete=models.CASCADE)

    object_type = models.CharField(max_length=100, blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)

    # weight should always be between 0 and 1; we allow 2 decimal places
    weight = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'v2_control_measure_map'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __str__(self):
        return "v2_control_measure_map: {} {}: weight: {}".format(
            self.object_type, self.object_id, self.weight)


class V2ControlGroup(models.Model):
    """
    Placeholder for creating a group of controls. The user can choose a group
    by specifying a foreign key to this table in the v2_global_settings table.

    """
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'v2_control_group'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __str__(self):
        return "v2_control_group: {}".format(self.name)


class V2Control(models.Model):
    """
    Create controls by connecting a specific control to a measure group and
    group them together via the control_group.
    """
    control_group = models.ForeignKey(
        'threedi_tools.V2ControlGroup', on_delete=models.CASCADE, blank=True, null=True)

    # control type: table, delta, pid, timed or memory
    control_type = models.CharField(max_length=15, blank=True, null=True)
    # pk of the control
    control_id = models.IntegerField(blank=True, null=True)

    measure_group = models.ForeignKey(
        'threedi_tools.V2ControlMeasureGroup', on_delete=models.CASCADE, blank=True, null=True)
    measure_frequency = models.IntegerField(
        blank=True, null=True, help_text="measure frequency in seconds")

    # Optional start and end in ISO 8601 format during which this control is
    # active. With the ISO 8601 format we can handle all use cases, even dates
    # without years. For more info, see https://en.wikipedia.org/wiki/ISO_8601.
    start = models.CharField(
        max_length=50, blank=True, null=True)  # ISO 8601
    end = models.CharField(
        max_length=50, blank=True, null=True)  # ISO 8601

    class Meta:
        db_table = 'v2_control'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __str__(self):
        return "v2_control: {}".format(self.id)


class V2Levee(models.Model):
    """Model representing a Levee for v2 models."""
    material = models.IntegerField(choices=Constants.LEVEE_MATERIAL_CHOICES,
                                   null=True, blank=True)
    max_breach_depth = models.FloatField(blank=True, null=True,
                                         help_text="in meter")
    crest_level = models.FloatField(blank=True, null=True,
                                    help_text="value in [mMSL]")
    code = models.CharField(
        max_length=100, blank=True,
        help_text='the original code that came from the provider/organisation')

    the_geom = models.LineStringField(blank=False, null=True, srid=WORK_SRID)

    objects = GeoManager()

    class Meta:
        db_table = 'v2_levee'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 levee: {}".format(self.pk)


class V2CalculationPoint(models.Model):
    """
    Model representing calculation points for 1D objects (channel, culvert,
    pipe)

    """
    content_type_id = models.IntegerField(null=False, blank=False)
    user_ref = models.CharField(max_length=80, null=False, blank=False)
    calc_type = models.IntegerField(null=False, blank=False)
    the_geom = models.PointField(blank=False, null=False, srid=WORK_SRID)

    objects = GeoManager()

    class Meta:
        db_table = 'v2_calculation_point'
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "V2CalculationPoint pk=%i" % self.pk


class V2ConnectedPoint(models.Model):
    """
    Model representing a point to connect a 1D calculation
    point with a 2D cell.

    """
    exchange_level = models.FloatField(null=True, blank=True)
    calculation_pnt = models.ForeignKey(
        V2CalculationPoint, on_delete=models.CASCADE, blank=False, null=False
    )
    levee = models.ForeignKey(
        V2Levee, on_delete=models.CASCADE, blank=True, null=True
    )
    the_geom = models.PointField(blank=False, null=False, srid=WORK_SRID)

    objects = GeoManager()

    class Meta:
        db_table = 'v2_connected_pnt'
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "V2ConnectedPoint pk=%i" % self.pk


class V2ConnectionNode(models.Model):
    """Model representing a ConnectionNode for v2 models."""
    storage_area = models.FloatField(
        _("Storage area of related hydro.structure."),
        null=True)
    initial_waterlevel = models.FloatField(
        _("Initial waterlevel in related hydro.structure."),
        null=True)
    code = models.CharField(
        max_length=100, blank=True,
        help_text='the original code that came from the provider/organisation')

    the_geom = models.PointField(_("geometry"), srid=WORK_SRID)
    the_geom_linestring = models.LineStringField(null=True, blank=True,
                                                 srid=WORK_SRID)

    class Meta:
        db_table = 'v2_connection_nodes'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "V2ConnectionNode pk=%i" % self.pk


class V2OneDeeBoundaryCondition(models.Model):
    """Model representing a OneDeeBoundaryCondition for v2 models."""
    connection_node = models.ForeignKey(V2ConnectionNode, on_delete=models.CASCADE, unique=True)
    boundary_type = models.IntegerField(
        _("Type of boundary"), null=True,
        choices=UrbanConstants.BOUNDARY_TYPE_CHOICES)
    timeseries = models.TextField(
        _("Timeseries with seconds and boundary value"),
        null=True)

    class Meta:
        db_table = 'v2_1d_boundary_conditions'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "surface water boundary conditions: {}".format(self.pk)


class V2Manhole(models.Model):
    """Model representing a Manhole structure for v2 models."""
    display_name = models.CharField(max_length=255, blank=True)
    code = models.CharField(
        max_length=100, blank=True,
        help_text='the original code that came from the provider/organisation')
    connection_node = models.ForeignKey(
        V2ConnectionNode,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        unique=True
    )

    # Input fields (copied from turtle_core)
    shape = models.CharField(_("shape"), max_length=4, help_text='input',
                             null=True, blank=True)
    width = models.FloatField(_("width"), null=True, help_text='input')
    length = models.FloatField(_("length"), null=True, help_text='input')

    # Model fields (some may be input fields as well)
    manhole_indicator = models.IntegerField(
        _("Type of manhole"),
        null=True,
        choices=UrbanConstants.MANHOLE_INDICATOR_CHOICES,
        help_text='turtle guess_manhole_indicator')
    calculation_type = models.IntegerField(
        _("Modelling type of manhole."),
        null=True,
        choices=UrbanConstants.MANHOLE_CALCULATION_TYPE_CHOICES)
    bottom_level = models.FloatField(
        _("Elevation level of manhole inside"),
        null=True)
    surface_level = models.FloatField(
        _("Level of surface elevation."),
        null=True)
    drain_level = models.FloatField(
        _("Level at which drainage should start (kolkhoogte)."),
        null=True)
    sediment_level = models.FloatField(
        _("Thickness of sediment layer."),
        null=True)
    zoom_category = models.IntegerField(
        _("Rank of objects."), null=True,
        choices=UrbanConstants.ZOOM_CATEGORY_CHOICES)

    class Meta:
        db_table = 'v2_manhole'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 manhole: {}".format(self.pk)


class V2Channel(models.Model):
    """Model representing a Channel for v2 models."""
    display_name = models.CharField(max_length=255, blank=True)
    code = models.CharField(
        max_length=100, blank=True,
        help_text='the original code that came from the provider/organisation')

    # TODO: PIPE_CALCULATION_TYPE_CHOICES must be re-worked!
    calculation_type = models.IntegerField(
        _("Modelling type of pipe"),
        null=True, blank=True,
        choices=UrbanConstants.PIPE_CALCULATION_TYPE_CHOICES)
    dist_calc_points = models.FloatField(
        _("Distance between 3di calculation points"), null=True)

    # TODO: check if more zoom categories might be needed
    zoom_category = models.IntegerField(
        _("Rank of object."), null=True,
        choices=UrbanConstants.ZOOM_CATEGORY_CHOICES)

    connection_node_start = models.ForeignKey(
        V2ConnectionNode,
        on_delete=models.CASCADE,
        related_name="channel_connection_node_start",
        null=True,
        blank=True)

    connection_node_end = models.ForeignKey(
        V2ConnectionNode,
        on_delete=models.CASCADE,
        related_name="channel_connection_node_end",
        null=True,
        blank=True)

    the_geom = models.LineStringField(_("geometry"), srid=WORK_SRID)

    objects = GeoManager()

    class Meta:
        db_table = 'v2_channel'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "surface water channel: {}".format(self.pk)


class V2CrossSectionDefinition(models.Model):
    """
    Model representing a CrossSectionDefinition for v2 models.

    - input fields (copied from turtle_core)
    - model fields (some may be input fields as well)
    - UrbanConstants.SHAPE_TYPE_CHOICES are also rural shape type choices

    """
    shape = models.IntegerField(_("Type of crosssection."), null=True,
                                choices=UrbanConstants.SHAPE_TYPE_CHOICES)
    width = models.CharField(_("Width."), max_length=255, null=True)
    height = models.CharField(_("Height."), max_length=255, null=True)
    code = models.CharField(
        max_length=100, blank=True,
        help_text='the original code that came from the provider/organisation')

    class Meta:
        db_table = 'v2_cross_section_definition'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 Cross section definition %s" % self.pk


class V2CrossSectionLocation(models.Model):
    """Model representing a CrossSectionLocation for v2 models."""
    channel = models.ForeignKey(V2Channel, on_delete=models.CASCADE, null=True)
    definition = models.ForeignKey(V2CrossSectionDefinition, on_delete=models.CASCADE, null=True)

    reference_level = models.FloatField(blank=True, null=True)
    friction_type = models.IntegerField(
        _("Friction type"), null=True,
        choices=Constants.FRICTION_TYPE_CHOICES)
    friction_value = models.FloatField(_("Friction value."), null=True)
    bank_level = models.FloatField(blank=True, null=True)
    code = models.CharField(
        max_length=100, blank=True,
        help_text='the original code that came from the provider/organisation')

    the_geom = models.PointField(blank=True, null=True, srid=WORK_SRID)

    objects = GeoManager()

    class Meta:
        db_table = 'v2_cross_section_location'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "%s %s" % (self.__class__.__name__, self.pk)


class V2OneDeeLateral(models.Model):
    """
    Model representing a V2OneDeeLateral model for v2 models.

    - input fields (copied from turtle_core)
    - model fields (some may be input fields as well)

    """
    connection_node = models.ForeignKey(V2ConnectionNode, on_delete=models.CASCADE)
    timeseries = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'v2_1d_lateral'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 1d Lateral {} (connection_node: {})".format(
            self.pk, self.connection_node.pk)


class V2Pipe(models.Model):
    """Model representing a Pipe for v2 models."""
    display_name = models.CharField(max_length=255, blank=True)
    code = models.CharField(
        max_length=100, blank=True,
        help_text='the original code that came from the provider/organisation')

    profile_num = models.IntegerField(
        null=True, blank=True,
        help_text='nummer bijzonder profiel (width, height, '
                  'shape should be empty)')

    sewerage_type = models.IntegerField(
        _("Type of pipe."), null=True, blank=True,
        choices=UrbanConstants.PIPE_SEWERAGE_TYPE_CHOICES)
    calculation_type = models.IntegerField(
        _("Modelling type of pipe"),
        null=True, blank=True,
        choices=UrbanConstants.PIPE_CALCULATION_TYPE_CHOICES)
    invert_level_start_point = models.FloatField(
        _("Elevation level inside pipe at start of pipe."), null=True)
    invert_level_end_point = models.FloatField(
        _("Elevation level inside pipe at end of pipe."), null=True)
    cross_section_definition = models.ForeignKey(
        V2CrossSectionDefinition,
        on_delete=models.CASCADE,
        null=True)
    friction_value = models.FloatField(_("Friction value."), null=True)
    friction_type = models.IntegerField(
        _("Friction type"), null=True,
        choices=Constants.FRICTION_TYPE_CHOICES)
    dist_calc_points = models.FloatField(
        _("Distance between 3di calculation points"), null=True)
    material = models.IntegerField(
        _("Material of pipe."), null=True,
        choices=Constants.MATERIAL_TYPE_CHOICES)
    original_length = models.FloatField(
        _("Real length of pipe as recorded in source data."), null=True)
    zoom_category = models.IntegerField(
        _("Rank of object."), null=True,
        choices=UrbanConstants.ZOOM_CATEGORY_CHOICES)

    connection_node_start = models.ForeignKey(
        V2ConnectionNode,
        on_delete=models.CASCADE,
        related_name="v2_pipe_connection_node_start",
        null=True,
        blank=True)

    connection_node_end = models.ForeignKey(
        V2ConnectionNode,
        on_delete=models.CASCADE,
        related_name="v2_pipe_connection_node_end",
        null=True,
        blank=True)

    objects = GeoManager()

    class Meta:
        db_table = 'v2_pipe'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 pipe: {}".format(self.pk)


class V2SurfaceParameters(models.Model):
    """parameters a surface can and must have to calculate its inflow"""

    outflow_delay = models.FloatField(
        blank=False, null=False, help_text='reaction factor (/min)'
    )
    surface_layer_thickness = models.FloatField(
        blank=False, null=False, help_text='surface_storage (mm)'
    )
    infiltration = models.BooleanField(
        blank=False, null=False, help_text='switch infiltration on or off'
    )
    max_infiltration_capacity = models.FloatField(
        blank=False, null=False,
        help_text='Max infiltration capacity (fb) in mm/h'
    )
    min_infiltration_capacity = models.FloatField(
        blank=False, null=False,
        help_text='Min infiltration capacity (fe) in mm/h'
    )
    infiltration_decay_constant = models.FloatField(
        blank=False, null=False,
        help_text='Time factor reduction (ka) of infiltration capacity (/h)'
    )
    infiltration_recovery_constant = models.FloatField(
        blank=False, null=False,
        help_text='Time factor recovery (kh) of infiltration capacity (/h)'
    )

    class Meta:
        db_table = 'v2_surface_parameters'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 surface parameter: {}".format(self.pk)


class V2Surface(models.Model):
    """a generic model for surfaces that can be used to calculate inflow"""

    display_name = models.CharField(max_length=255, blank=True)
    code = models.CharField(
        max_length=100, blank=True)
    zoom_category = models.IntegerField(
        null=True, blank=True, help_text="Rank of object"
    )
    nr_of_inhabitants = models.FloatField(
        null=True, blank=True, help_text="Number of inhabitants"
    )
    dry_weather_flow = models.FloatField(
        null=True, blank=True, help_text="Dry weather flow production"
    )
    function = models.CharField(
        max_length=64, null=True, blank=True,
        help_text="function of the surface"
    )
    area = models.FloatField(blank=True, null=True)
    surface_parameters = models.ForeignKey(
        V2SurfaceParameters, blank=True, null=True,
        on_delete=models.CASCADE,
    )
    the_geom = models.PolygonField(blank=True, null=True, srid=WORK_SRID)

    class Meta:
        db_table = 'v2_surface'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 surface: {}".format(self.pk)


class V2SurfaceMap(models.Model):
    """Model representing a SurfaceMap for v2 models."""
    surface_type = models.CharField(
        null=True, blank=True, max_length=40,
        help_text=
        'either the V2ImperviousSurface table named v2_impervious_surface or '
        'the V2Surface table named v2_surface')
    surface_id = models.IntegerField(
        null=True, blank=True, help_text=
        'the ID belonging to the surface_type entry'
    )
    connection_node = models.ForeignKey(V2ConnectionNode, on_delete=models.CASCADE)
    percentage = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'v2_surface_map'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 surface map: {}".format(self.pk)


class V2ImperviousSurface(models.Model):
    """Model representing a ImperviousSurface for v2 models."""
    display_name = models.CharField(max_length=255, blank=True)
    code = models.CharField(
        max_length=100, blank=True,
        help_text='the original code that '
                  'came from the provider/organisation'
    )

    surface_class = models.CharField(
        _("Surface class."),
        max_length=128,
        choices=UrbanConstants.SURFACE_CLASS_CHOICES)
    surface_sub_class = models.CharField(
        _("Surface sub class."),
        max_length=128, blank=True, null=True,
        help_text='Toekomst: klinkers, asfalt, etc...')
    surface_inclination = models.CharField(
        _("Surface inclination."),
        max_length=64,
        choices=UrbanConstants.SURFACE_INCLINATION_CHOICES)
    zoom_category = models.IntegerField(
        _("Rank of object."), null=True,
        choices=UrbanConstants.ZOOM_CATEGORY_CHOICES)
    nr_of_inhabitants = models.FloatField(
        _("Number of inhabitants."), null=True, blank=True)
    dry_weather_flow = models.FloatField(
        _("Dry weather flow production."), null=True, blank=True)
    area = models.FloatField(blank=True, null=True)

    the_geom = models.PolygonField(blank=True, null=True, srid=WORK_SRID)

    objects = GeoManager()

    class Meta:
        db_table = 'v2_impervious_surface'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 impervious Surface: {}".format(self.pk)


class V2Orifice(models.Model):
    """Model representing an Orifice for v2 models."""
    display_name = models.CharField(max_length=255, blank=True)
    code = models.CharField(
        max_length=100, blank=True,
        help_text='the original code that '
                  'came from the provider/organisation'
    )
    crest_level = models.FloatField(blank=True, null=True)
    sewerage = models.BooleanField(default=False)
    cross_section_definition = models.ForeignKey(V2CrossSectionDefinition, on_delete=models.CASCADE,
                                                 blank=True, null=True)
    friction_value = models.FloatField(_("Friction value."), null=True)
    friction_type = models.IntegerField(
        _("Friction type"), null=True,
        choices=Constants.FRICTION_TYPE_CHOICES)
    discharge_coefficient_positive = models.FloatField(blank=True, null=True)
    discharge_coefficient_negative = models.FloatField(blank=True, null=True)
    zoom_category = models.IntegerField(blank=True, null=True)
    # TODO: not NULL constraint
    crest_type = models.IntegerField(blank=True, null=True, default=4)

    connection_node_start = models.ForeignKey(
        V2ConnectionNode, on_delete=models.CASCADE, related_name="v2 orifice connection node start",
        null=True, blank=True
    )

    connection_node_end = models.ForeignKey(
        V2ConnectionNode, on_delete=models.CASCADE, related_name=" v2 orifice connection node end",
        null=True, blank=True
    )

    class Meta:
        db_table = 'v2_orifice'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 orifice: {}".format(self.pk)


class V2Pumpstation(models.Model):
    """
    Model representing a Pumpstation ((Riool)gemaal in Dutch) model for v2
    models.
    """
    display_name = models.CharField(max_length=255, blank=True)
    code = models.CharField(
        max_length=100, blank=True,
        help_text='the original code that came '
                  'from the provider/organisation'
    )

    classification = models.IntegerField(
        _("Type of "), null=True,
        choices=UrbanConstants.PUMPSTATION_CLASSIFICATION_CHOICES)
    type = models.IntegerField(
        _("Type of "), null=True,
        choices=UrbanConstants.PUMPSTATION_TYPE_CHOICES,
        default=1)
    sewerage = models.BooleanField(default=False)
    start_level = models.FloatField(blank=True, null=True)
    lower_stop_level = models.FloatField(blank=True, null=True)
    upper_stop_level = models.FloatField(blank=True, null=True)

    capacity = models.FloatField(blank=True, null=True)
    zoom_category = models.IntegerField(blank=True, null=True)

    connection_node_start = models.ForeignKey(
        V2ConnectionNode,
        on_delete=models.CASCADE,
        related_name='v2 pumpstation connection node start',
        null=True,
        blank=True
    )

    connection_node_end = models.ForeignKey(
        V2ConnectionNode,
        on_delete=models.CASCADE,
        related_name='v2 pumpstation connection node end',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'v2_pumpstation'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        if self.code:
            return "v2 pumpstation %s - %s" % (self.pk, self.code)
        else:
            return "v2 pumpstation %s" % self.pk


class V2PumpedDrainageArea(models.Model):
    """
    Model representing a PumpedDrainageArea (Bemalingsgebied in Dutch) for v2
    models.

    Helper table for pipe mappings in urban.
    """
    name = models.CharField(_("name"), max_length=64)
    code = models.CharField(
        max_length=100, blank=True,
        help_text='the original code that came '
                  'from the provider/organisation'
    )

    the_geom = models.PolygonField(_("geometry"), srid=WORK_SRID)

    class Meta:
        db_table = 'v2_pumped_drainage_area'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return self.name


class V2Culvert(models.Model):
    """
    Model representing a Culvert (Leiding in Dutch) for v2 models structure.
    """
    display_name = models.CharField(max_length=255, blank=True)
    code = models.CharField(
        max_length=100, blank=True,
        help_text='the original code that came from the provider/organisation')

    # Model fields (some may be input fields as well)
    # TODO: PIPE_CALCULATION_TYPE_CHOICES must be re-worked!
    calculation_type = models.IntegerField(
        null=True, blank=True,
        choices=UrbanConstants.PIPE_CALCULATION_TYPE_CHOICES
    )
    friction_value = models.FloatField(_("Friction value."), null=True)
    friction_type = models.IntegerField(
        _("Friction type"), null=True,
        choices=Constants.FRICTION_TYPE_CHOICES)
    dist_calc_points = models.FloatField(
        _("Distance between 3di calculation points"), null=True)
    zoom_category = models.IntegerField(
        _("Rank of object."), null=True,
        choices=UrbanConstants.ZOOM_CATEGORY_CHOICES)
    cross_section_definition = models.ForeignKey(
        V2CrossSectionDefinition,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    discharge_coefficient_positive = models.FloatField(blank=False, null=False, default=1)
    discharge_coefficient_negative = models.FloatField(blank=False, null=False, default=1)
    invert_level_start_point = models.FloatField(null=True)
    invert_level_end_point = models.FloatField(null=True)

    the_geom = models.LineStringField(_("geometry"), srid=WORK_SRID)

    objects = GeoManager()

    connection_node_start = models.ForeignKey(
        V2ConnectionNode,
        on_delete=models.CASCADE,
        related_name="culvert_connection_node_start",
        null=True,
        blank=True)

    connection_node_end = models.ForeignKey(
        V2ConnectionNode,
        on_delete=models.CASCADE,
        related_name="culvert_connection_node_end",
        null=True,
        blank=True)

    class Meta:
        db_table = 'v2_culvert'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 culvert: {}".format(self.pk)


class V2TwoDeeLateral(models.Model):
    """Model representing a TwoDeeLateral for v2 models."""
    type = models.IntegerField(null=True, blank=True)
    timeseries = models.TextField(blank=True, null=True)

    the_geom = models.PointField(blank=True, null=True, srid=WORK_SRID)

    objects = GeoManager()

    class Meta:
        db_table = 'v2_2d_lateral'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "%s %s" % (self.__class__.__name__, self.pk)


class V2NumericalSettings(models.Model):
    """advanced numerical settings"""

    cfl_strictness_factor_1d = models.FloatField(
        blank=True, null=True, help_text='(1.0)')
    cfl_strictness_factor_2d = models.FloatField(
        blank=True, null=True, help_text='(1.0')
    convergence_cg = models.FloatField(
        blank=True, null=True,
        help_text=
        'Convergence property of the conjugate gradient method, '
        'defaults to 1.0e-9'
    )
    convergence_eps = models.FloatField(null=True, blank=True)

    flow_direction_threshold = models.FloatField(
        blank=True, null=True,
        help_text=
        'determines the threshold for upwind direction, defaults to 1e-05'
    )
    frict_shallow_water_correction = models.IntegerField(
        blank=True, null=True,
        choices=Constants.FRICTION_SHALLOW_WATER_CORRECTION_CHOICES,
        help_text='defaults to 0'
    )
    general_numerical_threshold = models.FloatField(
        blank=True, null=True,
        help_text=
        'defaults to 1.0e-8'
    )
    integration_method = models.IntegerField(
        null=True, blank=True,
        choices=UrbanConstants.INTEGRATION_METHOD_CHOICES)

    limiter_grad_1d = models.IntegerField(
        null=True, blank=True,
        choices=Constants.LIMITER_GRAD_1D,
        help_text='defaults to 1'
    )
    limiter_grad_2d = models.IntegerField(
        null=True, blank=True,
        choices=Constants.LIMITER_GRAD_2D,
        help_text='defaults to 1'
    )
    limiter_slope_crossectional_area_2d = models.IntegerField(
        blank=True, null=True,
        choices=Constants.LIMITER_SLOPE_CROSSSECTIONAL_AREA_CHOICES,
        help_text='defaults to 0'
    )
    limiter_slope_friction_2d = models.IntegerField(
        blank=True, null=True,
        choices=Constants.LIMITER_SLOPE_FRICTION_CHOICES,
        help_text='defaults to 0'
    )
    max_nonlin_iterations = models.IntegerField(null=True, blank=True)
    max_degree = models.IntegerField(null=False, blank=False, default=0)

    minimum_friction_velocity = models.FloatField(
        blank=True, null=True,
        help_text='minimum friction velocity, default is  0.05 m/s'
    )
    minimum_surface_area = models.FloatField(
        blank=True, null=True,
        help_text='minimum surface area in m2, defaults to 1.0e-8'
    )
    precon_cg = models.IntegerField(
        blank=True, null=True, help_text='0 or 1 (1)')
    preissmann_slot = models.FloatField(
        blank=True, null=True,
        help_text='defaults to 0.0'
    )
    pump_implicit_ratio = models.FloatField(
        blank=True, null=True, help_text='(between 0 and 1')

    thin_water_layer_definition = models.FloatField(
        blank=True, null=True,
        help_text='thin water layer definition in m, defaults to 0.1'
    )
    use_of_cg = models.IntegerField(null=False, blank=False, default=0)
    use_of_nested_newton = models.IntegerField(
        null=False, blank=False, default=0)

    class Meta:
        db_table = 'v2_numerical_settings'
        ordering = ('pk',)
        app_label = 'threedi_tools'


class V2Interflow(models.Model):
    interflow_type = models.IntegerField(
        _("interflow type 0-4"), null=False, blank=False, default=0)
    porosity = models.FloatField(blank=True, null=True)
    porosity_file = models.CharField(max_length=255, blank=True, null=True)
    porosity_layer_thickness = models.FloatField(blank=True, null=True)
    impervious_layer_elevation = models.FloatField(blank=True, null=True)
    hydraulic_conductivity = models.FloatField(blank=True, null=True)
    hydraulic_conductivity_file = models.CharField(
        max_length=255, blank=True, null=True
    )
    display_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'v2_interflow'
        ordering = ('pk',)
        app_label = 'threedi_tools'


class V2SimpleInfiltration(models.Model):
    infiltration_rate = models.FloatField(null=False, blank=False)
    infiltration_rate_file = models.CharField(max_length=255, blank=True,
                                              null=True)
    infiltration_surface_option = models.IntegerField(null=True, blank=True)
    max_infiltration_capacity_file = models.TextField(
        blank=True, null=True,
        help_text='relative path to the max_infiltration_capacity_file')
    display_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'v2_simple_infiltration'
        ordering = ('pk',)
        app_label = 'threedi_tools'


class V2Groundwater(models.Model):
    groundwater_impervious_layer_level = models.FloatField(
        null=True, blank=True)
    groundwater_impervious_layer_level_file = models.CharField(
        max_length=255, blank=True, null=True)
    groundwater_impervious_layer_level_type = models.IntegerField(
        blank=True, null=True)
    phreatic_storage_capacity = models.FloatField(null=True, blank=True)
    phreatic_storage_capacity_file = models.CharField(
        max_length=255, blank=True, null=True)
    phreatic_storage_capacity_type = models.IntegerField(
        blank=True, null=True)
    equilibrium_infiltration_rate = models.FloatField(null=True, blank=True)
    equilibrium_infiltration_rate_file = models.CharField(
        max_length=255, blank=True, null=True)
    equilibrium_infiltration_rate_type = models.IntegerField(
        blank=True, null=True)
    initial_infiltration_rate = models.FloatField(null=True, blank=True)
    initial_infiltration_rate_file = models.CharField(
        max_length=255, blank=True, null=True)
    initial_infiltration_rate_type = models.IntegerField(blank=True, null=True)
    infiltration_decay_period = models.FloatField(
        null=True, blank=True)
    infiltration_decay_period_file = models.CharField(
        max_length=255, blank=True, null=True)
    infiltration_decay_period_type = models.IntegerField(blank=True, null=True)
    groundwater_hydro_connectivity = models.FloatField(null=True, blank=True)
    groundwater_hydro_connectivity_file = models.CharField(
        max_length=255, blank=True, null=True)
    groundwater_hydro_connectivity_type = models.IntegerField(
        blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    leakage = models.FloatField(blank=True, null=True)
    leakage_file = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'v2_groundwater'
        ordering = ('pk',)
        app_label = 'threedi_tools'


class V2GlobalSettings(models.Model):
    """Settings for v2 models."""
    use_2d_flow = models.BooleanField(null=False, blank=False)
    use_1d_flow = models.BooleanField(null=False, blank=False)
    # used as a boolean, no true boolean due to unexpected behaviour
    # during south migrations
    use_2d_rain = models.IntegerField(null=False, blank=False, default=1)

    manhole_storage_area = models.FloatField(blank=True, null=True)
    name = models.CharField(_("Name"), null=True, max_length=128, unique=True)
    sim_time_step = models.FloatField(blank=False, null=False)
    minimum_sim_time_step = models.FloatField(blank=True, null=True)
    maximum_sim_time_step = models.FloatField(blank=True, null=True)
    nr_timesteps = models.IntegerField(null=False, blank=False)
    start_time = models.DateTimeField(blank=True, null=True)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    grid_space = models.FloatField(null=False, blank=False)
    dist_calc_points = models.FloatField(null=False, blank=False)
    kmax = models.IntegerField(null=False, blank=False)
    guess_dams = models.IntegerField(blank=True, null=True)

    table_step_size = models.FloatField(null=False, blank=False)
    advection_1d = models.IntegerField(null=False, blank=False)
    advection_2d = models.IntegerField(null=False, blank=False)

    dem_file = models.CharField(max_length=255, blank=True, null=True)
    epsg_code = models.IntegerField(
        blank=True, null=True, help_text='required if no DEM')

    frict_type = models.IntegerField(
        blank=True, null=True, choices=Constants.FRICTION_TYPE_CHOICES)
    frict_coef = models.FloatField(blank=False, null=False)
    frict_coef_file = models.CharField(max_length=255, blank=True, null=True)
    frict_avg = models.IntegerField(
        blank=False, null=False, default=0,
        choices=Constants.FRICTION_AVG_CHOICES
    )
    water_level_ini_type = models.IntegerField(blank=True, null=True)
    initial_waterlevel = models.FloatField(null=False, blank=False)
    initial_waterlevel_file = models.CharField(max_length=255, blank=True,
                                               null=True)
    initial_groundwater_level = models.FloatField(blank=True, null=True)
    initial_groundwater_level_file = models.CharField(
        max_length=255, blank=True, null=True)
    initial_groundwater_level_type = models.IntegerField(blank=True, null=True)
    interception_global = models.FloatField(blank=True, null=True)
    interception_file = models.CharField(max_length=255, blank=True,
                                         null=True)
    dem_obstacle_detection = models.BooleanField(
        default=False, null=False, blank=False
    )
    dem_obstacle_height = models.FloatField(blank=True, null=True)
    embedded_cutoff_threshold = models.FloatField(
        blank=True, null=True)
    use_0d_inflow = models.IntegerField(
        blank=False, null=False, default=0,
        choices=Constants.USE_0D_INFLOW_CHOICES
    )
    # controls
    control_group = models.ForeignKey(V2ControlGroup, on_delete=models.CASCADE, blank=True, null=True)
    # numerics

    flooding_threshold = models.FloatField(null=False, blank=False)
    timestep_plus = models.BooleanField(
        default=False, help_text='(False)')
    max_angle_1d_advection = models.FloatField(
        blank=True, null=True, help_text='degrees, 90 or less (90)')

    # output
    output_time_step = models.FloatField(blank=True, null=True)

    wind_shielding_file = models.CharField(
        max_length=255, blank=True, null=True
    )
    table_step_size_1d = models.FloatField(null=True, blank=True)
    table_step_size_volume_2d = models.FloatField(null=True, blank=True)
    numerical_settings = models.ForeignKey(
        V2NumericalSettings, on_delete=models.CASCADE, blank=False, null=False)

    groundwater_settings = models.ForeignKey(
        V2Groundwater, on_delete=models.CASCADE, blank=True, null=True)
    simple_infiltration_settings = models.ForeignKey(
        V2SimpleInfiltration, on_delete=models.CASCADE, blank=True, null=True)
    interflow_settings = models.ForeignKey(
        V2Interflow, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'v2_global_settings'
        ordering = ('pk',)
        app_label = 'threedi_tools'


class V2GridRefinement(models.Model):
    """Model representing a GridRefinement for v2 models."""
    display_name = models.CharField(max_length=255, blank=True)
    refinement_level = models.IntegerField(null=True, blank=True)
    code = models.CharField(
        max_length=100, blank=True,
        help_text='the original code that came from the provider/organisation')

    the_geom = models.LineStringField(blank=True, null=True, srid=WORK_SRID)

    objects = GeoManager()

    class Meta:
        db_table = 'v2_grid_refinement'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 grid refinement %s" % self.pk


class V2GridRefinementArea(models.Model):
    """Model representing a GridRefinement area for v2 models."""
    display_name = models.CharField(max_length=255, blank=True)
    refinement_level = models.IntegerField(null=True, blank=True)
    code = models.CharField(
        max_length=100, blank=True,
        help_text='the original code that came from the provider/organisation')

    the_geom = models.PolygonField(blank=True, null=True, srid=WORK_SRID)

    objects = GeoManager()

    class Meta:
        db_table = 'v2_grid_refinement_area'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 grid refinement area %s" % self.pk


class V2FloodFill(models.Model):
    """Model representing a Floodfill for v2 models."""
    waterlevel = models.FloatField(blank=True, null=True)

    the_geom = models.PointField(blank=True, null=True, srid=WORK_SRID)

    objects = GeoManager()

    class Meta:
        db_table = 'v2_floodfill'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 floodfill %s" % self.pk


class V2Weir(models.Model):
    """Model representing a sewerage weir (NL: stuw) for v2 models."""
    display_name = models.CharField(max_length=255, blank=True)
    code = models.CharField(
        max_length=100, blank=True,
        help_text='the original code that came from the provider/organisation')

    crest_level = models.FloatField(blank=True, null=True)
    # TODO: not NULL constraint
    crest_type = models.IntegerField(
        _("sharp or broad crested weir"),
        null=True, blank=True)
    cross_section_definition = models.ForeignKey(V2CrossSectionDefinition, on_delete=models.CASCADE,
                                                 blank=True, null=True)
    sewerage = models.BooleanField(default=False)
    discharge_coefficient_positive = models.FloatField(blank=True, null=True)
    discharge_coefficient_negative = models.FloatField(blank=True, null=True)
    # corresponds to migration #37
    external = models.NullBooleanField(blank=True, null=True, default=None)
    zoom_category = models.IntegerField(blank=True, null=True)
    friction_value = models.FloatField(_("Friction value."), null=True)
    friction_type = models.IntegerField(
        _("Friction type"), null=True,
        choices=Constants.FRICTION_TYPE_CHOICES)

    connection_node_start = models.ForeignKey(
        V2ConnectionNode,
        on_delete=models.CASCADE,
        related_name="v2_weir_connection_node_start",
        null=True,
        blank=True
    )

    connection_node_end = models.ForeignKey(
        V2ConnectionNode,
        on_delete=models.CASCADE,
        related_name="v2_weir_connection_node_end",
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'v2_weir'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 weir: {}".format(self.pk)


class V2TwoDeeBoundaryConditions(models.Model):
    """Model representing TwoDeeBoundaryConditions for v2 models."""
    display_name = models.CharField(max_length=255, blank=True)
    timeseries = models.TextField(blank=True, null=True)
    boundary_type = models.IntegerField(null=True, blank=True)
    the_geom = models.LineStringField(blank=True, null=True, srid=WORK_SRID)
    objects = GeoManager()

    class Meta:
        db_table = 'v2_2d_boundary_conditions'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "%s %s" % (self.__class__.__name__, self.pk)


class V2Windshielding(models.Model):
    """
    Model representing a Windshielding for v2 models

    N.B.: odd class name to prevent Django auto-generated strings to become
    too long for auth_permission table!
    """
    channel = models.ForeignKey(V2Channel, on_delete=models.CASCADE, null=True, blank=True)
    north = models.FloatField(null=True, blank=True)
    northeast = models.FloatField(null=True, blank=True)
    east = models.FloatField(null=True, blank=True)
    southeast = models.FloatField(null=True, blank=True)
    south = models.FloatField(null=True, blank=True)
    southwest = models.FloatField(null=True, blank=True)
    west = models.FloatField(null=True, blank=True)
    northwest = models.FloatField(null=True, blank=True)

    the_geom = models.PointField(blank=True, null=True, srid=WORK_SRID)

    objects = GeoManager()

    class Meta:
        db_table = 'v2_windshielding'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 windshielding {0}".format(self.pk)


class V2Obstacle(models.Model):
    """Model representing an Obstacle for v2 models."""
    crest_level = models.FloatField(blank=True, null=True,
                                    help_text="value in [mMSL]")
    code = models.CharField(
        max_length=100, blank=True,
        help_text='the original code that came from the provider/organisation')

    the_geom = models.LineStringField(blank=False, null=True, srid=WORK_SRID)

    objects = GeoManager()

    class Meta:
        db_table = 'v2_obstacle'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 obstacle: {}".format(self.pk)


class V2ImperviousSurfaceMap(models.Model):
    """Model representing a ImperviousSurfaceMap for v2 models."""
    impervious_surface = models.ForeignKey(V2ImperviousSurface,on_delete=models.CASCADE,
                                           null=True, blank=True)
    connection_node = models.ForeignKey(V2ConnectionNode, on_delete=models.CASCADE)
    percentage = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'v2_impervious_surface_map'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 impervious_surface_map: {}".format(self.pk)


class V2AggregationSettings(models.Model):
    """Aggregation settings."""
    global_settings = models.ForeignKey(
        V2GlobalSettings, on_delete=models.CASCADE, null=True, blank=True, default=None,
        help_text='Empty=for all models, filled in=only for that model'
    )
    var_name = models.CharField(
        max_length=100, blank=True, default='',
        help_text='output var name (input var name if no flow_variable)'
    )
    flow_variable = models.CharField(
        max_length=100, blank=True, null=True, default='',
        help_text='(optional) input var name'
    )
    aggregation_method = models.CharField(
        max_length=100, blank=True, default='',
        help_text='aggregation method, choose one of: avg, min, max, cum, med'
                  ', cum_negative, cum_positive, duration_positive, '
                  'duration_negative'
    )
    aggregation_in_space = models.BooleanField(
        default=False,
        help_text='spatial aggregation'
    )
    timestep = models.IntegerField(
        default=300, help_text='output timestep in seconds'
    )

    class Meta:
        db_table = 'v2_aggregation_settings'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "V2AggregationSettings pk=%i" % self.pk


class DemAverageArea(models.Model):

    the_geom = models.PolygonField(blank=True, null=True, srid=WORK_SRID)

    class Meta:
        db_table = 'v2_dem_average_area'
        ordering = ('pk',)
        app_label = 'threedi_tools'

    def __unicode__(self):
        return "v2 DEM average area: {}".format(self.pk)
