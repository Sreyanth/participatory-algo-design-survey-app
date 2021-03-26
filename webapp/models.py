from django.contrib.auth.models import User
from django.db import models


class TimestampedModel(models.Model):
    """
    An abstract class to include timestamps of creation and modification.
    """

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class MechTaskUserGroup(TimestampedModel):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    has_deception = models.BooleanField(default=False)
    uses_proposed_payment_scheme = models.BooleanField(default=False)
    can_change_algorithm = models.BooleanField(default=False)
    can_change_attributes = models.BooleanField(default=False)

    attention_check_statement = models.CharField(
        max_length=500)

    def __str__(self):
        return self.name


class MechTaskAlgorithm(TimestampedModel):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MechTaskSurveyResponse(TimestampedModel):
    # User connection for authentication and authorization
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='mech_task_survey_response'
    )
    user_group = models.ForeignKey(MechTaskUserGroup, on_delete=models.CASCADE)

    # And to track previously known user ID for analytics
    previously_known_user_id = models.CharField(
        max_length=255, blank=True, null=True
    )

    # Consent details
    user_is_18_or_older = models.BooleanField(blank=True, null=True)
    user_read_and_understood_info = models.BooleanField(blank=True, null=True)
    user_wants_to_participate = models.BooleanField(blank=True, null=True)
    user_consented_to_survey = models.BooleanField(blank=True, null=True)

    # MTurk details
    mturk_id_attempt_1 = models.CharField(
        max_length=255, blank=True, null=True)
    mturk_id_attempt_2 = models.CharField(
        max_length=255, blank=True, null=True)
    final_mturk_id = models.CharField(max_length=255, blank=True, null=True)

    # Fields to track the user journey
    current_stage = models.CharField(max_length=255, default='consent')
    read_first_instruction = models.BooleanField(blank=True, null=True)
    read_percentile_description = models.BooleanField(blank=True, null=True)
    read_sample_data_points = models.BooleanField(blank=True, null=True)
    read_model_description = models.BooleanField(blank=True, null=True)
    read_that_model_is_off = models.BooleanField(blank=True, null=True)
    passed_first_attention_check = models.BooleanField(blank=True, null=True)
    passed_second_attention_check = models.BooleanField(blank=True, null=True)
    chose_bonus_baseline = models.BooleanField(blank=True, null=True)
    number_of_estimates_done = models.IntegerField(default=0)

    # User choices
    algorithm = models.ForeignKey(
        MechTaskAlgorithm, on_delete=models.CASCADE, blank=True, null=True)
    model_estimates_for_bonus_calc = models.BooleanField(blank=True, null=True)
    selected_attributes = models.CharField(
        max_length=500, blank=True, null=True)

    # Follow-up questions
    model_estimate_average_error = models.FloatField(blank=True, null=True)
    self_estimate_average_error = models.FloatField(blank=True, null=True)

    model_estimate_confidence = models.CharField(
        max_length=255, blank=True, null=True)
    self_estimate_confidence = models.CharField(
        max_length=255, blank=True, null=True)

    why_chose_the_attributes = models.TextField(blank=True, null=True)
    why_chose_the_algorithm = models.TextField(blank=True, null=True)

    why_chose_model_estimate = models.TextField(blank=True, null=True)
    why_chose_self_estimate = models.TextField(blank=True, null=True)

    representativeness = models.CharField(
        max_length=255, blank=True, null=True)
    transparency = models.CharField(max_length=255, blank=True, null=True)

    fairness_tutoring_resources = models.CharField(
        max_length=255, blank=True, null=True)
    fairness_scholarship = models.CharField(
        max_length=255, blank=True, null=True)
    fairness_absent_students = models.CharField(
        max_length=255, blank=True, null=True)
    fairness_explanation = models.TextField(blank=True, null=True)

    likeliness_to_use_model = models.CharField(
        max_length=255, blank=True, null=True)

    any_other_thoughts = models.TextField(blank=True, null=True)

    # Demographics
    age_bracket = models.CharField(max_length=255, blank=True, null=True)
    pronoun = models.CharField(max_length=255, blank=True, null=True)
    raceethnicity = models.CharField(max_length=255, blank=True, null=True)
    highest_level_of_education = models.CharField(
        max_length=255, blank=True, null=True)

    completed = models.BooleanField(default=False)


