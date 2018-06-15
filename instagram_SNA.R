
library("visNetwork")
library("sqldf")
library("dbConnect")

Sys.setlocale(category = "LC_ALL", locale = "zh_TW.UTF-8")

main <- read.csv("/Users/mars/Desktop/IG_follow_info.csv", header=T, as.is=T)
rela <- read.csv("/Users/mars/Desktop/IG_follow_link.csv", header=T, as.is=T)

main$title <- paste0('<b>', main$id, '</b><br>Account: ', main$account, '<br>Name: ', main$name)
main$label <- main$account
main$size <- 3
main$borderWidth <- 1

main$color.background <- "slategrey"
main$color.border <- "#364156"
main$color.highlight.background <- 'orange'
main$color.highlight.border <- "darkred"

rela$smooth <- TRUE
#rela$arrows <- 'to'
#rela$length <- 300

visNetwork(main, rela, height="800px", width="100%") %>%
		   visOptions(highlightNearest = TRUE,
			          nodesIdSelection = TRUE) %>%
		   visInteraction(dragNodes = FALSE, dragView = TRUE, zoomView = TRUE)