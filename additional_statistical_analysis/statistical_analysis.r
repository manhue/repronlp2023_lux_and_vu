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

# Distribution Analysis

# Boxplots
jpeg(file="plots/boxplot_fastspeech.jpeg")
boxplot(fs_daten$x, ylim = c(0,1), col="#49A4B9",
        main = "Preference for Fastspeech-proposed", ylab = "agreement ratio", notch = TRUE)
abline(h = p_original_fs_preferred, col = "blue", lwd = 2) # Vergleichswert von Studie A
text(0.7,p_original_fs_preferred, pos = 1, "Original study", col = "blue")
dev.off()

jpeg(file="plots/boxplot_fastspeech_absline_transposed.jpeg")
boxplot(fs_daten$x, ylim = c(0,1), col="#49A4B9",
        main = "Preference for Fastspeech-proposed", ylab = "agreement ratio", notch = TRUE)
abline(h = p_original_taco_preferred, col = "blue", lwd = 2) # Vergleichswert von Studie A
text(0.7,p_original_taco_preferred, pos = 1, "Original study", col = "blue")
dev.off()

jpeg(file="plots/boxplot_taco.jpeg")
boxplot(taco_daten$x, ylim = c(0,1), col="#49A4B9",
        main = "Preference for Tacotron-proposed", ylab = "agreement ratio", notch = TRUE)
abline(h = p_original_taco_preferred, col = "blue", lwd = 2) # Vergleichswert von Studie A
text(0.7,p_original_taco_preferred, pos = 1, "Original study", col = "blue")
dev.off()

jpeg(file="plots/boxplot_taco_absline_transposed.jpeg")
boxplot(taco_daten$x, ylim = c(0,1), col="#49A4B9",
        main = "Preference for Tacotron-proposed", ylab = "agreement ratio", notch = TRUE)
abline(h = p_original_fs_preferred, col = "blue", lwd = 2) # Vergleichswert von Studie A
text(0.7,p_original_fs_preferred, pos = 1, "Original study", col = "blue")
dev.off()


# Histogramms
jpeg(file="plots/histogram_fastspeech.jpeg")
hist(fs_daten$x,  xlim = c(0,1), col="#49A4B9",
     main = "Preference for Fastspeech-proposed: Histogram", ylab = "Number of evaluators",
     xlab = "Preference for FS-proposed", breaks = seq(0,1,0.05))
abline(v = p_original_fs_preferred, col = "blue", lwd = 2) # Vergleichswert von Studie A
text(0.7,p_original_fs_preferred, pos = 1, "Original study", col = "blue")
dev.off()

jpeg(file="plots/histogram_fastspeech_abline_transposed.jpeg")
hist(fs_daten$x,  xlim = c(0,1), col="#49A4B9",
     main = "Preference for Fastspeech-proposed: Histogram", ylab = "Number of evaluators",
     xlab = "Preference for FS-proposed", breaks = seq(0,1,0.05))
abline(v = p_original_taco_preferred, col = "blue", lwd = 2) # Vergleichswert von Studie A
text(0.7,p_original_taco_preferred, pos = 1, "Original study", col = "blue")
dev.off()


jpeg(file="plots/histogram_taco.jpeg")
hist(taco_daten$x,  xlim = c(0,1), col="#49A4B9",
     main = "Preference for Tacotron-proposed: Histogram", ylab = "Number of evaluators",
     xlab = "Preference Taco-proposed", breaks = seq(0,1,0.05))
abline(v = p_original_taco_preferred, col = "blue", lwd = 2) # Vergleichswert von Studie A
text(0.7,p_original_taco_preferred, pos = 1, "Original study", col = "blue")
dev.off()

jpeg(file="plots/histogram_taco_abline_transposed.jpeg")
hist(taco_daten$x,  xlim = c(0,1), col="#49A4B9",
     main = "Preference for Tacotron-proposed: Histogram", ylab = "Number of evaluators",
     xlab = "Preference Taco-proposed", breaks = seq(0,1,0.05))
abline(v = p_original_fs_preferred, col = "blue", lwd = 2) # Vergleichswert von Studie A
text(0.7,p_original_fs_preferred, pos = 1, "Original study", col = "blue")
dev.off()



# Vorzeichentest
# Fastspeech
binom.test(x = sum(fs_daten$x > 0.5), n = nrow(fs_daten), p = p_original_fs_preferred)
#binom.test(x = sum(fs_daten$x > p_original_fs_preferred), n = nrow(fs_daten))

# Fastspeech Transposed
binom.test(x = sum(fs_daten$x > 0.5), n = nrow(fs_daten), p = p_original_taco_preferred) # transposed

# Tacotron
binom.test(x = sum(taco_daten$x > 0.5), n = nrow(taco_daten), p = p_original_taco_preferred)

# Tacotron Transposed
binom.test(x = sum(taco_daten$x > 0.5), n = nrow(taco_daten), p = p_original_fs_preferred) # transposed



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

