import random

hooks = [
    "Most people don’t know this about cars.",
    "This is why cars feel different today.",
    "Almost nobody talks about this car fact.",
    "This happens every time you drive.",
    "Cars were never meant to feel like this."
]

topics = [
    [
        "Modern cars are faster than ever, but they feel slower.",
        "That’s because modern cars are designed to hide speed from the driver."
    ],
    [
        "Older cars felt more exciting, even at low speeds.",
        "They had less insulation, louder engines, and stiffer feedback."
    ],
    [
        "Your car is constantly adjusting things without you noticing.",
        "Steering, throttle, and traction are all being controlled."
    ],
    [
        "Speed feels different depending on sound, vibration, and seating.",
        "That’s why two cars at the same speed can feel completely different."
    ],
    [
        "Cars today are built for comfort first, excitement second.",
        "Safety systems quietly change how driving feels."
    ]
]

details = [
    "More sound insulation.",
    "Smoother suspension.",
    "Quieter engines.",
    "Electronic steering.",
    "Computer-controlled throttle."
]

loops = [
    "And that’s why driving feels different now.",
    "That’s why cars don’t feel the same anymore.",
    "And once you notice it, you can’t unfeel it.",
    "That’s why older cars felt more alive.",
    "And that’s what most drivers never realize."
]

topic = random.choice(topics)

script = f"""
{random.choice(hooks)}

{topic[0]}
{topic[1]}

{random.choice(details)}
{random.choice(details)}

{random.choice(loops)}
"""

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script.strip())

print("Generated scroll-stopping car script:")
print(script)
