PlotTrajectory <- function(points.mat, interval.len) {
	library(rgl)

	plot3d(points.mat)
	browser()
	for(i in 2:(nrow(points.mat) - interval.len + 1)) {
		points3d(points.mat)
		lines3d(points.mat[i:(i+interval.len-1),1], points.mat[i:(i+interval.len-1),2], points.mat[i:(i+interval.len-1),3], col="red", lwd=5)

		file.name <- paste(formatC(i, width=4, flag="0"), ".png", sep="")
		rgl.snapshot(file.name)
		rgl.clear()
	}
}