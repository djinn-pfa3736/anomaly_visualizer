CalcDiffMat <- function(data.mat) {

	diff.mat <- as.vector(NULL)
	for(i in 1:(nrow(data.mat)-1)) {
		diff.mat <- rbind(diff.mat, data.mat[i+1,] - data.mat[i,])
	}

	return(diff.mat)
}