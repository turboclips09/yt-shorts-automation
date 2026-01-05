import random
import datetime

topics = [
    "This car was banned in multiple countries",
    "This supercar failed despite insane specs",
    "This engine sound scares supercars",
    "This car company almost went bankrupt",
    "This luxury car secretly shares parts",
    "This car was too fast for the road",
    "This design mistake killed this car",
]

hooks = [
    "This car should not exist.",
    "Most people don’t know this.",
    "This almost destroyed a company.",
    "This shocked the entire car industry.",
    "This car broke the rules.",
]

loops = [
    "And that’s why this car disappeared.",
    "That’s why collectors want it today.",
    "And the ending is even crazier.",
    "That’s why this car is unforgettable.",
    "And that’s why it still matters.",
]

script = f"""
{random.choice(hooks)}

{random.choice(topics)}.

Engineered beyond limits.
Ignored common sense.
Built before regulations caught up.

{random.choice(loops)}
"""

today = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script)

print("Generated script:")
print(script)
