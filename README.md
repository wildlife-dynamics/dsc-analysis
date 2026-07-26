# DSC Analysis — User Guide

This guide walks you through configuring and running the Distance Sample Count (DSC) Analysis workflow, which ingests wildlife survey patrol data from EarthRanger, calculates distance sampling geometry, labels transects with satellite-derived environmental covariates, and exports analysis-ready datasets for population density modelling.

---

## Overview

The workflow supports **multiple surveys per run**. Each survey is automatically split into its **detected activity periods** — if a survey site was visited in, say, both February and June, the workflow produces two independent, period-tagged output sets instead of one combined one. For each survey period it produces:

- An **analysis metadata CSV** — survey event metadata including transect IDs, team members, observer counts, and event types
- A **field effort CSV** — per-team-member daily distance travelled, duration, and man-hours, derived from EarthRanger GPS tracks
- An **analysis data CSV** — wildlife observations enriched with off-transect distances, orthogonal distances, estimated animal positions, HLS NDVI, and terrain slope
- An **events GeoPackage** — spatial point layer of wildlife observations with key distance sampling geometry columns
- A **transect areas GeoPackage** — visited transect corridors (buffered) labelled with mean NDVI, terrain slope, and PALSAR woody cover from Google Earth Engine
- A **transect lines GeoPackage** — visited transect centrelines (unbuffered), reprojected to EPSG:4326

