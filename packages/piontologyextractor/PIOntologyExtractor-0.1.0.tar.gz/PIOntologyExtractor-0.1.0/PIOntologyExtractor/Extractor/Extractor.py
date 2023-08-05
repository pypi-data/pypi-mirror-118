import numpy as np
import pandas as pd


class Extractor:
    def __init__(self, ontology: dict, out_dir: str = 'data/extractor') -> None:
        try:
            from pathlib import Path
            Path(out_dir).mkdir(parents=True, exist_ok=True)
        except OSError as error:
            print("Directory cannot be created")
        self.ontology = ontology
        self.classes = ontology["classes"]
        self.relationships = ontology["relationships"]
        self.rules = ontology["rules"]
        self.ontology_df = {}
        self.create_ontology_mapping()
        
        
    def create_ontology_mapping(self) -> None:
        self.set_data_classes_from_ontology()
        for name, __loader__ in self.data_class_dict.items():
            self.ontology_df[name] = {}
            self.set_main_ontology(name)
            self.set_expansion_data_properties(name)
            self.set_expansion_object_properties(name)
            self.set_inheritance_object_properties(name)
    
    def set_data_classes_from_ontology(self):
        self.data_class_dict = {}
        self.data_class_dict['esc12'] = [item for item in self.classes if '/esc12' in item['uri']]
        self.data_class_dict['ontology'] = [item for item in self.classes if '/ontology' in item['uri']]
            
    def set_main_ontology(self, name: str):
        ont_id = []
        ont_label = []
        ont_color = []
        ont_inherit_ids = []
        ont_data_prop_ids = []
        ont_obj_prop_ids = []
        data_prop_id = []
        data_prop_data_type = []
        data_prop_label = []
        data_prop_color = []
        data_prop_inherit_ids = []
        obj_prop_id = []
        obj_prop_class_id = []
        label = []
        obj_prop_color = []
        obj_prop_inherit_ids = []

        for ont_item in self.data_class_dict[name]:
            ont_id.append(ont_item['uri'])
            if len(ont_item['annotations']) != 1:
                print(ont_item)
                raise Exception('# annotation != 1')
            ont_data_prop_ids_temp = []
            ont_obj_prop_ids_temp = []
            for prop_item in ont_item['properties']:
                try:
                    if prop_item["$type"] != 'ObjectPropertyInfo':
                        ont_data_prop_ids_temp.append(prop_item['uri'])
                        data_prop_id.append(prop_item['uri'])
                        data_prop_data_type.append(prop_item['dataType'])
                        if len(prop_item['annotations']) != 1:
                            print(prop_item)
                            raise Exception('# annotation != 1')
                        data_prop_label.append(prop_item['annotations'][0]['label'])
                        data_prop_color.append(prop_item['annotations'][0]['color'])
                        data_prop_inherit_ids.append(prop_item['inherits'])
                    else:
                        ont_obj_prop_ids_temp.append(prop_item['uri'])
                        obj_prop_id.append(prop_item['uri'])
                        obj_prop_class_id.append(prop_item['classUri'])
                        if len(prop_item['annotations']) != 1:
                            print(prop_item)
                            raise Exception('# annotation != 1')
                        label.append(prop_item['annotations'][0]['label'])
                        obj_prop_color.append(prop_item['annotations'][0]['color'])
                        obj_prop_inherit_ids.append(prop_item['inherits'])
                except:
                    print(prop_item)
                    raise Exception
            ont_data_prop_ids.append(ont_data_prop_ids_temp)
            ont_obj_prop_ids.append(ont_obj_prop_ids_temp)
            ont_label.append(ont_item['annotations'][0]['label'])
            ont_color.append(ont_item['annotations'][0]['color'])
            ont_inherit_ids.append(ont_item['inherits'])

        df_ont = pd.DataFrame(list(zip(ont_id, ont_label, ont_color, ont_inherit_ids, ont_data_prop_ids, ont_obj_prop_ids)),
                    columns =[f'id', f'label', f'color', f'inherit_id', f'data_prop_id', f'obj_prop_id'])
        if name == 'esc12': # ensure mapping between esc12, entity, ontology
            df_ont.loc[len(df_ont)] = np.array(['http://www.pandoraintelligence.com/esc12', 'esc12', None, ['http://www.pandoraintelligence.com/ontology'], [], []], dtype=object)
        df_ont.to_excel(f'./data/{name}_info.xlsx')
        
        df_data_prop = pd.DataFrame(list(zip(data_prop_id, data_prop_data_type, data_prop_label, data_prop_color, data_prop_inherit_ids)),
                    columns =['data_prop_id', 'data_prop_data_type', 'data_prop_label', 'data_prop_color', 'data_prop_inherit_id'])
        df_data_prop.to_excel(f'./data/{name}_data_prop_info.xlsx')
        
        df_obj_prop = pd.DataFrame(list(zip(obj_prop_id, obj_prop_class_id, label, obj_prop_color, obj_prop_inherit_ids)),
                    columns =['obj_prop_id', 'obj_prop_class_id', 'label', 'obj_prop_color', 'obj_prop_inherit_id'])
        df_obj_prop.to_excel(f'./data/{name}_obj_prop_info.xlsx')
        
        self.ontology_df[name]['main'] = df_ont
        self.ontology_df[name]['data_prop'] = df_data_prop
        self.ontology_df[name]['obj_prop'] = df_obj_prop
    
    def set_expansion_data_properties(self, name):  
        obsolete_columns = ['inherit_id','obj_prop_id','obj_prop_inherit_id', 'data_prop_inherit_id', 'label', 'color', 'data_prop_color']
        df_exploded = self.ontology_df[name]['main'].explode('data_prop_id').reset_index(drop=True)
        df_exploded = df_exploded.explode('obj_prop_id').reset_index(drop=True)
        df_exploded = pd.merge(df_exploded, self.ontology_df[name]['data_prop'], left_on='data_prop_id', right_on='data_prop_id')

        [df_exploded.drop(column, axis=1, inplace=True) for column in obsolete_columns if column in df_exploded.columns]
        df_exploded.drop_duplicates(inplace=True)
        df_exploded = df_exploded.sort_values('id').reset_index(drop=True)
        df_exploded.columns = ['pi_id_from', 'pi_id_to', 'node_type', 'label']
        df_exploded['label'] = '' # formatting
        df_exploded.to_excel(f'data/{name}_expansion_data_prop.xlsx')
        self.ontology_df[name]['expansion_data_prop'] = df_exploded
    
    def set_expansion_object_properties(self, name):
        df_exploded = self.ontology_df[name]['main'].explode('inherit_id').reset_index(drop=True)
        df_exploded.drop('data_prop_id', axis=1, inplace=True)
        df_exploded.drop('color', axis=1, inplace=True)
        df_exploded.drop('label', axis=1, inplace=True)
        df_exploded.drop('inherit_id', axis=1, inplace=True)
        df_exploded = df_exploded.explode('obj_prop_id').reset_index(drop=True)
        df_exploded = pd.merge(df_exploded, self.ontology_df[name]['obj_prop'], left_on='obj_prop_id', right_on='obj_prop_id')
        df_exploded.drop_duplicates(inplace=True)
        df_exploded = df_exploded[['id', 'obj_prop_id', 'obj_prop_class_id', 'label']]
        df_exploded.columns = ['pi_id_from', 'obj_prop_id', 'pi_id_to', 'label']
        df_exploded.to_excel(f'data/{name}_expansion_obj_prop.xlsx')
        self.ontology_df[name]['expansion_obj_prop'] = df_exploded
    
    def set_inheritance_object_properties(self, name, inherit_label:str = 'is'):
        df_exploded = self.ontology_df[name]['main'].explode('inherit_id').reset_index(drop=True)
        df_exploded = df_exploded[['inherit_id', 'label', 'id']]
        df_exploded.columns = ['pi_id_from', 'label', 'pi_id_to']
        df_exploded['label'] = f'{inherit_label.capitalize()} ' + df_exploded['label']
        df_exploded['label'] = '' # removed label
        df_exploded['obj_prop_id'] = df_exploded['pi_id_from'] + f'/{"_".join(inherit_label.lower().split())}_' + df_exploded['pi_id_to'].str.split('/').str[-1]

        if name == 'esc12': # ensure mapping between esc12, entity, ontology
            main_ontology_keys = [
                'http://www.pandoraintelligence.com/esc12',
                # 'http://www.pandoraintelligence.com/ontology/entitytype',
                # 'http://www.pandoraintelligence.com/ontology/propertytype'
            ]
            for row in df_exploded.loc[df_exploded.pi_id_from.isnull(), 'pi_id_from'].index:
                df_exploded.at[row, 'pi_id_from'] = main_ontology_keys

            df_exploded = df_exploded.explode('pi_id_from').reset_index(drop=True)
            
            #fix for proper ontology
            for row in df_exploded.loc[df_exploded.obj_prop_id.isnull(), 'obj_prop_id'].index:
                df_exploded.at[row, 'obj_prop_id'] = df_exploded.at[row, 'pi_id_from'] + '/' + str(df_exploded.at[row, 'label']).lower().replace(' ', '_') 
                
        df_exploded.to_excel(f'data/{name}_inheritance_obj_prop.xlsx')
        self.ontology_df[name]['inheritance_obj_prop'] = df_exploded
