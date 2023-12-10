# sequence_similarity

# Usage

## 1. Set up the environment

``` 
git clone https://github.com/ThankGodE/sequence_similarity.git
```

``` 
cd sequence_similarity
```

``` 
pwd
```

## 2. Edit NextFlow configuration file

```
vim similarity_nextflow/sequence_similarity.config
```

## 3. Run the pipeline

```
nextflow run similarity_nextflow/sequence_similarity.nf -c similarity_nextflow/sequence_similarity.config -with-singularity
```