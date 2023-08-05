
# import warnings

# import pandas as pd

# from .Extractor import Extractor

# warnings.filterwarnings('always')
# # warnings.filterwarnings('error')
# # warnings.filterwarnings("ignore", category=DeprecationWarning)

# class DBManager(Extractor):
#     def __init__(self, ontology: dict, out_dir: str = 'data/dbmanager'):
#         Extractor.__init__(self, ontology)
#         try:
#             from pathlib import Path
#             Path(out_dir).mkdir(parents=True, exist_ok=True)
#         except OSError as error:
#             print("Directory cannot be created")
    
#     def create_db_schema(self, query_language) -> None:
        
        
#     def create_gsql_db_schema(self) -> None:
#         # https://docs.tigergraph.com/start/gsql-examples/common-applications
#         # https://docs.tigergraph.com/start/gsql-101/define-a-schema
#         # https://towardsdatascience.com/efficient-use-of-tigergraph-and-docker-5e7f9918bf53

#         gsql_ontology_type_mapping = {
#             'TimestampRange': None, #tuple DATETIME DATETIME
#             'Route': None,
#             'Geometric2D': None, 
#             'Coordinate': None, #tuple DOUBLE DOUBLE
#             'ImageLink': 'STRING', 
#             'WebLink': 'STRING', 
#             'Double':'DOUBLE', 
#             'Boolean':'BOOL', 
#             'Text': 'STRING', 
#             'Timestamp':'DATETIME'
#         }
        
# Geometric2D
# Route


        



        
