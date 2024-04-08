import os

class DatasetParser:
    def __init__(self, path):
        self.path = path
        self.data = {
                "Определения": [],
                "Ответы определения": [],
                "Вопросы по настройке": [],
                "Ответы для настройки": [],
                "Возможные ситуации": [],
                "Пути их решения": []
            }

    def parse_file(self, file_path):
        current_section = None

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                
                if line.startswith("#"):
                    current_section = line[1:].strip()
                elif current_section and line:
                    self.data[current_section].append(line)


    def parse_all_dataset(self):
        for file in os.listdir(self.path):
            file_path = os.path.join(self.path, file)

            if os.path.isfile(file_path):
                if file_path.split('.')[-1] != 'txt':
                    continue
                self.parse_file(file_path)
            else:
                continue

        return self.data


# Проверка парсера
# path = os.path.join(os.getcwd(), "AI_agents\\dataset") 
# parser = DatasetParser(path)
# data = parser.parse_all_dataset()

# for section, data in data.items():
#     print(f"Секция: {section}")
#     for item in data:
#             print(f"{item}")
