import math



def shannon_entropy(string):
    """
    Calculates the Shannon entropy for the given  string.
    :param string: String to parse.
    :type string: str
    :returns: Shannon entropy (min bits per byte-character).
    :rtype: float
    """
    "Calculates the Shannon entropy of a string"

    # get probability of chars in string
    prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]

    # calculate the entropy
    entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])
    return entropy


def shannon_entropy_probability_list(list):
    """
    Calculates the Shannon entropy for the given probability distribution.
    :param list: A list that contaion proablity distrubutin .
    :type list: str
    :returns: Shannon entropy for the given probability distribution.
    :rtype: float
    """
    ent=0.0
    for prob in list:
        if (prob<0 or prob > 1):
            if(prob<0):
               raise Exception("Probability cannot be negative.Check the value",prob)
            else:
             raise Exception("Probability cannot be greater than one.Check the value",prob)   
        ent=ent+prob * (math.log((1/prob),2))
    return ent