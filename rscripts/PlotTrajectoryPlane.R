PlotTrajectoryPlane <- function(points.mat, interval.len) {

	for(i in 2:(nrow(points.mat) - interval.len + 1)) {
		file.name <- paste(formatC(i, width=4, flag="0"), ".png", sep="")
		png(file.name)
		plot(points.mat)
		lines(points.mat[i:(i+interval.len-1),1], points.mat[i:(i+interval.len-1),2], col="red", lwd=5)
		dev.off()
	}
}