# USDA census data extraction tool

The USDA census data provide detailed farm asset and commodity quantity by county by type for each state. The farm data are aggregated into multiple tables (more than 70 tables) for 
each state (e.g., California). Each state has single text file containing these tables. The tables are formatted in a way readable for humans, but are hard to extract data due to the complex and non-uniform formats. This data extraction
tool will help USDA data users to access required data based on a few data layout patterns in the text files. 