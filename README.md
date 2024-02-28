# Python for Football Manager 2023 Scouting

## Overview
Football Manager 2023 offers a vast and intricate database of player attributes, performance statistics, and potential within the simulated footballing world. However, harnessing this wealth of data for comprehensive scouting and analysis can be a complex task. This project presents a solution by leveraging Python scripts to streamline the extraction and compilation of player data from FM 23. By utilizing these scripts, users can gather player information from multiple seasons, tracking changes in attributes and performance over time. This facilitates the creation of a centralized and dynamic database that empowers Football Manager enthusiasts to delve deeper into player development trends, identify rising stars, and make strategic decisions within the game.

## Features
- **Data Extraction:** Extract player attributes and statistics from Football Manager 2023.
- **Compilation:** Compile seasons data into a structured database for easy analysis.
- **Historical Tracking:** Track player progression and changes in attributes over time.
- **Customization:** Adapt scripts for specific scouting needs or preferences.

## Goals
- **Streamlined Scouting:** Simplify the process of collecting and organizing player data from FM 23.
- **Data-driven Insights:** Enable users to derive meaningful insights by analyzing historical player information.
- **User Flexibility:** Provide customization options for tailored scouting experiences.

## Why have I created this?
Stats in Football Manager only last for a single season. The reset date varies by country and season, but when you reach the season start date for a specific country, all the stats from players of said country are gone. When you check the teams, all stats are 0 because they represent only the current season. As you will see on the files we'll create, storing this amount of data would make the game really heavy.

But the problem is: if we lose these stats, how can we have a real Moneyball approach to FM? Usually people only look for a whole season of data and analyze that. So if you are in Europe you would probably need to export stats on the first day of June to ensure everyone will have their stats. While this can be enough for most people, it didn't click for me. When I need to sign a player, I want to be able to look at his whole career before making a decision. The only way to do this is to export the stats before the season ends, but the problem is that we have two main kinds of seasons: the ones who follow the calendar year and the ones who follow the European style.

## Processing exports
The first step on the ladder is the file ``Exports processor.ipynb``. For this method to work properly, you should run this script twice a year so you always have the most recent data. This allows you to make mid-season signings and also to avoid losing data. In FM23, when a player moves between clubs his season stats are wiped and you can no longer export it through the Player Search screen. This is a common occurence because many players change clubs during the mid-season January window if you are in Europe. Also always remember to INCLUDE players from your club on the search.

To run this, you need to create 4 files of data:
- **Genie Scout** -> The file *Genie View.glf* is a custom view for Genie Scout. You just have to load the game into it and, while you are still at the FM Player Search screen, import all these players into the Genie Scout screen. Then export the data to CSV using the custom view columns.
- **FM Export** -> Using the *Python - Scouting.fmf* view, export a list of as many players as you want on FM23. Just go into the Player Search, hit CTRL+A and CTRL+P to print it as a Web Page to an HTML file. Always check the shape of the dataframe that comes from this html file. Exporting a large amount of players on FM is always a bit buggy. Also be aware that files over 50MB may not be read correctly by Python.
- **Interested players** -> Using the same filters as above, select the "Interested" box, load this sortlist into Genie and export to CSV
- **Filter list** -> I use this to filter players 4* CA or 4.5* PA, but you can use however you want. This creates a binary column and you can focus on these players on the analysis.

The end result you get from this is named like ``Scouting - 2023.12`` for December 2023 data. This is ready to analyze if you want to go early on and if you have a season full of data this could be a good idea. I tend to start my save games in May 2023 so I have a season worth of data to analyze before even choosing a team. But the best part here is that you can aggregate this exports (JUN23, DEC23, JUN24...) into a single one. This way you only have one line for each player with his total stats up until then and his latest attributes composition. This is done automatically by the script. You only have to keep all the CSV files in the same folder.

## How to create the exports

### FM Export

Go into the Player Search screen, set the view to the custom one, filter the way you want and select all the players by pressing CTRL+A. Try to keep it below 40,000 players. When the game selects everyone, you can press CTRL+P and export it to the script folder.

<img src="https://github.com/hmantovani/football-manager/blob/main/step1.png"/>

<img src="https://github.com/hmantovani/football-manager/blob/main/step2.png"/>

### Genie exports

Once you have the game loaded into Genie, you can follow the image below to load a shortlist into Genie. This will load every player in your Player Search screen to Genie.

<img src="https://github.com/hmantovani/football-manager/blob/main/step3.png"/>
