"""
This code creates batch processing of all required data from the USDA census file. Users need downloaded required state USDA file from the census and specifify the state name. Example usage is:

	state_batch = Batch_Process_State("California", "06")
    state_batch.run()



@author: Fei Xie
"""





import pandas as pd
from process_USDA_Chapter2_02282020 import Farm_County_Process

class Batch_Process_State:
    def __init__(self, state_name, state_id):
        self.state_name = state_name
        self.state_USDA = Farm_County_Process(state_name+"_USDA.txt")   #create a object for USDA processing
        self.county_list = pd.read_csv(state_name+"_county.csv", dtype=object)   #read county list for the target state
        self.required_data_county_as_row = pd.read_csv("county_as_row.csv")
        self.required_data_county_as_column = pd.read_csv("county_as_column.csv")
        self.processed_data_county_as_row = self.required_data_county_as_row
        self.processed_data_county_as_column = self.required_data_county_as_column
        self.state_id = state_id;
        
    def batch_process_county_as_row(self):
        print("processing county as rows: ")
        self.processed_data_county_as_row = self.required_data_county_as_row
        
        for index, row in self.county_list.iterrows():
            current_county = self.county_list.loc[index, 'CNTY_NAME']
            print(current_county)
            
            self.processed_data_county_as_row[current_county] = "NA"
            for index2, row2 in self.processed_data_county_as_row.iterrows():
                table_name = self.processed_data_county_as_row.loc[index2,"Table"]
                column_num = int(self.processed_data_county_as_row.loc[index2,"Column"])
                item_name = self.processed_data_county_as_row.loc[index2,"Item"]
                self.processed_data_county_as_row.loc[index2,current_county] = self.state_USDA.retreve_value_county_as_row(
                        table_name, current_county, column_num, item_name)
        self.processed_data_county_as_row.to_csv(r""+self.state_id+"_results_column_based_"+self.state_name + ".csv", index = None, header = True)
   
    def batch_process_county_as_column(self):
        print("processing county as columns: ")
        self.processed_data_county_as_column = self.required_data_county_as_column
        
        for index, row in self.county_list.iterrows():
            current_county = self.county_list.loc[index, 'CNTY_NAME']
            print(current_county)
            
            self.processed_data_county_as_column[current_county] = "NA"
            for index2, row2 in self.processed_data_county_as_column.iterrows():
                table_name = self.processed_data_county_as_column.loc[index2,"Table"]
                item_name = self.processed_data_county_as_column.loc[index2,"Item"]
                unit_name = self.processed_data_county_as_column.loc[index2,"Unit"]
                print(table_name)
                print(item_name)
                print(unit_name)
                self.processed_data_county_as_column.loc[index2,current_county] = self.state_USDA.retreve_value_county_as_column(
                        table_name, current_county, item_name, unit_name)
        
        self.processed_data_county_as_column.to_csv(r""+self.state_id+"_results_row_based_"+self.state_name + ".csv", index = None, header = True)
	
    def run(self):	
        self.batch_process_county_as_row()
        self.batch_process_county_as_column()
        
        
        
def main():

    state_batch = Batch_Process_State("California", "06")
    state_batch.run()
main()