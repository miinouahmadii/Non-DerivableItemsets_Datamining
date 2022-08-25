from os import sys

def get_sup(itemset: set, itemsets: dict):
    if len(itemset) == 0:
        return itemsets['-1']
    for x, sup in itemsets.items():
        if set(x.split(' ')) == itemset:
            return sup

def der_nonder(itemset: set, itemsets: dict):

    min_upper_bound = float('INF')
    max_lower_bound = float('-INF')

    Y = [{i for i,s in zip(itemset, status) if int(s)} for status in [(format(bit,'b').zfill(len(itemset))) for bit in range(2**len(itemset)-1)]]

    for y in Y:
        W = [{i for i,s in zip(itemset - y, status) if int(s)} for status in [(format(bit,'b').zfill(len(itemset - y))) for bit in range(2**len(itemset - y)-1)]]
        bound = 0
        for w in W:
            w.update(y)
            bound += (-1)**(len(itemset)-len(w)+1)*get_sup(w, itemsets)

        if (len(itemset)-len(y)) % 2 == 0:
            max_lower_bound = max(bound, max_lower_bound)
        else:
            min_upper_bound = min(bound, min_upper_bound)

    return [max_lower_bound, min_upper_bound, min_upper_bound == max_lower_bound]

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Bad Call")
        exit(-1)

    itemsets_path   =   sys.argv[1]
    ndi_path        =   sys.argv[2]

    itemsets_file = open(itemsets_path)
    itemsets = itemsets_file.readlines()
    itemsets = {row.split(' - ')[0]: int(row.strip('\n').split(' - ')[1]) for row in itemsets}
    itemsets_file.close()

    ndi_file = open(ndi_path)
    ndi = ndi_file.readlines()
    ndi = [row.strip('\n') for row in ndi]
    ndi_file.close()

    ans = [der_nonder(set(itemset.split(' ')), itemsets) for itemset in ndi]

    for row in ans:
        print('[' + str(row[0]) + ', ' + str(row[1]) + ']', 'derivable' if row[2] is True else 'non-derivable')