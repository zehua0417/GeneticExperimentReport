#!/usr/bin/Rscrip
## -*- coding: utf-8 -*-
rm(list = ls())

# data input -------------------------------------------------------------------
total.data <- read.csv(file =
                  "../data/GeneticsLabExperiment-HumanTraitStatistics-2023.csv",
                       na.strings = "")
total.data$ID <- seq(length.out = nrow(total.data))
total.data <- total.data[, c("ID", 
    names(total.data)[-which(names(total.data) == "ID")])]
head(total.data)

# 1. ABO血型遗传分析 -----------------------------------------------------------
##' @brief blood.data ABO Blood Class
#' @slot blood.count data.frame
#>        | XX | count | frequency | phenotypicfrequency |
#>        | A  |  ...  |    ...    |          ...        |
#>        | B  |  ...  |    ...    |          ...        |
#>        | AB |  ...  |    ...    |          ...        |
#>        | O  |  ...  |    ...    |          ...        |
#'
setClass(
  Class = "blood.data",
  slots = list(
    stu.num = "numeric",              # Number of students
    blood.data.raw = "data.frame",    # Raw blood type data
    blood.count = "data.frame",       # Processed blood type count data
    p.raw = "numeric",                # Uncorrected frequency of blood type A
    q.raw = "numeric",                # Uncorrected frequency of blood type B
    r.raw = "numeric",                # Uncorrected frequency of blood type O
    D = "numeric",                    # Correction factor D
    p = "numeric",                    # Corrected frequency of blood type A
    q = "numeric",                    # Corrected frequency of blood type B
    r = "numeric"                     # Corrected frequency of blood type O
  )
)

##' @brief constructor
#' @param data data.frame("ID", "ABO血型",...)
#' @return .Object
#' 
setMethod(
  f = "initialize",
  signature = "blood.data",
  definition = function(.Object, data) {
    blood.data.raw <- data[, c("ID", "ABO血型")]  # Extract relevant columns
    abo.count <- table(data$ABO血型)      # Count occurrences of each blood type
    # Calculate the number of students   
    stu.num <- abo.count["A"] + abo.count["B"] + abo.count["AB"] + abo.count["O"]
    blood.count <- data.frame(
      count = c(abo.count["A"], abo.count["B"], abo.count["O"],
                abo.count["AB"]),
      frequency = c(abo.count["A"]/stu.num, abo.count["B"]/stu.num,
                    abo.count["O"]/stu.num, abo.count["AB"]/stu.num)
    )
    # Calculate uncorrected frequencies and correction factor D
    p.raw <- 1 - sqrt(blood.count["A", 2] + blood.count["O", 2])
    q.raw <- 1 - sqrt(blood.count["B", 2] + blood.count["O", 2])
    r.raw <- sqrt(blood.count["O", 2])
    D <- 1 - p.raw - q.raw - r.raw
    # Calculate corrected frequencies
    p <- p.raw * (1 + 0.5 * D)
    q <- q.raw * (1 + 0.5 * D)
    r <- (r.raw + 0.5 * D) * (1 + 0.5 * D)
    
    # Calculate phenotypic frequencies based on corrected frequencies
    blood.count <- data.frame(
      count = blood.count$count,
      frequency = blood.count$frequency,
      phenotypicfrequency = c(p^2 + 2*p*r, q^2 + 2*q*r, r^2, 2*p*q)
    )
    
    # Assign values to slots of the blood.data object
    .Object@stu.num <- stu.num
    .Object@blood.data.raw <- blood.data.raw
    .Object@blood.count <- blood.count
    .Object@p.raw <- p.raw
    .Object@q.raw <- q.raw
    .Object@r.raw <- r.raw
    .Object@D <- D
    .Object@p <- p
    .Object@q <- q
    .Object@r <- r
    
    return(.Object)
  }
)

## Define a generic function for chi-square test
setGeneric(
  name = "chi.square.test",
  def = function(object) standardGeneric("chi.square.test")
)
## Define class method for the blood.data class to perform chi-square test
##' @brief chi.square.test
#' @return list(chi.square.result, p.value)
setMethod(
  f = "chi.square.test",
  signature = "blood.data",
  definition = function(object) {
    # Perform chi-square test using observed counts and expected frequencies
    chisq.result <- chisq.test(x = object@blood.count$count, 
                               p = object@blood.count$phenotypicfrequency,
                               rescale = TRUE)
    
    # Calculate p-value using the chi-square distribution
    p.value <- pchisq(chisq.result$statistic, df = 2,
                      lower.tail = FALSE)
    
    # Print the chi-square test result
    cat("Chi-Square Test:\n")
    print(chisq.result)
    cat("\nP-value:", p.value, "\n")
    
    # Return the chi-square test result
    return(list(chi.square.result = chisq.result, p.value = p.value))
  }
)
#' ***************************************************************************

# Create an instance of the blood.data class using the constructor
blood.data <- new("blood.data", data = total.data)
blood.data@blood.count

# Run the chi-square test method on the blood.data object
blood.data.result <- chi.square.test(blood.data)

# 2. 人类部分单基因性状的遗传分析 ----------------------------------------------
head(total.data)
counts_list <- lapply(total.data[, names(total.data)[-1]], table)

print(counts_list)

count_list$耳垂