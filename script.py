import random

hooks = [
    "Modern cars are faster than ever, yet somehow feel boring.",
    "This sounds crazy, but older cars felt faster than modern ones.",
    "Here’s why modern cars killed driving excitement.",
    "This is why driving doesn’t feel intense anymore.",
    "Cars didn’t always feel this numb."
]

provocations = [
    "Speed today is hidden on purpose.",
    "Modern cars are designed to calm you down.",
    "Driving is no longer supposed to scare you.",
    "Feeling speed is now considered a problem.",
    "Excitement has been engineered out."
]

sensory_hits = [
    "Your brain feels speed through sound, vibration, and resistance.",
    "Noise, steering weight, and feedback tell your body how fast you’re moving.",
    "Your senses react long before your eyes check the speedometer.",
    "Speed is something you feel, not something you read.",
    "Raw feedback creates tension."
]

modern_failures = [
    "Heavy insulation kills sound.",
    "Electronic steering removes resistance.",
    "Computers smooth every input.",
    "Stability systems correct everything.",
    "Modern suspension isolates you from the road."
]

contrast = [
    "Older cars didn’t protect you from speed.",
    "There was no filter between you and the road.",
    "Every vibration came straight to the driver.",
    "Even 60 felt intense.",
    "Driving demanded attention."
]

payoff = [
    "That’s why slow cars used to feel exciting.",
    "That’s why older cars felt alive.",
    "That’s why modern speed feels empty.",
    "That’s why people miss how cars used to feel.",
    "That’s why excitement isn’t about numbers."
]

loops = [
    "Once you notice this, modern cars won’t feel the same.",
    "After this, you’ll understand why driving feels different.",
    "And now you know what’s missing.",
    "You’ll feel this every time you drive.",
    "That realization changes everything."
]

script = " ".join([
    random.choice(hooks),
    random.choice(provocations),
    random.choice(sensory_hits),
    random.choice(modern_failures),
    random.choice(modern_failures),
    random.choice(contrast),
    random.choice(payoff),
    random.choice(loops)
])

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script)

print("🔥 High-energy Shorts script generated:")
print(script)
