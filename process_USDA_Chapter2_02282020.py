# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 14:53:33 2019

Retreve value from specific table based on whether county listed as row or column

Examples:
    print(california.retreve_value_county_as_column('Table 2', 'Tulare', 'Cattle and calves', '$1,000, 2017'))
    
    print(california.retreve_value_county_as_column('Table 2', 'aaa', 'Cattle and calves', '$1,000, 2017'))

Improvements:
    ver-02282020
        -When county name is not available for specific item for specific table, it returns "-"

@author: Fei Xie
"""

import csv
import pandas as pd
import numpy as np
import re

class Farm_County_Process:
    def __init__(self,filename):
        self.lines = self.read_text(filename)
        self.table_count = 56
        self.tables_start_end_line = self.store_table_line_positions(self.lines,1000,self.table_count)

    #common defined functions used to process text data
    #read state county file    
    def read_text(self,file_name):
        file = open(file_name, 'r')
        lines = file.readlines()
        file.close()
        return lines
    # check if certain text contains in the line, return true if it exists, false otherwise
    def if_find_text (self, line, text_string):
        #print(line)
        #print(text_string)
        if text_string in line:
            return True
        else:
            return False
    
    #to fine the next line that contains the string, from the starting line, if return 0, does not exist    
    def return_line_index_next_string (self, start_line_index, text, end_line_index, lines):
        if start_line_index == -1:
            return -1
        
        current_line = start_line_index
        if_find_line = False
        
        while (current_line<len(lines)) and (current_line <= end_line_index) and (not if_find_line):
            if self.if_find_text(lines[current_line], text):
                if_find_line = True
            else:
                current_line+=1
        
        if if_find_line == True:
            return current_line
        else:
            return -1
   
    #to find the "end_line_index" for "return_line_index_next_string"
    def return_end_line_index(self, table_name, start_line_index, lines):
        end_line_index = self.tables_start_end_line.loc[self.tables_start_end_line['Table'] == table_name, 'End_Line'].iloc[0]
        
        current_line = start_line_index + 7 #not considering the first "State Total"
        if_find_line = False
        
        while current_line <= end_line_index and not if_find_line:
            if self.if_find_text(lines[current_line], "State Total"):
                if_find_line = True
                end_line_index = current_line
            else:
                current_line += 1
        return end_line_index
        
    
    #to find the previous line that contains the string, from the starting line, if return 0, does not exist
    def return_line_index_previous_string(self, start_line_index, text, lines):
        if start_line_index == -1:
            return -1
        
        current_line = start_line_index
        if_find_line = False
        
        while current_line >= 1000 and not if_find_line:
            if self.if_find_text(lines[current_line], text):
                if_find_line = True
            else:
                current_line-=1
        
        if if_find_line == True:
            return current_line
        else:
            return -1
    
    #return the column index for the county, if county is listed by column
    def return_county_column(self, target_line_index, county, lines):
        if target_line_index == -1:
            return -1
        
        target_line = lines[target_line_index]
        #print(target_line) #debug
        target_line = target_line.split(":")
        target_line = [i.strip() for i in target_line]
       # print(target_line)
        #print(type(target_line)) #debug
        
        for i in range(1,len(target_line)):
            if target_line[i] == county.strip():
                return i
        return -1
    
    #return value based on column index from specific line
    def return_value_from_line_by_column_index(self, target_line_index, column_index, lines):
        if target_line_index == -1 or column_index ==-1:
            return "NA"
                
        target_line = lines[target_line_index]
        #print(target_line)
        target_line = re.split(r'\s{2,}|......:', target_line)
        while("" in target_line):
            target_line.remove("")
        #print(target_line)
        target_line = [i.strip() for i in target_line]
        #print(target_line)
        
        return target_line[column_index]
    
    def retreve_value_county_as_column(self, table_name, county, look_string1 = "", look_string2 = "", look_string3 = ""):
        #locate table position (start point and end point)
        current_line = self.tables_start_end_line.loc[self.tables_start_end_line['Table'] == table_name, 'Beg_Line'].iloc[0]
        max_line = self.tables_start_end_line.loc[self.tables_start_end_line['Table'] == table_name, 'End_Line'].iloc[0]
        
        #locate the table portion with the target item
        current_line = self.return_line_index_next_string(current_line, look_string1, max_line, self.lines)
        current_line = self.return_line_index_previous_string(current_line, table_name, self.lines)
        
        #locate the line with the county name
        
        current_line = self.return_line_index_next_string(current_line, county, max_line, self.lines)
        
        if current_line == -1:
            return "-"
            
        column_index = self.return_county_column(current_line,county,self.lines)
        
        if look_string1 != "":
            current_line = self.return_line_index_next_string(current_line, look_string1, max_line, self.lines)
        
        if look_string2 != "":
            current_line = self.return_line_index_next_string(current_line, look_string2, max_line, self.lines)
        
        if look_string3 != "":
            current_line = self.return_line_index_next_string(current_line, look_string3, max_line, self.lines)
        
        return self.return_value_from_line_by_column_index(current_line, column_index, self.lines)
        
        #print(current_line)
        #print(max_line)
    
    def retreve_value_county_as_column2(self, table_name, county, look_string1 = "", look_string2 = "", look_string3 = ""):
        #locate table position (start point and end point)
        current_line = self.tables_start_end_line.loc[self.tables_start_end_line['Table'] == table_name, 'Beg_Line'].iloc[0]
        max_line = self.tables_start_end_line.loc[self.tables_start_end_line['Table'] == table_name, 'End_Line'].iloc[0]
        
        #locate the table portion with the target item
        current_line = self.return_line_index_next_string(current_line, look_string1, max_line, self.lines)
        current_line = self.return_line_index_previous_string(current_line, table_name, self.lines)
        
        #locate the line with the county name
        
        current_line = self.return_line_index_next_string(current_line, county, max_line, self.lines)
        
        if current_line == -1:
            return "-"
            
        column_index = self.return_county_column(current_line,county,self.lines)+1
        
        if look_string1 != "":
            current_line = self.return_line_index_next_string(current_line, look_string1, max_line, self.lines)
        
        if look_string2 != "":
            current_line = self.return_line_index_next_string(current_line, look_string2, max_line, self.lines)
        
        if look_string3 != "":
            current_line = self.return_line_index_next_string(current_line, look_string3, max_line, self.lines)
        
        return self.return_value_from_line_by_column_index(current_line, column_index, self.lines)
    
    def retreve_value_county_as_row(self, table_name, county, column_index, item_text = ""):
        #locate table position (start point and end point)
        current_line = self.tables_start_end_line.loc[self.tables_start_end_line['Table'] == table_name, 'Beg_Line'].iloc[0]
        max_line = self.tables_start_end_line.loc[self.tables_start_end_line['Table'] == table_name, 'End_Line'].iloc[0]
        
        #print(current_line)
        #locate the table portion with the target item
        if item_text != "":
            current_line = self.return_line_index_next_string(current_line, item_text, max_line, self.lines)
        if current_line > max_line or current_line == -1:  #new added
            return "-"             #new added
        #locate the line with the county name
        
        current_line = self.return_line_index_next_string(current_line, county, self.return_end_line_index(table_name,current_line,self.lines), self.lines)
        if current_line > max_line or current_line == -1:
            return "-"
        
        return self.return_value_from_line_by_column_index(current_line, column_index, self.lines)
    

    def retreve_value_county_as_row2(self, table_name, county, column_index, item_text = ""):
        #locate table position (start point and end point)
        current_line = self.tables_start_end_line.loc[self.tables_start_end_line['Table'] == table_name, 'Beg_Line'].iloc[0]
        max_line = self.tables_start_end_line.loc[self.tables_start_end_line['Table'] == table_name, 'End_Line'].iloc[0]
        
        #print(current_line)
        #locate the table portion with the target item
        if item_text != "":
            current_line = self.return_line_index_next_string(current_line, item_text, max_line, self.lines)
        
        #locate the line with the county name
        
        current_line = self.return_line_index_next_string(current_line, county, self.return_end_line_index(table_name,current_line,self.lines), self.lines)
        #find the next line for the county
        current_line = self.return_line_index_next_string(current_line+1, county, self.return_end_line_index(table_name,current_line,self.lines), self.lines)
        if current_line > max_line or current_line == -1:
            return "-"
        
        return self.return_value_from_line_by_column_index(current_line, column_index, self.lines)

    
        
    def store_table_line_positions (self,lines, start_line_number, max_table_count):
        store_table_line_df = pd.DataFrame(columns=['Table', 'Beg_Line', 'End_Line'])
        if_start_line = False
        if_end_line = False
        current_line = start_line_number
        current_table_number = 1
        
        for current_table_number in range(1, max_table_count+1):
            this_table = "Table " + str(current_table_number) +"."
            next_table = "Table " + str(current_table_number+1) +"."
            if_start_line = False
            if_end_line = False
            start_line_position = 0
            end_line_position = len(lines)-1
            
            while current_line < len(lines) and not if_end_line:
                if not if_start_line:
                    if self.if_find_text(lines[current_line],this_table):
                        if_start_line = True
                        start_line_position = current_line
                elif not if_end_line:
                    if self.if_find_text(lines[current_line], next_table):
                        if_end_line = True
                        end_line_position = current_line-1
                        current_line -= 1
                current_line += 1
            
            store_table_line_df = store_table_line_df.append({"Table": "Table " + str(current_table_number), "Beg_Line": start_line_position, "End_Line": end_line_position}, ignore_index = True)
        print(store_table_line_df)
        return store_table_line_df





