from HitObject import HitObject


class Beatmap:
    def __init__(self, file_name: str):
        lines = []

        file_name = file_name.replace("\\\\", "\\")
        file_name = file_name.replace("\"", "")

        with open(file_name, 'r', encoding='utf8') as file:
            while line := file.readline():
                lines.append(line.rstrip('\n'))

        circle_count = 0
        hit_objects = []
        reached_hit_objects_line = False

        for line in lines:
            if reached_hit_objects_line:
                x = int(line.split(',')[0])
                y = int(line.split(',')[1])
                time = int(line.split(',')[2])
                object_type = int(line.split(',')[3])
                is_slider = False
                if object_type != 12:
                    if "|" in line:
                        is_slider = True
                    else:
                        circle_count += 1
                    hit_object = HitObject(x, y, time, object_type, is_slider)
                    hit_objects.append(hit_object)
                continue
            if "Title:" in line:
                self.title = line.split(':')[1]
            if "Artist:" in line:
                self.artist = line.split(':')[1]
            if "Creator:" in line:
                self.creator = line.split(':')[1]
            if "Version:" in line:
                self.version = line.split(':')[1]
            if "CircleSize:" in line:
                self.cs = float(line.split(':')[1])
            if "OverallDifficulty:" in line:
                self.od = float(line.split(':')[1])
                self.ar = self.od
            if "ApproachRate:" in line:
                self.ar = float(line.split(':')[1])
            if "[HitObjects]" in line:
                reached_hit_objects_line = True

        self.hit_objects = hit_objects
        self.circle_count = circle_count

    def print_beatmap(self):
        beatmap_name = f"{self.artist} - {self.title} ({self.creator}) [{self.version}]"
        difficulty_settings = "CS: " + str(self.cs) + ", AR: " + str(self.ar) + ", OD: " + str(self.od)
        print(beatmap_name + "\n" + difficulty_settings)
