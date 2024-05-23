from langchain.tools import StructuredTool


def intro():
    return "Introduction: Bienvenue dans la séquence des tâches."


def problem_definition():
    return "Définition du problème: Définissez le problème que vous rencontrez."


def question_1():
    return "Question 1: Quelle est la première question?"


def answer_1():
    return "Réponse 1: Voici la réponse à la première question."


def question_2():
    return "Question 2: Quelle est la deuxième question?"


def answer_2():
    return "Réponse 2: Voici la réponse à la deuxième question."


intro_tool = StructuredTool.from_function(
    func=intro,
    name="Intro",
    description="Fournit une introduction."
)

problem_definition_tool = StructuredTool.from_function(
    func=problem_definition,
    name="ProblemDefinition",
    description="Définit le problème."
)

question_1_tool = StructuredTool.from_function(
    func=question_1,
    name="Question1",
    description="Pose la première question."
)

answer_1_tool = StructuredTool.from_function(
    func=answer_1,
    name="Answer1",
    description="Fournit la réponse à la première question."
)

question_2_tool = StructuredTool.from_function(
    func=question_2,
    name="Question2",
    description="Pose la deuxième question."
)

answer_2_tool = StructuredTool.from_function(
    func=answer_2,
    name="Answer2",
    description="Fournit la réponse à la deuxième question."
)


class SequentialChain:
    def __init__(self, tools):
        self.tools = tools
        self.current_step = 0

    def run(self):
        if self.current_step < len(self.tools):
            result = self.tools[self.current_step].func()
            print(result)

            if self.check_transition(result):
                self.current_step += 1
            else:
                print("Condition pour passer à l'étape suivante non remplie.")
        else:
            return "Toutes les étapes ont été complétées."

    def check_transition(self, result):
        return "réponse" in result.lower()


tools = [intro_tool, problem_definition_tool, question_1_tool, answer_1_tool, question_2_tool, answer_2_tool]

sequential_chain = SequentialChain(tools=tools)

for _ in range(7):
    sequential_chain.run()
