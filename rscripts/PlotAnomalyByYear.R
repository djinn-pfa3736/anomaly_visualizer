PlotAnomalyByYear <- function(wave.vec, anomary.date.vec, date.vec, interval.len, plot.interval) {

	for(i in 1:length(anomary.date.vec)) {

		anomary.date <- anomary.date.vec[i]
		idx <- which(anomary.date == date.vec)
		file.name <- paste(as.character(anomary.date), ".png", sep="")
		png(file.name)
		plot(wave.vec[(idx - plot.interval + 1):(idx + plot.interval)], type="l", xlab="", ylab="")
		plot.idx <- floor(length((idx - plot.interval + 1):(idx + plot.interval))/2)
		for(j in 0:(interval.len-1)) {
			lines(c(plot.idx+j, plot.idx+j+1), c(wave.vec[idx+j], wave.vec[idx+j+1]), lwd=2, col="red")
		}
		dev.off()
	}

}