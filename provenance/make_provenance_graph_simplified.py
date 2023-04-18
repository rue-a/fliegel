from provo import ProvOntologyGraph
from os import listdir
from os.path import isfile, join

pog = ProvOntologyGraph(
    namespace="https://github.com/rue-a/fliegel/tree/master/",
    namespace_abbreviation="fliegel",
    lang="en",
)


fliegel_geog_names = pog.add_entity(
    "interim/fliegel_geog_names.csv", "Fliegel Geog. Names"
)


admin_levels = pog.add_entity(
    "admin_codes/admin_levels.csv", "Admin Areas Hierarchy Table"
)


abbreviations = pog.add_entity("misc/abbreviations.csv", "Abbreviations List")


headlines_into_schema = pog.add_activity(
    "03_headlines_into_schema.py", "Dissolve Headlines"
)
headlines_into_schema.used(abbreviations)
headlines_into_schema.used(admin_levels)
headlines_into_schema.used(fliegel_geog_names)

schematized = pog.add_entity(
    "interim/fliegel_schematized.csv", "Fliegel Dissolved Entries"
)
schematized.was_generated_by(headlines_into_schema)

condense = pog.add_activity("04_condense_duplicates.py", "Aggregate Duplicates")
condense.used(schematized)
condensed = pog.add_entity(
    "interim/fliegel_condensed.csv", "Fliegel Aggregated Entires"
)
condensed.was_generated_by(condense)

heuristics = pog.add_activity(
    "05_apply_heuristics.py", "Heuristically Assign Feature Types"
)
heuristics.used(condensed)
heuristics.used(admin_levels)

typed = pog.add_entity("interim/fliegel_typed.csv", "Fliegel Typed Entries")
typed.was_generated_by(heuristics)

# omit for understandibility
# files = [
#     pog.add_entity(
#         f.replace(".txt", ".zip"),
#         f,
#         namespace="https://download.geonames.org/export/dump/",
#     )
#     for f in listdir("geonames")
#     if isfile(join("geonames", f)) and f != "geonames_prepared.csv"
# ]

geonames_files = pog.add_entity(
    "",
    "GeoNames Database",
    namespace="https://download.geonames.org/export/dump/",
)

prep_geonames = pog.add_activity("06_prepare_geonames.py", "Preprocess GeoNames")
prep_geonames.used(geonames_files)
# for entity in files:
#     prep_geonames.used(entity)

geonames = pog.add_entity(
    "geonames/geonames_prepared.csv",
    "Preprocessed GeoNames Database",
)
geonames.was_generated_by(prep_geonames)

prep_geocode = pog.add_activity("07_prepare_geocode.py", "Prepare for Geocoding")
prep_geocode.used(typed)
prep_geocode.used(admin_levels)

prepared = pog.add_entity("interim/fliegel_prepared.csv", "Fliegel Prepared Entries")
prepared.was_generated_by(prep_geocode)

geocode = pog.add_activity("08_geocode.py", "Geocode")
geocode.used(prepared)
geocode.used(geonames)

geocoded = pog.add_entity("interim/fliegel_geocoded.csv", "Fliegel Geocoded Entries")
geocoded.was_generated_by(geocode)

postprocessing = pog.add_activity("09_post_processing.py", "Postprocess")
postprocessing.used(geocoded)

gazetteer = pog.add_entity(
    "fliegel_gazetteer.csv", "Gazetteer of Geographic Names in Fliegel Index"
)
gazetteer.was_generated_by(postprocessing)

geocode_white_ppl = pog.add_activity(
    "10_geocode_white_ppl_index.py", "Geocode Fliegel White People Index"
)

white_ppl = pog.add_entity(
    "Fliegel_WhitePeople_sentiment.csv",
    "Fliegel White People Index - with Sentiment Analysis",
)
geocode_white_ppl.used(gazetteer)
geocode_white_ppl.used(white_ppl)

white_ppl_geocoded = pog.add_entity(
    "interim/white_ppl_index_geocoded.csv", "Fliegel White People Index Geocoded"
)
white_ppl_geocoded.was_generated_by(geocode_white_ppl)

postprocess_white = pog.add_activity(
    "11_post_processing_white_ppl_index.py", "Postprocess"
)
postprocess_white.used(white_ppl_geocoded)

geoperson = pog.add_entity(
    "fliegel_geoperson.csv", "White Ppl. Ind. - Geoinfo in Person Description"
)
geoperson.was_generated_by(postprocess_white)
geofactoid = pog.add_entity(
    "fliegel_geofactoid.csv", "White Ppl. Ind. - Geoinfo in Factoid"
)
geofactoid.was_generated_by(postprocess_white)
person_and_factoid = pog.add_entity(
    "fliegel_geoperson_and_geofactoid.csv", "White Ppl. Ind. - Geoinfo in Both"
)
person_and_factoid.was_generated_by(postprocess_white)

make_geojsons = pog.add_activity("12_geojsons_from_white_ppl_index.py", "Make GeoJSONs")
make_geojsons.used(geofactoid)
geojsons = pog.add_entity("geojsons/", "Fliegel White Ppl. Ind. GeoJSONs")
geojsons.was_generated_by(make_geojsons)

pog.export_as_mermaid_flowchart(
    file_name="provenance/provenance_graph_simplified.md",
    user_options={
        "revert-relations": True,
        "entity": {"fill": "#DA4E3DFF", "stroke": "#DA4E3DFF", "color": "#eee"},
        "activity": {"fill": "#276EBAFF", "stroke": "#276EBAFF", "color": "#eee"},
    },
)
