from RiotAPI import RiotAPI
import RiotConsts as Consts
import time
import csv


def main():

    summoner_id = Consts.SUMMONER_ID['emjay3000']

    api = RiotAPI('RANKED_SOLO_5x5', '', '', '82a7b066-b6f2-4e3f-8f15-9ee01aa68c22')
    l = api.get_match_list(summoner_id)
    ranked_games = l['totalGames']

    # Find How Many Games Need to be Updated
    for i in range(l['totalGames']):
        if l['matches'][i]['matchId'] == Consts.MATCH_ID['latest']:
            update = i
            break

    # If no update needed, end program
    if 'update' not in locals():
        print('Match History Up To Date')
        return
    else:
        print(update)

    # Initialize Dictionaries
    match_id = dict()
    season = dict()
    match_length = dict()
    mins = dict()
    secs = dict()
    result = dict()
    role = dict()
    champion = dict()
    kills = dict()
    deaths = dict()
    assists = dict()
    kda = dict()
    cpm = dict()
    gpm = dict()
    cpm_0to10 = dict()
    cpm_10to20 = dict()
    cpm_20to30 = dict()
    cpm_30toend = dict()
    gpm_0to10 = dict()
    gpm_10to20 = dict()
    gpm_20to30 = dict()
    gpm_30toend = dict()
    wards_placed = dict()
    wards_cleared = dict()
    damage_dealt = dict()
    damage_taken = dict()

    # Initialize Counting Variables
    count = 1
    num = 0

    # Make Initial API call
    api = RiotAPI('RANKED_SOLO_5x5', 0, 10, '82a7b066-b6f2-4e3f-8f15-9ee01aa68c22')
    r = api.get_match_history(summoner_id)

    for i in range(update):
        if 'Retry-After' in r:
            time.sleep(float(r['retry-after']))
            r = api.get_match_history(summoner_id)

        # Match Information
        match_id[i] = r['matches'][num]['matchId']
        season[i] = r['matches'][num]['season']
        match_length[i] = r['matches'][num]['matchDuration']
        result[i] = r['matches'][num]['participants'][0]['stats']['winner']

        # Champion Information
        champion_id = r['matches'][num]['participants'][0]['championId']
        lane = r['matches'][num]['participants'][0]['timeline']['lane']
        champ_type = r['matches'][num]['participants'][0]['timeline']['role']

        # Champion Stats
        kills[i] = r['matches'][num]['participants'][0]['stats']['kills']
        deaths[i] = r['matches'][num]['participants'][0]['stats']['deaths']
        assists[i] = r['matches'][num]['participants'][0]['stats']['assists']
        damage_dealt[i] = r['matches'][num]['participants'][0]['stats']['totalDamageDealtToChampions']
        damage_taken[i] = r['matches'][num]['participants'][0]['stats']['totalDamageTaken']
        cpm_0to10[i] = r['matches'][num]['participants'][0]['timeline']['creepsPerMinDeltas']['zeroToTen']
        gpm_0to10[i] = r['matches'][num]['participants'][0]['timeline']['goldPerMinDeltas']['zeroToTen']
        cpm[i] = (r['matches'][num]['participants'][0]['stats']['minionsKilled'] +
                  r['matches'][num]['participants'][0]['stats']['neutralMinionsKilled'])/(match_length[i]/60)
        gpm[i] = (r['matches'][num]['participants'][0]['stats']['goldEarned'])/(match_length[i]/60)

        if match_length[i] > 2100:
            cpm_10to20[i] = r['matches'][num]['participants'][0]['timeline']['creepsPerMinDeltas']['tenToTwenty']
            gpm_10to20[i] = r['matches'][num]['participants'][0]['timeline']['goldPerMinDeltas']['tenToTwenty']
            cpm_20to30[i] = r['matches'][num]['participants'][0]['timeline']['creepsPerMinDeltas']['twentyToThirty']
            cpm_30toend[i] = r['matches'][num]['participants'][0]['timeline']['creepsPerMinDeltas']['thirtyToEnd']
            gpm_20to30[i] = r['matches'][num]['participants'][0]['timeline']['goldPerMinDeltas']['twentyToThirty']
            gpm_30toend[i] = r['matches'][num]['participants'][0]['timeline']['goldPerMinDeltas']['thirtyToEnd']
        elif 1800 < match_length[i] <= 2100:
            cpm_10to20[i] = r['matches'][num]['participants'][0]['timeline']['creepsPerMinDeltas']['tenToTwenty']
            gpm_10to20[i] = r['matches'][num]['participants'][0]['timeline']['goldPerMinDeltas']['tenToTwenty']
            cpm_20to30[i] = r['matches'][num]['participants'][0]['timeline']['creepsPerMinDeltas']['twentyToThirty']
            gpm_20to30[i] = r['matches'][num]['participants'][0]['timeline']['goldPerMinDeltas']['twentyToThirty']
            cpm_30toend[i] = 0
            gpm_30toend[i] = 0
        elif 1200 < match_length[i] <= 1800:
            cpm_10to20[i] = r['matches'][num]['participants'][0]['timeline']['creepsPerMinDeltas']['tenToTwenty']
            gpm_10to20[i] = r['matches'][num]['participants'][0]['timeline']['goldPerMinDeltas']['tenToTwenty']
            cpm_20to30[i] = 0
            cpm_30toend[i] = 0
            gpm_20to30[i] = 0
            gpm_30toend[i] = 0
        else:
            cpm_10to20[i] = 0
            gpm_10to20[i] = 0
            cpm_20to30[i] = 0
            cpm_30toend[i] = 0
            gpm_20to30[i] = 0
            gpm_30toend[i] = 0

        wards_placed[i] = r['matches'][num]['participants'][0]['stats']['wardsPlaced']
        wards_cleared[i] = r['matches'][num]['participants'][0]['stats']['wardsKilled']

        # Calculations Based on Extracted Data
        champion[i] = Consts.CHAMP_ID[str(champion_id)]
        mins[i] = int(match_length[i]/60)
        secs[i] = (match_length[i]/60-int(match_length[i]/60))*60

        if deaths[i] == 0:
            kda[i] = kills[i]+assists[i]
        else:
            kda[i] = (kills[i]+assists[i])/deaths[i]

        # Assigning League Relevant Values Based on Extracted Data
        if result[i] is True:
            result[i] = 'Win'
        else:
            result[i] = 'Loss'

        # Assign Season Names for easy excel sorting
        if season[i] == 'SEASON2014':
            season[i] = '2014S'
        elif season[i] == 'PRESEASON2015':
            season[i] = '2015P'
        elif season[i] == 'SEASON2015':
            season[i] = '2015S'

        # Reassign Lane Names based on League Conventions
        if lane == ('BOT' or 'BOTTOM') and champ_type == 'DUO_CARRY':
            role[i] = 'ADC'
        elif lane == ('BOT' or 'BOTTOM') and champ_type == 'DUO_SUPPORT':
            role[i] = 'Support'
        else:
            role[i] = lane

        # Make additional necessary API Calls
        if num == 9:
            num = 0
            time.sleep(1)
            if i+10 >= update:
                api = RiotAPI('RANKED_SOLO_5x5', i, update, '82a7b066-b6f2-4e3f-8f15-9ee01aa68c22')
            else:
                api = RiotAPI('RANKED_SOLO_5x5', i, i+10, '82a7b066-b6f2-4e3f-8f15-9ee01aa68c22')
            r = api.get_match_history(summoner_id)
        else:
            num += 1

    # Write Values to csv file
    with open('UpdateSoloQLog.csv', 'w') as csv_file:
        fieldnames = ['Match_ID', 'Season', 'Length', 'Mins', 'Secs', 'Result', 'Role', 'Champion', 'Kills', 'Deaths',
                      'Assists', 'KDA', 'CS/min', 'GPM', 'Wards_Placed', 'Wards_Cleared', 'CS/min_0-10', 'CS/min_10-20',
                      'CS/min_20-30', 'CS/min_30+', 'GPM_0-10', 'GPM_10-20', 'GPM_20-30', 'GPM_30+',
                      'Damage Dealt', 'Damage Taken']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(ranked_games):
            print(i, '   ', match_id[i])
            writer.writerow({'Match_ID': match_id[i], 'Season': season[i], 'Length': match_length[i], 'Mins': mins[i],
                             'Secs': secs[i], 'Result': result[i], 'Role': role[i], 'Champion': champion[i],
                             'Kills': kills[i], 'Deaths': deaths[i], 'Assists': assists[i], 'KDA': kda[i],
                             'CS/min': cpm[i], 'GPM': gpm[i], 'Wards_Placed': wards_placed[i],
                             'Wards_Cleared': wards_cleared[i], 'CS/min_0-10': cpm_0to10[i],
                             'CS/min_10-20': cpm_10to20[i], 'CS/min_20-30': cpm_20to30[i], 'CS/min_30+': cpm_30toend[i],
                             'GPM_0-10': gpm_0to10[i], 'GPM_10-20': gpm_10to20[i], 'GPM_20-30': gpm_20to30[i],
                             'GPM_30+': gpm_30toend[i], 'Damage Dealt': damage_dealt[i],
                             'Damage Taken': damage_taken[i]})


if __name__ == "__main__":
    main()
