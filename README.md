# Hack the South 2020 Southampton

This is the official GitHub account for the Hack-The-South team in the University of Southampton for the 2020 competition.

**Team Members**: Gregory Parkes, Owen Howe, Mikolaj Kacki, Zuza Skorniewska, Philippa Wakefield

- Movie dataset can be found [here](https://www.kaggle.com/rounakbanik/the-movies-dataset#movies_metadata.csv).
- Documentation to build a website in Python using `flask` found [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/).
- Pandas documentation can be found [here](https://pandas.pydata.org/pandas-docs/stable/reference/index.html).

## TODO:

1. Find a labelled image dataset with basic generic categories (food, cities, buildings etc.)
2. Think about how to formulate a mathematical objective function to link these options with a preferred movie.

See the **Issues** tab for current coding problems, see the **Project** tab for Ideas, To Do and In Progress Milestones.

## Installation

To use Python, download the Anaconda distribution found [here](https://www.anaconda.com/), then install.

If you are using Mac or Linux, do the following in Terminal (in hacksouth directory):

```bash
# creates consistent python environment - this could take a while if Anaconda needs to download packages.
conda env create -f environment.yml
# activates python environment
conda activate hacksouth
# run jupyter in this environment
jupyter notebook
```

If you are using Windows, open up Anaconda Navigator, and select 'Environments', click 'Import' and select `environment.yml` file. Once this has loaded, select the `hacksouth` environment and run a Jupyter notebook from it.

This ensures that the correct version/software packages that we're using are consistent between all the team members and we reduce the chance of creep import bugs.
