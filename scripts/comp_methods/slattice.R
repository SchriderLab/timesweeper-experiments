#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

library(readr)
library(slattice)

df <- read_csv(args[1], col_names=c("N", "N.A"))

estimate <- estimate.s(df, 500, method="Soft EM")

fileConn<-file(paste0(args[1], ".out"))
writeLines(as.character(estimate$s), fileConn)
close(fileConn)