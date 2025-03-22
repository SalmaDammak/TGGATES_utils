from collections import Counter, defaultdict
import random
import csv

def generate_grouped_csv(input_filepath, output_filepath):
    """
    Reads a CSV file with headers COMPOUND, FINDING_TYPE, and ORGAN_x, then groups data by COMPOUND
    filtering only for findings in Kidney or Liver. Writes a new CSV file with each row representing 
    a compound and its filtered findings.
    
    Parameters:
    input_filepath (str): Path to the input CSV file.
    output_filepath (str): Path to the output grouped CSV file.
    """
    grouped_data = defaultdict(list)
    
    with open(input_filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            organ = row["ORGAN_x"].strip()
            if organ in {"Kidney"}:  # Filter for Kidney and Liver
                compound = row["COMPOUND_NAME_x"].strip()
                finding = row["FINDING_TYPE"].strip().replace(",", "_")  # Replace commas with underscores
                grouped_data[compound].append(finding)
    
    with open(output_filepath, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for compound, findings in grouped_data.items():
            writer.writerow([compound] + findings)

def read_csv(filepath):
    """
    Reads a CSV file and parses it into a list of tuples.
    Each row represents a subgroup with a name and associated class labels.
    
    Parameters:
    filepath (str): Path to the CSV file.
    
    Returns:
    list: A list of tuples (name, list of class labels).
    """
    subgroups = []
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name = row[0]
            labels = [label.strip() for label in row[1:] if label.strip()]
            subgroups.append((name, labels))
    return subgroups

def evaluate_partition(T, S):
    """
    Evaluates the quality of a partition by computing class balance difference.
    Lower values indicate better balance.
    
    Parameters:
    T, S (list of tuples): Partitioned subgroups.
    
    Returns:
    int: Total imbalance score.
    """
    count_T, count_S = Counter(), Counter()
    for _, subgroup in T:
        count_T.update(subgroup)
    for _, subgroup in S:
        count_S.update(subgroup)
    
    imbalance = sum(abs(count_T[label] - count_S[label]) for label in set(count_T.keys()).union(set(count_S.keys())))
    return imbalance

def greedy_partition(findings_by_drug):
    """
    Greedy algorithm to split subgroups into two sets while maintaining class balance.
    
    Parameters:
    findings_by_drug (list of tuples): Each subgroup is a tuple (drug name, list of findings).
    
    Returns:
    tuple: (T, S) where T and S are two lists containing the partitioned subgroups with names.
    """
    T, S = [], []
    count_T, count_S = Counter(), Counter()
    
    # Shuffle to avoid bias in input ordering
    random.shuffle(findings_by_drug)
    
    for drug, findings in findings_by_drug:
        # Count occurrences of each class in the subgroup
        finding_counter = Counter(findings)
        
        # Calculate imbalance if added to T or S
        imbalance_T = 0
        imbalance_S = 0
        for label in finding_counter:
            #imabalance = how many of this label are in T + how many of this label are in the current subgroup - how many of this label are in S
            # this line answers the question: what would be the imbalance between sets if we add the current drug (subgroup) to T?
            # so, we add the current drug to T to see how many of a certain finding T would have, then subtract how much of this finding is already in S, 
            # to see how much more/fewer of this label T would have.
            imbalance_T += abs((count_T[label] + finding_counter[label]) - count_S[label])
            imbalance_S += abs((count_S[label] + finding_counter[label]) - count_T[label])
        
        # Assign to the set that maintains better balance (if both are equal, assign to S)
        # we want this behaviour because we want the test set to be richer
        if imbalance_T < imbalance_S:
            T.append((drug, findings))
            count_T.update(findings)
        else:
            S.append((drug, findings))
            count_S.update(findings)
    
    return T, S, count_T, count_S

# Generate grouped CSV
input_filepath = "/Volumes/temporary/salma/Experiments/TG-GATES_OOD/merged_output.csv"  # Update with actual input CSV file path
output_filepath = "/Volumes/temporary/salma/Experiments/TG-GATES_OOD/abnormalities_per_group.csv"
generate_grouped_csv(input_filepath, output_filepath)

# Experiment with 100 random seeds
data = read_csv(output_filepath)

best_T, best_S = None, None
best_score = float('inf')
results = []

seed_idx = 0
for seed in range(1000):
    
    random.seed(seed)
    T, S, count_T, count_S = greedy_partition(data)
    score = evaluate_partition(T, S)
    results.append((seed, score, T, S))
    
    
    if score < best_score:
        best_score = score
        best_T, best_S = T, S
        best_count_T, best_count_S = count_T, count_S
        best_score_idx = seed_idx

    seed_idx = seed_idx + 1
    

with open("/Volumes/temporary/salma/Experiments/TG-GATES_OOD/partition_scores.txt", "w") as f:
    for seed, score, T, S in results:
        f.write(f"Seed: {seed}, Score: {score}\n")

T_drugs = dict(results[best_score_idx][2]).keys()
S_drugs = dict(results[best_score_idx][3]).keys()

# write drug lists to csv
with open("/Volumes/temporary/salma/Experiments/TG-GATES_OOD/T_drugs.csv", "w") as f:
    for drug in T_drugs:
        f.write(f"{drug}\n")
with open("/Volumes/temporary/salma/Experiments/TG-GATES_OOD/S_drugs.csv", "w") as f:
    for drug in S_drugs:
        f.write(f"{drug}\n")


# Write best counts to CSV
with open("/Volumes/temporary/salma/Experiments/TG-GATES_OOD/best_counts.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Label", "T Count", "S Count"])
    for label in set(best_count_T.keys()).union(set(best_count_S.keys())):
        writer.writerow([label, best_count_T[label], best_count_S[label]])
    
    # add num samples in T and S
    writer.writerow(["Total", sum(best_count_T.values()), sum(best_count_S.values())])

print(f"Best partition found with seed {results[best_score_idx][0]} and score {best_score}")
