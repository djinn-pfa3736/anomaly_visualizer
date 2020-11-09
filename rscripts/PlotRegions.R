PlotRegions <- function (wave.vec, idx.vec, interval.len, range.interval) {

	source("PlotAnomaryRegions.R")

	for(i in seq(1, length(wave.vec) - interval.len + 1, by=range.interval)) {
		png(paste(i, ".png", sep=""))
		PlotAnomaryRegion(wave.vec, idx.vec, interval.len, c(i, i + (range.interval - 1)))
		dev.off()
	}

}