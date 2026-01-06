import random

HOOKS = [
    "Modern cars are faster than ever, yet most people enjoy driving less than before.",
    "Here’s a car truth no manufacturer wants you thinking about.",
    "Cars didn’t become boring by accident — they were engineered that way.",
    "This is why driving today feels impressive but empty.",
    "The biggest lie about modern cars isn’t horsepower or speed."
]

FACTS = [
    "In the 90s, a 300-horsepower car was considered borderline insane.",
    "Today, even family sedans quietly cross 300 horsepower.",
    "But raw speed was never what made cars exciting.",
    "Old cars forced drivers to think, react, and feel every mistake.",
    "Steering used to fight back. Brakes demanded respect. Throttle inputs mattered.",
    "Modern cars smooth out everything before it reaches you.",
    "Electronic steering filters road feel on purpose.",
    "Stability control corrects slides before your brain even notices.",
    "Automatic gearboxes decide for you when excitement is inconvenient.",
    "Sound engineers now fake engine noise through speakers.",
    "Some sports cars are quieter inside than economy cars from the 90s."
]

TRUTHS = [
    "Cars became safer, cleaner, and faster — but also emotionally muted.",
    "Manufacturers optimize for comfort scores, not driver connection.",
    "Most drivers don’t want involvement, they want reassurance.",
    "So cars stopped demanding skill and started offering confidence.",
    "That’s great for safety, but terrible for passion."
]

PAYOFFS = [
    "That’s why slower cars used to feel faster.",
    "That’s why speed today feels strangely forgettable.",
    "That’s why a cheap old car can feel more alive than a modern supercar.",
    "The thrill wasn’t the speed — it was the risk and feedback.",
    "Once you notice this, driving will never feel the same again."
]

def pick_unique(lst, n):
    return random.sample(lst, n)

script = " ".join(
    pick_unique(HOOKS, 1)
    + pick_unique(FACTS, 6)
    + pick_unique(TRUTHS, 4)
    + pick_unique(PAYOFFS, 2)
)

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script)

print(script)
