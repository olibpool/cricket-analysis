import matplotlib.pyplot as plt
import pandas as pd

analyse = True
matchtype = 'test'
odi = "Men ODI Player Innings Stats - 21st Century.csv"

while analyse == True:
    # Prompt input from user:
    batyes = True
    bowlyes = True
    rollrange = 20
    matchformat = "Men Test Player Innings Stats - 21st Century.csv"

    print()
    print("Do you want to analyse tests or ODIs? Leave blank for tests or type ODI for ODIs.")
    if input() != '':
        matchformat = odi
        matchtype = 'ODI'
    print()

    print("Choose a player to analyse:")
    print("Make sure to write the name in the form that cricinfo uses (e.g BA Stokes).")
    player = str(input())
    print()

    print("What period do you want to analyse over? (integer number of games, leave blank for 20)")
    x = input()
    if x != '':
        while x.isdigit() == False:
            print("Please make sure you input an integer value")
            x = input()
        rollrange = int(x)

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
    rollingbat = []
    rollingbowl = []
    graphmax = 0
    rollgraphmax = 0
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
        for i in range(0, len(playerdata)):
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

        for i in range(1, len(batmatchstats) + 1):
            if i > rollrange:
                rollruns = 0
                rollouts = 0
                rollbowlruns = 0
                rollwickets = 0

                for j in range(i - rollrange, i):
                    rollruns += int(batmatchstats[j][2])
                    rollouts += int(batmatchstats[j][3])
                    rollbowlruns += int(bowlmatchstats[j][2])
                    rollwickets += int(bowlmatchstats[j][3])

                # Creating rolling batting average
                if rollouts != 0:
                    rollingbat.append(rollruns / rollouts)
                else:
                    rollingbat.append(0)
                
                # Creating rolling bowling average
                if rollwickets != 0:
                    rollingbowl.append(rollbowlruns / rollwickets)
                else:
                    rollingbowl.append(0)
                
                # Sort out graph range
                if batyes == True:
                    if rollingbat[-1] > rollgraphmax:
                        rollgraphmax = rollingbat[-1]
                if bowlyes == True:
                    if rollingbowl[-1] > rollgraphmax:
                        rollgraphmax = rollingbowl[-1]
                

        #Print out the data
        print('Rolling ' + str(matchtype) + ' averages for ' + str(player))
        print("==============================================================")
        if batyes == True:
            print("Rolling batting average for previous period of " + str(rollrange) + " games at each match.")
            print(rollingbat)
            print("==============================================================")
        if bowlyes == True:
            print("Rolling bowling average for previous period of " + str(rollrange) + " games at each match.")
            print(rollingbowl)
            print("==============================================================")
        print()
        print("Number of " + str(matchtype) + " matches played: " + str(match - 1))
        print()    

        if batyes == True:
            plt.plot(range(rollrange , match), rollingbat, label = "Rolling batting average")
        if bowlyes == True:
            plt.plot(range(rollrange , match), rollingbowl, label = "Rolling bowling average")
        plt.axis([rollrange , match, 0, rollgraphmax + 5])
        plt.grid(alpha = 100)
        plt.xlabel('Number of matches')
        plt.ylabel('Average')
        plt.title('Rolling ' + str(matchtype) + ' averages over a period of ' + str(rollrange) + ' games, for ' + str(player))
        plt.legend()
        plt.show()

        print("Type 'exit' to quit the program or press enter to analyse another player.")
        if input() == 'exit':
            analyse = False
