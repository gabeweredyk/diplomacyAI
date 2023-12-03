territories = ['nao', 'nwg', 'bar', 'cly', 'lvp', 'edi', 'yor', 'wal', 'iri', 'mao', 'eng', 'lon', 'nth', 'nwy', 'stp', 'fin', 'swe', 'ska', 'bot', 'den', 'lvn', 'bal', 'hel', 'bre', 'pic', 'bel', 'hol', 'kie', 'par', 'bur', 'ruh', 'ber', 'pru', 'mos', 'war', 'ukr', 'sev', 'mun', 'sil', 'gas', 'spa', 'por', 'mar', 'pie', 'tyr', 'boh', 'gal', 'vie', 'tri', 'ven', 'lyo', 'tus', 'wes', 'naf', 'tun', 'tys', 'rom', 'nap', 'apu', 'adr', 'alb', 'bud', 'ser', 'gre', 'rum', 'bla', 'ank', 'arm', 'syr', 'eas', 'ion', 'bul', 'con', 'aeg', 'smy']

f = open("neighbors.txt")
neighbors = {}
for i in territories:
    neighbors[i] = []

neigh = f.read().split("\n")
for i in neigh:
    arr = i.split(",")
    neighbors[arr[0]].append(arr[1])
territories.sort()
print(territories)


['adr', 'aeg', 'alb', 'ank', 'apu', 'arm', 'bal', 'bar', 'bel', 'ber', 'bla', 'boh', 'bot', 'bre', 'bud', 'bul', 'bur', 'cly', 'con', 'den', 'eas', 'edi', 'eng', 'fin', 'gal', 'gas', 'gre', 'hel', 'hol', 'ion', 'iri', 'kie', 'lon', 'lvn', 'lvp', 'lyo', 'mao', 'mar', 'mos', 'mun', 'naf', 'nao', 'nap', 'nth', 'nwg', 'nwy', 'par', 'pic', 'pie', 'por', 'pru', 'rom', 'ruh', 'rum', 'ser', 'sev', 'sil', 'ska', 'smy', 'spa', 'stp', 'swe', 'syr', 'tri', 'tun', 'tus', 'tyr', 'tys', 'ukr', 'ven', 'vie', 'wal', 'war', 'wes', 'yor']