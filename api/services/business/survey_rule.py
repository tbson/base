from typing import Dict
from django.db.models import QuerySet

MAX_QUESTIONS = 5


class SurveyRule:
    @staticmethod
    def get_weight_map(survey_questions: QuerySet) -> Dict:
        result = {}
        for survey_question in survey_questions:
            weight = survey_question.weight
            standard_answers = survey_question.survey_source.survey_answers.all()
            for answer in standard_answers:
                result[answer.pk] = weight
        return result

    @staticmethod
    def calculator(survey_results: QuerySet) -> int:
        if not survey_results.count():
            return 0

        result = 0
        for survey_result in survey_results:
            question = survey_result.survey_question
            answer = survey_result.survey_answer

            result += question.weight * answer.value / 100

        return result

    @staticmethod
    def is_valid_source(survey_question: QuerySet):
        if survey_question.pk:
            return True
        survey = survey_question.survey
        count = survey.survey_questions.filter(
            survey_source_id=survey_question.survey_source_id
        ).count()
        return not count
