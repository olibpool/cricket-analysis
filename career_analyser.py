import matplotlib.pyplot as plt
import pandas as pd

analyse = True
odi = "Men ODI Player Innings Stats - 21st Century.csv"

while analyse == True:
    # Prompt player to analyse:
    batyes = True
    bowlyes = True
    matchformat = "Men Test Player Innings Stats - 21st Century.csv"
    matchtype = 'Test'
    
    print()
    print("Do you want to analyse tests or ODIs? Leave blank for tests or type ODI for ODIs.")
    if input() != '':
        matchformat = odi
        matchtype = 'ODI'
    print()

    print("Choose a player to analyse:")
    print("Make sure to write the name in the form used by cricinfo (e.g BA Stokes).")
    player = str(input())
    print()
    
    print("Do you want to analyse their batting? Leave empty for yes, or type no if not:")
    if input() != '':
        batyes = False
    print()

    print("Do you want to analyse their bowling? Leave empty for yes, or type no if not:")
    if input() != '':
        bowlyes = False


    # Initialising variables
    batmatchstats = [('Match Number', 'Match Date', 'Runs Scored', 'Number of Dismissals')]
    bowlmatchstats = [('Match Number', 'Match Date', 'Runs Conceeded', 'Wickets')]
    cumulativebat = []
    cumulativebowl = []
    graphmax = 0
    match = 1
    runs = 0
    bowlruns = 0
    outs = 0
    wickets = 0
    totruns = 0
    totouts = 0
    totbowlruns = 0
    totwickets = 0
    firstrow = True
    date = "blah"

    # Getting data for player
    df = pd.read_csv(matchformat)
    playerdata = df.loc[df['Innings Player'] == player]

    # Main Loop
    print()
    print()

    if playerdata.empty:
        print("There is no player in the database called " + str(player))
        print("Make sure you use the format used by cricinfo (e.g BA Stokes).")
        print()

    else:
        for i in range(0,len(playerdata)):
            rowdata = playerdata.iloc[i]
            
            if rowdata.loc['Innings Date'] != date or i == len(playerdata) - 1:
                if firstrow != True:
                    
                    totruns += runs
                    totouts += outs
                    totbowlruns += bowlruns
                    totwickets += wickets

                    if totouts != 0:
                        cumulativebat.append(totruns/totouts)
                    else:
                        cumulativebat.append(0)
                    if totwickets != 0:
                        cumulativebowl.append(totbowlruns/totwickets)
                    else:
                        cumulativebowl.append(0)
                    if cumulativebat[match - 1] > graphmax:
                        graphmax = cumulativebat[match - 1]
                    if cumulativebowl[match - 1] > graphmax:
                        graphmax = cumulativebowl[match - 1]

                    batmatchstats.append((match, date, runs, outs))
                    bowlmatchstats.append((match, date, bowlruns, wickets))

                    match += 1
                    runs = 0
                    outs = 0
                    bowlruns = 0
                    wickets = 0

                else:
                    firstrow = False

                date = rowdata.loc['Innings Date']

                

            if rowdata.loc['Innings Batted Flag'] == 1:
                runs += int(rowdata.loc['Innings Runs Scored Num'])
                if int(rowdata.loc['Innings Not Out Flag']) != 1:
                    outs += 1
            else:
                if rowdata.loc['Innings Bowled Flag'] == 1:
                    bowlruns += int(rowdata['Innings Runs Conceded'])
                    wickets += int(rowdata['Innings Wickets Taken'])


        print('Career ' + str(matchtype) + ' Summary for ' + str(player))
        print()
        print("==============================================================")
        if batyes == True:
            print("Batting match stats for each match: ")
            print(batmatchstats)
            print("==============================================================")
        if bowlyes == True:
            print("Bowling match stats for each match: ")
            print(bowlmatchstats)
            print("==============================================================")
        print()
        print("Number of " + str(matchtype) + " matches played: " + str(match - 1))
        print()
        if batyes == True:
            print("Batting average = " + str(cumulativebat[-1]))
            print()
        if bowlyes == True:
            print("Bowling average = " + str(cumulativebowl[-1]))
            print()
        print("Average over time: ")
        if batyes == True:
            print("Batting = " + str(cumulativebat))
            print()
        if bowlyes == True:
            print("Bowling = " + str(cumulativebowl))
            print()

        if batyes == True:
            plt.plot(range(1, match), cumulativebat, label = "Batting average")
        if bowlyes == True:
            plt.plot(range(1, match), cumulativebowl, label = "Bowling average")
        plt.axis([0,match,0,graphmax + 5])
        plt.xlabel('Number of matches')
        plt.ylabel('Average')
        plt.title(str(matchtype) + ' averages for ' + str(player))
        plt.legend()
        plt.show()

    print("Type 'exit' to quit the program or press enter to anlayse another player.")
    if input() == 'exit':
        analyse = False
