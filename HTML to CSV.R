# Load necessary libraries
library(rvest)
library(data.table)

folder <- "C:/Mantovani/Careers/Football Manager 2023/PythonFM/Switzerland/raw/"

atts_html_path <- paste(folder, "atts.html", sep = "")
atts_csv_path <- paste(folder, "atts.csv", sep = "")
stats_html_path <- paste(folder, "stats.html", sep = "")
stats_csv_path <- paste(folder, "stats.csv", sep = "")

########################################################

atts_html_content <- read_html(atts_html_path, encoding = "UTF-8")

atts_table <- atts_html_content %>% 
  html_nodes("table") %>%
  html_table(fill = TRUE)

atts_data <- atts_table[[1]]

fwrite(atts_data, file = atts_csv_path, sep = ";", quote = TRUE)

########################################################

stats_html_content <- read_html(stats_html_path, encoding = "UTF-8")

stats_table <- stats_html_content %>% 
  html_nodes("table") %>%
  html_table(fill = TRUE, dec=",")

stats_data <- stats_table[[1]]
stats_data <- apply(stats_data, 2, function(x) ifelse(x == "-", 0, x))
stats_data <- as.data.frame(stats_data)
stats_data$Mins <- gsub("\\.", "", as.character(stats_data$Mins))
stats_data$`Pas A` <- gsub("\\.", "", stats_data$`Pas A`)
stats_data$`Ps C` <- gsub("\\.", "", stats_data$`Ps C`)
stats_data$`Sprints/90` <- gsub("\\,", "\\.", stats_data$`Sprints/90`)
stats_data$`xGP` <- gsub("\\,", "\\.", stats_data$`xGP`)
stats_data$`Hdrs A` <- gsub("\\.", "", stats_data$`Hdrs A`)
stats_data$`Hdrs` <- gsub("\\.", "", stats_data$`Hdrs`)
stats_data$`Clear` <- gsub("\\,", "\\.", stats_data$`Clear`)

fwrite(stats_data, file = stats_csv_path, sep = ";", quote = TRUE)