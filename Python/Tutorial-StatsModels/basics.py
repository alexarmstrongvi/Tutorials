#!/usr/bin/env python3
################################################################################
# Table of Contents
# * Creating
#
# * References
#   * https://www.statsmodels.org/stable/user-guide.html
################################################################################

import statsmodels.api as sm

########################################
# R-formula syntax
# * See 11.1 of https://cran.r-project.org/doc/manuals/r-release/R-intro.pdf
# * https://patsy.readthedocs.io/en/latest/formulas.html
########################################

########################################
# Tools (sm.tools)
########################################
# sm.add_constant (sm.tools.add_constant)

########################################
# Statistics (sm.stats)
########################################
sm.stats.Table(df)
sm.stats.anova_lm(model)

########################################
# Distributions (sm.distributions)
########################################

########################################
# Graphics (sm.graphics)
########################################
# sm.qqplot
# sm.qqplot_2samples
# sm.qqline
# sm.ProbPlot


########################################
# Regression
########################################
# sm.regression

# sm.OLS - Ordinary Least Squares
mod = sm.OLS(y, X)
res = mod.fit()
print(res.summary())
print(res.params)
print(res.rsquared)

sm.stats.linear_rainbow(res)

sm.graphics.plot_partregress(y=y_label, x=x_xlabel, data=df, obs_labels=False)

# sm.WLS - Weighted Least Squares

# sm.GLS - General Least Squares

# sm.GLSAR - Generalized Least Squares with AR covariance structure

# sm.RecursiveLS - Recursvie Least Squares

# sm.GLM - Generalized Linear Models
# sm.GLMGam

# sm.RLM - Robust Linear Models

# sm.GEE - Generalized Estimating Equations
# sm.NominalGEE
# sm.OrdinalGEE

# sm.MixedLM - Mixed effects Linear Model
# sm.BinomialBayesMixedGLM
# sm.PoissonBayesMixedGLM

########################################
# Classification
########################################
# sm.categorical

# sm.Logit
# sm.MNLogit

# sm.Probit

# sm.Poisson
# sm.GeneralizedPoisson
# sm.ZeroInflatedPoisson
# sm.ZeroInflatedGeneralizedPoisson

# sm.NegativeBinomial
# sm.NegativeBinomialP
# sm.ZeroInflatedNegativeBinomialP


########################################
# Example Datasets ('sm.datasets')
########################################
n_datasets = len([x for x in dir(sm.datasets) if not x.startswith('__')])
print("statsmodels.datasets contains ~{n_datasets} example datasets") # 35 examples

########################################
# Time series analysis ('sm.tsa')
########################################
# sm.tsa.statespace
# sm.tsa.vector_ar

########################################
# Other models
########################################
# sm.nonparametric

# sm.multivariate
# sm.PCA (sm.multivariate.PCA)
# sm.MANOVA (sm.multivariate.MANOVA)
# sm.Factor (sm.multivariate.Factor)

# sm.SurvfuncRight

# sm.PHReg

# sm.QuantReg

########################################
# Multiple Imputation
########################################
# sm.MICE
# sm.MICEData
# sm.MI
# sm.BayesGaussMI

########################################
# Emprical Likelihood (sm.emplike)
########################################

########################################
# Utilities
########################################
# sm.iolib
# sm.os
# sm.load
# sm.load_pickle
# sm.webdoc
# sm.show_versions
# sm.test

########################################
# Miscellaneous
########################################
# sm.robust

# sm.cov_struct

# sm.duration

# sm.formula

# sm.genmod
# sm.families
# sm.gam
