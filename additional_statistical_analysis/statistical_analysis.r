require(plyr)

## Read data
form_data <- read.csv("aggregated_form_data.csv")

# Column description:
# Person : Unique ID for a survey participant
# Question : Survey question ID
# Encoding : Provides the order and identity of systems for each question
# Method : Indicates whether the question was about Fastspeech or Tacotron 
# Preference : Which option was selected: A1 = Audio 1 und A2 = Audio 2
# Response = 0 or 1, where
#            1: Audio of proposed system was perceived as better
#            0: Audio of baseline was perceived as better or equal


#### Evaluation 1 ###

# Aggregation zu Anteilen pro Person

agg_data <- aggregate(form_data$Response, list(Person = form_data$Person,
                                                    Method = form_data$Method), mean)

# Data per Method
fs_daten <- agg_data[agg_data$Method == "fastspeech",]
taco_daten <- agg_data[agg_data$Method == "tacotron",]

p_original_fs_preferred <- 0.25 # Ratio of Response "Fastspeech-proposed is better than Tacotron-baseline" in original study
p_original_taco_preferred <- 0.52 # Ratio of Response "Tacotron-proposed is better than Tacotron-baseline" in original study


# Distribution Analysis: Visualise preference value & confidence intervals of binomial test
# Original order
jpeg(file="plots/binomial_test.jpeg")
bfast <- binom.test(x = sum(fs_daten$x > 0.5), n = nrow(fs_daten), p = p_original_fs_preferred)
btaco <- binom.test(x = sum(taco_daten$x > 0.5), n = nrow(taco_daten), p = p_original_taco_preferred)
plot(0,0, type = "n", ylim = c(0,1), xlim = c(0.5,2.5), las = 1, xlab = "System",
     ylab = "Agreement Ratio", xaxt = "n")
axis(1, c(1,2), c("Fastspeech","Tacotron"))
points(1,bfast$estimate, pch = 19, col = "blue")
points(1,p_original_fs_preferred, pch = 17, col = "darkblue")
arrows(1,bfast$conf.int[1],1,bfast$conf.int[2], angle = 90, length = 0.1, code = 3)
points(2,btaco$estimate, pch = 19, col = "green")
points(2,p_original_taco_preferred, pch = 17, col = "chartreuse4")
arrows(2,btaco$conf.int[1],2,btaco$conf.int[2], angle = 90, length = 0.1, code = 3)
# Add values as labels
# fastspeech (left side)
text(1.15, bfast$estimate, col = "blue", labels = round(bfast$estimate, digits=3))
text(1.15, p_original_fs_preferred, col = "darkblue", labels = p_original_fs_preferred)
text(0.85, bfast$conf.int[1], col = "black", labels = round(bfast$conf.int[1], 3))
text(0.85, bfast$conf.int[2], col = "black", labels = round(bfast$conf.int[2], 3))
# tacotron (right side)
text(2.15, btaco$estimate, col = "green", labels = round(btaco$estimate, digits=3))
text(2.15, p_original_taco_preferred, col = "chartreuse4", labels = p_original_taco_preferred)
text(1.85, btaco$conf.int[1], col = "black", labels = round(btaco$conf.int[1], 3))
text(1.85, btaco$conf.int[2], col = "black", labels = round(btaco$conf.int[2], 3))
dev.off()

# Transposed order
jpeg(file="plots/binomial_test_transposed.jpeg")
bfast <- binom.test(x = sum(fs_daten$x > 0.5), n = nrow(fs_daten), p = p_original_taco_preferred)
btaco <- binom.test(x = sum(taco_daten$x > 0.5), n = nrow(taco_daten), p = p_original_fs_preferred)
plot(0,0, type = "n", ylim = c(0,1), xlim = c(0.5,2.5), las = 1, xlab = "System",
     ylab = "Agreement Ratio", xaxt = "n")
