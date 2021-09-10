import math

from scipy import optimize

from Beatmap import Beatmap
from HitObject import HitObject


def calculate_hit_probability(current: HitObject, last: HitObject, second_last: HitObject, circle_size: float,
                              skill: float, clock_rate: float):
    radius = 54.4 - 4.48 * circle_size
    delta_time = (current.time - last.time) / clock_rate

    if skill == 0 or radius == 0 or delta_time == 0:
        return 0

    x_shift = math.fabs(current.x - last.x)
    y_shift = math.fabs(current.y - last.y)

    # assume hit error along any dimension is normally distributed
    # twice the velocity is sqrt(2) times the hit error, and twice the skill level is half the hit error

    x_deviation = math.sqrt(x_shift) / (delta_time * skill)
    y_deviation = math.sqrt(y_shift) / (delta_time * skill)

    x_hit_probability: float
    y_hit_probability: float

    if second_last is not None:

        # angle corrections
        # TODO: collect angle data

        last_to_current = math.sqrt(pow(last.x - current.x, 2) + pow(last.y - current.y, 2))
        second_last_to_current = math.sqrt(pow(second_last.x - current.x, 2) + pow(second_last.y - current.y, 2))
        second_last_to_last = math.sqrt(pow(second_last.x - last.x, 2) + pow(second_last.y - last.y, 2))

        if last_to_current > 0 and second_last_to_last > 0:
            cos_angle = (last_to_current ** 2 - second_last_to_current ** 2 + second_last_to_last ** 2) / (
                    2 * last_to_current * second_last_to_last)
            cos_angle = max(min(cos_angle, 1), -1)
            angle = math.acos(cos_angle)

            # angle_deviation_multiplier = 1.0 + radius / 32 * delta_time / 1000 * angle
            # x_deviation *= angle_deviation_multiplier
            # y_deviation *= angle_deviation_multiplier

        # strain corrections
        # TODO: collect strain data

        last_delta_time = (last.time - second_last.time) / clock_rate
        delta_time_ratio = max(last_delta_time / delta_time, delta_time / last_delta_time)

        delta_time_ratio_deviation_multiplier = 0.5 / delta_time_ratio + 0.5

        x_deviation *= delta_time_ratio_deviation_multiplier
        y_deviation *= delta_time_ratio_deviation_multiplier

    else:
        x_deviation *= 0.7
        y_deviation *= 0.7

    if x_shift == 0:
        x_hit_probability = 1
    else:
        x_hit_probability = math.erf(radius / (math.sqrt(2) * x_deviation))

    if y_shift == 0:
        y_hit_probability = 1
    else:
        y_hit_probability = math.erf(radius / (math.sqrt(2) * y_deviation))

    return x_hit_probability * y_hit_probability


def calculate_aim_difficulty(beatmap: Beatmap, hr=False, dt=False):
    minimum_skill = 0
    maximum_skill = 1
    root_finding_method = 'brentq'

    def calculate_expected_hits_minus_threshold(skill: float):
        threshold = 0.5
        expected_hits = 1  # assume first object has 100% hit probability, so expected hits starts at 1

        hit_objects = beatmap.hit_objects
        cs = beatmap.cs
        clock_rate = 1

        if hr:
            cs *= 1.3

        if cs > 10:
            cs = 10

        if dt:
            clock_rate = 1.5

        for i in range(1, len(hit_objects)):
            current = hit_objects[i]
            last = hit_objects[i - 1]
            second_last = None
            if i > 1:
                second_last = hit_objects[i - 2]
            p = calculate_hit_probability(current, last, second_last, cs, skill, clock_rate)
            expected_hits += p

        return len(hit_objects) - expected_hits - threshold

    skill_level = optimize.root_scalar(calculate_expected_hits_minus_threshold,
                                       bracket=[minimum_skill, maximum_skill],
                                       method=root_finding_method)
    return skill_level.root


def calculate_aim_stars(beatmap: Beatmap, hr=False, dt=False):
    scale = 300
    exp = math.log(1.4) / math.log(1.5)  # 0.83
    aim_difficulty = calculate_aim_difficulty(beatmap, hr, dt)
    return scale * math.pow(aim_difficulty, exp)
