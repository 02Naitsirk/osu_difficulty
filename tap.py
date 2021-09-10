import math

from scipy import optimize

from Beatmap import Beatmap


def calculate_tap_difficulty(beatmap: Beatmap, hr=False, dt=False):
    hit_objects = beatmap.hit_objects
    ar = beatmap.ar
    clock_rate = 1

    if hr:
        ar *= 1.4

    if dt:
        clock_rate = 1.5

    streak = 0
    lowest_effective_delta_time = math.inf
    for i in range(2, len(hit_objects)):
        current = hit_objects[i]
        last = hit_objects[i - 1]
        second_last = hit_objects[i - 2]

        delta_time = (current.time - last.time) / clock_rate
        last_delta_time = (last.time - second_last.time) / clock_rate

        ratio = min(1, delta_time / last_delta_time)

        streak += 1
        streak *= ratio

        effective_delta_time = delta_time / math.log2(math.log2(2 + streak))
        if effective_delta_time < lowest_effective_delta_time:
            lowest_effective_delta_time = effective_delta_time

    return 1 / lowest_effective_delta_time


def calculate_tap_stars(beatmap: Beatmap, hr=False, dt=False):
    scale = 90
    exp = math.log(1.4) / math.log(1.5)  # 0.83
    tap_difficulty = calculate_tap_difficulty(beatmap, hr, dt)
    return scale * math.pow(tap_difficulty, exp)


def calculate_accuracy_difficulty(beatmap: Beatmap, count_100: float, count_50: float, hr=False, dt=False):
    deviation = calculate_deviation(beatmap, count_100, count_50, hr, dt)
    return 5000 * deviation ** -2


def calculate_deviation(beatmap: Beatmap, count_100: float, count_50: float, hr=False, dt=False):
    od = beatmap.od
    clock_rate = 1

    if dt:
        clock_rate = 1.5

    if hr:
        od *= 1.4

    if od > 10:
        od = 10

    great_hit_window = (79.5 - 6 * od) / clock_rate
    count_300_adjusted = max(0, beatmap.circle_count - count_100 - count_50)

    # TODO: figure out the distribution of 50s

    # most 50s come from misreads, double-tapping, tiredness, or some other factor
    # unrelated to the player's natural ability to tap accurately
    # so for now just assume 50s count as two 100s

    def likelihood(x):
        return -((count_300_adjusted + 1) * math.log(math.erf(great_hit_window / (math.sqrt(2) * x)))
                 + (count_100 + 2 * count_50 + 1) * math.log(1 - math.erf(great_hit_window / (math.sqrt(2) * x))))

    deviation = optimize.minimize_scalar(likelihood, bounds=(2, 100), method="bounded")

    return deviation.x


def calculate_tap_pp(beatmap: Beatmap, count_100: float, count_50: float, hr=False, dt=False):
    sr = calculate_tap_stars(beatmap, hr, dt)
    deviation = calculate_deviation(beatmap, count_100, count_50, hr, dt)
    tap_scale = math.erf(6.5 / deviation)
    return tap_scale * sr ** 3
