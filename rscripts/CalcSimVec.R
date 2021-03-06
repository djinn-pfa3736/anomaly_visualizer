CalcSimVec <- function(wave.vec, start.idx, interval.len, search.len, method) {

	source("./rscripts/CalcSimilarity.R")

	sim.vec <- as.vector(NULL)
	target.wave <- wave.vec[start.idx:(start.idx + interval.len - 1)]

	for(i in (start.idx - search.len + 1):(start.idx - 1)) {
		ref.wave <- wave.vec[i:(i + interval.len - 1)]

		sim.vec <- c(sim.vec, CalcSimilarity(target.wave, ref.wave, method))
	}

	return(sim.vec)
}