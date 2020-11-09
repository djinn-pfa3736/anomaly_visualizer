ApplyBandpassFilter <- function(wave.vec, freq.sample, filter.low, filter.high) {

	library(signal)

	filter.N <- 2

	butterworth.filter <- signal::butter(filter.N, c(filter.low, filter.high)/(freq.sample/2), type="pass", plane="z")
	filtered.wave <- signal::filtfilt(butterworth.filter, wave.vec)

	return(filtered.wave)
}