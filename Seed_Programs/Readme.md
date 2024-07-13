## Purpose

This artifact contains the necessary data and code to reproduce the results of ICSE 2024 paper `Fast Deterministic Black-box Context-free Grammar Inference`. We are applying for the **Available** and **Reusable** badges. 

**Available:** This package is publicly available on a figshare link with a DOI. We adopt an open source license (MIT) for this artifact.

**Reusable:** The artifact is functional and contains a Docker image to easily duplicate the environment we have run our experiments on. We also outlined the steps to run the experiments and reproduce the results presented in the paper.

## Provenance

All source code, experimental data, and dependencies are bundled in a Docker image, available on figshare: https://doi.org/10.6084/m9.figshare.23907738 

A copy of all source code for easy forking and ongoing development on GitHub: https://github.com/rifatarefin/treevada

The preprint can be found here: https://doi.org/10.48550/arXiv.2308.06163 

## Data

We collected the 1k test programs and oracle binaries for each benchmark from prior work (i.e., Arvada's artifact). The Arvada artifact is available here: https://hub.docker.com/r/carolemieux/arvada-artifact. We organize the data as follows.

### Directory Structure

All the seed programs and the black-box oracles are in the folder `Seed Programs`. The first set of languages aka micro-benchmarks use an `ANTLR4` generated parser as an oracle. The rest (`curl`, `nodejs`, `tinyc`) aka macro-benchmarks use an external 3rd party program as an oracle. For each benchmark `$bench` (json, lisp, turtle, while, xml, curl, tinyc, nodejs), there is a directory with the following content:

- `parse_$bench`: the oracle for the benchmark, taken from the [Arvada](https://github.com/neil-kulkarni/arvada) artifact.
- `$bench-train-*`: Seed sets `r1` and `r2` for all 8 benchmarks, plus `r5` for tinyc and nodejs. Seed set `ase21-h` in the micro-benchmarks' directory and `ase21-r0` in the macro-benchmarks' directory were used in the Arvada study.
- `$bench-test`: test programs for recall calculation, all experiments are done on this single test set.
- `cpp_build`: build folder for ANTLR4 (only for the micro-benchmarks) 
    - `cpp_build/g_$bench.g4`: ground-truth grammar

## Setup

**Hardware requirements:** At least 32GB RAM to reproduce TreeVada results and at least 256 GB RAM to reproduce baseline Arvada results. (In our experiments 32GB RAM was not enough for some Arvada runs so we eventually used a 256GB RAM machine for some Arvada runs.)

**Software requirements:** You need to have [Docker](https://docs.docker.com/engine/install/) installed in your system. First pull the TreeVada image from [DockerHub](https://hub.docker.com/r/marefin/treevada).
```
docker pull marefin/treevada:v2
```
Alternatively, load the docker image from `treevada.tar` file

```
docker load -i treevada.tar
```
Now run the container
```
docker run --rm -it marefin/treevada:v2
```

## Usage

### Check Installation
```
./runscript --check
```
This command from a running container runs TreeVada on json inputs, it should take 1--2 minutes to display the results.

### Reproducing TreeVada 
To reproduce TreeVada results on `r1` and `r5` seeds run,
```
./runscript.sh
```
Change the `seed` variable in the script to run on different seed sets. On a Ryzen 9 5900HX machine TreeVada takes 50 minutes for the micro-benchmarks and 2 hours for macro-benchmarks to run on `r1` seeds. On the larger `r5` seeds, TreeVada takes 6.5 hours. Now, to parse the raw results from the log files and print in a tabular format, run

```
python3 parse_results.py 
```
Argument options:
```
--seed    r1, r2, r5, ase21-r0, ase21-h
--lang    json, lisp, turtle, while, xml, curl, tinyc, nodejs
```
By default `parse_results.py` prints results of all languages on `r1` seeds. You can specify the seed set or the languages from the command line option too. Since TreeVada is deterministic, the results are reproducible. On the other hand, Arvada results reported in our paper may not be reproducible because of its non-deterministic nature. To run Arvada, simply checkout to the branch `replication`. Remember that we have removed the parser timeout here (unlike the original implementation)
```
git checkout replication
```
Use the `runscript.sh` script to run Arvada on different seed sets as mentioned above. Because of its being non-deterministic, you'll get different results from the paper results. 

### Ablation Study

For each ablation study, we have maintained a branch. These are organized in the following way:

| Study Description      | Branch name  |
| :---        |    ----:   |
| TreeVada     |    `master`  |
| Arvada replication      | `replication`       |
| Deterministic version of Arvada   | `deterministic-replication`|
| Re-apply learned rules   | `reapply-deterministic` |
| Initial bracket-based trees   | `tree-all-bubble` |
| Tree without partial merge   | `reapply-tree` |

Just checkout to the target branch and run the experiments like before. Completing these steps will reproduce the results of table 3, 5-8.

### TreeVada on custom benchmark

Suppose you have a directory containing a set of examples, `TRAIN_DIR`, and an oracle for a valid example, `ORACLE_CMD`. The restrictions on `ORACLE_CMD` are as follows:

- `ORACLE_CMD filename` should run the oracle on the file with name `filename`
- `ORACLE_CMD filename` should return 0 if the example in `filename` is valid, and an exit code greater than 0 if it is invalid.

You can then run TreeVada via:
```
$ python3 search.py external ORACLE_CMD TRAIN_DIR LOG_FILE
```
this will store the learned grammar as a pickled dictionary in `LOG_FILE.gramdict`, and some information about training in `LOG_FILE`.

If you also have a held-out test set in `TEST_DIR`, you can evaluate the precision and recall of the mined grammar with the utility `eval.py`. This utility also handily prints out the unpickled grammar to `LOG_FILE.eval` file. The provided `LOG_FILE` must match one generated by search.py, as this utility looks for `LOG_FILE.gramdict`.
```
$ python3 eval.py external ORACLE_CMD TEST_DIR LOG_FILE [PRECISION_SET_SIZE]
```
The optional `PRECISION_SET_SIZE` argument specifies how many inputs to sample from the mined grammar to evaluate precision. It is 1000 by default. 

We used `nodejs v10.24.1`, `curl v7.61.1`, and `gcc v11.2.0` in our experiments.

### Grammar Statistics

`evaluation/mine.py` module parses the unpickled grammar file and prints the grammar statistics (number of production rules, non-terminal/terminals, etc.)
```
python3 evaluation/mine.py LOG_FILE.eval
```

Running this module on all inferred grammars (for `r1` and `r5` seeds) will reproduce Table 4.
