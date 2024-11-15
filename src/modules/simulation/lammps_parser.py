from utilities.files.file_reader import DataReaderInterface
import re


class LammpsLogParser:

    def __init__(self, data_reader: DataReaderInterface):
        self.data_reader = data_reader

    def get_value_of_variable(self, searching_text, type_of_command):
        if type_of_command == "v":
            searching_sentence = f"variable {searching_text} equal"
        elif type_of_command == "p":
            searching_sentence = searching_text

        for line in self.data_reader.read():
            if searching_sentence in line:
                match = re.search(r'([-\d.]+)', line)
                if match:
                    return float(match.group(1))

    def get_text_using_label(self, label, output_text_pos, instance_match_num):
        found_instances = []
        for line in self.data_reader.read():
            if label in line:
                found_instances.append(line.split())

        return found_instances[instance_match_num - 1][output_text_pos]

    def get_number_of_particles(self):
        try:
            # Pattern to match the desired lines
            pattern = r"Number of molecules for (\w+): (\d+)"

            # List to store the extracted information
            particles_info = []

            # Extracting information from each line
            for line in self.data_reader.read():
                match = re.search(pattern, line)
                if match:
                    particle_name = match.group(1)
                    particle_count = int(match.group(2))
                    particles_info.append((particle_name, particle_count))

            return particles_info
        except Exception as e:
            raise e
            return str(e)


if __name__ == '__main__':
    lmp_log = LammpsLogParser('../../../data/logs/log.lammps.0')
    value = lmp_log.get_value_of_variable('Number of molecules', "p")
    particle_info = lmp_log.get_number_of_particles()
    pass
