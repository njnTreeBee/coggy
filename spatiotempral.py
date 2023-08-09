import numpy as np

class RCC8:
    def __init__(self):
        self.constraints = []

    def add_constraint(self, i, j, relation):
        self.constraints.append((i, j, relation))

    def reason(self):
        network = [[set() for _ in range(len(self.constraints))] for _ in range(len(self.constraints))]
        for i, j, relation in self.constraints:
            network[i][j].add(relation)
        for i in range(len(network)):
            for j in range(len(network)):
                if i != j:
                    for k in range(len(network)):
                        if i != k and j != k:
                            network[i][j] = self.path_consistency(network[i][k], network[k][j])
        return network

    def path_consistency(self, relations1, relations2):
        result = set()
        for r1 in relations1:
            for r2 in relations2:
                composition = self.compose(r1, r2)
                if composition:
                    result.add(composition)
        return result

    def compose(self, r1, r2):
        compositions = {
("before", "before"): {"before"},
("before", "meets"): {"meets"},
("before", "overlaps"): {"overlaps"},
("before", "during"): {"during"},
("before", "starts"): {"starts"},
("before", "equals"): {"equals"},
("before", "finishes"): {"finishes"},
("before", "overlapped-by"): {"overlaps"},
("before", "met-by"): {"meets"},
("before", "after"): {"before"},
("before", "started-by"): {"starts"},
("before", "during-inverse"): {"during"},
("before", "finished-by"): {"finishes"},
("meets", "before"): {"before"},
("meets", "meets"): {"meets"},
("meets", "overlaps"): {"overlaps"},
("meets", "during"): {"during"},
("meets", "starts"): {"starts"},
("meets", "equals"): {"equals"},
("meets", "finishes"): {"finishes"},
("meets", "overlapped-by"): {"overlapped-by"},
("meets", "met-by"): {"before"},
("meets", "after"): {"before"},
("meets", "started-by"): {"starts"},
("meets", "during-inverse"): {"during"},
("meets", "finished-by"): {"finishes
("overlaps", "before"): {"before"},
("overlaps", "meets"): {"meets"},
("overlaps", "overlaps"): {"overlaps"},
("overlaps", "during"): {"during"},
("overlaps", "starts"): {"starts"},
("overlaps", "equals"): {"equals"},
("overlaps", "finishes"): {"during"},
("overlaps", "overlapped-by"): {"overlapped-by"},
("overlaps", "met-by"): {"met-by"},
("overlaps", "after"): {"before"},
("overlaps", "started-by"): {"starts"},
("overlaps", "during-inverse"): {"during"},
("overlaps", "finished-by"): {"during-inverse"},
("during", "before"): {"before"},
("during", "meets"): {"meets"},
("during", "overlaps"): {"overlaps"},
("during", "during"): {"during"},
("during", "starts"): {"starts"},
("during", "equals"): {"equals"},
("during", "finishes"): {"finishes"},
("during", "overlapped-by"): {"overlapped-by"},
("during", "met-by"): {"met-by"},
("during", "after"): {"before"},
("during", "started-by"): {"starts"},
("during", "during-inverse"): {"during"},
("during", "finished-by"): {"finishes"},
("starts", "before"): {"before"},
("starts", "meets"): {"meets"},
("starts", "overlaps"): {"overlaps"},
("starts", "during"): {"during"},
("starts", "starts"): {"starts"},
("starts", "equals"): {"equals"},
("starts", "finishes"): {"during"},
("starts", "overlapped-by"): {"overlapped-by"},
("starts", "met-by"): {"met-by"},
("starts", "after"): {"before"},
("starts", "started-by"): {"starts"},
("starts", "during-inverse"): {"during"},
("starts", "finished-by"): {"during-inverse"},
("equals", "before"): {"before"},
("equals", "meets"): {"meets"},
("equals", "overlaps"): {"overlaps"},
("equals", "during"): {"during"},
("equals", "starts"): {"starts"},
("equals", "equals"): {"equals"},
("equals", "finishes"): {"finishes"},
("equals", "overlapped-by"): {"overlapped-by"},
("equals", "met-by"): {"met-by"},
("equals", "after"): {"before"},
("equals", "started-by"): {"starts"},
("equals", "during-inverse"): {"during"},
("equals", "finished-by"): {"finishes"},
("finishes", "before"): {"before"},
("finishes", "meets"): {"meets"},
("finishes", "overlaps"): {"overlaps"},
("finishes", "during"): {"during"},
("finishes", "starts"): {"starts"},
("finishes", "equals"): {"equals"},
("finishes", "finishes"): {"finishes"},
("finishes", "overlapped-by"): {"overlapped-by"},
("finishes", "met-by"): {"met-by"},
("finishes", "after"): {"before"},
("finishes", "started-by"): {"starts"},
("finishes", "during-inverse"): {"during"},
("finishes", "finished-by"): {"finishes"},
("overlapped-by", "before"): {"after"},
("overlapped-by", "meets"): {"after"},
("overlapped-by", "overlaps"): {"overlapped-by"},
("overlapped-by", "during"): {"during-inverse"},
("overlapped-by", "starts"): {"finished-by"},
("overlapped-by", "equals"): {"equals"},
("overlapped-by", "finishes"): {"finishes"},
("overlapped-by", "overlapped-by"): {"overlapped-by"},
("overlapped-by", "met-by"): {"met-by"},
("overlapped-by", "after"): {"after"},
("overlapped-by", "started-by"): {"finished-by"},
("overlapped-by", "during-inverse"): {"during-inverse"},
("overlapped-by", "finished-by"): {"finished-by"},
("met-by", "before"): {"after"},
("met-by", "meets"): {"after"},
("met-by", "overlaps"): {"overlapped-by"},
("met-by", "during"): {"during-inverse"},
("met-by", "starts"): {"finished-by"},
("met-by", "equals"): {"equals"},
("met-by", "finishes"): {"finishes"},
("met-by", "overlapped-by"): {"overlapped-by"},
("met-by", "met-by"): {"after"},
("met-by", "after"): {"after"},
("met-by", "started-by"): {"finished-by"},
("met-by", "during-inverse"): {"during-inverse"},
("met-by", "finished-by"): {"finished-by"},
("after", "before"): {"after"},
("after", "meets"): {"after"},
("after", "overlaps"): {"after"},
("after", "during"): {"after"},
("after", "starts"): {"after"},
("after", "equals"): {"after"},
("after", "finishes"): {"after"},
("after", "overlapped-by"): {"after"},
("after", "met-by"): {"after"},
("after", "after"): {"after"},
("after", "started-by"): {"after"},
("after", "during-inverse"): {"after"},
("after", "finished-by"): {"after"},
("started-by", "before"): {"after"},
("started-by", "meets"): {"after"},
("started-by", "overlaps"): {"overlapped-by"},
("started-by", "during"): {"during-inverse"},
("started-by", "starts"): {"equals"},
("started-by", "equals"): {"equals"},
("started-by", "finishes"): {"finishes"},
("started-by", "overlapped-by"): {"overlapped-by"},
("started-by", "met-by"): {"met-by"},
("started-by", "after"): {"after"},
("started-by", "started-by"): {"equals"},
("started-by", "during-inverse"): {"during-inverse"},
("started-by", "finished-by"): {"finishes"},
("during-inverse", "before"): {"after"},
("during-inverse", "meets"): {"after"},
("during-inverse", "overlaps"): {"overlapped-by"},
("during-inverse", "during"): {"during-inverse"},
("during-inverse", "starts"): {"finished-by"},
("during-inverse", "equals"): {"equals"},
("during-inverse", "finishes"): {"finishes"},
("during-inverse", "overlapped-by"): {"overlapped-by"},
("during-inverse", "met-by"): {"met-by"},
("during-inverse", "after"): {"after"},
("during-inverse", "started-by"): {"finished-by"},
("during-inverse", "during-inverse"): {"during-inverse"},
("during-inverse", "finished-by"): {"finishes"},
("finished-by", "before"): {"after"},
("finished-by", "meets"): {"after"},
("finished-by", "overlaps"): {"overlapped-by"},
("finished-by", "during"): {"during-inverse"},
("finished-by", "starts"): {"equals"},
("finished-by", "equals"): {"equals"},
("finished-by", "finishes"): {"finishes"},
("finished-by", "overlapped-by"): {"overlapped-by"},
("finished-by", "met-by"): {"met-by"},
("finished-by", "after"): {"after"},
("finished-by", "started-by"): {"equals"},
("finished-by", "during-inverse"): {"during-inverse"},
("finished-by", "finished-by"): {"finishes"},
}
        return compositions.get((r1, r2))

class STCC:
    def __init__(self):
        self.constraints = []

    def add_constraint(self, i, j, relation):
        self.constraints.append((i, j, relation))

    def reason(self):
        network = [[set() for _ in range(len(self.constraints))] for _ in range(len(self.constraints))]
        for i, j, relation in self.constraints:
            network[i][j].add(relation)
        for i in range(len(network)):
            for j in range(len(network)):
                if i != j:
                    for k in range(len(network)):
                        if i != k and j != k:
                            network[i][j] = self.path_consistency(network[i][k], network[k][j])
        return network

    def path_consistency(self, relations1, relations2):
        result = set()
        for r1 in relations1:
            for r2 in relations2:
                composition = self.compose(r1, r2)
                if composition:
                    result.add(composition)
        return result

    def compose(self, r1, r2):
        compositions = {
("before", "before"): {"before"},
("before", "meets"): {"meets"},
("before", "overlaps"): {"overlaps"},
("before", "during"): {"during"},
("before", "starts"): {"starts"},
("before", "equals"): {"equals"},
("before", "finishes"): {"finishes"},
("before", "overlapped-by"): {"overlaps"},
("before", "met-by"): {"meets"},
("before", "after"): {"before"},
("before", "started-by"): {"starts"},
("before", "during-inverse"): {"during"},
("before", "finished-by"): {"finishes"},
("meets", "before"): {"before"},
("meets", "meets"): {"meets"},
("meets", "overlaps"): {"overlaps"},
("meets", "during"): {"during"},
("meets", "starts"): {"starts"},
("meets", "equals"): {"equals"},
("meets", "finishes"): {"finishes"},
("meets", "overlapped-by"): {"overlapped-by"},
("meets", "met-by"): {"before"},
("meets", "after"): {"before"},
("meets", "started-by"): {"starts"},
("meets", "during-inverse"): {"during"},
("meets", "finished-by"): {"finishes
("overlaps", "before"): {"before"},
("overlaps", "meets"): {"meets"},
("overlaps", "overlaps"): {"overlaps"},
("overlaps", "during"): {"during"},
("overlaps", "starts"): {"starts"},
("overlaps", "equals"): {"equals"},
("overlaps", "finishes"): {"during"},
("overlaps", "overlapped-by"): {"overlapped-by"},
("overlaps", "met-by"): {"met-by"},
("overlaps", "after"): {"before"},
("overlaps", "started-by"): {"starts"},
("overlaps", "during-inverse"): {"during"},
("overlaps", "finished-by"): {"during-inverse"},
("during", "before"): {"before"},
("during", "meets"): {"meets"},
("during", "overlaps"): {"overlaps"},
("during", "during"): {"during"},
("during", "starts"): {"starts"},
("during", "equals"): {"equals"},
("during", "finishes"): {"finishes"},
("during", "overlapped-by"): {"overlapped-by"},
("during", "met-by"): {"met-by"},
("during", "after"): {"before"},
("during", "started-by"): {"starts"},
("during", "during-inverse"): {"during"},
("during", "finished-by"): {"finishes"},
("starts", "before"): {"before"},
("starts", "meets"): {"meets"},
("starts", "overlaps"): {"overlaps"},
("starts", "during"): {"during"},
("starts", "starts"): {"starts"},
("starts", "equals"): {"equals"},
("starts", "finishes"): {"during"},
("starts", "overlapped-by"): {"overlapped-by"},
("starts", "met-by"): {"met-by"},
("starts", "after"): {"before"},
("starts", "started-by"): {"starts"},
("starts", "during-inverse"): {"during"},
("starts", "finished-by"): {"during-inverse"},
("equals", "before"): {"before"},
("equals", "meets"): {"meets"},
("equals", "overlaps"): {"overlaps"},
("equals", "during"): {"during"},
("equals", "starts"): {"starts"},
("equals", "equals"): {"equals"},
("equals", "finishes"): {"finishes"},
("equals", "overlapped-by"): {"overlapped-by"},
("equals", "met-by"): {"met-by"},
("equals", "after"): {"before"},
("equals", "started-by"): {"starts"},
("equals", "during-inverse"): {"during"},
("equals", "finished-by"): {"finishes"},
("finishes", "before"): {"before"},
("finishes", "meets"): {"meets"},
("finishes", "overlaps"): {"overlaps"},
("finishes", "during"): {"during"},
("finishes", "starts"): {"starts"},
("finishes", "equals"): {"equals"},
("finishes", "finishes"): {"finishes"},
("finishes", "overlapped-by"): {"overlapped-by"},
("finishes", "met-by"): {"met-by"},
("finishes", "after"): {"before"},
("finishes", "started-by"): {"starts"},
("finishes", "during-inverse"): {"during"},
("finishes", "finished-by"): {"finishes"},
("overlapped-by", "before"): {"after"},
("overlapped-by", "meets"): {"after"},
("overlapped-by", "overlaps"): {"overlapped-by"},
("overlapped-by", "during"): {"during-inverse"},
("overlapped-by", "starts"): {"finished-by"},
("overlapped-by", "equals"): {"equals"},
("overlapped-by", "finishes"): {"finishes"},
("overlapped-by", "overlapped-by"): {"overlapped-by"},
("overlapped-by", "met-by"): {"met-by"},
("overlapped-by", "after"): {"after"},
("overlapped-by", "started-by"): {"finished-by"},
("overlapped-by", "during-inverse"): {"during-inverse"},
("overlapped-by", "finished-by"): {"finished-by"},
("met-by", "before"): {"after"},
("met-by", "meets"): {"after"},
("met-by", "overlaps"): {"overlapped-by"},
("met-by", "during"): {"during-inverse"},
("met-by", "starts"): {"finished-by"},
("met-by", "equals"): {"equals"},
("met-by", "finishes"): {"finishes"},
("met-by", "overlapped-by"): {"overlapped-by"},
("met-by", "met-by"): {"after"},
("met-by", "after"): {"after"},
("met-by", "started-by"): {"finished-by"},
("met-by", "during-inverse"): {"during-inverse"},
("met-by", "finished-by"): {"finished-by"},
("after", "before"): {"after"},
("after", "meets"): {"after"},
("after", "overlaps"): {"after"},
("after", "during"): {"after"},
("after", "starts"): {"after"},
("after", "equals"): {"after"},
("after", "finishes"): {"after"},
("after", "overlapped-by"): {"after"},
("after", "met-by"): {"after"},
("after", "after"): {"after"},
("after", "started-by"): {"after"},
("after", "during-inverse"): {"after"},
("after", "finished-by"): {"after"},
("started-by", "before"): {"after"},
("started-by", "meets"): {"after"},
("started-by", "overlaps"): {"overlapped-by"},
("started-by", "during"): {"during-inverse"},
("started-by", "starts"): {"equals"},
("started-by", "equals"): {"equals"},
("started-by", "finishes"): {"finishes"},
("started-by", "overlapped-by"): {"overlapped-by"},
("started-by", "met-by"): {"met-by"},
("started-by", "after"): {"after"},
("started-by", "started-by"): {"equals"},
("started-by", "during-inverse"): {"during-inverse"},
("started-by", "finished-by"): {"finishes"},
("during-inverse", "before"): {"after"},
("during-inverse", "meets"): {"after"},
("during-inverse", "overlaps"): {"overlapped-by"},
("during-inverse", "during"): {"during-inverse"},
("during-inverse", "starts"): {"finished-by"},
("during-inverse", "equals"): {"equals"},
("during-inverse", "finishes"): {"finishes"},
("during-inverse", "overlapped-by"): {"overlapped-by"},
("during-inverse", "met-by"): {"met-by"},
("during-inverse", "after"): {"after"},
("during-inverse", "started-by"): {"finished-by"},
("during-inverse", "during-inverse"): {"during-inverse"},
("during-inverse", "finished-by"): {"finishes"},
("finished-by", "before"): {"after"},
("finished-by", "meets"): {"after"},
("finished-by", "overlaps"): {"overlapped-by"},
("finished-by", "during"): {"during-inverse"},
("finished-by", "starts"): {"equals"},
("finished-by", "equals"): {"equals"},
("finished-by", "finishes"): {"finishes"},
("finished-by", "overlapped-by"): {"overlapped-by"},
("finished-by", "met-by"): {"met-by"},
("finished-by", "after"): {"after"},
("finished-by", "started-by"): {"equals"},
("finished-by", "during-inverse"): {"during-inverse"},
("finished-by", "finished-by"): {"finishes"},
}
        return compositions.get((r1, r2))

def main():
    calculus = RCC8()
    calculus.add_constraint(0, 1, "before")
    calculus.add_constraint(1, 2, "before")
    network = calculus.reason()
    for row in network:
        print(row)

if __name__ == "__main__":
    main()
