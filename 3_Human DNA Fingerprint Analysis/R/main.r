#!/d/vscode/compiler/R-4.2.2/bin/Rscript
rm(list=ls())

# Set working directory
setwd("F://Onedrive//study//生物//遗传学//实验报告//3_人类DNA指纹分析//R")

# Get all CSV files in the ./data/ folder, excluding summary.csv
csv_files <- list.files(path = "../data", pattern = "\\.csv$", full.names = TRUE)
csv_files <- csv_files[!grepl("summary\\.csv$", csv_files)]

# Import CSV files in batch
data_list <- lapply(csv_files, function(file) {
  read.csv(file, stringsAsFactors = FALSE)  # Use read.csv or read.csv2 based on the CSV file format
})

# Display the imported data
#for (i in seq_along(data_list)) {
#  cat("Data from file", csv_files[i], ":\n")
#  print(data_list[[i]])
#}

# define data edge
edge <- 0

# Create an empty data frame for the results
result_df <- 
  data.frame(
    File = character(),
    Lane = numeric(),
    Category = character(),
    MW = character(),
    RepeatNum = character(),
    homoORheter = character(),
    stringsAsFactors = FALSE
  )

# Loop through each imported data file
for (i in seq_along(data_list)) {
  # Loop through unique Lane values in the current file
  for (j in unique(data_list[[i]]$Lane..)) {
    # Check if the maximum Band value for the current Lane is 11
    if (max(data_list[[i]]$Band..[data_list[[i]]$Lane.. == j]) == 11) {
      # Add a row to the result_df for marker
      result_df <- 
        rbind(
          result_df,
          data.frame(
            File = csv_files[i],
            Lane = j,
            Category = "marker",
            MW = NA,
            RepeatNum = NA,
            homoORheter = NA
          )
        )
    } else {
      # Calculate repeat_num based on MW values
      repeat_num <- 1 + (data_list[[i]]$MW[data_list[[i]]$Lane.. == j & data_list[[i]]$MW > edge] - 161) / 16
      # Check if there are MW values greater than edge
      if (length(repeat_num) > 0) {
        MW_values <- data_list[[i]]$MW[data_list[[i]]$Lane.. == j & data_list[[i]]$MW > edge & repeat_num > 0]
        # Check the number of MW values and determine homo/hetero/contamination
        if(length(data_list[[i]]$MW[data_list[[i]]$Lane.. == j & data_list[[i]]$MW > edge & repeat_num > 0]) == 0) {
          hh <- "no result"
        } else if(length(data_list[[i]]$MW[data_list[[i]]$Lane.. == j & data_list[[i]]$MW > edge & repeat_num > 0]) == 1) {
          hh <- "homo"
        } else if(length(data_list[[i]]$MW[data_list[[i]]$Lane.. == j & data_list[[i]]$MW > edge & repeat_num > 0]) == 2) {
          hh <- "heter"
        } else if(length(data_list[[i]]$MW[data_list[[i]]$Lane.. == j & data_list[[i]]$MW > edge & repeat_num > 0]) > 2) {
          hh <- "contamination"
        } else {
          hh <- "???"
        }
        # Add a row to the result_df for unidentified bands
        result_df <- 
          rbind(
            result_df,
            data.frame(
              File = csv_files[i],
              Lane = j,
              Category = "target bands",
              MW = paste(as.character(MW_values), collapse = ", "),
              RepeatNum = paste(as.character(repeat_num[repeat_num > 0]), collapse = ", "),
              homoORheter = hh
            )
          )
      }
    }
  }
}

# Print the final result_df
tail(result_df)

table(result_df$homoORheter)

data <- result_df[(result_df$homoORheter == "homo" | result_df$homoORheter == "heter") & result_df$Category == "target bands", ]
table(data$homoORheter)

library(ggplot2)

convert_string_to_coordinates <- function(input_string) {
  split_values <- strsplit(input_string, ", ")[[1]]
  numeric_values <- as.numeric(split_values)
  return(numeric_values)
}

class(convert_string_to_coordinates("1, 2"))

data$Lane <- sapply(data$Lane,as.factor)
data$MW_num <- sapply(data$MW, convert_string_to_coordinates)
data$MW_num <- sapply(data$MW, unlist)
data$RepeatNum_num <- sapply(data$RepeatNum, convert_string_to_coordinates)
data$RepeatNum_num <- sapply(data$RepeatNum_num, unlist)

test <- data[data$File=="../data/data1.csv",]

ggplot(test, aes(x = Lane, y = RepeatNum_num)) +
  geom_point(size = 3)
