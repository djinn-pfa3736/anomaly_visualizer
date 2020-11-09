CalcSlidingWindowDataMat <- function(wave.vec, start.idx, end.idx, interval.len) {

	data.mat <- as.vector(NULL)
	for(i in start.idx:(end.idx - interval.len + 1)) {
		data.vec <- wave.vec[i:(i + interval.len - 1)]
		data.mat <- rbind(data.mat, data.vec)
	}

	return(data.mat)
}