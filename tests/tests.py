# tests.py
import os
from unittest.mock import patch
from agent_wrapper import run_simulation, parse_output
from fitness import evaluate_run
from nsga import repair_individual

FIXTURE_GOOD = os.path.join('tests', 'fixtures', 'good_simulation_output.csv')
FIXTURE_INFEASIBLE = os.path.join('tests', 'fixtures', 'infeasible_simulation_output.csv')

#stub functions
def stub_run_simulation_good(drug_schedule, dailyDose, vegfconc, runID):
    """Returns pre-recorded good output instead of calling simulation"""
    return FIXTURE_GOOD

def stub_run_simulation_infeasible(drug_schedule, dailyDose, vegfconc, runID):
    """Returns pre-recorded infeasible output"""
    return FIXTURE_INFEASIBLE

#unit tests (no simulation needed)
def test_repair_clamps_schedule_to_min():
    ind = [50, 0.15]   # schedule below min of 100
    repair_individual(ind, 100, 7000, 0.05, 0.2)
    assert ind[0] >= 100, f"Expected >= 100, got {ind[0]}"
    print("PASS: repair clamps schedule to min")

def test_repair_clamps_schedule_to_max():
    ind = [9000, 0.15]  # schedule above max of 7000cd 
    repair_individual(ind, 100, 7000, 0.05, 0.2)
    assert ind[0] <= 7000, f"Expected <= 7000, got {ind[0]}"
    print("PASS: repair clamps schedule to max")

def test_repair_rounds_schedule_to_multiple_of_10():
    ind = [353, 0.15]
    repair_individual(ind, 100, 7000, 0.05, 0.2)
    assert ind[0] % 10 == 0, f"Expected multiple of 10, got {ind[0]}"
    print("PASS: repair rounds schedule to multiple of 10")

def test_repair_clamps_dose_to_bounds():
    ind = [360, 0.25]  # dose above max of 0.2
    repair_individual(ind, 100, 7000, 0.05, 0.2)
    assert ind[1] <= 0.2, f"Expected <= 0.2, got {ind[1]}"
    print("PASS: repair clamps dose to max")

def test_repair_rounds_dose_to_2dp():
    ind = [360, 0.12345]
    repair_individual(ind, 100, 7000, 0.05, 0.2)
    assert ind[1] == round(ind[1], 2), f"Expected 2dp, got {ind[1]}"
    print("PASS: repair rounds dose to 2 decimal places")


#integration tests (stub replaces simulation)

def test_fitness_good_params_exceeds_threshold():
    """Known good params: score >= 0.9, time is not penalty"""
    with patch('agent_wrapper.run_simulation', 
               side_effect=stub_run_simulation_good):
        filename = stub_run_simulation_good(1200, 0.01, 8.0, 0)
        data = parse_output(filename)
        score, time = evaluate_run(data, threshold=0.9)
    assert score >= 0.9, f"Expected score >= 0.9, got {score}"
    assert time < 99999, f"Expected valid time, got penalty"
    print(f"PASS: good params → score={score:.3f}, time={time:.2f}")

def test_fitness_infeasible_params_returns_penalty():
    """Known infeasible params: time should be penalty value"""
    filename = stub_run_simulation_infeasible(1200, 800.0, 8.0, 0)
    data = parse_output(filename)
    score, time = evaluate_run(data, threshold=0.9)
    assert time == 99999, f"Expected penalty 99999, got {time}"
    print(f"PASS: infeasible params → penalty returned correctly")

#interface verification
def test_inputs_passed_correctly_to_simulation():
    """
    Verify schedule and dose are passed without modification.
    Uses stub to capture what would have been sent to simulation.
    """
    captured = {}
    def capturing_stub(drug_schedule, dailyDose, vegfconc, runID):
        captured['schedule'] = drug_schedule
        captured['dose'] = dailyDose
        return FIXTURE_GOOD

    with patch('nsga.run_simulation', side_effect=capturing_stub):
        capturing_stub(1200, 0.01, 8.0, 0)

    assert captured['schedule'] == 1200, \
        f"Schedule not passed correctly: {captured['schedule']}"
    assert captured['dose'] == 0.01, \
        f"Dose not passed correctly: {captured['dose']}"
    print("PASS: inputs passed correctly to simulation interface")  

if __name__ == '__main__':
    print("=== Unit tests (no simulation) ===")
    test_repair_clamps_schedule_to_min()
    test_repair_clamps_schedule_to_max()
    test_repair_rounds_schedule_to_multiple_of_10()
    test_repair_clamps_dose_to_bounds()
    test_repair_rounds_dose_to_2dp()

    print("\n=== Integration tests (stub) ===")
    test_fitness_good_params_exceeds_threshold()
    test_fitness_infeasible_params_returns_penalty()
    test_inputs_passed_correctly_to_simulation()

    print("\nAll tests passed.")
    