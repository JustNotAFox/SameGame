import random
import datetime

def genetic(g):
    pop = []
    for i in range(20):
        heur = {}
        heur["heur"] = []
        for t in range(5):
            heur["heur"].append(random.random())
        pop.append(heur)
    for i in pop:
        i["fitness"] = solve(g,i["heur"])["score"]
    for i in range(100):
        pop = sorted(pop,key=lambda x:x["fitness"],reverse=True)
        x = random.randint(1,19)
        pop[x]["heur"] = mutate(pop[x]["heur"])
        pop[x]["fitness"] = solve(g,pop[x]["heur"])["score"]
        pop = sorted(pop,key=lambda x:x["fitness"],reverse=True)
        x = random.randint(1,19)
        y = random.randint(1,19)
        pop[x]["heur"] = breed(pop[y]["heur"],pop[0]["heur"])
        pop[x]["fitness"] = solve(g,pop[x]["heur"])["score"]
    return pop

def mutate(h):
    h[random.randint(0,4)] = random.random()
    return h

def breed(h,h2):
    r = []
    for i in range(5):
        x = random.randint(1,4)
        if x == 1:
            r.append(h[i])
            continue
        if x == 2:
            r.append(h2[i])
            continue
        if x == 3:
            r.append((h[i] + h2[i]) / 2)
            continue
        if x == 4:
            r.append(random.random())
            continue
    return r

def woc(g,h):
    score = 0
    while listMoves(g):
        m = []
        for heur in h:
            m.append(getMove(g,heur))
        n = [i["spaces"][0] for i in m]
        o = set(n)
        while len(n) > len(o):
            n = [i for i in n if not i in o or o.remove(i)]
            o = set(n)
        n = n[0]
        m = [i for i in m if i["spaces"][0] == n][0]
        score += m["score"]
        g = m["after"]
    return score


def getMove(g, h):
    m = listMoves(g)
    im = []
    for move in m:
        a = {"spaces": move, "after": postMove(g.copy(), move)}
        a["score"] = (len(a["spaces"]) - 2) ** 2
        a["aftermoves"] = listMoves(a["after"])
        total = 0
        for group in a["aftermoves"]:
            total += (len(group) - 2) ** 2
        a["aftertotal"] = total
        total = 0
        for i in range(3):
            total += (sum(1 for col in a["after"].values() if col == i + 1) - 2) ** 2
        a["maxtotal"] = total
        score = 0
        score += h[0] * a["score"]
        score += h[1] * len(a["aftermoves"])
        score += h[2] * a["aftertotal"]
        score += h[3] * a["maxtotal"]
        if a["aftermoves"]:
            score += h[4] * a["aftertotal"] / len(a["aftermoves"])
        a["hscore"] = score
        im.append(a)
    return max(im, key=lambda t:t["hscore"])

def checkMove(g, c, x, y):
    m = [(x, y)]
    if x > 0:
        if (x - 1, y) not in c and g[x,y] == g[x-1,y]:
            c.append((x - 1, y))
            m.extend(checkMove(g,c,x - 1,y))
    if y > 0:
        if (x, y - 1) not in c and g[x,y] == g[x,y - 1]:
            c.append((x, y - 1))
            m.extend(checkMove(g,c,x,y - 1))
    if x < 15:
        if (x + 1, y) not in c and g[x,y] == g[x+1,y]:
            c.append((x + 1, y))
            m.extend(checkMove(g,c,x+1,y))
    if y < 11:
        if (x, y + 1) not in c and g[x,y] == g[x,y + 1]:
            c.append((x, y + 1))
            m.extend(checkMove(g,c,x,y + 1))
    return m

def postMove(g,m):
    outx = 0
    outy = 0
    for x in range(16):
        for y in range(12):
            if (x,y) not in m:
                g[(outx,outy)] = g[(x,y)]
                outy += 1
        if outy > 0:
            for z in range(outy,12):
                g[(outx,z)] = 0
            outy = 0
            outx += 1
    for x in range(outx,16):
        for y in range(12):
            g[x,y] = 0
    return g

def listMoves(g):
    checked = []
    moves = []
    for x in range(16):
        if g[x,0] == 0:
            break
        for y in range(12):
            if g[x, y] == 0:
                break
            if (x, y) not in checked:
                checked.append((x,y))
                moves.append(checkMove(g,checked,x,y))
    return [move for move in moves if len(move) > 1]

def genBoard(x,y):
    g = {}
    for x in range(16):
        for y in range(12):
            g[x,y] = random.randint(1,3)
    return g

def solve(g,h):
    r = {}
    r["score"] = 0
    r["moves"] = []
    while(listMoves(g)):
        a = getMove(g,h)
        r["score"] += a["score"]
        r["moves"].append(a["spaces"])
        g = a["after"]
    return r

f = open('out.csv', 'a')
f.write("Run,Greedy (Move Score),Greedy (Move Score + Potential Move Score),Best,Worst,Time,WOC,WOC Time\n")
f.close()
c = 1
while True:
    print(c)
    g = genBoard(1,1)
    f = open('out.csv', 'a')
    f.write(str(c) + ',')
    s = solve(g,[1,0,0,0,0])
    s2 = solve(g,[1,0,1,0,0])
    f.write(str(s["score"]) + ',' + str(s2["score"]))
    time = datetime.datetime.now()
    i = genetic(g)
    f.write(str(i[0]["fitness"]) + ',' + str(i[len(i) - 1]["fitness"]) + ',' + str(datetime.datetime.now() - time) + ',')
    time = datetime.datetime.now()
    i = sorted(i,key=lambda x:x["fitness"],reverse=True)
    t = woc(g, [t["heur"] for t in i[:5]])
    f.write(str(t) + ',' + str(datetime.datetime.now() - time) + '\n')
    f.close()
    c += 1
