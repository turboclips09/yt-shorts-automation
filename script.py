import random

hooks = [
    "Modern cars are insanely fast. But here’s the uncomfortable truth.",
    "Cars today are quicker than ever, yet they feel strangely boring.",
    "Something important was removed from modern cars. Almost nobody noticed."
]

facts = [
    "Number one. A three hundred horsepower car in the nineties felt absolutely terrifying.",
    "Number two. Old cars talked to you through the steering, pedals, and vibrations.",
    "Number three. Modern cars filter everything through computers before you feel it.",
    "Number four. Traction control saves you, but it quietly deletes the thrill.",
    "Number five. Speed used to demand skill. Today it mostly demands money."
]

wow = [
    "That’s why slower cars used to feel faster than today’s supercars.",
    "That’s why driving used to feel dangerous, raw, and alive.",
    "The excitement didn’t disappear. It was engineered out.",
    "Modern speed feels impressive, but emotionally empty."
]

loop = [
    "Once you notice this, you’ll never experience driving the same way again.",
    "And now you know why old cars still feel alive."
]

script = " ".join([
    random.choice(hooks),
    random.sample(facts, 3)[0],
    random.sample(facts, 3)[1],
    random.sample(facts, 3)[2],
    random.choice(wow),
    random.choice(loop)
])

# 🔥 WRITE SCRIPT (DO NOT READ)
with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script)

print("✅ script.txt generated")
print(script)
