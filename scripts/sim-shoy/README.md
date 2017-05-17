# Monte Carlo simulation of SHOY format

The code in this directory is to simulate the current format of the SHOY, and wonder about the risks of day 1

The current assumptions are made in creating these simulations:

## Description of tournament format

To remind, there are 18 teams playing in this tournament, and 6 pools of three teams start day 1 by playing one another.  Once each team has played everyone in their pool (2 games), teams are reseeded, and then play equivalently ranked teams in a crossover game.  After this, teams are reseeded again, and the ranks of these teams will determine entry into the 1-8 bracket.

Ranking a team is done first by W-L record, then by point differential, then by points scored total.

## Description of simulations

probabilities of winning a game is based on the seeding in the pools-- These can be customized in run-simshoy.py.  After reseeding, there is a single game played, and previous rank does not impact the probability of that either team winning.


### Random variables
- W/L is a bernoulli random variable, following the inputs given according to seeding.
- point differential is a poisson random variable
- points scored is derived by having a total score follow a discrete normal distribution, and then applying the point differential generated above.

## Running the code

```python run_simshoy.py```

## Example simulations

### Conservative

![](https://github.com/erjenkins/shsu-stats/scripts/sim-shoy/SHOY-sim-conservative.png "Conservative")

### Realistic
![](https://github.com/erjenkins/shsu-stats/scripts/sim-shoy/SHOY-sim-realistic.png "Realistic")