In addition, the workflow ingests weather station data **once per run** (it isn't scoped to any one survey or period):

- A **station metadata file** — one row per weather station, with its conservancy and coordinates
- **Per-station, per-year weather reading files** — precipitation, temperature, humidity, and wind speed observations

---

## Prerequisites

Before running the workflow, ensure you have:

- Access to an **EarthRanger** instance with DSC patrol data logged using the event types:
  - `distancecountpatrol_rep` — survey metadata (transect ID, team, observer count)
  - `distancecountwildlife_rep` — wildlife observations (species, count, distance, radial angle)
- A **Google Earth Engine** service account configured in Ecoscope (used to retrieve NDVI, slope, and woody cover imagery)
- The **EarthRanger spatial group ID** for each survey's transect lines
- The **patrol type ID** (numeric or UUID) for the DSC patrol type in EarthRanger
- Team members recorded on each patrol should correspond to named **subjects/trackers** in EarthRanger, so their GPS tracks can be used to compute field effort
- An **EarthRanger connection with a weather station subject group** (e.g. a TAHMO Stations group) — used to fetch and export weather station readings

---

## Step-by-Step Configuration

### Step 1 — Add the Workflow Template

In Ecoscope, go to **Workflow Templates** and click **Add Workflow Template**. Paste the GitHub repository URL into the **Github Link** field:

```
https://github.com/wildlife-dynamics/dsc_analysis.git
```

Then click **Add Template**. The card may show **Initializing…** briefly while the environment is set up.

---

### Step 2 — Select the Workflow

After the template is added it appears in the **Workflow Templates** list as **dsc_analysis**. Click the card to open the workflow configuration form.

---

### Step 3 — Set Workflow Details and Time Range

The configuration form opens with two sections at the top.

**Set Workflow Details**

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run (required) |
| Workflow Description | Optional notes, e.g. survey season or region |

**Time Range**

This field is required on all Ecoscope workflows. It now directly controls which patrol events are fetched: patrol events on or after **Since** and up to **Until** are retrieved from EarthRanger for every survey configured in Step 5. It is also used for timestamp display and UTC conversion.

One shared time range covers every survey in the run — there is no longer a separate time window per survey.

| Field | Description |
|-------|-------------|
| Timezone | Local timezone for display and UTC conversion, e.g. `Africa/Nairobi (UTC+03:00)` |
| Since | Start of the data fetch window — applied to every survey in this run |
| Until | End of the data fetch window — applied to every survey in this run |

> If different surveys need different fetch windows, submit them as separate workflow runs — a single run applies one Time Range to every survey it contains.

---

### Step 4 — Configure Google Earth Engine Connection

Select your Google Earth Engine service account from the **Data Source** dropdown. This connection is used to build HLS NDVI composites and terrain slope images for transect labelling.

> Only one GEE connection is needed — it is shared across all surveys in the run.

---

### Step 5 — Configure Weather Station Connection

The **Weather Station Subject Group** section configures the workflow's single, shared weather ingestion — this is independent of the per-survey EarthRanger connections in Step 6 and runs once for the whole workflow run, not once per survey or period.

| Field | Description |
|-------|-------------|
| Data Source | The EarthRanger connection that hosts the weather station subject group |
| Weather Station Subject Group | EarthRanger subject group name containing the weather stations, e.g. `TAHMO Stations` (defaults to `TAHMO Stations`) |

> This EarthRanger connection can be the same as, or different from, any of the survey connections configured in Step 6 — whichever site actually hosts the weather station subjects.

---

### Step 6 — Configure EarthRanger Connection and Survey Details

Scroll down to **Configure EarthRanger and Survey Details**. Click **+ Add** to add a survey entry — each entry is one independent survey, fetched using the shared Time Range from Step 3.

| Field | Description |
|-------|-------------|
| Data Source | Select the EarthRanger connection for this survey (e.g. `Amboseli Trust for Elephants`) |
| Patrol Type ID | The numeric or UUID identifier for the DSC patrol type in EarthRanger |
| Transects Group ID | The EarthRanger spatial group ID(s) that contain this survey's transect line features. Click **+ Add** within this field to add more than one group ID if the survey's transects span multiple spatial groups |

> To configure another survey, click the outer **+ Add** button again to add a new entry — whether it points at the same or a different EarthRanger connection, each entry runs as an independent survey.

---

## Running the Workflow

Once all parameters are configured, click **Submit**. For each survey the workflow will:

1. Fetch patrol events matching the configured patrol type ID and the workflow's Time Range from EarthRanger.
2. Split the survey's patrol events into their detected activity periods — each period is processed as an independent branch, tagged with a `{survey}_{yyyy}_{mm}` label.
3. Fetch transect lines from the configured EarthRanger spatial group, once per survey period.
4. Retrieve individual wildlife observation events from the patrol event IDs.
5. Process and normalise survey metadata events — extract transect ID, team members, and observer count.
6. Propagate metadata fields to wildlife observation rows using backward/forward fill within each patrol.
7. Compute field effort per team member — daily distance travelled, duration, and man-hours, from EarthRanger subject GPS tracks.
8. Reproject events and transects to a UTM coordinate system for metric distance calculations.
9. Calculate the perpendicular distance from each observer position to the transect centreline (`off_transect_dist`).
10. Estimate the true animal position from each observation's radial angle and distance to centre (`dist_to_centre`).
11. Calculate the orthogonal distance from the estimated animal position to the transect centreline (`ortho_dist`).
12. Filter events to those that intersect a 500 m transect buffer corridor; discard unvisited transects.
13. Label visited transects with mean HLS NDVI (max 30 % cloud cover), terrain slope, and PALSAR woody cover (dry-season composite) from Google Earth Engine.
14. Merge transect covariates into the wildlife observation dataset.
15. Export all outputs per survey period to `$ECOSCOPE_WORKFLOWS_RESULTS`.

Independently of the per-survey steps above, and only once for the whole run, the workflow also:

16. Fetches observations from the configured weather station subject group and extracts precipitation, temperature, humidity, and wind speed from each reading.
17. Tags each weather station with the conservancy boundary it falls within.
18. Exports one station metadata file and one weather readings file per station per year to `$ECOSCOPE_WORKFLOWS_RESULTS`.

---

## Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`. Six files are produced for **each survey period** — `{survey}_{period}` is replaced by the name of the EarthRanger site (subdomain) that survey's connection points to, followed by the detected activity period (e.g. `olaremotorogi_2026_02`).

| File | Description |
|------|-------------|
| `{survey}_{period}_analysis_metadata.csv` | Survey metadata events: transect IDs, team members, observer counts, event types, lat/lon |
| `{survey}_{period}_field_effort.csv` | Per-team-member daily field effort: `survey_date`, `id`, `name`, `team_size`, `distance` (km), `duration` (h), `man_hours` |
| `{survey}_{period}_analysis_data.csv` | Wildlife observations with all distance sampling fields: species, total count, juveniles, `dist_to_centre`, `radialangle`, `off_transect_dist`, `ortho_dist`, estimated geometry, `NDVI_HSL`, `slope`, `survey_id`, and more |
| `{survey}_{period}_events.gpkg` | Spatial point layer of wildlife observations (columns: `serial_number`, `transect_id`, `dist_to_centre`, `ortho_dist`, `intersects_transect`, `geometry`) |
| `{survey}_{period}_transect_areas.gpkg` | Visited transect corridors (buffered polygons) in EPSG:4326 with `NDVI_HSL`, `slope`, `WoodyCover`, and `img_date_hsl_ndvi` columns |
| `{survey}_{period}_transect_lines.gpkg` | Visited transect centrelines (unbuffered) in EPSG:4326 |

> If a survey has no visited transects or no matching patrol events for a given period, that period's outputs are skipped gracefully rather than raising an error — other periods and surveys in the same run are unaffected.

> As of this revision, `WoodyCover` is labelled onto the transect corridors and appears in `{survey}_{period}_transect_areas.gpkg`, but is not yet included in the `{survey}_{period}_analysis_data.csv` column selection — only `NDVI_HSL` and `slope` are currently carried through to that file.

In addition to the six per-survey-period files above, the workflow produces two **workflow-wide** weather outputs — these are fetched once for the whole run against the workflow's overall Time Range, independent of any survey or period:

| File | Description |
|------|-------------|
| `station_metadata.parquet` | One row per weather station: `Station ID`, `Conservancy`, `Latitude`, `Longitude` — produced once per run |
| `{station_id}_{year}.parquet` | One file per weather station per calendar year covered by the Time Range: `Station ID`, `Precipitation`, `Humidity`, `Temperature`, `Windspeed`, `fixtime` — join back to `station_metadata.parquet` on `Station ID` for coordinates and conservancy |
