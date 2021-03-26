from pathlib import Path

import pandas as pd
from django.shortcuts import (HttpResponse, HttpResponseRedirect, render,
                              reverse)
from django.views import View

from .regression_code import run_regression


BASE_DIR = str(Path(__file__).resolve().parent)
DATASET = BASE_DIR + '/data/pisa2009.csv'
df = pd.read_csv(DATASET)
new_cols = df.columns


class CreateLinearRegressionView(View):
    def build_model(self, cols):
        use_cols = [col for x in cols for col in new_cols if x in col]
        df_use = df[use_cols]
        X = df_use
        y = df['readingScore'].rank(pct=True)

        result, df_pred = run_regression(X, y)

        print(result)
        print(df_pred)
        return HttpResponse('API home')

    def get(self, request):
        cols = ['male', 'preschool', 'expectBachelors', 'motherHS', 'motherBachelors',
                'motherWork', 'fatherHS', 'fatherBachelors', 'fatherWork', 'selfBornUS',
                'motherBornUS', 'fatherBornUS', 'englishAtHome',
                'computerForSchoolwork', 'read30MinsADay', 'minutesPerWeekEnglish',
                'studentsInEnglish', 'schoolHasLibrary', 'publicSchool', 'urban',
                'schoolSize', 'raceeth']
        return self.build_model(cols)
