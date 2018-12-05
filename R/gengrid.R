#!/usr/bin/env Rscript

library(png)
library(grid)
library(gridExtra)

pdf(file="../data/grid.pdf")

grid.arrange(
   rasterGrob(readPNG('../data/pq1a.png')),
   rasterGrob(readPNG('../data/pq1b.png')),
   rasterGrob(readPNG('../data/pq1c.png')),
   rasterGrob(readPNG('../data/pq1d.png')),
   rasterGrob(readPNG('../data/pq2.png')),
   rasterGrob(readPNG('../data/sembolsa.png')),
   ncol=2)