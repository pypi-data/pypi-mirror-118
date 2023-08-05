#
#     QuantLET-ml - Machine learning extensions
#
#     Copyright (C) 2006 Jorge M. Faleiro Jr.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published
#     by the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import logging

import numpy as np
import pandas as pd
from quantlet.streams import QLet
from quantlet.streams.metadata import cast_to_canonical, cast_to_dataframe
from sklearn.metrics import (explained_variance_score, mean_squared_error,
                             r2_score)
from sklearn.model_selection import GridSearchCV


@QLet
def one_hot(df, columns, prefixes=None):
    result = df.copy()
    for i, column in enumerate(columns):
        prefix = column if prefixes is None else prefixes[i]
        result = result.join(pd.get_dummies(df[column], prefix=prefix))
        result.drop(column, axis=1, inplace=True)
    return result


@QLet
def scale(df, columns, scalers=None):
    result = df.copy()
    for i, column in enumerate(columns):
        c = result[column]
        result[column] = (
            (c - c.mean()) / (c.max() - c.min())
            if scalers is None
            else scalers[i].fit_transform(result[[column]])
        )
    return result


@QLet
def online_fit_predict(
    iterator,
    model,
    prediction_tag,
    response_variable_tag="response",
    error_tag="error",
    ignore_tags=None,
    error_type="squared",
):
    """
    Online learning and prediction. Partial fit of features and response on previous sample, and prediction on
    features of current sample
    :param iterator: stream generator
    :param model online model, i.e. one that takes a partial_fit online training
    """
    iterator = cast_to_canonical(iterator)
    error_functions = dict(
        squared=lambda x, y: (x - y) ** 2, absolute=lambda x, y: abs((x - y) / y)
    )
    error_function = error_functions[error_type]
    ignore_tags = [] if ignore_tags is None else ignore_tags
    ignore_tags += ["index", prediction_tag, response_variable_tag]
    fitted = False
    lagging_error = None
    for i, item in enumerate(iterator):
        features = np.array(
            [item[k] for k in sorted(item.keys()) if k not in ignore_tags]
        ).reshape(1, -1)
        response = np.array([item[response_variable_tag]])
        if np.isnan(features).any():
            logging.info("skipping NaN features in row %d", i)
        elif np.isnan(response).any():
            logging.info("skipping NaN response in row %d", i)
        else:
            if fitted:
                item[prediction_tag] = model.predict(features)[0]
                item[error_tag] = lagging_error
                yield item
            model.partial_fit(features, response)
            lagging_error = error_function(
                model.predict(features)[0], response[0])
            fitted = True


@QLet
def window_shift(df, columns, shift, separator="_"):
    reverse, shift = shift < 0, abs(shift)
    for column in columns:
        for i in range(1, shift + 1):
            pd_shift = -i if reverse else i
            df["%s%s%s" % (column, separator, i)] = df[column].shift(pd_shift)
    return df


@QLet
def unscale(df, columns, scalers, index_column="index"):
    """Unscale columns based on scalers previous fitting"""
    df = cast_to_dataframe(df, index_column=index_column)
    result = df.copy()
    for i, column in enumerate(columns):
        result[column] = scalers[i].inverse_transform(result[[column]])
    return result


@QLet
def split_feature_response(
    df, index_tag="index", response_tag="feature", ignore_tags=[]
):
    """split a dataframe into feature and response"""
    df = cast_to_dataframe(df.copy(), index_tag)
    ignore_tags += [index_tag, response_tag]
    response = df.pop(response_tag).values
    feature_columns = [k for k in sorted(df.columns) if k not in ignore_tags]
    feature = df.loc[:, feature_columns]
    return feature, response


class PredictResult(object):

    scorers = dict(
        r2=r2_score,
        explained_variance=explained_variance_score,
        mean_squared_error=lambda x, y, z: mean_squared_error(x, y, z),
    )

    def __init__(self, prediction, x_test):
        self.x_test = x_test

    def scores(self, y_test):
        return {
            k: scorer(y_test, self.prediction)
            for k, scorer in PredictResult.scorers.items()
        }


