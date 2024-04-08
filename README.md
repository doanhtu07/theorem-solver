# Theorem Solver

A solver that can take simple first-order logical clauses and literals.

Then, it will output whether the target clause is valid or not together with steps to reach that conclusion.

The solver uses the strategy of resolution by refutation.

## Example

Let us consider a correct solution for testing the validity of ¬z ∨ y, given the input:

```
∼p q
∼z y
p
∼z y
```

**NOTE:** The last line of the input is the target clause.

The program’s output should be:

```
1. ∼p q {}
2. ∼z y {}
3. p {}
4. z {}
5. ∼y {}
6. q {3,1}
7. y {4,2}
8. ∼z {5,2}
9. Contradiction {7,5}
Valid
```

## Run

```
python3 main.py [input path]
```

- `input path` is required: The input file path like ./ex1_in.txt
  - The input file should have the same format as `ex1_in.txt`
  - The last line of the input file is the clause we will try to prove
  - Other previous lines are forming the knowledge base