# player_headshots

I'm imagining this will work similar to this process:

1. Get every player in the NBA during time of execution (get roster for each team)
2. Get their headshot from NBA.com with their id
3. Make a directory of their id in this repo if it does not already exist
4. Put headshot in directory with the file name either being the season id or season year

I'm not sure how we can easily access this. Making a small flask app for this wouldnt be hard but is that even necessary? Maybe Github offers some file api? My ideal api flow is:

1. User makes a request with play id and year
2. If we have it, return the bytes of file
3. If we do not, return bytes of generic not found avatar
