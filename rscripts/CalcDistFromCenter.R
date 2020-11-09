CalcDistFromCenter <- function(data.mat) {

	center.vec <- apply(data.mat, 2, median)
	dist.vec <- apply(data.mat, 1, function(x) {
			return(sqrt(sum((x - center.vec)^2)));
		})

	return(dist.vec)
}