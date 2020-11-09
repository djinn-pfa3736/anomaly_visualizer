CalcFFTMat <- function(wave.vec, interval.len) {

	fft.mat <- as.vector(NULL)
	for(i in 1:(length(wave.vec) - interval.len + 1)) {
		target.wave <- wave.vec[i:(i + interval.len - 1)]
		fft.res <- fft(target.wave)
		fft.mat <- rbind(fft.mat, Mod(fft.res))
	}

	return(fft.mat)
}