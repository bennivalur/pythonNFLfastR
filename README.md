# Python and NFLFastR
Some python files and function to help explore the NFLFastR

## Getting started
I recommend taking a look at the following links 
- [Deryck97's nflfastR python guide][pythonguide]
- The twitter account of [nflfastR][twNFLFastR]
- This [R beginner guide][variableNames] by Ben Baldwin, here is a list of all column names


## Tips/Notes
- Most of the scripts will generate a folder for the files they create.

## Files and functions

### getData.py
Contains one function helps create the csv data file with the data needed withouth all the unwanted columns. The function can be imported into any other python file like this

```python
from getData import getD
```

It has takes 4 input parameters
- year_from: number (1999-2019)
- year_to: number (1999-2019)
- columns: array -> what columns to keep - example = ['game_id','posteam','play_type','epa','temp','season']
- _directory: string -> will create a folder with that name and save the datafile there

### trubisky.py
Prop the reason you are here.  Creates the graph seen [here][benbaldwintweet] or [here][bigcattweet]
This plots QB performance when the temperature is exactly 66° fahrenheit when QBs have a minimum 30 attempted passes and mora than 1 rushing attempt.

There is a method error in the script.  Since I grouped by name, the Carr brothers were grouped in to a single person.  The fix would be to group by id and name instead of just name.

Since this script is just ment to be funny, I decided not to fix it, but just acknowledge the error here

### pepsimaxXG
Plots the expected goals(xG) vs expected goals against(xGA) for the teams in the Icelandic Pepsi-Max league.

You need to create a folder called 'pepsi_max_logos' with the logos of the teams.  The filenames should match the ones of the teams in the script.



[pythonguide]: https://gist.github.com/Deryck97/dff8d33e9f841568201a2a0d5519ac5e
[twNFLFastR]: https://twitter.com/nflfastR
[variableNames]: https://mrcaseb.github.io/nflfastR/articles/beginners_guide.html
[benbaldwintweet]:https://twitter.com/benbbaldwin/status/1286799784028839938?s=20
[bigcattweet]:https://twitter.com/BarstoolBigCat/status/1287054168939728909?s=20