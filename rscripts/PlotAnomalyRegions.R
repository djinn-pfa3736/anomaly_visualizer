PlotAnomalyRegion <- function(wave.vec, idx.vec, interval.len, plot.range) {

	plot(wave.vec, type="l", xlim=plot.range)
	for(i in 1:length(idx.vec)) {
		for(j in 0:(interval.len-1)) {
			lines(c(idx.vec[i]+j, idx.vec[i]+j+1), c(wave.vec[idx.vec[i]+j], wave.vec[idx.vec[i]+j+1]), lwd=2, col="red", xlim=plot.range)
		}
	}

}