import numpy as np
import scipy.stats

class LinearRegression:
    def __init__(self):
        self.X = None
        self.y = None
        self.y_hat = None
        self.residuals = None
        self.n = None
        self.d = None

    def fit(self, X, y):
        self.X = np.column_stack((np.ones(len(X)), X))
        self.y = y
        self.n = X.shape[0]
        self.d = X.shape[1]
        self.beta = self.OLS()
        self.y_hat = self.X @ self.beta
        self.residuals = self.y - self.y_hat
        self.R2 = self.R_squared()
        self.alpha = 1 - self.R2

    # ----- Sum and Squares -----

    def OLS(self):
        self.beta = np.linalg.inv(self.X.T @ self.X) @ self.X.T @ self.y
        return self.beta

    def SSE(self):
        return np.sum(self.residuals ** 2)
    
    def SSR(self):
        return np.sum((self.y_hat - np.mean(self.y)) ** 2)
    
    def SST(self):
        return np.sum((self.y - np.mean(self.y)) ** 2)
    
    def MSE(self, adjusted = False):
        if adjusted:
            return self.SSE() / (self.n - self.d - 1)
        else:
            return self.SSE() / self.n
    
    def RMSE(self, adjusted = False):
        return np.sqrt(self.MSE(adjusted = adjusted))
    
    # ----- Variance -----

    def variance_hat(self):
        return self.SSE() / (self.n - self.d - 1)
    
    def sample_variance(self):
        return np.sum((self.y - np.mean(self.y)) **2) / (self.n - 1)
    
    # ----- Standard deviation -----

    def standard_deviation(self):
        return np.sqrt(self.sample_variance())

    # ----- F-test -----

    def F_Statistic(self):
        MSR = self.SSR() / self.d
        MSE = self.variance_hat()
        F = MSR / MSE
        prob_F = scipy.stats.f.sf(F, self.d, self.n - self.d - 1)
        return F, prob_F
    
    # ----- T-tests -----

    def t_statistic(self):
        sigma2 = self.variance_hat()
        cov_beta = sigma2 * np.linalg.inv(self.X.T @ self.X)
        se = np.sqrt(np.diag(cov_beta))
        t_stats = self.beta / se
        prob_t = 2 * scipy.stats.t.sf(np.abs(t_stats), df=self.n - self.d - 1)
        return t_stats, prob_t
    
    # ----- Confidence Intervals -----

    def confidence_intervals(self, alpha):
        t_crit = scipy.stats.t.ppf(1 - alpha/2, df=self.n - self.d -1)
        S = np.sqrt(self.SSE() / (self.n - self.d - 1))
        se = S * np.sqrt(np.diag(np.linalg.inv(self.X.T @ self.X)))
        lower = self.beta - t_crit * se
        upper = self.beta + t_crit * se
        return lower, upper
    
    # ----- R-squared -----
    
    def R_squared(self, adjusted=False):
        R2 = self.SSR() / self.SST()
        if adjusted:
            return 1 - (1 - R2) * (self.n - 1) / (self.n - self.d - 1)
        else:
            return R2
        
    # ----- Pearson correlation coefficient -----

    def pearson_correlation(self):
        x = self.X[:, 1:]
        d = x.shape[1]
        corr = np.zeros((d, d))
        prob_corr = np.zeros((d, d))
        for i in range(d):
            for j in range(d):
                r, p = scipy.stats.pearsonr(x[:,i], x[:, j])
                corr[i, j] = r
                prob_corr[i, j] = p
        return corr, prob_corr

