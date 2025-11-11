# APSingleCodebase APREDICT trial 

## Use
**buildSpringAgent.sh**: This builds the springAgent executable (or python .so) locally.

**springAgent**: executable which needs to be run with [runtime arguments](#Runtime-args).

## Command line args
**Note**: the ordering of the arguments passed does not matter when using the buildSpringAgent.sh and campScript.sh. However, the ordering does matter when using the springAgent executable.

### Build args

- The buildSpringAgent.sh can be passed a '--graphics' flag which will turn graphics on in the compiled sim. This does not work with the pybind version or with the camp script.

APSingleCodebase git:(Master): ./BuildSpringAgent.sh --graphics 

## Runtime args
The following arguments are taken in by the springAgent executable, in the following order:
1. **drug_delivery_schedule** - integer - default to 2880 which means every 12 hours, as 1 timestep = 15 seconds of real time. 
2. **dailyDose** - integer - the dose in mg of the drug taken - default 5pm in APREDICT study
3. **readInGradient** - integer - determins the distribution gradient of VEGF - 0 = flat, 1 = exp, 2 = steady, 3 = fixed macros, 4 = astro linear, 5 = curved circles 6 = astro uniform. currently only expects 0 (flat gradient and uses VEGFconc value) or 2 = steady and uses VconcST value to set the vegf levels, so set to 0 or 1 and then ensure VConcST or Vconc value below is set.
4. **VconcST** - float - amount of VEGF in each grid site when there is a linearly increasing gradient of VEGF in the y axis - default value for normal tip selection patterning = 0.04 
5. **VEGFconc** - float - amount of VEGF in each grid site when there is a flat (uniform) distribution of VEGF (readInGradient set to 0) - default value 0.8 for normal tip selection
6. **RUNS** - integer - this sets the run number incase you want to run multiple runs of the same parameter inputs above - e.g for averaging results or running on the cluster. default - set to 0.

./SpringAgent 2880 5 1 0.04 0.8 1

## Output


Output file will be named "%d_dose_%g_gradient_%d_VconcST_%g_Vconc_%g_run_%d.csv" and set with the values of the read in arguments: drug_delivery_schedule,dailyDose,readInGradient,VconcST,VEGFconc,RUNS

it contains the following information (defined in analysis.cpp APREDICT_Supply_lines_Score()):
1. 1st line is the tab delineated parameters from the run (read in arguments and the Protein_binding_percent which is now default always set to 1 and doesnt change)
2. 2ndline is the timestep in hours (for setting axes labels when plotting results), saved every 60 timesteps
3. 3rd line is DrugSupplied_store_Tumour - drug level in the tumour vessels per timesteps , saved every 60 timesteps (this should for now be equal to the level in the blood)
4. 4th line is accumulatedDrug_store_Gut - drug level in the gut compartment, saved every 60 timesteps
5. 5th line is the accumulatedDrug_store_Blood_mgL - amount of drug in mg/L in the blood compartment, saved every 60 timesteps
6. 6th line is the accumulatedDrug_store_Blood_nM - amount of drug converted to nM units in the blood compartment, saved every 60 timesteps
7. 7th line is the supplyLine_store - called vascularization score in the Methods write up), saved every 60 timesteps
8. 8th line drugEffect_VR2_store - which calculates how much the VEGFR-2 receptor has been inhibited by the drug in the tumour vessels, saved every 60 timesteps
9. 9th line is the Dll4_store - which is the average dll4 expression level of the cells, saved every 60 timesteps


## Python Plotting 

TBC 