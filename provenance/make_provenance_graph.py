from provo import ProvOntologyGraph
from os import listdir
from os.path import isfile, join

pog = ProvOntologyGraph(
    namespace="https://github.com/rue-a/fliegel/tree/master/",
    namespace_abbreviation="fliegel",
    lang="en",
)

geogNames_xml = pog.add_entity("fliegel_geogNames.xml", "fliegel_geogNames.xml")

xml2Csv = pog.add_activity(
    "01_xml2csv.py", "01_xml2csv.py"
)
xml2Csv.used(geogNames_xml)

fliegel_geog_names = pog.add_entity(
    "interim/fliegel_geog_names.csv", "interim/fliegel_geog_names.csv"
)
fliegel_geog_names.was_generated_by(xml2Csv)

countries = pog.add_entity("admin_codes/downloads/countries.csv", "countries")
admin1 = pog.add_entity(
    "admin_codes/downloads/geonames_admin1CodesASCII.csv",
    "geonames_admin1",
)
admin2 = pog.add_entity(
    "admin_codes/downloads/geonames_admin2Codes.csv",
    "geonames_admin2",
)

make_admin_levels_list = pog.add_activity(
    "02_makle_admin_levels_list.py", "02_makle_admin_levels_list.py"
)
make_admin_levels_list.used(countries)
make_admin_levels_list.used(admin1)
make_admin_levels_list.used(admin2)

admin_levels = pog.add_entity(
    "admin_codes/admin_levels.csv", "admin_codes/admin_levels.csv"
)


admin_levels.was_generated_by(make_admin_levels_list)

abbreviations = pog.add_entity("misc/abbreviations.csv", "misc/abbreviations.csv")


headlines_into_schema = pog.add_activity(
    "03_headlines_into_schema.py", "03_headlines_into_schema.py"
)
headlines_into_schema.used(abbreviations)
headlines_into_schema.used(admin_levels)
headlines_into_schema.used(countries)
headlines_into_schema.used(fliegel_geog_names)

schematized = pog.add_entity(
    "interim/fliegel_schematized.csv", "interim/fliegel_schematized.csv"
)
schematized.was_generated_by(headlines_into_schema)

condense = pog.add_activity("04_condense_duplicates.py", "04_condense_duplicates.py")
condense.used(schematized)
condensed = pog.add_entity(
    "interim/fliegel_condensed.csv", "interim/fliegel_condensed.csv"
)
condensed.was_generated_by(condense)

heuristics = pog.add_activity("05_apply_heuristics.py", "05_apply_heuristics.py")
heuristics.used(condensed)
heuristics.used(countries)
heuristics.used(admin_levels)

typed = pog.add_entity("interim/fliegel_typed.csv", "interim/fliegel_typed.csv")
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
    "geonames_dl",
    namespace="https://download.geonames.org/export/dump/",
)

prep_geonames = pog.add_activity("06_prepare_geonames.py", "06_prepare_geonames.py")
prep_geonames.used(geonames_files)
# for entity in files:
#     prep_geonames.used(entity)

geonames = pog.add_entity(
    "geonames/geonames_prepared.csv",
    "geonames_prepared - not in repo, too large",
)
geonames.was_generated_by(prep_geonames)

prep_geocode = pog.add_activity("07_prepare_geocode.py", "07_prepare_geocode.py")
prep_geocode.used(typed)
prep_geocode.used(admin_levels)
prep_geocode.used(countries)
prep_geocode.used(fliegel_geog_names)

prepared = pog.add_entity(
    "interim/fliegel_prepared.csv", "interim/fliegel_prepared.csv"
)
prepared.was_generated_by(prep_geocode)

geocode = pog.add_activity("08_geocode.py", "08_geocode.py")
geocode.used(prepared)
geocode.used(geonames)

geocoded = pog.add_entity(
    "interim/fliegel_geocoded.csv", "interim/fliegel_geocoded.csv"
)
geocoded.was_generated_by(geocode)

postprocessing = pog.add_activity("09_post_processing.py", "09_post_processing.py")
postprocessing.used(geocoded)
postprocessing.used(condensed)

gazetteer = pog.add_entity("fliegel_gazetteer.csv", "fliegel_gazetteer.csv")
gazetteer.was_generated_by(postprocessing)

geocode_white_ppl = pog.add_activity(
    "10_geocode_white_ppl_index.py", "10_geocode_white_ppl_index.py"
)

white_ppl = pog.add_entity(
    "Fliegel_WhitePeople_sentiment.csv", "Fliegel_WhitePeople_sentiment.csv"
)
geocode_white_ppl.used(gazetteer)
geocode_white_ppl.used(white_ppl)

white_ppl_geocoded = pog.add_entity(
    "interim/white_ppl_index_geocoded.csv", "interim/white_ppl_index_geocoded.csv"
)
white_ppl_geocoded.was_generated_by(geocode_white_ppl)

postprocess_white = pog.add_activity(
    "11_post_processing_white_ppl_index.py", "11_post_processing_white_ppl_index.py"
)
postprocess_white.used(white_ppl_geocoded)

geoperson = pog.add_entity("fliegel_geoperson.csv", "fliegel_geoperson.csv")
geoperson.was_generated_by(postprocess_white)
geofactoid = pog.add_entity("fliegel_geofactoid.csv", "fliegel_geofactoid.csv")
geofactoid.was_generated_by(postprocess_white)
person_and_factoid = pog.add_entity(
    "fliegel_geoperson_and_geofactoid.csv", "fliegel_geoperson_and_geofactoid.csv"
)
person_and_factoid.was_generated_by(postprocess_white)

make_geojsons = pog.add_activity(
    "12_geojsons_from_white_ppl_index.py", "12_geojsons_from_white_ppl_index.py"
)
make_geojsons.used(geofactoid)
geojsons = pog.add_entity("geojsons/", "geojsons/")
geojsons.was_generated_by(make_geojsons)

pog.export_as_mermaid_flowchart(file_name="provenance_graph.md")
pog.serialize_as_rdf(file_name="provenance_graph.ttl")
