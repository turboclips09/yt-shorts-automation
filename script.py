import random

def pick(pool):
    return random.choice(pool)

hooks = [
    "Modern cars are insanely fast, but they feel dead.",
    "This is why driving doesn’t feel thrilling anymore.",
    "Cars today are quicker than ever, yet somehow boring.",
    "Driving used to feel dangerous. Now it feels numb.",
    "Here’s why modern cars killed excitement."
]

opinions = [
    "Speed is no longer meant to scare you.",
    "Modern cars are built to calm you down.",
    "Feeling speed is now considered a flaw.",
    "Excitement has been engineered out.",
    "Driving is designed to feel safe, not intense."
]

sensory = [
    "Your body feels speed through noise, vibration, and resistance.",
    "Sound and steering tell your brain how fast you’re moving.",
    "You feel speed long before you see the number.",
    "Raw feedback creates tension.",
    "Fear is part of excitement."
]

tech_filters = [
    "Electronic steering removes resistance.",
    "Heavy insulation kills engine noise.",
    "Computers smooth every movement.",
    "Stability systems interfere constantly.",
    "Modern suspension isolates the road."
]

old_cars = [
    "Older cars didn’t protect you from speed.",
    "There was no filter between you and the road.",
    "Every vibration reached the driver.",
    "Even moderate speeds felt intense.",
    "Driving demanded focus."
]

payoffs = [
    "That’s why slow cars used to feel exciting.",
    "That’s why older cars felt alive.",
    "That’s why modern speed feels empty.",
    "That’s why people miss old driving.",
    "That’s why numbers don’t equal excitement."
]

loops = [
    "Once you notice this, modern cars won’t feel the same.",
    "After this, you’ll feel it every time you drive.",
    "And now you know what’s missing.",
    "That realization changes everything.",
    "You won’t unfeel this."
]

# Build script with guaranteed uniqueness
script_parts = [
    pick(hooks),
    pick(opinions),
    pick(sensory),
    pick(tech_filters),
    pick(old_cars),
    pick(payoffs),
    pick(loops)
]

# Ensure no duplicates (extra safety)
script_parts = list(dict.fromkeys(script_parts))

script = " ".join(script_parts)

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script)

print("🔥 High-energy, non-repetitive Shorts script:")
print(script)