axis(1, c(1,2), c("Fastspeech","Tacotron"))
points(2,bfast$estimate, pch = 19, col = "blue")
points(1,p_original_fs_preferred, pch = 17, col = "darkblue")
arrows(2,bfast$conf.int[1],2,bfast$conf.int[2], angle = 90, length = 0.1, code = 3)
points(1,btaco$estimate, pch = 19, col = "green")
points(2,p_original_taco_preferred, pch = 17, col = "chartreuse4")
arrows(1,btaco$conf.int[1],1,btaco$conf.int[2], angle = 90, length = 0.1, code = 3)
# Add values as labels
# fastspeech (right side)
text(2.15, bfast$estimate, col = "blue", labels = round(bfast$estimate, digits=3))
text(1.15, p_original_fs_preferred, col = "darkblue", labels = p_original_fs_preferred)
text(1.85, bfast$conf.int[1], col = "black", labels = round(bfast$conf.int[1], 3))
text(1.85, bfast$conf.int[2], col = "black", labels = round(bfast$conf.int[2], 3))
# tacotron (left side)
text(1.15, btaco$estimate, col = "green", labels = round(btaco$estimate, digits=3))
text(2.15, p_original_taco_preferred, col = "chartreuse4", labels = p_original_taco_preferred)
text(0.85, btaco$conf.int[1], col = "black", labels = round(btaco$conf.int[1], 3))
text(0.85, btaco$conf.int[2], col = "black", labels = round(btaco$conf.int[2], 3))
dev.off()



# Binomial Test repeat results per-person vs original results
# Fastspeech
binom.test(x = sum(fs_daten$x > 0.5), n = nrow(fs_daten), p = p_original_fs_preferred)
#binom.test(x = sum(fs_daten$x > p_original_fs_preferred), n = nrow(fs_daten))

# Fastspeech Transposed
binom.test(x = sum(fs_daten$x > 0.5), n = nrow(fs_daten), p = p_original_taco_preferred) # transposed

# Tacotron
binom.test(x = sum(taco_daten$x > 0.5), n = nrow(taco_daten), p = p_original_taco_preferred)

# Tacotron Transposed
binom.test(x = sum(taco_daten$x > 0.5), n = nrow(taco_daten), p = p_original_fs_preferred) # transposed


# Binomial Test repeat results per-person preference data vs repeat results aggregated preference
# Fastspeech
binom.test(x = sum(fs_daten$x > 0.5), n = nrow(fs_daten), p = 0.29)

# Tacotron
binom.test(x = sum(taco_daten$x > 0.5), n = nrow(taco_daten), p = 0.5)



#### Evaluation 2 ###

# Mixed effect model
library("lme4")
fit <- glmer(Response ~  Method + (1|Person), data = form_data,
             family = "binomial")
summary(fit)


## Explanation & additional info
# Model formula
# Y = 1 = proposed better than baseline
# log(Odds) = log(P(Y = 1)/(1 - P(Y = 1))) = b0 + b1*Methodtacotron + pi
# Methodtacotron = binary variable: 1 if Method = tacotron, 0 if Method = fastspeech
b0 = -0.00036 # from output of summary(fit)
b1 = -0.95558 # from output of summary(fit)
# pi = random effect for each person. Each person’s random effect is assumed
#       to be drawn from a normal distribution with mean 0 and standard deviation 0.5222 (variance = 0.2727)

# Interpretation:
# With odds via coefficients:
exp(-0.955)
# The odds of "method is better than baseline" is about 0.3848 times lower for the tacotron questions than
# the corresponding odds for the fastspeech questions
# Mathematically:
# odds_tacotron = exp(b0) * exp(b1) * exp(pi)
# odds_fastspeech = exp(b0) * exp(pi)
# -> odds_tacotron  = odds_fastspeech * exp(-0.955) = odds_fastspeech * 0.3848
# 95% Confidence Interval for difference in odds:
exp(confint(fit, parm = "Methodtacotron")) 

# With probabilities:
# Predicted mean probabilities (P(Y = 1)) for each method:
predict(fit, type = "response",  re.form = NA,
        newdata = data.frame(Method = c("fastspeech", "tacotron")))
# Fastspeech: P(Y = 1) = P(Y = "Proposed better than baseline") = 0.4999094
# Tacotron: P(Y = 1) = 0.2776920 

odds_tacotron = exp(b0) * exp(b1) * exp(pi)
exp(b0 + pi)

