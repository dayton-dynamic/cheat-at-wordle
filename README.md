# cheat-at-wordle
Provide suggestions consistent with what is known during the game.

`poetry install`

To run: `wordle`

Enter results of a guess like 'xgxyy', where
- g: Green (correct)
- y: Yellow (correct, but misplaced)
- x: Grey (wrong)

## Running with Docker

On Windows machines, it may be more convenient to run this program using Docker.

With Docker running in the background, run

`docker build -t wordle .`

followed by

`docker run -it wordle`

I would _not_ recommend looking to this Dockerfile for insight, as it is largely copy/pasted from another project.
