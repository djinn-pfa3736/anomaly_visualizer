CalcSimMedianVec <- function(wave.vec, start.idx, end.idx, interval.len, search.len, method) {
	source("CalcSimVec.R")

	median.sim.vec <- as.vector(NULL)
	for(s in start.idx:(end.idx - interval.len + 1)) {
		sim.vec <- CalcSimVec(wave.vec, s, interval.len, search.len, method)
		
		if(s == 172 || (s - start.idx) == 100 || (s - start.idx) == 200) {
		# if(median(sim.vec) < -0.1) {
			browser()
		}
		median.sim.vec <- c(median.sim.vec, median(sim.vec))
	}

	return(median.sim.vec)
}