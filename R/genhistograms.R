#!/usr/bin/env Rscript

## installing R dependencies
if("png" %in% rownames(installed.packages()) == FALSE) {install.packages("png")}
if("grid" %in% rownames(installed.packages()) == FALSE) {install.packages("grid")}
if("gridExtra" %in% rownames(installed.packages()) == FALSE) {install.packages("gridExtra")}

args = commandArgs(trailingOnly=TRUE)
filename=args[1]
title=args[2]
outputfile=args[3]

# Create data for the graph.
dat = readLines(filename)
dat <- as.numeric(dat)

# Give the chart file a name.
png(file = paste("../docs/", outputfile, ".png", sep=""))

# Create the histogram
hist(dat, xlab = "csindexbr score", col = "yellow", border = "blue", main=title, breaks=10)

# Save the file.
dev.off()