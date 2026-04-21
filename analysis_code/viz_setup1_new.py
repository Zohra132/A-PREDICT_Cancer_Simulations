#Code Bentley Lab created, currently confidential as paper under review Au et al Cancer Cell 2026
import pandas as pd
import glob
import os


def extract_all_data_long_format(directory_path, output_file="simulation_data_param_results600.csv"):
    """Extract all simulation data in long format - one row per time point"""

    all_rows = []

    csv_files = glob.glob(os.path.join(directory_path, "*.csv"))

    for filepath in csv_files:
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()

            # Keep original structure
            lines = [line.strip() for line in lines]

            if len(lines) < 10:
                continue

            # Parse parameters from row 0
            params = lines[0].split('\t')
            schedule = float(params[0])
            dose = float(params[1])
            gradient = int(float(params[2]))
            VconcST = float(params[3])
            Vconc = float(params[4])
            run = int(float(params[6]))

            # Get VEGF level based on gradient
            vegf_level = VconcST if gradient == 2 else Vconc

            # Extract all data arrays
            hours = [float(x) for x in lines[2].split('\t') if x.strip()]
            drug_tumour_nM = [float(x) for x in lines[3].split('\t') if x.strip()]
            drug_gut_mgL = [float(x) for x in lines[4].split('\t') if x.strip()]
            drug_blood_mgL = [float(x) for x in lines[5].split('\t') if x.strip()]
            drug_blood_nM = [float(x) for x in lines[6].split('\t') if x.strip()]
            vasc_score = [float(x) for x in lines[7].split('\t') if x.strip()]
            vegfr_inhibition = [float(x) for x in lines[8].split('\t') if x.strip()]
            dll4_average = [float(x) for x in lines[9].split('\t') if x.strip()]

            all_arrays = [hours, drug_tumour_nM, drug_gut_mgL, drug_blood_mgL,
                          drug_blood_nM, vasc_score, vegfr_inhibition, dll4_average]
            min_length = min(len(arr) for arr in all_arrays if len(arr) > 0)

            # Create one row for each time point
            for i in range(min_length):
                row = {
                    'filename': os.path.basename(filepath),
                    'schedule': schedule,
                    'dose': dose,
                    'gradient': gradient,
                    'vegf_level': vegf_level,
                    'VconcST': VconcST,
                    'Vconc': Vconc,
                    'run': run,
                    'hours': hours[i] if i < len(hours) else None,
                    'drug_tumour_nM': drug_tumour_nM[i] if i < len(drug_tumour_nM) else None,
                    'drug_gut_mgL': drug_gut_mgL[i] if i < len(drug_gut_mgL) else None,
                    'drug_blood_mgL': drug_blood_mgL[i] if i < len(drug_blood_mgL) else None,
                    'drug_blood_nM': drug_blood_nM[i] if i < len(drug_blood_nM) else None,
                    'vasc_score': vasc_score[i] if i < len(vasc_score) else None,
                    'vegfr_inhibition': vegfr_inhibition[i] if i < len(vegfr_inhibition) else None,
                    'dll4_average': dll4_average[i] if i < len(dll4_average) else None
                }
                all_rows.append(row)

        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            continue

    df = pd.DataFrame(all_rows)
    df.to_csv(output_file, index=False)

    print(f"Saved {len(df)} rows to {output_file}")
    print(f"Data from {df['filename'].nunique()} files")
    print(f"Columns: {list(df.columns)}")

    print(f"\nData summary:")
    print(f"Gradient types: {sorted(df['gradient'].unique())}")
    print(f"Doses: {sorted(df['dose'].unique())}")
    print(f"VEGF levels: {sorted(df['vegf_level'].unique())}")
    print(f"Time range: {df['hours'].min():.1f} - {df['hours'].max():.1f} hours")

    # Range (to sanity check)
    variables = ['drug_gut_mgL', 'drug_blood_mgL',
                 'drug_blood_nM', 'vasc_score', 'vegfr_inhibition', 'dll4_average']

    print(f"\nVariable ranges:")
    for var in variables:
        if df[var].notna().any():
            min_val = df[var].min()
            max_val = df[var].max()
            print(f"{var}: {min_val:.4f} - {max_val:.4f}")
        else:
            print(f"{var}: all NaN")

    return df


def filter_for_analysis(df, gradient_type=None, output_file=None):
    filtered = df.copy()

    if gradient_type is not None:
        filtered = filtered[filtered['gradient'] == gradient_type]

    # Remove rows with all NaN values in measurement columns
    measurement_cols = ['drug_gut_mgL', 'drug_blood_mgL',
                        'drug_blood_nM', 'vasc_score', 'vegfr_inhibition', 'dll4_average']
    filtered = filtered.dropna(subset=measurement_cols, how='all')

    if output_file:
        filtered.to_csv(output_file, index=False)
        print(f"Saved {len(filtered)} filtered rows to {output_file}")

    return filtered


# Main execution
if __name__ == "__main__":
    directory_path = "./results-600"

    df = extract_all_data_long_format(directory_path)

    print("All data saved.")
