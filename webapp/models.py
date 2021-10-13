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
    use_freely = models.BooleanField(default=False)
    has_deception = models.BooleanField(default=False)
    uses_proposed_payment_scheme = models.BooleanField(default=False)
    can_change_algorithm = models.BooleanField(default=False)
    can_change_attributes = models.BooleanField(default=False)
    only_10_percentile_change = models.BooleanField(default=False)
    use_model_estimates_only = models.BooleanField(
        default=False)

    attention_check_statement = models.CharField(
        max_length=1000)
    algo_attr_attention_check_statement = models.CharField(
        max_length=1000, default='')

    # A flag to control which groups will be in prod
    in_production = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MechTaskAlgorithm(TimestampedModel):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    average_error = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class MechTaskCustomModel(TimestampedModel):
    attributes = models.CharField(max_length=500)
    average_error = models.DecimalField(max_digits=10, decimal_places=2)


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
    user_agreed_to_take_only_once = models.BooleanField(blank=True, null=True)

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
    passed_algo_attr_attention_check = models.BooleanField(
        blank=True, null=True)
    read_understand_algos = models.BooleanField(blank=True, null=True)
    chose_bonus_baseline = models.BooleanField(blank=True, null=True)
    number_of_estimates_done = models.IntegerField(default=0)

    # Fields to track their understanding of the tasks
    user_first_instruction_ans = models.CharField(
        max_length=500, blank=True, null=True)
    user_understood_first_instruction = models.BooleanField(
        blank=True, null=True)
    # the answer for the field is True so it's equivalent to understood last instruction
    user_last_instruction_ans = models.CharField(
        max_length=500, blank=True, null=True)

    # User choices
    use_model_estimates_for_bonus_calc = models.BooleanField(
        blank=True, null=True)
    algorithm = models.ForeignKey(
        MechTaskAlgorithm, on_delete=models.CASCADE, blank=True, null=True)
    selected_attributes = models.CharField(
        max_length=500, blank=True, null=True)
    model = models.ForeignKey(
        MechTaskCustomModel, on_delete=models.CASCADE, blank=True, null=True)

    # Placebo & user choices
    user_selected_algorithm = models.ForeignKey(
        MechTaskAlgorithm, on_delete=models.CASCADE, blank=True, null=True, related_name='placebo_response')
    user_selected_attributes = models.CharField(
        max_length=500, blank=True, null=True)

    # Follow-up questions
    model_estimate_average_error = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    model_estimate_average_error_when_user_did_not_select_model = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    self_estimate_average_error = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    model_estimate_confidence = models.CharField(
        max_length=255, blank=True, null=True)
    model_estimate_confidence_when_user_did_not_select_model = models.CharField(
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
    age = models.CharField(max_length=255, blank=True, null=True)
    pronoun = models.CharField(max_length=255, blank=True, null=True)
    race = models.CharField(max_length=255, blank=True, null=True)
    ethnicity = models.CharField(max_length=255, blank=True, null=True)
    confidence_in_math = models.CharField(
        max_length=255, blank=True, null=True)
    prev_mturk_algo_participation_number = models.CharField(
        max_length=255, blank=True, null=True)
    highest_level_of_education = models.CharField(
        max_length=255, blank=True, null=True)

    # Attention check - in exit survey
    model_performance_as_per_user = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    model_performance_correctly_identified = models.BooleanField(
        blank=True, null=True)

    # Payment & bonus related fields
    base_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    bonus = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    # Average absolute error ~ average_deviation
    average_deviation = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    used_model_for_bonus = models.BooleanField(
        blank=True, null=True)
    human_aae = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    model_aae = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

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
    minutesPerWeekEnglish = models.DecimalField(
        max_digits=10, decimal_places=2)

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
    real_score = models.DecimalField(max_digits=10, decimal_places=2)

    # Linear regression score
    linear_regression_prediction = models.DecimalField(
        max_digits=10, decimal_places=2)

    # Ridge regression score
    ridge_prediction = models.DecimalField(max_digits=10, decimal_places=2)

    # Lasso regression score
    lasso_prediction = models.DecimalField(max_digits=10, decimal_places=2)

    # Decision tree regression score
    decision_tree_prediction = models.DecimalField(
        max_digits=10, decimal_places=2)

    # Random forest regression score
    random_forest_prediction = models.DecimalField(
        max_digits=10, decimal_places=2)

    # KNeighbors regression score
    kneighbors_prediction = models.DecimalField(
        max_digits=10, decimal_places=2)

    # SVM regression score
    svm_reg_prediction = models.DecimalField(max_digits=10, decimal_places=2)


class MechTaskCustomModelSample(TimestampedModel):
    model = models.ForeignKey(MechTaskCustomModel, on_delete=models.CASCADE)
    sample = models.ForeignKey(MechTaskStudentSample, on_delete=models.CASCADE)
    real_score = models.DecimalField(max_digits=10, decimal_places=2)
    linear_regression_prediction = models.DecimalField(
        max_digits=10, decimal_places=2)


class MechTaskSurveyEstimate(TimestampedModel):
    survey_response = models.ForeignKey(
        MechTaskSurveyResponse,
        on_delete=models.CASCADE,
        related_name='survey_estimates'
    )
    sample = models.ForeignKey(
        MechTaskStudentSample, on_delete=models.CASCADE, blank=True, null=True)
    custom_sample = models.ForeignKey(
        MechTaskCustomModelSample, on_delete=models.CASCADE, blank=True, null=True)

    real_score = models.DecimalField(max_digits=10, decimal_places=2)
    model_estimate = models.DecimalField(max_digits=10, decimal_places=2)
    user_estimate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    completed = models.BooleanField(default=False)
