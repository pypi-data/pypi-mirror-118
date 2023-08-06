data {
    int<lower=1> num_permus;
    int<lower=2> num_algorithms;
    int permus [num_permus, num_algorithms]; 
    real alpha; 
    real beta;
}

parameters {
    simplex[num_algorithms] ratings;
}
 
transformed parameters {
  real loglik;
  real rest;
  
  loglik = 0;
  for (s in 1:num_permus){
    for (i in 1:(num_algorithms - 1)) {
      rest = 0;

      for (j in i:num_algorithms) {
        rest = rest + ratings[permus[s, j]];
      }

      loglik = loglik + log(ratings[permus[s, i]] / rest);
    }
  }
}
 
model {
    for (i in 1:num_algorithms) {
        ratings[i] ~ gamma(alpha, beta);
    }

    target += loglik;
}