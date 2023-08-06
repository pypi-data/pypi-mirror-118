
WORDNET_LEXNAMES_TO_DEFINITIONS = {
    "adj.all": "all adjective clusters",
    "adj.pert": "relational adjectives (pertainyms)",
    "adv.all": "all adverbs",
    "noun.Tops": "unique beginner for nouns",
    "noun.act": "nouns denoting acts or actions",
    "noun.animal": "nouns denoting animals",
    "noun.artifact": "nouns denoting man-made objects",
    "noun.attribute": "nouns denoting attributes of people and objects",
    "noun.body": "nouns denoting body parts",
    "noun.cognition": "nouns denoting cognitive processes and contents",
    "noun.communication": "nouns denoting communicative processes and contents",
    "noun.event": "nouns denoting natural events",
    "noun.feeling": "nouns denoting feelings and emotions",
    "noun.food": "nouns denoting foods and drinks",
    "noun.group": "nouns denoting groupings of people or objects",
    "noun.location": "nouns denoting spatial position",
    "noun.motive": "nouns denoting goals",
    "noun.object": "nouns denoting natural objects (not man-made)",
    "noun.person": "nouns denoting people",
    "noun.phenomenon": "nouns denoting natural phenomena",
    "noun.plant": "nouns denoting plants",
    "noun.possession": "nouns denoting possession and transfer of possession",
    "noun.process": "nouns denoting natural processes",
    "noun.quantity": "nouns denoting quantities and units of measure",
    "noun.relation": "nouns denoting relations between people or things or ideas",
    "noun.shape": "nouns denoting two and three dimensional shapes",
    "noun.state": "nouns denoting stable states of affairs",
    "noun.substance": "nouns denoting substances",
    "noun.time": "nouns denoting time and temporal relations",
    "verb.body": "verbs of grooming, dressing and bodily care",
    "verb.change": "verbs of size, temperature change, intensifying, etc.",
    "verb.cognition": "verbs of thinking, judging, analyzing, doubting",
    "verb.communication": "verbs of telling, asking, ordering, singing",
    "verb.competition": "verbs of fighting, athletic activities",
    "verb.consumption": "verbs of eating and drinking",
    "verb.contact": "verbs of touching, hitting, tying, digging",
    "verb.creation": "verbs of sewing, baking, painting, performing",
    "verb.emotion": "verbs of feeling",
    "verb.motion": "verbs of walking, flying, swimming",
    "verb.perception": "verbs of seeing, hearing, feeling",
    "verb.possession": "verbs of buying, selling, owning",
    "verb.social": "verbs of political and social activities and events",
    "verb.stative": "verbs of being, having, spatial relations",
    "verb.weather": "verbs of raining, snowing, thawing, thundering",
    "adj.ppl": "participial adjectives"
}

WORDNET_LEXNAMES = list(WORDNET_LEXNAMES_TO_DEFINITIONS.keys())

WORDNET_LEXNAMES_BY_POS = {
    'adj': [], 'adv': [], 'noun': [], 'verb': []
}

for lexname in WORDNET_LEXNAMES:
    WORDNET_LEXNAMES_BY_POS[lexname.split('.')[0]].append(lexname)
