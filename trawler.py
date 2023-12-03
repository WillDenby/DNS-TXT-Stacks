import pandas as pd
import dns.resolver
import re
import json

# Fetch DNS TXT Data Function
def fetch_data(domain, df):
    try:
        record_type = 'TXT'
        answers = dns.resolver.resolve(domain, record_type)

        data_lines = set()
        for rdata in answers:
            # Updated regular expression to capture the first word before hyphens or equals signs
            first_word_match = re.match(r'^"([^=\s.*"#@:,}!/+-]+)', str(rdata))
            if first_word_match:
                data_lines.add(first_word_match.group(1))

        filtered_data_lines = [line.lower() for line in data_lines if line[0].isalpha() and not (line.startswith('\\') or line == 'v' or line == 'as' or len(line) > 30 or "]" in line)]
        filtered_data_lines = list(set(filtered_data_lines))

        print(domain, ":", filtered_data_lines)

        if not filtered_data_lines:
            print("Skipped")
        else:
            # Create a temporary DataFrame for the current domain
            temp_df = pd.DataFrame({'URLS': [domain]})
            
            # Process Var2
            for col_name in filtered_data_lines:
                # Check if the column exists in the dataframe, if not, add it
                if col_name not in temp_df.columns:
                    temp_df[col_name] = False  # Add the column and initialize with False for the first row

                # Check if each column exists in the string and update the relevant cell in the newly created row
                temp_df.at[temp_df.index[-1], col_name] = col_name in filtered_data_lines
            
            # Concatenate the temporary DataFrame to the main DataFrame
            df = pd.concat([df, temp_df], ignore_index=True)

    except :
        print("Error on", domain)

    return df
  
# Initialise Blank DF with URLs Column
columns = ['URLS']
results = pd.DataFrame(columns=columns)

# Load Domains into DF
domains_list = pd.read_csv('domains.csv')

# Apply the fetch_data function to each row in domains and update results
for index, row in domains_list.iterrows():
    results = fetch_data(row['domain'], results)

# Drop columns with only one True value
columns_to_drop = results.columns[(results == True).sum() <= 1]
columns_to_drop = columns_to_drop[columns_to_drop != 'URLS']  # Exclude 'URLS'
results = results.drop(columns=columns_to_drop)

# Transpose the DataFrame, set the first column as the index, and reset the index to make it a column again
results = results.set_index(results.columns[0]).transpose().reset_index()
for column in results.columns:
    results[column] = results[column].apply(lambda x: column if x == True else x)

# Handle NaN values
results.fillna('', inplace=True)

# Creating a new column 'value' by concatenating all other columns
results['value'] = results.iloc[:, 1:].astype(str).agg(','.join, axis=1)

results['value'] = results['value'].str.replace(',+', ',', regex=True)

# Remove leading and trailing commas
results['value'] = results['value'].str.strip(',')

# Creating a new DataFrame with only 'key' and 'value' columns
result_df = results[['index', 'value']].rename(columns={'index': 'key'})

result_df['key'] = result_df['key'].str.capitalize()

####################
## OUTPUTS #########
####################

# Get keys list for website jquery
result_list = ','.join(map(str, result_df['key'].values))
result_list = result_list.split(',')
print(result_list)

# Get JSON to upload to CF Workers KV
df = result_df
json_data = []
for index, row in df.iterrows():
    key = row['key']
    values = ', '.join(map(str, row[1:]))
    
    key_value_object = {
        'key': key,
        'value': values
    }
    
    json_data.append(key_value_object)

output_file_path = 'output.json'
with open(output_file_path, 'w') as output_file:
    json.dump(json_data, output_file, indent=2)

print(f"JSON data has been saved to: {output_file_path}")


# Get HTML Table function

# The function
def list_to_html_table(my_list):

    my_list.sort()
    # Opening tag for the table
    html_string = "<table>\n"

    # Calculate the number of rows needed
    num_rows = (len(my_list) + 2) // 3

    # Adding list items to the HTML string
    for row in range(num_rows):
        html_string += "  <tr>"
        for col in range(3):
            index = row * 3 + col
            if index < len(my_list):
                html_string += f"<td style='text-align:center;'>{my_list[index]}</td>"
            else:
                html_string += "<td></td>"
        html_string += "</tr>\n"

    # Closing tag for the table
    html_string += "</table>"

    return html_string

# Convert the list to an HTML unordered list
html_output = list_to_html_table(result_list)


# Print or use the HTML string as needed
print(html_output)