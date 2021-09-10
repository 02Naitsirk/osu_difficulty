import aim
import tap
from Beatmap import Beatmap

if __name__ == '__main__':
    beatmap_file = input("beatmap: ")
    beatmap = Beatmap(beatmap_file)

    count_100 = 0
    count_50 = 0

    # lists for output purposes

    aim_star_list = []
    tap_star_list = []
    total_star_list = []

    aim_pp_list = []
    tap_pp_list = []
    acc_pp_list = []
    total_pp_list = []

    for i in range(0, 4):
        dt = i >> 1 & 1
        hr = i >> 0 & 1

        aim_sr = aim.calculate_aim_stars(beatmap, hr, dt)
        aim_star_list.append(round(aim_sr, 2))

        tap_sr = tap.calculate_tap_stars(beatmap, hr, dt)
        tap_star_list.append(round(tap_sr, 2))

        total_sr = pow(aim_sr ** 3 + tap_sr ** 3, 1 / 3)
        total_star_list.append(round(total_sr, 2))

        aim_pp = aim_sr ** 3
        aim_pp_list.append(round(aim_pp))

        tap_pp = tap.calculate_tap_pp(beatmap, count_100, count_50, hr, dt)
        tap_pp_list.append(round(tap_pp))

        acc_pp = tap.calculate_accuracy_difficulty(beatmap, count_100, count_50, hr, dt)
        acc_pp_list.append(round(acc_pp))

        total_pp_list.append(round(aim_pp + tap_pp + acc_pp))

    accuracy = (300 * (len(beatmap.hit_objects) - count_100 - count_50) + 100 * count_100 + 50 * count_50) / (
                300 * (len(beatmap.hit_objects)))

    print()

    beatmap.print_beatmap()
    print(str(round(100 * accuracy, 2)) + "%")

    print()

    print("Aim SR: " + str(aim_star_list))
    print("Tap SR: " + str(tap_star_list))
    print("SR: " + str(total_star_list))

    print()

    print("Aim PP: " + str(aim_pp_list))
    print("Tap PP: " + str(tap_pp_list))
    print("Acc PP: " + str(acc_pp_list))

    print()

    print("PP: " + str(total_pp_list))
