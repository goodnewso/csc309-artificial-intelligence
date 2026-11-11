"""example_rain_bayes.py: updating a belief with Bayes' rule.

In the rainy season it rains on 40% of afternoons.  Dark clouds appear
before 90% of rainy afternoons and before 30% of dry ones.
"""
p_rain = 0.40
p_clouds_given_rain = 0.90
p_clouds_given_dry = 0.30

p_clouds = p_clouds_given_rain * p_rain + p_clouds_given_dry * (1 - p_rain)
p_rain_given_clouds = p_clouds_given_rain * p_rain / p_clouds

print(f"P(rain)               = {p_rain:.2f}   (prior)")
print(f"P(dark clouds)        = {p_clouds:.2f}")
print(f"P(rain | dark clouds) = {p_rain_given_clouds:.2f}   (posterior)")
