UtilizeCCAByInterval <- function(wave.vec, start.idx1, start.idx2, data.len, interval.len) {

	library(CCA)

	source("CalcSlidingWindowDataMat.R")
	data.mat1 <- CalcSlidingWindowDataMat(wave.vec, start.idx1, start.idx1 + data.len, interval.len)
	data.mat2 <- CalcSlidingWindowDataMat(wave.vec, start.idx2, start.idx2 + data.len, interval.len)

	cc.res <- cc(data.mat1, data.mat2)

	return(cc.res)
}