class MechTaskStudentSample(TimestampedModel):
    # We need a way to track this student sample in the Pandas dataframe
    # in the training / testing datasets later
    index_in_dataframe = models.IntegerField(blank=True, null=True)

    # Sample features / attributes

    # male: Whether the student is male (1/0)
    male = models.BooleanField()

    # raceeth: The race/ethnicity composite of the student
    raceeth = models.CharField(max_length=255)

    # preschool: Whether the student attended preschool (1/0)
    preschool = models.BooleanField()

    # expectBachelors: Whether the student expects to obtain a bachelor's
    # degree (1/0)
    expectBachelors = models.BooleanField()

    # motherHS: Whether the student's mother completed high school (1/0)
    motherHS = models.BooleanField()

    # motherBachelors: Whether the student's mother obtained a bachelor's
    # degree (1/0)
    motherBachelors = models.BooleanField()

    # motherWork: Whether the student's mother has part-time or full-time work
    # (1/0)
    motherWork = models.BooleanField()

    # fatherHS: Whether the student's father completed high school (1/0)
    fatherHS = models.BooleanField()

    # fatherBachelors: Whether the student's father obtained a bachelor's
    # degree (1/0)
    fatherBachelors = models.BooleanField()

    # fatherWork: Whether the student's father has part-time or full-time work
    # (1/0)
    fatherWork = models.BooleanField()

    # selfBornUS: Whether the student was born in the United States of America
    # (1/0)
    selfBornUS = models.BooleanField()

    # motherBornUS: Whether the student's mother was born in the United States
    # of America (1/0)
    motherBornUS = models.BooleanField()

    # fatherBornUS: Whether the student's father was born in the United States
    # of America (1/0)
    fatherBornUS = models.BooleanField()

    # englishAtHome: Whether the student speaks English at home (1/0)
    englishAtHome = models.BooleanField()

    # computerForSchoolwork: Whether the student has access to a computer for
    # schoolwork (1/0)
    computerForSchoolwork = models.BooleanField()

    # read30MinsADay: Whether the student reads for pleasure for 30 minutes/day
    # (1/0)
    read30MinsADay = models.BooleanField()

    # minutesPerWeekEnglish: The number of minutes per week the student spend
    # in English class
    minutesPerWeekEnglish = models.FloatField()

    # studentsInEnglish: The number of students in this student's English class
    # at school
    studentsInEnglish = models.IntegerField()

    # schoolHasLibrary: Whether this student's school has a library (1/0)
    schoolHasLibrary = models.BooleanField()

    # publicSchool: Whether this student attends a public school (1/0)
    publicSchool = models.BooleanField()

    # urban: Whether this student's school is in an urban area (1/0)
    urban = models.BooleanField()

    # schoolSize: The number of students in this student's school
    schoolSize = models.IntegerField()

    # User's real score
    real_score = models.FloatField()

    # Linear regression score
    linear_regression_prediction = models.FloatField()

    # Ridge regression score
    ridge_prediction = models.FloatField()

    # Lasso regression score
    lasso_prediction = models.FloatField()

    # Decision tree regression score
    decision_tree_prediction = models.FloatField()

    # Random forest regression score
    random_forest_prediction = models.FloatField()

    # KNeighbors regression score
    kneighbors_prediction = models.FloatField()

    # SVM regression score
    svm_reg_prediction = models.FloatField()


class MechTaskSurveyEstimate(TimestampedModel):
    survey_response = models.ForeignKey(
        MechTaskSurveyResponse,
        on_delete=models.CASCADE,
        related_name='survey_estimates'
    )
    sample = models.ForeignKey(MechTaskStudentSample, on_delete=models.CASCADE)

    real_score = models.FloatField()
    model_estimate = models.FloatField()
    user_estimate = models.FloatField(blank=True, null=True)

    completed = models.BooleanField(default=False)