class PredictResults(object):
    def __init__(self, predict_results):
        self.predict_results = predict_results


class FitResult(object):
    def __init__(self, clf):
        self.clf = clf

    def best_score(self):
        return self.clf.best_score_

    def best_parameters(self):
        # return {k: all_parameters[k] for k, v in clf.parameters.items() if k
        return self.clf.best_estimator_.get_params()
        # in all_parameters}

    def predict(self, x_test):
        prediction = self.clf.predict(x_test)
        return PredictResult(prediction, x_test)


class FitResults(object):
    def __init__(self, fit_results):
        self.fit_results = fit_results

    def best_result(self):
        result = None
        for fit_result in self.fit_results:
            if result is None:
                result = fit_result
            elif fit_result.best_score() > result.best_score():
                result = fit_result
        return result

    def predict(self, x_test):
        predict_results = []
        for fit_result in self.fit_results:
            predict_results += [fit_result.predict(x_test)]
        return PredictResults(predict_results)


class MultiModelSearchCV(object):
    def __init__(self, models, parameters, cv=5, verbose=0, scoring="r2"):
        self.models = models
        self.parameters = parameters
        self.cv = cv
        self.verbose = verbose

    def fit(self, x, y):
        results = []
        for model, parameter in zip(self.models, self.parameters):
            clf = GridSearchCV(model, parameter, cv=self.cv,
                               verbose=self.verbose)
            clf.fit(x, y)
            fit_result = FitResult(clf)
            results += [fit_result]
        return FitResults(results)


class MultiModelSelector(object):
    def __init__(self, models, parameters, searcher_factory):
        self._models = models
        self._parameters = parameters
        self._searcher_factory = searcher_factory
        self._searchers = []
        self._predictions = []

    def _fit(self, x_train, y_train):
        for model, parameters in zip(self._models, self._parameters):
            searcher = self._searcher_factory(model, parameters)
            searcher.fit(x_train, y_train)
            self._searchers += [searcher]

    def _predict(self, x_test, y_test):
        for searcher in self._searchers:
            model = searcher.best_estimator_
            prediction = model.predict(x_test)
            self._predictions += [(y_test, prediction)]

    def run(self, x_train, y_train, x_test, y_test):
        self._fit(x_train, y_train)
        self._predict(x_test, y_test)

    def best_performances(self):
        return sorted(
            [
                dict(
                    estimator=clf.estimator,
                    best_score=clf.best_score_,
                    best_parameters={
                        k: v for k, v in clf.best_estimator_.get_params().items()
                    },
                )
                for clf in self._searchers
            ],
            key=lambda d: d["best_score"],
            reverse=True,
        )

    def best_scores(
        self,
        score_functions=dict(
            r2=r2_score, explained_variance=explained_variance_score),
        loss_functions=dict(mse=mean_squared_error),
    ):
        result = []
        print(self._searchers)
        for _, prediction in zip(self._searchers, self._predictions):
            y_test, y_hat = prediction
            sum_scores = sum(
                [scorer(y_test, y_hat) for scorer in score_functions.values()]
            )
            sum_inv_losses = sum(
                [1 / loss(y_test, y_hat) for loss in loss_functions.values()]
            )
            score = (sum_scores + sum_inv_losses) / (
                len(score_functions) + len(loss_functions)
            )
            print(result, score)
            result += [score]
        return result

    def performances_as_dataframe(self):
        dfs = [pd.DataFrame(s.cv_results_) for s in self._searchers]
        result = pd.concat(dfs, sort=True)
        result["p"] = [str(k) for k in result.params]
        result["mean_score"] = (
            result.mean_test_score + result.mean_train_score) / 2.0
        return result.set_index("p")

    def plot_performances(self, figsize=(12, 10)):
        x = self.performances_as_dataframe()
        # sklearn behavior: negative values are actually error measurements:
        # https://stackoverflow.com/questions/21443865/scikit-learn-cross-validation-negative-values-with-mean-squared-error
        x = x[(x.mean_train_score > 0) & (x.mean_test_score > 0)]
        x["mean_train_score mean_test_score mean_score".split()].plot.barh(
            figsize=figsize, log=True
        )
