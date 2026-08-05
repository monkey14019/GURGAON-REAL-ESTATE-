from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

base_dir = Path(__file__).resolve().parent
candidate_paths = [
    base_dir.parent / 'data of gurugram real Estate.csv',
    base_dir / 'data of gurugram real Estate.csv',
    Path.cwd() / 'data of gurugram real Estate.csv',
]

csv_path = next((p for p in candidate_paths if p.exists()), None)
if csv_path is None:
    raise FileNotFoundError(f'CSV file not found. Tried: {candidate_paths}')

df = pd.read_csv(csv_path)
print(df.info())
print(df.head())
print(df.columns.tolist()) # this will print the list of columns in the dataframe. It will help us to understand the structure of the dataframe and to know what columns are present in the dataframe. It will also help us to know what columns we can use for data visualization.

# DATA CLEANING
df.columns = df.columns.str.strip().str.replace(" ","_").str.upper()  # this will remove any leading or trailing spaces from the column names, replace any spaces with underscores and convert all the column names to uppercase. This will help us to avoid any issues while accessing the columns in the dataframe. It will also help us to maintain consistency in the column names.
print(df.columns.tolist())
df=df.drop_duplicates() # this will remove any duplicate rows from the dataframe. It will help us to avoid any issues while analyzing the data and to maintain the integrity of the data. It will also help us to avoid any issues while visualizing the data.

# NUMERICAL COLUMNS CLEANING
df["PRICE"] = df["PRICE"].str.replace(",","").astype(float).astype(int)  # CONVERTED THE DATATYPE OF PRICE COLUMN FROM STRING TO FLOAT AND THEN TO INT. 
print(df["PRICE"])
df.rename(columns={"SOCITY":"SOCIETY"}, inplace=True) # "inplace=True" means that the changes will be made in the original dataframe and it will not return a new dataframe. It will modify the original dataframe.
print(df.columns.tolist())
df["RATE_PER_SQFT"] = df["RATE_PER_SQFT"].str.replace(",","").astype(int) # CONVERTED THE DATATYPE OF RATE_PER_SQFT COLUMN FROM STRING TO INT.
print(df["RATE_PER_SQFT"])

# CATEGORY COLUMNS CLEANING
df["STATUS"] = df["STATUS"].str.strip().str.upper().str.replace(" ","_")
print(df["STATUS"])
df["RERA_APPROVAL"] = df["RERA_APPROVAL"].str.strip().str.upper().str.replace(" ","_").map({'APPROVED_BY_RERA': True , 'NOT_APPROVED_BY_RERA': False})
print(df["RERA_APPROVAL"])
# print(df.info()) 

# Q.1 WHICH IS THE COSTLIEST FLAT IN GURGAON ?
# costliest_flat=df["PRICE"].max() # THIS WILL RETURN THE MAXIMUM VALUE IN THE PRICE COLUMN. BUT WE WANT TO GET ALL THE DETAILS OF THE COSTLIEST FLAT. SO WE WILL USE LOC[] FUNCTION TO ACCESS THAT ROW AND GET ALL THE DETAILS OF THE COSTLIEST FLAT.
# print(costliest_flat) 
costliest_flat = df.loc[[df["PRICE"].idxmax()]]  # idxmax() function is used to return the index of the first occurrence of the maximum value in the specified column. In this case, it will return the index of the row with the maximum value in the "PRICE" column. Then we use loc[] function to access that row and get all the details of the costliest flat in Gurgaon.
print(costliest_flat) 

# OUTPUT OF THE ABOVE CODE WILL BE LIKE THIS:
''' PRICE                                  1226300000
STATUS                              READY_TO_MOVE
AREA                                        16500
RATE_PER_SQFT                               74323
PROPERTY_TYPE    6 BHK Apartment in DLF Camellias
LOCALITY                                Sector 42
BUILDER_NAME                    Provident Capital
RERA_APPROVAL                               False
BHK_COUNT                                     6.0
SOCIETY                             DLF Camellias
COMPANY_NAME                                  DLF
FLAT_TYPE                               Apartment
Name: 2839, dtype: object  '''    # THIS 2839 IS THE INDEX OF THE ROW WITH THE MAXIMUM VALUE IN THE "PRICE" COLUMN. IT WILL HELP US TO KNOW THE LOCATION OF THE COSTLIEST FLAT IN GURGAON.

# Q.2 WHICH LOCALITY HAS THE HIGHEST AVERAGE PRICE?
''' locality_avg_price = df.groupby("LOCALITY")["PRICE"].mean().idxmax() # groupby() function is used to group the dataframe by the "LOCALITY" column. Then we use mean() function to calculate the average price for each locality. Finally, we use idxmax() function to get the locality with the highest average price.
print(locality_avg_price)
highest_avg_price_value = locality_avg_price.loc[locality_avg_price.max()] 
print(highest_avg_price_value)''' # THIS WILL PRINT THE HIGHEST AVERAGE PRICE VALUE. IT WILL HELP US TO KNOW THE AVERAGE PRICE OF THE LOCALITY WITH THE HIGHEST AVERAGE PRICE.

