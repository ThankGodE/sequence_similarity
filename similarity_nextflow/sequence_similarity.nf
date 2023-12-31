#!/usr/bin/env nextflow

params.output_directory = "$params.path_to_output_directory"
params.absolute_path_project_root_dir = "$params.absolute_path_to_project_root_dir_source"
params.path_to_fasta_files = "$params.path_to_fasta_files"
params.fasta_file_extension = "$params.fasta_file_extension"

println params.fasta_file_extension

// create channels for fasta files
fasta_files_ch = Channel.fromFilePairs("${params.path_to_fasta_files}/*{1,2}*${params.fasta_file_extension}", checkIfExists: true, followLinks: true)

process CONCATENATE_ASSEMBLIES() {

    publishDir params.output_directory, mode:'copy'

    output:
    val "$params.output_directory/assemblies_concatenated.fasta"

    shell:
    """
    find $params.path_to_fasta_files -type f -name '*$params.fasta_file_extension' -exec cat {} + | \
    awk '!/>/ { gsub(/[^A-Za-z]/, "*"); print; next } { print }' > $params.output_directory/assemblies_concatenated.fasta
    """

}

process CLUSTER_ASSEMBLY() {

    publishDir params.output_directory, mode:'copy'
    input:
    path "$params.output_directory/assemblies_concatenated.fasta"

    output:
    val "clustering_completed"

    shell:
    """
    cd-hit -d 100 -c $params.similarity_identity -aL $params.coverage_factor \
    -i $params.output_directory/assemblies_concatenated.fasta -o $params.output_directory/assemblies_concatenated_clustered.fasta
    """

}

process UNIQUE_SEQUENCES() {

    publishDir params.output_directory, mode:'copy'
    input:
    tuple val(file_id), path(protein_files)

    output:
    val "unique_sequences_completed"

    shell:
    """
    pip install -r $params.absolute_path_project_root_dir/similarity_python/requirements.txt
    python3 $params.absolute_path_project_root_dir/similarity_python/src/main/unique_sequences.py \
    -o $params.output_directory -i $params.path_to_fasta_files/${protein_files[1]} -w $params.path_to_fasta_files/${protein_files[0]}
    """


}

process MAP_UNIPROT_ID() {

    publishDir params.output_directory, mode:'copy'
    input:
    path "clustering_completed"

    output:
    val "mapping_completed"

    shell:
    """
    upimapi -i $params.path_to_fasta_files/assembly_2.prot.fa -o $params.output_directory/  -db uniprot -t 8
    """

}



workflow() {

    concatenate_assemblies_ch = CONCATENATE_ASSEMBLIES()
    cluster_assembly_ch = CLUSTER_ASSEMBLY(concatenate_assemblies_ch)
    unique_sequences_ch = UNIQUE_SEQUENCES(fasta_files_ch)


    if( params.interrogate_uniprot) {

        map_uniprot_id_ch = MAP_UNIPROT_ID(cluster_assembly_ch)
    }

}
