PlotAnomalyOverYear <- function(wave.vec, anomary.date.vec, date.vec, interval.len, plot.interval, year.count) {

	for(i in 1:length(anomary.date.vec)) {

		anomary.date <- anomary.date.vec[i]
		idx <- which(anomary.date == date.vec)
		file.name <- paste(as.character(anomary.date), ".png", sep="")

		max.val <- -10000
		min.val <- 10000
		for(k in year.count:1) {
			tmp.max.val <- max(wave.vec[(idx - plot.interval + 1 - 365*k):(idx + plot.interval - 365*k)])
			tmp.min.val <- min(wave.vec[(idx - plot.interval + 1 - 365*k):(idx + plot.interval - 365*k)])

			max.val <- max(max.val, tmp.max.val)
			min.val <- min(min.val, tmp.min.val)
		}

		sub.data.mat <- as.vector(NULL)
		png(file.name)
		for(k in year.count:1) {
			plot(wave.vec[(idx - plot.interval + 1 - 365*k):(idx + plot.interval - 365*k)], type="l", xlab="", ylab="", ylim=c(min.val, max.val))
			par(new=TRUE)
			sub.data.mat <- rbind(sub.data.mat, wave.vec[(idx - plot.interval + 1 - 365*k):(idx + plot.interval - 365*k)])
		}
		plot(wave.vec[(idx - plot.interval + 1):(idx + plot.interval)], type="l", xlab="", ylab="", ylim=c(min.val, max.val), col="orange")
		sub.data.mat <- rbind(sub.data.mat, wave.vec[(idx - plot.interval + 1):(idx + plot.interval)])
		
		write.csv(t(sub.data.mat), file=paste(anomary.date, ".csv", sep=""))

		plot.idx <- floor(length((idx - plot.interval + 1):(idx + plot.interval))/2)
		for(j in 0:(interval.len-1)) {
			lines(c(plot.idx+j, plot.idx+j+1), c(wave.vec[idx+j], wave.vec[idx+j+1]), lwd=2, col="red", ylim=c(min.val, max.val))
		}
		dev.off()
	}

}