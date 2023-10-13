#!/bin/bash

modify_input_parameters()
{
    sed -i "/N\,*/c\N\, $1" ../inputs/input_params.txt
    sed -i "/C\,*/c\C\, $2" ../inputs/input_params.txt
    cp ../inputs/input_params.txt input_params_N_$1_C_$2.txt
}

run_program()
{	
	# N_array=(10 12)
	# C_array=(0.027 0.038)
	N_array=(10.0 30.0 50.0 100.0 150.0 200.0 250.0 300.0 400.0 500.0 600.0 700.0 800.0 900.0 1000.0)
	C_array=(0.01 0.02 0.03 0.04 0.06 0.08 0.1 0.12 0.14 0.16 0.18 0.2 0.22 0.24 0.26)
	for i in ${N_array[@]}; do 
		for j in ${C_array[@]}; do
			modify_input_parameters $i $j
			sbatch --export=program_file=run_model.py,input_file=input_params_N_"$i"_C_"$j".txt run_model.slurm
		done
	done
}

run_program