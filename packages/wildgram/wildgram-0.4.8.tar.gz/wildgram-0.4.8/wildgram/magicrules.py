from wildgram import wildgram
import connect_umls as um
import itertools
import numpy as np
def getSubset(tokens, i, startOffset, endOffset):
    start = i+startOffset
    end = i+endOffset
    if start < 0:
        start = 0
    if end > len(tokens):
        end =len(tokens)
    subset = tokens[start:i]
    if i != len(tokens)-1:
        subset = subset + tokens[i+1:end]
    return subset

class MagicRules:
    def __init__(self):
        self.W = {}
        self.Triggers = {}
    def add_umls_cui(self, cui_code, apikey):
        umls = um.UMLS(apikey)
        cui = um.CUI(apikey, cui_code, "")
        triggers = cui.synonyms()
        for trigger in triggers:
            self.add_trigger(trigger, "UMLS", cui_code)

    def add_trigger(self, trigger, unit, value):
        code = unit +"|||"+value
        tokens = wildgram(trigger, returnNoise=False)
        for token in tokens:
            tok = token["token"]
            self.W[tok] = 5
            self.Triggers[tok] = {}
            self.Triggers[tok][code] = {}
            self.Triggers[tok][code][tok] = 5
            continue
        combos = itertools.combinations(tokens, 2)
        for combo in combos:
            self.Triggers[combo[0]["token"]][code][combo[1]["token"]] = 5
            self.Triggers[combo[1]["token"]][code][combo[0]["token"]] = 5

    def predict(self, text):
        tokens = wildgram(text, returnNoise=False)
        assignments = {}
        for i in range(len(tokens)):
            snippet = tokens[i]["token"]
            if snippet in self.Triggers:
                ## nearby:
                subset = getSubset(tokens, i, -10, 10)
                sums = {}
                for code in self.Triggers[snippet]:
                    sums[code] = {}
                    sums[code]["total"] = 0
                    sums[code]["num"] = 0
                for token in subset:
                    for code in self.Triggers[snippet]:
                        if token["token"] in self.Triggers[snippet][code]:
                            sums[code]["num"] = sums[code]["num"] +self.Triggers[snippet][code][token["token"]]
                            sums[code]["total"] = sums[code]["total"] +np.abs(self.Triggers[snippet][code][token["token"]])
                for code in self.Triggers[snippet]:
                    base = self.Triggers[snippet][code][snippet]/self.W[snippet]
                    givens = 0
                    if sums[code]["total"] >= 5:
                        givens = sums[code]["num"]/sums[code]["total"]
                    probability = base + givens
                    if probability > 0.8:
                        if code not in assignments:
                            assignments[code] = []
                        assignments[code].append(i)
        ret = []
        for code in assignments:
            bud = [0,0]
            prevIndex = -1
            for index in sorted(assignments[code]):
                if index == prevIndex + 1:
                    bud[1] = tokens[index]["endIndex"]
                    prevIndex = index
                    continue
                if index != prevIndex + 1:
                    if bud != [0,0]:
                        ret.append({"unit":code.split("|||")[0], "value":code.split("|||")[1], "startIndex": bud[0], "endIndex": bud[1], "snippet": text[bud[0]:bud[1]]})
                    prevIndex = index
                    bud = [tokens[index]["startIndex"],tokens[index]["endIndex"]]
            if bud != [0,0]:
                ret.append({"unit":code.split("|||")[0], "value":code.split("|||")[1], "startIndex": bud[0], "endIndex": bud[1], "snippet": text[bud[0]:bud[1]]})
        return ret

    def map_text(self, text, assignments, key="codes"):
        tokens = wildgram(text, returnNoise=False)
        for i in range(len(tokens)):
            tokens[i][key] = []
            for j in range(len(assignments)):
                ## only assign if the token fits into or is equal to the assignment
                if tokens[i]["startIndex"] < assignments[j]["startIndex"]:
                    continue
                if tokens[i]["endIndex"] > assignments[j]["endIndex"]:
                    continue
                tokens[i][key].append(j)
        return tokens

    def update_trigger(self, tokens, i, code, modifier=1):
        snippet = tokens[i]["token"]
        if snippet not in self.Triggers:
            self.Triggers[snippet] = {}
        if code not in self.Triggers[snippet]:
            self.Triggers[snippet][code] = {}
        if snippet not in self.Triggers[snippet][code]:
            self.Triggers[snippet][code][snippet] = 0
        self.Triggers[snippet][code][snippet] = self.Triggers[snippet][code][snippet] + modifier
        subset = getSubset(tokens, i, -10, 10)
        for token in subset:
            if token["token"] not in self.Triggers[snippet][code]:
                self.Triggers[snippet][code][token["token"]] = 0
            self.Triggers[snippet][code][token["token"]] = self.Triggers[snippet][code][token["token"]] + modifier


    def train_one_document(self, text, correct):
        predicted = self.predict(text)
        predicted_tokens = self.map_text(text, predicted, "prediction")
        correct_tokens = self.map_text(text, correct, "correct")
        for i in range(len(correct_tokens)):
            if correct_tokens[i]["token"] not in self.W:
                self.W[correct_tokens[i]["token"]] = 0
            self.W[correct_tokens[i]["token"]] = self.W[correct_tokens[i]["token"]] +1
            ## tp, fn, we do the same thing..
            for index in correct_tokens[i]["correct"]:
                code = correct[index]["unit"] + "|||" + correct[index]["value"]
                self.update_trigger(correct_tokens, i, code)
            ## fp
            for index in predicted_tokens[i]["prediction"]:
                code = predicted[index]["unit"] + "|||" + predicted[index]["value"]
                found = False
                for ind in correct_tokens[i]["correct"]:
                    if predicted[index]["unit"] != correct[ind]["unit"]:
                        continue
                    if predicted[index]["value"] != correct[ind]["value"]:
                        continue
                    found = True
                if not found:
                    self.update_trigger(correct_tokens,i,code, -2)
