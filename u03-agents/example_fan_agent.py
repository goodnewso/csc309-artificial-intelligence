"""example_fan_agent.py: a simple reflex agent that controls a room fan.

Percept: room temperature.  Actions: OFF, LOW, HIGH.
Performance measure: hours the room is comfortable (23-27 C),
minus a small cost for each hour the fan runs.
"""
def agent(temp):                       # condition-action rules
    if temp < 25:
        return "OFF"
    if temp < 29:
        return "LOW"
    return "HIGH"

COOLING = {"OFF": 0, "LOW": 2, "HIGH": 4}
COST = {"OFF": 0, "LOW": 0.1, "HIGH": 0.2}
outside = [24, 26, 29, 31, 33, 32, 30, 27]      # hourly temperature
score = 0
for hour, t_out in enumerate(outside, start=10):
    action = agent(t_out)
    room = t_out - COOLING[action]
    comfortable = 23 <= room <= 27
    score += comfortable - COST[action]
    print(f"{hour}:00  outside {t_out}C  fan {action:<4}  room {room}C",
          "comfortable" if comfortable else "")
print("performance score:", round(score, 1))
