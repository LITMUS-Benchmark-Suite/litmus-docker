select 'Clearing existing data...';
-- Add here all the graphs we use for a clean update (RDF_GLOBAL_RESET deletes them all)
SPARQL CLEAR GRAPH <http://test.org>;

