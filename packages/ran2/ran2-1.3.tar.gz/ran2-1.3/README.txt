RAN2

Python port of the ran2 random number generator from FORTRAN NUMERICAL RECIPES.
Long period (> 2 × 1018) random number generator of L’Ecuyer with Bays-Durham shuffle
and added safeguards. Returns a uniform random deviate between 0.0 and 1.0 (exclusive of
the endpoint values). Call with iseed, a "large" negative number to initialize.


EXAMPLE:

Create a random seed. Must be a "large" negative number

iseed = -12345678

Initialize the wrapper with that iseed. 
Each class instance can use a different seed to get a different sequence

x = ran2_wrapper(iseed)

Call the random number generator

x.ran2()