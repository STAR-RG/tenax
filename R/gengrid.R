#!/usr/bin/env Rscript

library(png)
library(grid)
library(gridExtra)

pdf(file="../docs/grid.pdf")

grid.arrange(
   rasterGrob(readPNG('../docs/pq1a.png')),
   rasterGrob(readPNG('../docs/pq1b.png')),
   rasterGrob(readPNG('../docs/pq1c.png')),
   rasterGrob(readPNG('../docs/pq1d.png')),
   rasterGrob(readPNG('../docs/pq2.png')),
   rasterGrob(readPNG('../docs/sembolsa.png')),
   ncol=2)