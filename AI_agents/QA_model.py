from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
import os

# from dataset import dataset_parser


class QA_Model_ML:
    def __init__(self, dataset):
        self.dataset = dataset
        self.model = self.build_model()

    
    def build_model(self):
        X = []
        y = []
        sections = list(self.dataset.keys())

        for i in range(len(sections)):
            section = sections[i]

            if section.startswith("Определения"):
                definitions = self.dataset[section]

                for j in range(len(definitions)):
                    X.append(definitions[j])
                    y.append(self.dataset["Ответы определения"][j])
            elif section.startswith("Вопросы по настройке"):
                questions = self.dataset[section]

                for k in range(len(questions)):
                    X.append(questions[k])
                    y.append(self.dataset["Ответы для настройки"][k])
            elif section.startswith("Возможные ситуации"):
                situations = self.dataset[section]

                for m in range(len(situations)):
                    X.append(situations[m])
                    y.append(self.dataset["Пути их решения"][m])

        text_clf = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', LinearSVC())
        ])

        text_clf.fit(X, y)

        return text_clf

    def get_answer(self, question):
        predicted_category = self.model.predict([question])

        if predicted_category:
            return predicted_category
        else:
            return "Ответ не найден"





# if __name__ == "__main__":
#     path = os.path.join(os.getcwd(), "AI_agents\\dataset") 
#     parser = dataset_parser.DatasetParser(path)
#     dataset = parser.parse_all_dataset()
#     qa_model_ml = QA_Model_ML(dataset)

#     questions = [
#         "Что такое VLAN?",
#         "Как настроить DHCP на маршрутизаторе для автоматической выдачи IP-адресов клиентам в сети?",
#         "Конфликт IP-адресов в сети",
#         "Отказ в работе VPN из-за несовместимости параметров настройки",
#         "Что такое дуплекс",
#         "Что делает команда show version?",
#         "show interfaces switchport?"
#     ]

#     for question in questions:
#         answer = qa_model_ml.get_answer(question)[0][2:]
#         print(f"Вопрос: {question}")
#         print(f"Ответ: {answer}\n")
