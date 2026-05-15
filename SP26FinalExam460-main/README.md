# The Torchbearer

**Student Name:** _Suber Ebrahim_
**Student ID:** _827410383_
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  _Dijkstra's finds the shortest path to each node independently
  but cannot account for the requirement to visit all relics in a specific sequence._

- **What decision remains after all inter-location costs are known:**
  _The optimal order of relic collection that minimizes the cumulative fuel cost before heading to the exit is determined_

- **Why this requires a search over orders (one sentence):**
  _Because the graph is directed and has many stops, we must explore different sequences to find the minimum fuel cost path._

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source |
|---|---|
| _node S_ | _To find the shortest fuel cost from the start to the first relic in any possible sequence_ |
| _node M_ | _To find paths between relics and from the final relic to the exit node T_ |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property | Your answer |
|---|---|
| Data structure name | Nested Dictionary |
| What the keys represent | Outer keys, source nodes, Inner keys, destination nodes |
| What the values represent | The minimum fuel cost to travel from source to destination |
| Lookup time complexity | O(1) average case|
| Why O(1) lookup is possible | Python dictionaries use hash tables, allowing instant access to values via keys |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs: _K + 1_
- **Cost per run: _O(m log n)_
- **Total complexity: _O((K + 1) * m log n)_
- **Justification (one line): _We run Dijkstra once for the entrance and once for each of the k relic chambers to map all possible starting points_

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  _The distance value is the true, absolute shortest path from the source, and it will not be updated again._

- **For nodes not yet finalized (not in S):**
  _The distance value is the length of the shortest known path from the source using only finalized nodes as intermediate steps._

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  _Only the source is set to 0 and all others to infinity, which is correct since no edges have been explored yet._

- **Maintenance : why finalizing the min-dist node is always correct:**
  _Because edge weights are nonnegative, the node with the minimum distance in the priority queue cannot be reached
  through any other node with smaller total cost._

- **Termination : what the invariant guarantees when the algorithm ends:**
  _When the priority queue is empty, the invariant ensures that every reachable node has been finalized with its minimum distance._

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

_The whole search for the relics depends on these costs being the absolute minimum, 
If the distances from Dijkstra are wrong, the search part won't work right because 
it will pick a path it thinks is the cheapest when it actually isn't._

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** _A greedy strategy always moves to the nearest uncollected relic,
    which ignores how that choice impacts the cost of reaching the remaining relics or the exit._
- **Counter-example setup:** _Using the spec example, starting at S, the distances to relics are B = 1, C = 2, and D = 2__
- **What greedy picks:** _Greedy picks B first because it is the closest to S. However,
  from B, the paths to C or D might be significantly more expensive down the line._
- **What optimal picks:** _Unlike greedy optimal picks globally cheap choices rather than locally cheap
  meaning it may choose to go to C or D because they might lead to cheaper overall cost later on._
- **Why greedy loses:** _Greedy loses because it makes a "local" decision that results in a "global" fuel penalty,   
  potentially doubling back through expensive edges to finish the mission, or in the case of directed grpah going to deadends._

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- _The algorithm must explore every possible order of relic collection to identify the sequence that results 
  in the mininmum total fuel cost_

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_loc | str | current location of torchbearer |
| Relics already collected | relics_remaining | set | a collection of the relic nodes no visted so far |
| Fuel cost so far | cost_so_far | float | the total fuel spent to reach current node |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | set |
| Operation: check if relic already collected | Time complexity: O(1) |
| Operation: mark a relic as collected | Time complexity: O(1)|
| Operation: unmark a relic (backtrack) | Time complexity: O(1)|
| Why this structure fits | a set allows for very fast lookups ensuring search doesn slow down as number of relics increases |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _O(k!)_
- **Why:** _ther are k! possible orderings in which k relics can be visted._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _We track the lowest total fuel cost found for any complete valid route from start to all relics to exit._
- **When it is used:** _It is checked at the start of every recursive call to compare the cost_so_far against the current record._
- **What it allows the algorithm to skip:** _It allows it to stop exploring any partial path that is already as expensive as known path._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _The cost_so_far, the current_loc, and which relics are still in relics_remaining._
- **What the lower bound accounts for:** _cost_so_far is the lowerbound because fuel cannot be less than what is already spent at the current moment so far._
- **Why it never overestimates:** _Because all edge weights are positive the current cost is the absolute minimum the final path could possibly be._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Pruning is safe because if current cost already more than or equal to out best complete path while we have remaining relics, there is no reason to keepe going
   so terminaitng ensures only minimum cost is considered._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
