CalcCCAVec <- function(wave.vec, data.len, interval.len, start.idx, end.idx) {
	source("UtilizeCCAByInterval.R")

	ccor.vec <- as.vector(NULL)
	for(i in start.idx:(end.idx - data.len - 1)) {
		cc.res <- UtilizeCCAByInterval(wave.vec, i, i + data.len + 1, data.len, interval.len)
		ccor.vec <- c(ccor.vec, max(cc.res$cor))
	}

	return(ccor.vec)
}