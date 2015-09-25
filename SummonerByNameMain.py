from RiotAPI import RiotAPI


def main():
    api = RiotAPI('', '', '', '82a7b066-b6f2-4e3f-8f15-9ee01aa68c22')
    r = api.get_summoner_by_name('ricofromjalisco')
    print(r['ricofromjalisco'])


if __name__ == "__main__":
    main()
