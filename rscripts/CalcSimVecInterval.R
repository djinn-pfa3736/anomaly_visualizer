CalcSimVecInterval <- function(wave.vec, start.idx, search.start.idx, search.end.idx, interval.len, method) {

	source("CalcSimilarity.R")

	sim.vec <- as.vector(NULL)
	for(i in search.start.idx:(search.end.idx - interval.len + 1)) {
		target.wave <- wave.vec[start.idx:(start.idx + interval.len - 1)]
		ref.wave <- wave.vec[i:(i + interval.len - 1)]

		sim.vec <- c(sim.vec, CalcSimilarity(target.wave, ref.wave, method))
	}

	return(sim.vec)
}