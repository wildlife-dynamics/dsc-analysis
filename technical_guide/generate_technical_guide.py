"""
Generate the DSC Analysis Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: dsc_analysis_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "dsc_analysis_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"DSC Analysis — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

W = A4[0] - 4*cm   # usable width

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("DSC Analysis", TITLE),
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Distance Sample Count — Wildlife Survey Analysis Pipeline", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>dsc_analysis</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>dsc_analysis</b> workflow ingests Distance Sample Count (DSC) "
      "wildlife survey data from EarthRanger and produces structured, analysis-ready "
      "datasets for use in population density modelling. The workflow supports "
      "<b>multiple surveys</b> in a single run, each defined by its own EarthRanger "
      "connection, patrol type, survey time window, and transect spatial group. "
      "Each survey is further split automatically into its <b>detected activity "
      "periods</b>, so a site visited in e.g. both February and June produces two "
      "independent, period-tagged output sets rather than one combined one."),
    sp(4),
    p("For each survey period the workflow delivers:"),
    bullet("A <b>metadata CSV</b> — survey-level observations including transect IDs, "
           "observer counts, team members, and event types"),
    bullet("A <b>field effort CSV</b> — per-team-member daily distance travelled, "
           "duration, and man-hours, derived from EarthRanger subject GPS tracks"),
    bullet("An <b>analysis data CSV</b> — wildlife observation events enriched with "
           "off-transect distances, orthogonal distances, estimated animal positions, "
           "and satellite-derived environmental covariates (NDVI, terrain slope)"),
    bullet("An <b>events GeoPackage</b> — spatial point layer of wildlife observations "
           "with key distance sampling geometry fields"),
    bullet("A <b>transect areas GeoPackage</b> — visited transect corridors (buffered) "
           "labelled with mean NDVI, slope, and PALSAR woody cover values from Google "
           "Earth Engine"),
    bullet("A <b>transect lines GeoPackage</b> — visited transect centrelines "
           "(unbuffered), reprojected to EPSG:4326"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output type", "Format", "Description"],
            ["{survey}_{period}_analysis_metadata", "CSV",
             "Survey event metadata: transect IDs, team members, observer counts, event types"],
            ["{survey}_{period}_field_effort", "CSV",
             "Per-team-member daily distance, duration, and man-hours from GPS tracks"],
            ["{survey}_{period}_analysis_data",     "CSV",
             "Wildlife observations with distance fields, animal position estimates, "
             "NDVI, and slope covariates"],
            ["{survey}_{period}_events",            "GeoPackage",
             "Spatial point layer of wildlife observation events"],
            ["{survey}_{period}_transect_areas",    "GeoPackage",
             "Visited transect corridors (buffered) with NDVI, slope, and woody cover labels (EPSG:4326)"],
            ["{survey}_{period}_transect_lines",    "GeoPackage",
             "Visited transect centrelines (unbuffered) in EPSG:4326"],
        ],
        [5.5*cm, 2.5*cm, W - 8*cm],
    ),
    note("{survey} is the survey name as defined in the connection configuration and "
         "{period} is the detected activity period label (e.g. 2026_02). All six output "
         "file sets are produced independently for each survey period."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies"),
    hr(),
    h2("2.1  Python packages"),
    p("The workflow declares six versioned packages from the Ecoscope "
      "prefix.dev channels:"),
    make_table(
        [
            ["Package", "Version", "Channel"],
            ["ecoscope-platform",                      ">=2.15.0, <2.16.0", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",          "0.1.0rc14.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",             "0.0.0rc1.*",   "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-distance-sample-counts", "1.0.5.*", "ecoscope-workflows-custom"],
            ["pydeck",                                  "0.9.2", "conda-forge"],
            ["opentelemetry-sdk",                       ">=1.20.0, <2.0.0", "conda-forge"],
        ],
        [7*cm, 3.5*cm, W - 10.5*cm],
    ),
    note("Earlier revisions of this workflow additionally pinned separate "
         "ecoscope-workflows-core / ecoscope-workflows-ext-ecoscope packages plus "
         "site-specific extensions (ecoscope-workflows-ext-big-life, -ext-mnc, "
         "-ext-ate). These have been consolidated into the single ecoscope-platform "
         "package and removed where no longer required."),
    sp(6),
    h2("2.2  Google Earth Engine connection"),
    p("A Google Earth Engine (GEE) service account connection is required "
      "(<b>set_gee_connection</b>). The GEE client is used to build satellite "
      "imagery composites and label transect lines with environmental covariates. "
      "The same GEE client is shared across all surveys in a single run."),
    sp(6),
    h2("2.3  EarthRanger connections"),
    p("One EarthRanger connection is required <i>per survey</i>. Each entry in "
      "<b>connection_config</b> pairs an EarthRanger server and patrol type ID "
      "with one or more survey definitions (survey name, time window, and "
      "transect spatial group ID). Connections are split and distributed to "
      "parallel per-survey pipelines via <b>split_connection_configs</b>."),
    sp(6),
    h2("2.4  EarthRanger data requirements"),
    p("The workflow expects the following event types to be present in EarthRanger "
      "for each patrol:"),
    make_table(
        [
            ["Event type", "Role"],
            ["distancecountpatrol_rep",        "Survey metadata event — carries transect ID, "
                                               "team members, and observer count"],
            ["distance_count_patrol_metadata", "Alternative metadata event type (also retained "
                                               "during metadata filtering)"],
            ["distancecountwildlife_rep",       "Wildlife observation event — carries species, "
                                               "total count, distance to centre, radial angle, "
                                               "and juvenile count"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(6),
    note("Field effort computation additionally requires that team members recorded "
         "on patrol metadata events (Team Members / reported_by) match named "
         "subjects/trackers in EarthRanger, so their GPS observations can be "
         "retrieved and converted into daily distance and duration statistics."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. INPUT CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Input Configuration"),
    hr(),
    h2("3.1  Workflow-level parameters"),
    make_table(
        [
            ["Parameter", "Description"],
            ["workflow_details",  "Human-readable name and optional description for this "
                                  "workflow run — used for dashboard registration"],
            ["time_range",        "Required on all Ecoscope workflows. Used for timestamp "
                                  "display and UTC conversion only — does not filter which "
                                  "patrol events are fetched. Set broadly to cover all surveys "
                                  "in the run. Each survey's own time window controls data fetching."],
            ["gee_client",        "Google Earth Engine service account connection"],
            ["connection_config", "Array of EarthRanger connection entries, one per survey "
                                  "(see Section 3.2)"],
        ],
        [4*cm, W - 4*cm],
    ),
    sp(6),
    h2("3.2  Connection config entry (per survey)"),
    p("Each entry in <b>connection_config</b> defines one EarthRanger site and "
      "one or more surveys to run against it:"),
    make_table(
        [
            ["Field", "Type", "Description"],
            ["earthranger.server",     "Connection", "EarthRanger data source connection"],
            ["earthranger.patrol_type_id", "String",
             "Numeric or UUID identifier for the patrol type containing DSC surveys"],
            ["surveys[].surveyName",   "String",  "Unique name for this survey (used as output filename prefix)"],
            ["surveys[].time_range",   "Object",  "Survey-specific data fetch window. Patrol events within this "
                                                  "since / until range are retrieved from EarthRanger for this "
                                                  "survey. This is the field that controls which data is pulled — "
                                                  "not the top-level time_range."],
            ["surveys[].erSpatialTransectsGroupId", "String",
             "EarthRanger spatial group ID that contains the transect line features"],
        ],
        [4*cm, 2*cm, W - 6*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. DATA INGESTION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Data Ingestion"),
    hr(),
    h2("4.1  Connection splitting"),
    p("The combined <b>connection_config</b> is split into individual "
      "per-survey connection objects via <b>split_connection_configs</b>. "
      "All subsequent steps that require per-survey data use "
      "<b>mapvalues</b> to fan out over this list in parallel."),
    sp(6),
    h2("4.2  Patrol events"),
    p("For each survey, <b>fetch_patrol_events</b> retrieves all patrols matching "
      "the configured patrol type ID within the survey time window. "
      "The resulting patrol DataFrame is indexed on the <b>id</b> column via "
      "<b>set_dataframe_index</b> to enable subsequent join operations."),
    sp(6),
    h2("4.3  Survey period splitting"),
    p("Before any further processing, each survey's patrol events are passed through "
      "<b>split_survey_by_period</b>, which detects the distinct activity periods "
      "within the fetched patrol events (e.g. a site visited in February and again "
      "in June) and splits them into independent, period-keyed branches. "
      "<b>unpack_period_connection_survey</b> and <b>unpack_period_patrol_events</b> "
      "then extract the connection/survey config and patrol events for each period, "
      "and <b>get_survey_period_label</b> derives the period label (e.g. "
      "<b>2026_02</b>) used in output filenames. From this point on, every "
      "downstream step fans out over survey <i>periods</i> rather than surveys."),
    sp(6),
    h2("4.4  Patrol transects"),
    p("Transect lines are fetched per survey period via <b>fetch_transects</b>, "
      "using the spatial group ID specified in the survey's connection config. "
      "Because a survey's transect geometry does not change between periods, the "
      "same transects are fetched once per period (duplicated across periods of the "
      "same survey) so that each period's output is self-contained. The transects "
      "are GeoDataFrames in EPSG:4326 as returned by EarthRanger."),
    sp(6),
    h2("4.5  Survey observation events"),
    p("Individual wildlife observation events are fetched from the patrol event IDs "
      "produced by period splitting using <b>fetch_events</b> "
      "(chunk_size: 75). This two-step approach — fetch patrols first, then fetch "
      "the events within them — is required because the EarthRanger API does not "
      "support direct patrol-type filtering on the events endpoint."),
    sp(6),
    h2("4.6  EarthRanger server name"),
    p("The EarthRanger server name (site identifier) is retrieved per survey period "
      "via <b>get_server_name</b> and zipped with the survey event DataFrame. It is "
      "passed to <b>process_events_details</b> as the <b>client</b> argument so "
      "that EarthRanger field IDs can be resolved to human-readable display names. "
      "The domain name is retrieved separately via a second <b>get_server_name</b> "
      "call for use in filename/traceability construction."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. EVENT PROCESSING PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Event Processing Pipeline"),
    hr(),
    h2("5.1  Metadata event branch"),
    p("Survey metadata events (<b>distancecountpatrol_rep</b> and "
      "<b>distance_count_patrol_metadata</b>) are processed through a dedicated "
      "branch to produce the <i>analysis metadata</i> output:"),
    make_table(
        [
            ["Step", "Task", "Purpose"],
            ["1", "filter_row_values",
             "Retain only metadata event types from the raw event fetch"],
            ["2", "parse_df_point",
             "Extract latitude and longitude columns from the GeoDataFrame geometry"],
            ["3", "normalize_json_column (reported_by)",
             "Flatten the reported_by JSON field into flat columns"],
            ["4", "join_list_column (reported_by__name)",
             "Collapse list values in reported_by__name to a comma-separated string"],
            ["5", "process_events_details",
             "Resolve EarthRanger field IDs to display names "
             "(map_to_titles: true, ordered: true)"],
            ["6", "normalize_json_column (event_details)",
             "Flatten the event_details JSON into flat columns"],
            ["7", "map_columns",
             "Retain and rename key columns: time, event_type, serial_number, "
             "latitude, longitude, reported_by, Transect ID, Team Members, "
             "Number of Observers"],
            ["8", "parse_list_column / join_list_column (Team Members)",
             "Parse and flatten Team Members list into a comma-separated string"],
            ["9", "drop_null_columns",
             "Drop any columns that are entirely null after normalisation"],
        ],
        [1.5*cm, 4.5*cm, W - 6*cm],
    ),
    p("The resulting DataFrame is persisted as "
      "<b>{survey_name}_{period}_analysis_metadata.csv</b>."),
    sp(6),
    h2("5.2  Wildlife observation event branch"),
    p("Wildlife observation events (<b>distancecountwildlife_rep</b>) pass through "
      "a separate normalisation branch before being merged with patrol-level "
      "metadata:"),
    make_table(
        [
            ["Step", "Task", "Purpose"],
            ["1", "select_columns (event_details)",
             "Extract only the event_details column from the raw event fetch "
             "for merging with the patrol DataFrame"],
            ["2", "merge_two_dataframes (left join on index)",
             "Join the patrol DataFrame with the event_details column using "
             "the patrol id index"],
            ["3", "convert_column_timezone",
             "Convert the time column to UTC using the timezone from the global time_range "
             "(used for display/conversion only, not for data filtering)"],
            ["4", "normalize_json_column (event_details)",
             "Flatten the merged event_details JSON into flat columns"],
            ["5", "map_columns (patrol rename)",
             "Rename flattened distance sampling fields to standardised names "
             "(see table below)"],
            ["6", "format_text_column (transect_id, lower)",
             "Lowercase transect_id so it matches the lowercased transect names "
             "used downstream for name-based transect matching"],
            ["7", "bfill_within_patrols / ffill_within_patrols",
             "Backward- then forward-fill transect_id and num_observers "
             "within each patrol (group_col: patrol_serial_number) to propagate "
             "metadata event values to wildlife observation rows"],
            ["8", "filter_row_values (wildlife sightings + patrol \"conducted\" markers)",
             "Retain distancecountwildlife_rep, distancecountpatrol_rep, and "
             "distance_count_patrol_metadata after fill propagation. The two patrol "
             "marker types are kept alongside sightings so that a transect with a "
             "patrol but zero sightings still has a row to test against the transect "
             "corridor downstream (Section 6.3) — without this, that transect would "
             "never be flagged as visited"],
            ["9", "add_constant_column (survey_id)",
             "Stamp each row with the survey+period base name (e.g. olaremotorogi_2026_02) "
             "as a survey_id identifier"],
        ],
        [1.5*cm, 4.5*cm, W - 6*cm],
    ),
    note("A later step, filter_row_values (distancecountwildlife_rep only) — Section "
         "6.3 — narrows back down to sightings-only immediately before the merge that "
         "feeds analysis_data.csv / events.gpkg. The patrol marker rows are only ever "
         "needed to establish which transects were visited; they do not appear in "
         "either of those two exports."),
    sp(6),
    h2("5.3  Field name mapping"),
    p("The <b>map_columns</b> step in the wildlife observation branch renames "
      "the flattened EarthRanger field codes to analysis-ready column names:"),
    make_table(
        [
            ["Source field (EarthRanger)", "Target column"],
            ["event_details__distancecountpatrol_numberofobservers", "num_observers"],
            ["event_details__distancecountpatrol_teammembers",        "Team Members"],
            ["event_details__distancecountpatrol_transectid",         "transect_id"],
            ["event_details__distancecountwildlife_distancetocentre", "dist_to_centre"],
            ["event_details__distancecountwildlife_numberofjuveniles","num_juveniles"],
            ["event_details__distancecountwildlife_radialangle",       "radialangle"],
            ["event_details__distancecountwildlife_species",           "species"],
            ["event_details__distancecountwildlife_totalcount",        "totalcount"],
            ["event_details__Transect_ID  (alt. form, underscore)",    "transect_id_v2"],
            ["event_details__Transect ID  (alt. form, space)",         "transect_id_v2"],
            ["event_details__Team_members (alt. form)",                "Team Members"],
            ["event_details__Number_of_observers (alt. form)",         "num_observers"],
        ],
        [8*cm, W - 8*cm],
    ),
    note("The mapping includes both the snake_case EarthRanger internal names and "
         "alternative title-case forms to handle variation across EarthRanger "
         "server configurations — including servers that render the field label "
         "with a literal space (\"Transect ID\") rather than an underscore. "
         "raise_if_not_found is set to false so that missing columns are silently "
         "ignored."),
    note("Both alt-form transect ID fields land in transect_id_v2, a separate column "
         "from transect_id (populated by the distancecountpatrol_transectid mapping "
         "above). A following map_columns step (\"Normalize transect_id column name "
         "across schemas\") renames transect_id_v2 → transect_id so both schemas "
         "converge on one column before the parse/lowercase/fill steps below run."),
    sp(6),
    h2("5.4  Field effort computation"),
    p("In parallel with the metadata and wildlife observation branches, "
      "<b>compute_field_effort</b> derives a daily field-effort summary per team "
      "member from the metadata event DataFrame (post drop_null_columns) and the "
      "survey's EarthRanger connection:"),
    make_table(
        [
            ["Step", "Description"],
            ["1. Roster reconstruction", "Team Members (or reported_by as a fallback) "
             "is parsed per event and grouped by recorder and survey_date to build a "
             "daily team roster. If no member names are recorded, a placeholder "
             "roster of size 3 (DEFAULT_TEAM_SIZE) is generated from the recorder "
             "so that a team size estimate is still produced."],
            ["2. Subject resolution", "Roster member names are matched against "
             "EarthRanger subjects (get_subjects) to resolve subject IDs. If no "
             "match is found for individual members, the recorder name is matched "
             "against subjects as a fallback."],
            ["3. Observation window", "Each survey_date is assigned a fixed daily "
             "observation window (04:00–13:00 UTC) used to bound the GPS "
             "observation fetch for that date."],
            ["4. Track retrieval", "Subject GPS observations are fetched per "
             "survey_date via get_subject_observations and converted to "
             "relocations, then to trajectories (process_relocations / "
             "relocations_to_trajectory), filtered to segments between 0.1 m and "
             "100 km, 1 second and 6 hours, and 1–100 km/h."],
            ["5. Distance/duration summary", "Trajectory segments are summarised "
             "per subject/day (summarize_df) into total distance (km) and total "
             "duration (h), then merged back onto the roster."],
            ["6. Man-hours", "man_hours is computed as team_size × duration "
             "for each subject/day row."],
        ],
        [4*cm, W - 4*cm],
    ),
    p("The resulting DataFrame — columns survey_date, id, name, team_size, "
      "distance, duration, man_hours — is persisted as "
      "<b>{survey_name}_{period}_field_effort.csv</b>."),
    note("If no GPS observations are returned for a survey period, "
         "compute_field_effort returns an empty DataFrame with the expected "
         "columns rather than raising an error, so downstream persistence is "
         "skipped gracefully for that period."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. TRANSECT PROCESSING
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Transect Processing"),
    hr(),
    h2("6.1  CRS conversion to UTM"),
    p("Distance sampling calculations require a metric coordinate reference system. "
      "The UTM zone is estimated automatically from the transect geometry via "
      "<b>estimate_utm_crs</b>. Both the transect GeoDataFrame and the wildlife "
      "observation GeoDataFrame are then reprojected to this UTM CRS via "
      "<b>reproject_gdf</b> before any distance calculations are performed."),
    sp(6),
    h2("6.2  Transect simplification and buffering"),
    p("Before spatial intersection tests, the transect lines are prepared as follows:"),
    make_table(
        [
            ["Step", "Task", "Parameters", "Purpose"],
            ["1", "merge_transect_lines", "—",
             "Merge all transect line segments for the survey into a unified "
             "GeoDataFrame keyed by transect name"],
            ["2", "simplify_transects", "tolerance: 50 m",
             "Reduce transect vertex count while preserving shape — "
             "improves intersection performance"],
            ["3", "buffer_transects",
             "distance: 500 m, cap_style: round, single_sided: false, resolution: 5",
             "Create a 500 m bilateral corridor around each transect for "
             "event intersection testing"],
        ],
        [1.5*cm, 4*cm, 4*cm, W - 9.5*cm],
    ),
    note("cap_style is round rather than flat. A flat cap terminates the corridor in "
         "a straight edge exactly at each transect's start/end point, which excluded "
         "events recorded just before reaching or just after finishing the transect "
         "even when they were only a few metres away — diagnostics showed the "
         "excluded events consistently projected to position 0 or line-length on the "
         "transect (i.e. clamped to an endpoint), not because they were actually far "
         "from it. The round cap extends the corridor in an arc past each endpoint "
         "instead, capturing those near-endpoint events."),
    sp(6),
    h2("6.3  Event–transect intersection filter"),
    p("Wildlife observation events are tested against the buffered transect corridors "
      "via <b>flag_events_intersecting_transect</b>. This step adds an "
      "<b>intersects_transect</b> boolean column and records which transect each "
      "event falls within (transect_id_column: transect_id, "
      "transect_name_column: name, index_column: id)."),
    sp(4),
    p("Only transects visited by at least one intersecting event are retained for "
      "the final output via <b>filter_visited_transects</b>. This removes "
      "transects that were planned but not walked during the survey period. Because "
      "the upstream filter (Section 5.2, step 8) now keeps patrol \"conducted\" "
      "marker events alongside wildlife sightings, a transect that was walked but "
      "had zero sightings still has an intersecting event here and is retained as "
      "visited — it would previously have been dropped."),
    sp(4),
    p("The patrol marker rows carried through <b>flag_events_intersecting_transect</b> "
      "exist only to establish visited status and do not belong in the wildlife "
      "observation exports. Downstream of transect labeling, a dedicated "
      "<b>filter_row_values</b> step (\"Keep only wildlife sightings for "
      "analysis_data / events export\", id: <b>filter_wild_analysis</b>) re-filters "
      "the same <b>flag_events_intersecting_transect</b> output back down to "
      "<b>distancecountwildlife_rep</b> only, before it is paired with the labelled "
      "transects and merged (Section 9). This keeps analysis_data.csv and "
      "events.gpkg wildlife-sightings-only while still letting patrol-only "
      "transects surface in transect_areas.gpkg / transect_lines.gpkg."),
    sp(6),
    h2("6.4  Re-projection to EPSG:4326 for export"),
    p("After intersection filtering, visited transects are reprojected back to "
      "EPSG:4326 (<b>reproject_gdf</b>, target_crs: \"epsg:4326\") before "
      "satellite imagery labeling and GeoPackage export."),
    sp(4),
    note("The visited, buffered corridor geometry from this step is exported as "
         "the transect_areas GeoPackage (Section 9). A second, independent branch "
         "filters the pre-buffer simplified centrelines (from Section 6.2, step 2) "
         "down to the same visited transect names (filter_transect_lines_by_visited) "
         "and reprojects them to EPSG:4326 for export as the transect_lines "
         "GeoPackage — the same visited subset, but with line rather than polygon "
         "geometry."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. GEOMETRIC CALCULATIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Geometric Calculations"),
    hr(),
    h2("7.1  Off-transect distance (observer position)"),
    p("The perpendicular distance from the <i>observer's recorded GPS position</i> "
      "to the nearest transect centreline is calculated via "
      "<b>add_off_transect_distance</b> and stored in the column "
      "<b>off_transect_dist</b>. Events where the computed distance equals "
      "<b>−1</b> (indicating that no matching transect was found) are removed "
      "via <b>filter_rows</b> (op: \"ne\", value: −1)."),
    sp(6),
    h2("7.2  Estimated animal position"),
    p("The true animal position is estimated from the observer position, the "
      "recorded radial angle (<b>radialangle</b>), and the recorded distance "
      "from observer to detected animal (<b>dist_to_centre</b>) via "
      "<b>estimate_animal_positions</b>. The original observer geometry is "
      "preserved first by <b>add_orig_geometry</b> into the column "
      "<b>orig_geometry</b>; the main geometry column is then replaced with "
      "the estimated animal position."),
    sp(6),
    h2("7.3  Orthogonal distance (animal position)"),
    p("After the animal position is estimated, the perpendicular distance from "
      "the <i>estimated animal position</i> to the transect centreline is "
      "computed via a second call to <b>add_off_transect_distance</b> and "
      "stored as <b>ortho_dist</b>. This is the key detection distance used "
      "in distance sampling density estimation models."),
    sp(4),
    p("Events with ortho_dist == −1 are again removed via "
      "<b>filter_rows</b> before the data proceeds to imagery labeling."),
    sp(6),
    h2("7.4  Distance calculation summary"),
    make_table(
        [
            ["Column", "Task", "Geometry used", "Meaning"],
            ["off_transect_dist", "add_off_transect_distance (1st call)",
             "Observer GPS position",
             "Distance from observer to transect centreline — QA check"],
            ["orig_geometry",     "add_orig_geometry",
             "Observer GPS position",
             "Preserved original observer geometry before position estimation"],
            ["geometry",          "estimate_animal_positions",
             "Computed from radialangle + dist_to_centre",
             "Estimated true animal location"],
            ["ortho_dist",        "add_off_transect_distance (2nd call)",
             "Estimated animal position",
             "Perpendicular distance from animal to transect — used in DSC models"],
        ],
        [3*cm, 4*cm, 4*cm, W - 11*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. SATELLITE IMAGERY LABELING
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Satellite Imagery Labeling"),
    hr(),
    p("Each transect line is labelled with two satellite-derived environmental "
      "covariates using Google Earth Engine. These covariates are commonly used "
      "as predictors in distance sampling detection function models."),
    sp(6),
    h2("8.1  HLS NDVI"),
    p("A Harmonized Landsat Sentinel-2 (HLS) NDVI composite is built per survey "
      "via <b>build_hls_ndvi_image</b>:"),
    make_table(
        [
            ["Parameter", "Value", "Notes"],
            ["ndvi_window_days", "null",
             "No fixed window — uses the full image archive available "
             "up to the survey start date"],
            ["max_cloud_cover",  "30 %",
             "Scenes with more than 30 % cloud cover are excluded from the composite"],
            ["ndvi_band_name",   "NDVI_HSL",
             "Output band name stored in the labelled transect column"],
        ],
        [4*cm, 2.5*cm, W - 6.5*cm],
    ),
    sp(4),
    p("The NDVI image is evaluated over each transect's geometry and the mean "
      "pixel value within each transect is computed via "
      "<b>label_features_with_image_stat</b> (scale: 30 m, reducer_key: mean, "
      "out_column: NDVI_HSL). The survey start date is added as a "
      "<b>img_date_hsl_ndvi</b> column for traceability."),
    sp(6),
    h2("8.2  Terrain slope"),
    p("A slope layer is derived from the USGS SRTM 1-arc-second DEM "
      "(<b>USGS/SRTMGL1_003</b>) via <b>build_slope_image</b>. The mean slope "
      "value within each transect is then computed via a second call to "
      "<b>label_features_with_image_stat</b> (scale: 30 m, reducer_key: mean, "
      "out_column: slope)."),
    sp(6),
    h2("8.3  PALSAR woody cover"),
    p("A woody cover layer is built from PALSAR imagery via "
      "<b>build_palsar_woody_cover_image</b>, using a dry-season window of "
      "<b>July–September</b> (dry_season_start_month: 7, dry_season_end_month: 9) "
      "and output band name <b>WoodyCover</b>. Like the HLS NDVI composite, this image "
      "is built per survey period, anchored to that period's minimum patrol event date "
      "(zip_aoi_min_date)."),
    sp(4),
    p("The mean woody cover value within each transect is computed via a third call to "
      "<b>label_features_with_image_stat</b> (scale: 50 m, reducer_key: mean, "
      "out_column: WoodyCover), chained after the slope-labelled transects via "
      "<b>zip_woody_cover_image</b>."),
    sp(6),
    h2("8.4  Imagery labeling workflow"),
    p("The transects are converted to a Google Earth Engine FeatureCollection "
      "via <b>to_ee_feature_collection</b> before labeling. The period's minimum "
      "patrol event date (<b>get_survey_min_date</b>) is both added as a column to "
      "the transect DataFrame and passed to the NDVI image builder as the "
      "<b>since</b> parameter to anchor the composite date."),
    sp(6),
    h2("8.5  Final transect column selection"),
    p("After labeling, transects are trimmed to the columns required for "
      "merging and export:"),
    make_table(
        [
            ["Column", "In transect_areas.gpkg", "Included in merge", "Description"],
            ["name",             "Yes", "Yes", "Transect identifier (matches transect_id in patrol events)"],
            ["img_date_hsl_ndvi","Yes", "Yes", "Period min. patrol date used as NDVI image anchor"],
            ["NDVI_HSL",         "Yes", "Yes", "Mean HLS NDVI value along transect"],
            ["slope",            "Yes", "Yes", "Mean terrain slope along transect"],
            ["WoodyCover",       "Yes", "Yes", "Mean PALSAR woody cover value along transect"],
            ["geometry",         "Yes", "No",  "Transect corridor geometry (excluded from CSV merge)"],
        ],
        [3.5*cm, 3.2*cm, 2.5*cm, W - 9.2*cm],
    ),
    note("The separately exported transect_lines.gpkg (Section 6.4) carries only "
         "the transect name and unbuffered line geometry — it is not labelled with "
         "NDVI_HSL, slope, WoodyCover, or img_date_hsl_ndvi."),
    note("\"Included in merge\" means the column survives into merge_filtered_patrols' "
         "right-hand input (exclude_geom). WoodyCover does reach that merge step, but "
         "as of this revision it is then dropped by the final analysis_data.csv column "
         "selection (select_patrol_event_cols), which was not updated to include it "
         "alongside NDVI_HSL and slope — see Section 9 for the current analysis_data.csv "
         "column list."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Output Files"),
    hr(),
    p("All outputs are written under <b>$ECOSCOPE_WORKFLOWS_RESULTS</b>, into a "
      "dedicated subfolder per output type rather than the flat results root, so "
      "reviewers see files pre-sorted by type. Each subfolder is constructed once "
      "per run via <b>build_output_subfolder</b> (root_path: "
      "$ECOSCOPE_WORKFLOWS_RESULTS, subfolder: &lt;name&gt;) and its return value "
      "is used as the root_path for the corresponding persist_df step. "
      "Six file sets are produced for each survey period. "
      "{survey} is the survey name defined in the connection config and {period} "
      "is the detected activity period label (e.g. 2026_02)."),
    sp(6),
    make_table(
        [
            ["Subfolder", "File", "Format", "Description"],
            ["ER_Metadata/", "{survey}_{period}_analysis_metadata.csv", "CSV",
             "Survey metadata events: transect IDs, team members, observer counts, "
             "event types, lat/lon"],
            ["ER_FieldEffort/", "{survey}_{period}_field_effort.csv", "CSV",
             "Per-team-member daily field effort: survey_date, id, name, team_size, "
             "distance (km), duration (h), man_hours"],
            ["ER_AnalysisData/", "{survey}_{period}_analysis_data.csv", "CSV",
             "Wildlife observation events with all distance sampling fields: "
             "species, totalcount, num_juveniles, dist_to_centre, radialangle, "
             "off_transect_dist, ortho_dist, survey_id, orig_geometry (WKT), "
             "estimated geometry (WKT), NDVI_HSL, slope, img_date_hsl_ndvi, "
             "intersects_transect, transect_id, num_observers, time, "
             "serial_number, patrol_id, patrol_serial_number"],
            ["ER_Events/", "{survey}_{period}_events.gpkg", "GeoPackage",
             "Spatial point layer of wildlife observations. Columns: serial_number, "
             "transect_id, dist_to_centre, ortho_dist, intersects_transect, geometry"],
            ["ER_SurveyAreas/", "{survey}_{period}_transect_areas.gpkg", "GeoPackage",
             "Visited transect corridors — buffered polygons (EPSG:4326) with "
             "environmental covariates: name, img_date_hsl_ndvi, NDVI_HSL, slope, "
             "WoodyCover, geometry"],
            ["ER_MasterTransects/", "{survey}_{period}_transect_lines.gpkg", "GeoPackage",
             "Visited transect centrelines — unbuffered lines (EPSG:4326), the same "
             "visited subset as transect_areas but without environmental covariates"],
        ],
        [3*cm, 5*cm, 2*cm, W - 10*cm],
    ),
    sp(6),
    note("The _events GeoPackage contains a subset of columns optimised for "
         "spatial QA and GIS workflows. The _analysis_data CSV contains the full "
         "column set including all covariates and is the primary input for "
         "distance sampling density estimation models. If a survey period has no "
         "visited transects or no field-effort GPS data, the corresponding file(s) "
         "for that period are simply not produced rather than raising an error."),
    note("Visited transects now include those with a patrol \"conducted\" marker "
         "event and zero wildlife sightings (Section 6.3) — such transects appear "
         "in _transect_areas.gpkg / _transect_lines.gpkg but contribute no rows to "
         "_analysis_data.csv / _events.gpkg, which stay wildlife-sightings-only."),
    note("WoodyCover is labelled onto transects and appears in _transect_areas.gpkg "
         "(Section 8.5), but as of this revision it is not included in the "
         "_analysis_data.csv column list above — only NDVI_HSL and slope are currently "
         "carried through to that file."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("10. Workflow Execution Logic"),
    hr(),
    h2("10.1  Skip conditions"),
    p("All tasks share a global default skip policy defined in "
      "<b>task-instance-defaults</b>:"),
    bullet("<b>any_is_empty_df</b> — skips the task if any upstream DataFrame "
           "dependency is empty"),
    bullet("<b>any_dependency_skipped</b> — skips the task if any upstream "
           "task was itself skipped"),
    p("This means that if a survey returns no patrol events or no transects, "
      "all downstream tasks for that survey branch are skipped gracefully "
      "without raising an error. Many <b>groupbykey</b> steps additionally set "
      "<b>any_keyed_iterables_are_skips</b> (unpack_depth: 1) so that if either "
      "input iterable for a given key was itself a skip, that key's pairing is "
      "dropped instead of propagating a malformed pair downstream."),
    sp(4),
    note("The final publish-path aggregation step (Section 10.6 / dsc_publish handoff) "
         "deliberately omits any_keyed_iterables_are_skips: with many independent "
         "survey periods, it is normal for some individual period to have nothing "
         "persisted (e.g. no visited transects that period) while others succeed. "
         "groupbykey's own SkippedDependencyFallback already drops just the "
         "skipped entries and keeps the rest, so using the stricter check there "
         "would discard every other period's real output."),
    sp(6),
    h2("10.2  Per-survey-period fan-out with mapvalues"),
    p("Every data-bearing step is executed once per survey <i>period</i> via the "
      "<b>mapvalues</b> directive. The fan-out list originates from "
      "<b>split_connection_configs</b>, is then exploded per detected activity "
      "period by <b>split_survey_by_period</b>, and flows through all subsequent "
      "steps. Key fan-out points:"),
    make_table(
        [
            ["Step", "mapvalues source"],
            ["fetch_patrol_events",       "split_connection_config.return"],
            ["period_split (activity period detection)", "zip_conn_patrol_events.return"],
            ["fetch_patrol_transects",    "period_connection_survey.return"],
            ["fetch_events_from_ids",     "period_split.return"],
            ["All event processing steps","Chained from fetch_events_from_ids"],
            ["compute_field_effort",      "zip_connection_metadata.return"],
            ["Transect CRS / distance steps", "Chained from fetch_patrol_transects"],
            ["GEE labeling steps",        "Chained from reproject_transects"],
            ["All persist steps",         "Chained via zip_filename_* groupbykey"],
        ],
        [6*cm, W - 6*cm],
    ),
    sp(6),
    h2("10.3  groupbykey — multi-input coordination"),
    p("<b>groupbykey</b> (the successor to the older zip_groupbykey task) is used "
      "throughout the workflow to combine two or more per-period iterables into "
      "paired tuples before feeding them into a multi-argument mapvalues step. "
      "Key uses:"),
    bullet("<b>zip_conn_patrol_events</b> — pairs split_connection_config with "
           "set_patrol_index to feed period_split"),
    bullet("<b>zip_conn_survey_df</b> — pairs the event DataFrame with the "
           "EarthRanger server name to feed process_events_details"),
    bullet("<b>zip_connection_metadata</b> — pairs period_connection_survey with "
           "the metadata summary table to feed compute_field_effort"),
    bullet("<b>zip_patrol_transects</b> — pairs patrol events (UTM) with transects "
           "(UTM) to feed add_off_transect_distance"),
    bullet("<b>zip_aoi_min_date</b> — pairs the EE FeatureCollection with the "
           "period's minimum patrol date to feed build_hls_ndvi_image"),
    bullet("<b>zip_lines_visited</b> — pairs the pre-buffer simplified transect "
           "lines with the visited-transects list to feed "
           "filter_transect_lines_by_visited"),
    bullet("<b>zip_filename_*</b> — pairs dynamically constructed filenames "
           "with DataFrames to feed persist_df"),
    sp(6),
    h2("10.4  Dynamic filename construction"),
    p("Output filenames are constructed at runtime with <b>join_with_underscore</b>. "
      "The survey name and period label are first combined into a shared base name "
      "(<b>combine_survey_period_name</b>, e.g. olaremotorogi_2026_02) that is then "
      "joined with a fixed suffix per output:"),
    make_table(
        [
            ["Suffix", "Output file purpose"],
            ["analysis_metadata", "Metadata events CSV"],
            ["field_effort",      "Field effort summary CSV"],
            ["analysis_data",     "Wildlife observations CSV"],
            ["events",            "Events GeoPackage"],
            ["transect_areas",    "Visited transect corridors (buffered) GeoPackage"],
            ["transect_lines",    "Visited transect centrelines (unbuffered) GeoPackage"],
        ],
        [4*cm, W - 4*cm],
    ),
    note("The constructed filename is combined with the output's dedicated "
         "subfolder (Section 9) — built once per run via build_output_subfolder — "
         "at the persist_df step for that output, so each file lands in "
         "$ECOSCOPE_WORKFLOWS_RESULTS/&lt;subfolder&gt;/&lt;filename&gt; rather "
         "than directly under $ECOSCOPE_WORKFLOWS_RESULTS."),
    sp(6),
    h2("10.5  Fill propagation for metadata fields"),
    p("Patrol events in EarthRanger are recorded sequentially: a metadata event "
      "(distancecountpatrol_rep) carrying the transect ID and observer count "
      "typically appears once per transect walk, while multiple wildlife "
      "observation events (distancecountwildlife_rep) follow it. Because "
      "both event types share the same patrol_serial_number, the workflow "
      "uses backward fill (<b>bfill_within_patrols</b>) followed by forward "
      "fill (<b>ffill_within_patrols</b>) to propagate the transect_id and "
      "num_observers values to every row within the patrol before "
      "filtering to wildlife observation events only. transect_id is lowercased "
      "immediately beforehand so it matches the lowercased transect names used "
      "for name-based transect matching."),
    sp(6),
    h2("10.6  Publish handoff (prepared, not yet wired in)"),
    p("The workflow builds a text widget (<b>create_text_widget_single_view</b>, "
      "title: \"Files ready to publish\") listing every persisted transects and "
      "patrol-events GeoPackage path across all surveys and periods, intended for "
      "a reviewer to copy into a companion <b>dsc_publish</b> workflow. As of this "
      "revision the widget is built but not yet attached to the dashboard "
      "(<b>overall_dashboard.widgets</b> is empty, with the widget reference "
      "commented out) — it is prepared for future wiring."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 11. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("11. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned"],
            ["ecoscope-platform",                      ">=2.15.0, <2.16.0"],
            ["ecoscope-workflows-ext-custom",          "0.1.0rc14.*"],
            ["ecoscope-workflows-ext-ste",             "0.0.0rc1.*"],
            ["ecoscope-workflows-ext-distance-sample-counts", "1.0.5.*"],
            ["pydeck",                                  "0.9.2"],
            ["opentelemetry-sdk",                       ">=1.20.0, <2.0.0"],
        ],
        [8*cm, W - 8*cm],
    ),
    sp(6),
    note("All packages are resolved from the prefix.dev Ecoscope conda channels. "
         "The wildcard patch-version pin (.*) allows bug-fix releases to be "
         "picked up automatically while keeping minor and major versions locked."),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"Written → {OUTPUT_FILE}")
