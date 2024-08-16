import sources


query = input("Search: ")
search_name = query.strip().lower()

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


import matplotlib.pyplot as plt

x = data.keys()
y_boys = []
y_girls = []

for year in x:
    boys_key = (year, search_name, "M")
    girls_key = (year, search_name, "F")

    boys_count = 0
    boys_name = namemap.get(boys_key)
    if boys_name:
        boys_count = boys_name.count
    girls_count = 0
    girls_name = namemap.get(girls_key)
    if girls_name:
        girls_count = girls_name.count

    y_boys.append(boys_count)
    y_girls.append(girls_count)

plt.title(query)
line_boys, = plt.plot(x, y_boys, color="blue")
line_boys.set_label("M")
line_girls, = plt.plot(x, y_girls, color="red")
line_girls.set_label("F")
plt.legend()
plt.xlabel("Year")
plt.ylabel("Birth count")
#plt.axvline(1977)
plt.show()
