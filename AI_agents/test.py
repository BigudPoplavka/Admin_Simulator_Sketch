from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
import os

from dataset import dataset_parser

class QA_Model:
    def __init__(self, dataset):
        self.dataset = dataset
        self.model = self.build_model()

    def build_model(self):
        X = []
        y = []

        for section, data in self.dataset.items():
            if section.startswith("Определения"):
                definitions = self.dataset.get("Определения", [])
                definition_answers = self.dataset.get("Ответы определения", [])

                for i in range(min(len(definitions), len(definition_answers))):
                    X.append(definitions[i])
                    y.append(definition_answers[i])
            elif section.startswith("Вопросы по настройке"):
                setup_questions = self.dataset.get("Вопросы по настройке", [])
                setup_answers = self.dataset.get("Ответы для настройки", [])

                for i in range(min(len(setup_questions), len(setup_answers))):
                    X.append(setup_questions[i])
                    y.append(setup_answers[i])
            elif section.startswith("Возможные ситуации"):
                situations = self.dataset.get("Возможные ситуации", [])
                solutions = self.dataset.get("Пути их решения", [])

                for i in range(min(len(situations), len(solutions))):
                    X.append(situations[i])
                    y.append(solutions[i])

        text_clf = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', LinearSVC())
        ])

        text_clf.fit(X, y)

        return text_clf

    def get_answer(self, question):
        return self.model.predict([question])[0]

# Пример использования
if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "AI_agents\\dataset") 
    parser = dataset_parser.DatasetParser(path)
    dataset = parser.parse_all_dataset()

    qa_model = QA_Model(dataset)

    # Задаем вопрос
    question = "Что такое маршрутизатор?"

    # Получаем ответ
    answer = qa_model.get_answer(question)
    print(answer)