# ALTERNATIVE METHOD 
avg_price_by_locality = df.groupby("LOCALITY")["PRICE"].mean()
print(avg_price_by_locality) # it will print the average price of each locality in Gurgaon. It will help us to know the average price of each locality and to compare the average prices of different localities. It will also help us to identify the locality with the highest average price.

highest_locality = avg_price_by_locality.idxmax() # this will return the locality with the highest average price. It will help us to know which locality has the highest average price in Gurgaon. 
print(highest_locality) # this will print the locality with the highest average price which is Baliwas.
# OUTPUT : BALIAWAS

highest_value = avg_price_by_locality.loc[highest_locality] #loc[] function is used to access the value of the highest locality in the avg_price_by_locality series. It will help us to know the average price of the locality with the highest average price.
print(highest_value) # it will give the average price of the locality Baliawas with the highest average price which is 583333333.3333334


# Q.3 WHICH LOCALITY HAS THE HIGHEST RATE PER SQUARE FOOT ?
rate_per_sqft_by_locality = df.groupby("LOCALITY")["RATE_PER_SQFT"].mean()
print(rate_per_sqft_by_locality) # it will print the average rate per square foot of each locality in Gurgaon. It will help us to know the average rate per square foot of each locality and to compare the average rates per square foot of different localities. It will also help us to identify the locality with the highest average rate per square foot.
highest_rate_locality = rate_per_sqft_by_locality.idxmax() # idxmax() function is used to return the index of the first occurrence of the maximum value in the specified column. In this case, it will return the index of the row with the maximum value in the "RATE_PER_SQFT" column which will be SECTOR 42.
print(highest_rate_locality) # this will print the locality with the highest average rate per square foot i.e. SECTOR 42
highest_value_rate = rate_per_sqft_by_locality.loc[highest_rate_locality]
print(highest_value_rate)   # 55989.083333333336 this is value of the highest average rate per square foot in SECTOR 42. 

max_rate= df["RATE_PER_SQFT"].max()
print(max_rate) # 310000 this is the maximum rate per square foot in the entire dataset. It will help us to know the maximum rate per square foot in Gurgaon. It will also help us to identify the locality with the highest rate per square foot.
max_rate_index = df["RATE_PER_SQFT"].idxmax() # so first we will find the index of the row with the maximum value in the "RATE_PER_SQFT" column using idxmax() function which is 2115.
print(max_rate_index) # OUTPUT: 2115
row_with_max_rate = df.loc[[max_rate_index]]
print(row_with_max_rate) 
# OUTPUT:
# PRICE     STATUS  AREA  RATE_PER_SQFT     PROPERTY_TYPE  ... RERA_APPROVAL   BHK_COUNT   SOCIETY       COMPANY_NAME FLAT_TYPE
#108500000  RESALE   350     310000          Residential Plot  ...   False       0.0     Outside Socity   Outside       Plot

# Q.4 DO READY TO MOVE PROPERTIES COST MORE THAN UNDER CONSTRUCTION PROPERTIES?
ready_to_move = df[df["STATUS"] == 'READY_TO_MOVE']["PRICE"].mean()
under_construction = df[df["STATUS"] == 'UNDER_CONSTRUCTION']["PRICE"].mean()
print(ready_to_move) # output: 41521381.791256554
print(under_construction) # output: 39579456.39760865
if(ready_to_move > under_construction):
    print(f"Ready to move properties cost more than under construction properties i.e. {ready_to_move}")
else:
    print(f"Under construction properties cost more than ready to move properties i.e. {under_construction}")

# Q.5 DO RERA APPROVAL PROPERTIES COMMANDS A PRICE PREMIUM ?
rera_approved = df[df["RERA_APPROVAL"] == True]["PRICE"].mean()
rera_not_approved = df[df["RERA_APPROVAL"] == False]["PRICE"].mean()
print(rera_approved) 
print(rera_not_approved)
if rera_approved > rera_not_approved :
    print(f"RERA approved properties command a price premium i.e. {rera_approved}")
else:
    print(f"RERA approved properties does not command a price premium i.e. {rera_not_approved}")
    
# Q.6 HOW DOES AREA IMPACT THE PRICE ?
sns.scatterplot(data=df , x="AREA" , y="PRICE")
# plt.show()

# Q.7 WHICH BHK CONFIGURATION IS MOST EXPENSIVE ?
bhk_expensive = df.groupby("BHK_COUNT")["PRICE"].mean().idxmax()
print(bhk_expensive)  # OUTPUT: 7 BHK

# Q.8 WHICH PROPERTY TYPE IS THE COSTLIEST ?
property_type_expensive = df.groupby("PROPERTY_TYPE")["PRICE"].mean().idxmax()
print(property_type_expensive) # OUTPUT: 6 BHK Apartment in DLF Camellias

# Q.9 DO CERTAINS BUILDERS PRICE HIGHERS ?
builder_expensive = df.groupby("BUILDER_NAME")["PRICE"].mean().idxmax()
print("Q.9 Builder Answer:", builder_expensive)
builder_company_name_expensive = df.groupby("COMPANY_NAME")["PRICE"].mean().idxmax()
print("Q.9 Company Answer:", builder_company_name_expensive)