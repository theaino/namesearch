import sources


query = input("Search: ").lower().strip()

data = {}
namemap = {}

for source in sources.SOURCES:
    print(f"Fetching {source.name}...")
    source_data = source.fetch()
    for year in source_data.keys():
        if year not in data:
            data[year] = []
        year_data = source_data[year]
        for name in year_data:
            name_key = (year, name.name, name.gender)
            if name_key in namemap.keys():
                namemap[name_key].count += name.count
                continue
            data[year].append(name)
            namemap[name_key] = data[year][-1]
    print(f"Fetched {source.name}")


for year in data.keys():
    boys_key = (year, query, "M")
    girls_key = (year, query, "F")

    boys_count = 0
    boys_name = namemap.get(boys_key)
    if boys_name:
        boys_count = boys_name.count
    girls_count = 0
    girls_name = namemap.get(girls_key)
    if girls_name:
        girls_count = girls_name.count

    print(year)
    print(f"\tM: {boys_count}")
    print(f"\tF: {girls_count}")
