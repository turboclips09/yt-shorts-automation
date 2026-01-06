import random

hooks = [
    "A 300-horsepower car in the 90s felt wilder than today’s supercars.",
    "Modern cars are faster than ever, yet somehow feel boring.",
    "Driving used to feel dangerous. Now it feels sanitized.",
    "Here’s why modern cars killed excitement."
]

details = [
    "You could feel the road fighting the steering wheel.",
    "Engine noise alone made your heart race.",
    "Every input felt mechanical and raw.",
    "Mistakes actually had consequences."
]

modern = [
    "Modern cars are designed to calm you down.",
    "Electronic steering removes resistance.",
    "Stability systems correct every slide.",
    "Computers filter everything you feel."
]

payoff = [
    "That’s why slower cars used to feel exciting.",
    "That’s why speed today feels empty.",
    "That’s what modern cars lost."
]

loop = [
    "Once you notice this, driving won’t feel the same.",
    "You can’t unfeel this now."
]

script = " ".join([
    random.choice(hooks),
    random.choice(details),
    random.choice(modern),
    random.choice(payoff),
    random.choice(loop)
])

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script)

print(script)
