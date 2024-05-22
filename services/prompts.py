from services.utils import load_document, split_document_by_sections


def init_system():
    document = load_document("data/Rolling-Industries.pdf")
    splitted_document = split_document_by_sections(document)
    return splitted_document


splitted_document = init_system()

system_prompt = """
Tu es programmé pour agir comme un intervieweur experte dans le cadre de simulations \
d'entretiens de conseil en stratégie. Ton rôle consiste à évaluer les compétences des candidats \
en résolution de problèmes, en analyse de données et en communication efficace. Vous poserez des \
questions de cas spécifiques au secteur, guiderez les discussions et évaluerez les réponses des \
candidats pour mesurer leur aptitude à formuler des recommandations stratégiques pertinentes.\
Votre objectif est de créer un environnement d'entretien réaliste et d'offrir des retours constructifs \
pour aider les candidats à se perfectionner."""


intro_prompt = """
Bien sûr ! \
Voici le cas sur lequel tu vas être interrogé et quelques informations à son sujet : """ \
+ splitted_document['Intro']

problem_definition_prompt = splitted_document['Problem_definition']

question_answers_prompts = {}

for key in splitted_document.keys():
    if key != 'Intro' and key != 'Problem_definition':
        if 'Question' in key:
            question_answers_prompts[key] = splitted_document[key]
        elif 'Answer' in key:
            question_answers_prompts[key] = splitted_document[key]
