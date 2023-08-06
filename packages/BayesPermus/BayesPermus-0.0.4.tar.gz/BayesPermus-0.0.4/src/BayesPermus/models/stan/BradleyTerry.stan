functions {
    
   real calculate_prob(int num_algorithms, int[] permu, vector ratings) {
       real prob = 1;

       for (i in 1:num_algorithms) {
           for (j in (i + 1):num_algorithms) {
               prob = prob * ratings[permu[i]];
           }
       }

       return prob;
   }

   real calculate_constant(int num_algorithms, vector ratings) {
       
      // Heap algorithm to generate every possible permutation

      int c[num_algorithms];
      int permu[num_algorithms];
      int i;
      int aux;
      real result = 0;

      for (k in 1:num_algorithms) {
          c[k] = 1;
          permu[k] = k;
      }

      result = result + calculate_prob(num_algorithms, permu, ratings);

      i = 2;
      while (i <= num_algorithms) {
        if (c[i] < i) {
            if (i % 2 != 0) {
                aux = permu[1];
                permu[1] = permu[i];
                permu[i] = aux;
            } else {
                aux = permu[c[i]];
                permu[c[i]] = permu[i];
                permu[i] = aux;
            }

          result = result + calculate_prob(num_algorithms, permu, ratings);

          c[i] += 1;
          i = 2;
        } else {
            c[i] = 1;
            i += 1;
        }
      }

      return result;
    }
}

data {
    int<lower=1> num_permus;
    int<lower=2> num_algorithms;
    int permus [num_permus, num_algorithms];
    vector[num_algorithms] alpha;
}

parameters {
    simplex[num_algorithms] ratings;
}
 
transformed parameters {
  real loglik;
  real rest;
  real constant = calculate_constant(num_algorithms, ratings);
  
  loglik = 0;
  for (s in 1:num_permus){
    rest = 1;
    for (i in 1:(num_algorithms - 1)) {
      for (j in (i + 1):num_algorithms) {
        rest = rest * ratings[permus[s, i]];
      }
    }

    loglik = loglik + log(rest / constant);
  }
}
 
model {
    ratings ~ dirichlet(alpha);
    target += loglik;
}