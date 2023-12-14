Large language models (LLMs) have the potential to revolutionize how
users interact with databases. In this paper we describe an exploration of
the integration of reinforcement learning (RL) into teaching LLMs how to
translate natural language instructions along with a database schema to
(often) executable and accurate SQL. This tool can be used to help users
without a technical background as they will be able to easily interact with
databases. We employ the OpenLLaMA v2 model at a size of ∼ 3 Billion parameters 
and train in two phases. We initially pretrain a supervised
fine-tuning objective on the disjoint subset of the sql-create-context dataset
against the Spider dataset and then further trained on synthetic preference
data generated from the intersection of sql-create-context and the Spider
training split using a modern LLM RL technique (DPO). From the rein-
forcement learning perspective, we performed our second phase of training
in a contextual bandit setting, where our designed prompt served as a con-
text and the generated SQL query was the bandit selection. Our approach
is novel as we explore a new technique for generating preference data and
establish a new approach for metric engineering in the text2sql space.
We plot DPO rewards as detailed in [1] above. The dpo-rewards-chosen
(green line) shows the chosen or and is relatively stable compared to the
other signals. The dpo-rewards-reject (brown line) represents the rewards
associated with rejected actions or hypotheses. The rate of rejection is
decreasing over time which could be a sign of learning and improvement.
This is visited again in the Results section.

Authors: Abirami Sabbani and Nelson Lojo
