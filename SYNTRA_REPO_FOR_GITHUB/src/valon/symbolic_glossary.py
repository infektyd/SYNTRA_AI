def symbolic_meaning(term):
    glossary = {
        "gear": "transmission element that transfers power",
        "oil": "lubricant representing system health",
        "coolant": "temperature regulation symbol",
        "torque": "rotational force and mechanical intent"
    }
    return glossary.get(term.lower(), "symbol not yet defined")