# Step 3.1: Fetch HTML Content
# Please be careful to follow instructions on how to run the program; 
# the Run menu or right-click > Run options do not work in the simulated environment. 
# Ensure you have run the terminal command to install the correct libraries using pip.
# You must use the terminal window as directed in Step 3.
import requests
from bs4 import BeautifulSoup

### YOUR CODE HERE ###
# For demonstration, we'll use mock HTML. In a real scenario, you would fetch this
# from a live URL.
# url = "http://your-target-website.com/sports"
# response = requests.get(url)
# response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
# soup = BeautifulSoup(response.text, 'html.parser')

mock_html = """
<html>
    <body>
        <h2>Team Standings</h2>
        <table class='stats_table'>
            <thead>
                <tr><th>Team Name</th><th>Wins</th><th>Losses</th></tr>
            </thead>
            <tbody>
                <tr><td>Dragons</td><td>28</td><td>2</td></tr>
                <tr><td>Wizards</td><td>22</td><td>8</td></tr>
                <tr><td>Goblins</td><td>15</td><td>15</td></tr>
                <tr><td>Knights</td><td>11</td><td>19</td></tr>
            </tbody>
        </table>
    </body>
</html>
"""
soup = BeautifulSoup(mock_html, 'html.parser')

# Step 3.2: Extract the Required Data
### YOUR CODE HERE ###
game_data = []
table = soup.find('table', class_='stats_table')
for row in table.find('tbody').find_all('tr'):
    cols = row.find_all('td')
    if len(cols) == 3:
        team_name = cols[0].text.strip()
        wins = int(cols[1].text.strip())
        losses = int(cols[2].text.strip())
        game_data.append({'Team': team_name, 'Wins': wins, 'Losses': losses})

# Step 4.1: Convert to a DataFrame
# Import pandas
### YOUR CODE HERE ###
import pandas as pd

# Convert the game data into a pandas DataFrame
### YOUR CODE HERE ###
df = pd.DataFrame(game_data)

# Inspect the DataFrame
### YOUR CODE HERE ###
print("--- Inspected DataFrame ---")
print(df.head())

# Save and print the shaped data
### YOUR CODE HERE ###
print("\nData extraction and shaping complete.")

# Step 5.1: Save to a CSV File
# Save the DataFrame to a CSV file named sports_statistics.csv
### YOUR CODE HERE ###
df.to_csv('sports_statistics.csv', index=False)
print("Data saved to sports_statistics.csv")