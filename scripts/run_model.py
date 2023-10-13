"""
Script that computes the eigenvalues for a large number of realizations of the random matrix 
"""

import numpy as np
import scipy.linalg as spl
import sys
sys.path.add('../')
import utils.matrix_generation as mg
import utils.model_analysis as ma
import argparse
import ast
import os

def parse_input_parameters(filename, params_flag=False):
	"""
	Function that parses input parameters from input parameter file and parameter list file. 

	:param filename: Parameter file name
	:type filename: string
	:param params_flag: Flag that tells the function whether to read an input parameter file (False) or parameter list file (True). Default = False
	:type params_flag: bool

	:return input_parameters: Dictionary containing input parameters
	:rtype input_parameters: dict
	"""
	input_parameters = {}
	with open(filename, 'r') as f:
		
		count = 0
		for line in f:
			line = line.strip()
			if line:
				if line.find('#') == -1:
					if not params_flag:
						var_name = line.split(',')[0]
						var_value = ",".join(line.split(',')[1:]) 
						# handle lines with more than 1 comma
						try:
							input_parameters[var_name] = float(var_value)
						except ValueError: 
						# This occurs when python cannot convert list into a float.
							# Evaluate the python expression as a list
							input_parameters[var_name] = ast.literal_eval(var_value)
					else:
						if count == 0:
							var_name = line.strip('\n')
							input_parameters[var_name] = []
							count += 1
						else:
							try:
								input_parameters[var_name].append(
									float(line.strip('\n')))
							except ValueError:  
							# This occurs when python cannot convert list into a float.
								# Evaluate the python expression as a list
								input_parameters[var_name].append(
									ast.literal_eval(line.strip('\n')))
	return input_parameters

def write_input_parameters(output_file, input_params):
	"""
	Function that writes input parameters from input parameter file into ``output_file`` 

	:param output_file: Target file to write input parameters
	:type output_file: string
	:param input_params: Dictionary containing input parameters
	:type params_flag: dict
	"""
	with open(output_file, 'w+') as f:
		for key in input_params.keys():
			f.write(''.join(key) + ',' + str(input_params[key]) + '\n')

def select_model(model_type):
	"""
	Function that selects the appropriate model from ``matrix_generation.py`` depending on the type in the input parameter file. Model types:
	1. Random interaction model
	2. Random predator-prey model
	3. Random mutualism model
	4. Random competition model
	5. Random mixture (competition+mutualism) model
	6. Random cascade predator-prey model
	7. Random niche predator-prey model
	8. Random bipartite mutualism model 

	:param model_type: Number that defines the model. 
	:type model_type: int
	"""

	if model_type == 1:
		return mg.random_interaction_model
	elif model_type == 2:
		return mg.random_predator_prey_model
	elif model_type == 3:
		return mg.random_mutualism_model
	elif model_type == 4:
		return mg.random_competition_model
	elif model_type == 5:
		return mg.random_mixture_model
	elif model_type == 6:
		return mg.random_predator_prey_cascade_model
	elif model_type == 7:
		return mg.random_predator_prey_niche_model
	elif model_type == 8:
		return mg.random_mutualism_bipartite_model
	elif model_type == 9:
		return mg.random_predator_prey_preferential_preying

def select_add(add_type):
	"""
	Function that selects the appropriate model to add from ``matrix_generation.py`` depending on the type in the input parameter file. Add types:
	1. Add predator interactions randomly

	:param add_type: Number that defines the append type 
	:type add_type: int
	"""

	if add_type == 1:
		return mg.add_predators_random

def build_model(parameters):
	"""
	Function to build model 

	:param parameters: Dictionary that contains parameters containing details on how to assemble model
	:type parameters: dict
	"""
	if parameters['assemble_option'] == 1:
		model_type = select_model(parameters['model_type'])
		model = model_type(
			C=parameters['C'],
			N=parameters['N'],
			sigma=parameters['sigma'],
			d=parameters['d'])

	elif parameters['assemble_option'] == 2:
		base_model_type = select_model(parameters['model_type'])
		base_model = base_model_type(
			C=parameters['C'],
			N=parameters['N'],
			sigma=parameters['sigma'],
			d=parameters['d'])
		add_type = select_add(parameters['add_type'])
		model = add_type(base_model=base_model, 
			N=parameters['N_add'], 
			C=parameters['C_add'], 
			sigma=parameters['sigma_add'],
			d=parameters['d_add']
			)

	return model

def analyze_model(model, parameters):
	"""
	Function that performs different analysis on ``model``

	:param model: Object of one of the model classes present in ``utils.matrix_generation.py`` or assembled by ``utils.model_assembly.py``
	:type model: class object
	:param parameters: Dictionary containing options for different kinds of analysis on the model
	:type parameters: dict 
	"""
	
	# generate and store eigenvalues
	if parameters['generate_and_store_eigenvalues'] == 1:
		ma.compute_and_store_eigenvalues(
			model=model, 
			target_file_name=os.path.join(
				parameters['target_directory'],
				parameters['eigenvalue_storage_file_name']),
			num_matrix=int(parameters['num_matrix'])
			)

	# compute probability of stability
	if parameters['calculate_probability_of_stability'] == 1:
		p = ma.calculate_probability_of_stability(
			model=model, 
			eigenvalue_file_name=os.path.join(
				parameters['target_directory'],
				parameters['eigenvalue_storage_file_name']),
			num_matrix=int(parameters['num_matrix'])
			)
		ma.write_analysis_data(target_file_name=os.path.join(
				parameters['target_directory'],
				parameters['analysis_file_name']),
				data_description='probability of stability',
				value=p)


# define the function that computes the eigenvalues

if __name__ == '__main__':

	# define parser for command line arguments
	parser = argparse.ArgumentParser(
		description='Take input parameters to run model')
	parser.add_argument('--i',
		help="Name of input parameter file", 
		required = True)
	# parser.add_argument('--p',
	# 	help="Name of file containing parameter sweep information", 
	# 	required = False)
	# parser.add_argument('--pN',
	# 	help="Parameter number from parameter sweep file (indexed from 1)", 
	# 	required = False)
	args = parser.parse_args()
	
	# read parameter file
	parameters = parse_input_parameters(args.i)
	# read parameter sweep file
	# assert args.p is not None, (
	# 	"You need to supply a parameter file: param_list.txt!")
	# sweep_param = parse_input_parameters(args.p, params_flag=True)
	# par_name = str(list(sweep_param.keys())[0])
	# par_values = sweep_param[par_name] 
	# par_values = par_values[int(args.pN)-1]
	# parameters[par_name] = par_values 
	
	# make output directory
	parameters['target_directory'] = (parameters['target_directory'] 
		+ '/C_' + str(parameters['C']) + '_N_' + str(parameters['N']) 
		+ '_sigma_' + str(parameters['sigma']) + '_d_' + str(parameters['d'])) 
	if parameters['assemble_option'] >= 1.0:
		parameters['target_directory'] = (parameters['target_directory'] 
			+ '_C_add_' + str(parameters['C_add']) 
			+ '_N_add_' + str(parameters['N_add'])	
			+ '_sigma_add_' + str(parameters['sigma_add']))
	# write input parameters to output directory
	if not os.path.exists(parameters['target_directory']):
		os.makedirs(parameters['target_directory'])
		write_input_parameters(os.path.join(
			parameters['target_directory'],
			'input_params.txt'), parameters)

	
	# build model
	model = build_model(parameters)

	# analyze model
	analyze_model(model, parameters)