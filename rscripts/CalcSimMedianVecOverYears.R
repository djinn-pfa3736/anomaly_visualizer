CalcSimMedianVecOverYears <- function(wave.vec, start.idx, end.idx, year.count, interval.len, search.len, method) {
	source("CalcSimVecInterval.R")

	median.sim.vec <- as.vector(NULL)
	for(s in start.idx:(end.idx - interval.len + 1)) {
		sim.vec <- as.vector(NULL)
		for(y in year.count:1) {
			tmp.vec <- CalcSimVecInterval(wave.vec, s, s - 365*y - search.len, s - 365*y + search.len - 1, interval.len, method)
			sim.vec <- c(sim.vec, tmp.vec)
		}
		median.sim.vec <- c(median.sim.vec, median(sim.vec))
	}

	return(median.sim.vec)
}