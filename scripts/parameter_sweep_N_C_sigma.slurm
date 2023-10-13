#!/bin/bash

modify_input_parameters()
{
	sed -i "/N_add\,*/c\N_add\, $1" ../inputs/input_params_add_predator.txt
	sed -i "/C_add\,*/c\C_add\, $2" ../inputs/input_params_add_predator.txt
	sed -i "/sigma_add\,*/c\sigma_add\, $3" ../inputs/input_params_add_predator.txt
	cp ../inputs/input_params_add_predator.txt input_params_N_$1_C_$2_sigma_$3.txt
}

run_program()
{	
	# N_array=(50)
	# C_array=(0.22)
	N_array=(10 50 100 150 200 300 400 500 600 700 800)
	C_array=(0.02 0.12 0.25)
	sigma_array=(0.1 0.3 0.5 0.8 1.0 2.0 3.0 4.0)
	# sigma_array=(0.1 0.3)
	for i in ${N_array[@]}; do 
		for j in ${C_array[@]}; do
			for k in ${sigma_array[@]}; do
				modify_input_parameters $i $j $k
				sbatch --export=program_file=run_model.py,input_file=input_params_N_"$i"_C_"$j"_sigma_"$k".txt run_model.slurm
			done
		done
	done
}

run_program