import requests
import RiotConsts as Consts
import time


class RiotAPI(object):

    def __init__(self, ranked_queues, begin_index, end_index, api_key, region=Consts.REGIONS['north_america']):
        self.rankedQueues = ranked_queues
        self.beginIndex = begin_index
        self.endIndex = end_index
        self.api_key = api_key
        self.region = region

    def _request(self, api_url, params={}):
        args = {'rankedQueues': self.rankedQueues, 'beginIndex': self.beginIndex, 'endIndex': self.endIndex,
                'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        response = requests.get(
            Consts.URL['base'].format(
                proxy=self.region,
                region=self.region,
                url=api_url
            ),
            params=args
        )
        if response.status_code != 200:
            print(response.status_code)
            if response.status_code == 429:
                print(response.headers)
                return response.headers
        else:
            return response.json()

    def get_summoner_by_name(self, name):
        api_url = Consts.URL['summoner_by_name'].format(
            version=Consts.API_VERSIONS['summoner'],
            names=name
        )
        return self._request(api_url)

    def get_match_history(self, id):
        api_url = Consts.URL['match_history'].format(
            version=Consts.API_VERSIONS['match_history'],
            summonerId=id
        )
        return self._request(api_url)

    def get_team_by_team_id(self, id):
        api_url = Consts.URL['team'].format(
            version=Consts.API_VERSIONS['team'],
            teamIDs=id
        )
        return self._request(api_url)

    def get_match_by_match_id(self, id):
        api_url = Consts.URL['match'].format(
            version=Consts.API_VERSIONS['match'],
            matchId=id
        )
        return self._request(api_url)

    def get_stats_by_summoner_id(self, id):
        api_url = Consts.URL['stats'].format(
            version=Consts.API_VERSIONS['stats'],
            summonerId=id
        )
        return self._request(api_url)

    def get_match_list(self, id):
        api_url = Consts.URL['match_list'].format(
            version=Consts.API_VERSIONS['match_list'],
            summonerId=id
        )
        return self._request(api_url)
