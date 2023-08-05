
import warnings

import pandas as pd

from .Extractor import Extractor

warnings.filterwarnings('always')
# warnings.filterwarnings('error')
# warnings.filterwarnings("ignore", category=DeprecationWarning)

class Visualizer(Extractor):
    def __init__(self, ontology: dict, out_dir: str = 'data/visualizer'):
        Extractor.__init__(self, ontology)
        try:
            from pathlib import Path
            Path(out_dir).mkdir(parents=True, exist_ok=True)
        except OSError as error:
            print("Directory cannot be created")
        self.node_df, self.edge_df = pd.DataFrame(columns=['id']), pd.DataFrame(columns=['from', 'to'])
        self.default_vis_opts = {
            'autoResize': True,
            'height': '1200px',
            'width': '100%',
            'manipulation': 
                {
                    'enabled': True, 
                    'addNode': True
                }
        }

    def deploy_ontology_visualization(self, vis_opts: dict = {}):
        # set vis opts
        if not vis_opts:
            vis_opts = self.default_vis_opts
        # import
        from jaal import Jaal

        # load the data
        self.set_jaal_formatted_ontology()
        # init Jaal and run server
        Jaal(self.edge_df, self.node_df).plot(directed=False, vis_opts=vis_opts)
        
    def set_jaal_formatted_ontology(self):
        self.set_jaal_formatted_ontology_node_df()
        self.set_jaal_formatted_ontology_edge_df()
        

        
    def set_jaal_formatted_ontology_node_df(self):
        id = []
        node_type = []
        data_prop = []
        pi_id = []

        for name in list(self.ontology_df.keys()):
            id += self.ontology_df[name]['main']['label'].tolist() 
            pi_id += self.ontology_df[name]['main']['id'].tolist()
            node_type += len(self.ontology_df[name]['main']['label']) * [name]

        for name in list(self.ontology_df.keys()):
            id += self.ontology_df[name]['data_prop']['data_prop_label'].tolist() 
            pi_id += self.ontology_df[name]['data_prop']['data_prop_id'].tolist()
            node_type += self.ontology_df[name]['data_prop']['data_prop_data_type'].tolist()
        
        node_df = pd.DataFrame(list(zip(id, node_type, pi_id)),
                columns=['id', 'node_type', 'pi_id'])
        node_df['importance'] = node_df['pi_id'].str.count('/').astype(int)
        node_df['importance'] = (node_df['importance'] - node_df['importance'].max() - 1).abs()
        
        # save and delete duplicates
        self.node_df = node_df
        self.node_df[self.node_df.duplicated(subset=['id'], keep=False)].to_excel('duplicate_nodes.xlsx')
        self.node_df = self.node_df.drop_duplicates(subset=['id'], keep='first')
        self.node_df.to_excel(f'data/nodes.xlsx')
        

    
    def set_jaal_formatted_ontology_edge_df(self):
        pi_id_from = []
        pi_id_to = []
        label = []
        edge_type = []
        
        obj_prop_name_mapping = {
            'inheritance_obj_prop': 'Class Inheritance',
            'expansion_obj_prop': 'Object Property Relation',
            'expansion_data_prop': 'Data Property'
        }
        for name in list(self.ontology_df.keys()):      
            for obj_prop_type in ['inheritance_obj_prop', 'expansion_obj_prop', 'expansion_data_prop']:
                pi_id_from += self.ontology_df[name][obj_prop_type]['pi_id_from'].tolist()
                pi_id_to += self.ontology_df[name][obj_prop_type]['pi_id_to'].tolist()
                label += self.ontology_df[name][obj_prop_type]['label'].tolist()
                edge_type += len(self.ontology_df[name][obj_prop_type]['label'].tolist()) * [obj_prop_name_mapping[obj_prop_type]]
            
            
        edge_df = pd.DataFrame(list(zip(pi_id_from, pi_id_to, label, edge_type)),
                columns=['pi_id_from', 'pi_id_to', 'label', 'edge_type'])
    
        edge_df = pd.merge(edge_df, self.node_df[['pi_id', 'id']], left_on='pi_id_from', right_on='pi_id')
        edge_df = pd.merge(edge_df, self.node_df[['pi_id', 'id']], left_on='pi_id_to', right_on='pi_id')
        edge_df = edge_df[['id_x', 'id_y', 'label', 'edge_type']]
        edge_df.columns = ['from', 'to', 'label', 'edge_type']
        
        # faulty ontology
        self.edge_df = edge_df.sort_values('label',ascending=True)
        self.edge_df[self.edge_df.duplicated(subset=['from', 'to'], keep=False)].to_excel('duplicate_edges.xlsx')
        self.edge_df = self.edge_df.drop_duplicates(subset=['from', 'to'], keep='first')
        self.edge_df.to_excel(f'data/edges.xlsx')

        
