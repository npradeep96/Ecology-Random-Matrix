#!/bin/bash
#SBATCH -J RandomMatrix
#SBATCH --mail-user npradeep96
#SBATCH -p sched_mit_arupc
#SBATCH -t 12:00:00
#SBATCH --mem-per-cpu 10000 
cd "$SLURM_SUBMIT_DIR"
echo $PWD

run_program()
{
    source activate random-matrix
    echo "$input_file"
    python $program_file --i $input_file
    conda deactivate
}

cleanup_files()
{
rm $input_file
echo "DONE"
}

run_program
cleanup_files