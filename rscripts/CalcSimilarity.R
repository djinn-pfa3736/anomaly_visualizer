CalcSimilarity <- function(wave1, wave2, method="cor") {

  result <- -1
  if(method == "cor") {
  	result <- cor(wave1, wave2)
  } else if(method == "fft") {
  	fft.res1 <- fft(wave1)
  	fft.res2 <- fft(wave2)
  	
  	result <- sqrt(sum((Mod(fft.res1) - Mod(fft.res2))^2))
  	# if(result == 0) {
  	# 	result <- 10
  	# } else {
  	# 	result <- 1/result
  	# }

    # result <- cor(Mod(fft.res1), Mod(fft.res2))

  } else if(method == "euc") {
    result <- sqrt(sum((wave1 - wave2)^2))
  } else if(method == "norm") {
    wave1 <- wave1 - mean(wave1)
    wave2 <- wave2 - mean(wave2)
    result <- sqrt(sum((wave1 - wave2)^2))
  } else if(method == "abs") {
    result <- abs(sum(wave1 - wave2))
  }

  return(result)
}