#!/usr/bin/env Rscript

print("Imported Data")
dat <- read.table("/Users/moizqureshi/Desktop/CSE145/BlueHat_nRF52_Central/train_tests/rawData3.txt", header=TRUE, sep=",")


powerfunction <- function(x, b0, b1, b2) {b0 + b1*(x^b2)}
sink("/dev/null")
power.fit <- nls(Distance ~ powerfunction(Ratio, intercept, multiplier, power), data = dat, start = list(intercept=0,multiplier=1,power=2), trace = T)
sink()
print("Power Curve Coefficients")
coef(power.fit)

