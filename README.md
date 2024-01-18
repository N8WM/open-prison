# open-prison
An investigation of agent-based learning for the classic game theory thought experiment, The Prisoner's Dilemma.

## What is the Prisoner's Dilemma?

The Wikipedia page for the [Prisoner's Dilemma](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma) is a great resource for learning more about the thought experiment.

William Poundstone's description from his book in 1993:

> Two members of a criminal gang are arrested and imprisoned. Each prisoner is in solitary confinement with no means of speaking to or exchanging messages with the other. The police admit they don't have enough evidence to convict the pair on the principal charge. They plan to sentence both to a year in prison on a lesser charge. Simultaneously, the police offer each prisoner a Faustian bargain. If he testifies against his partner, he will go free while the partner will get three years in prison on the main charge. Oh, yes, there is a catch ... If both prisoners testify against each other, both will be sentenced to two years in jail. The prisoners are given a little time to think this over, but in no case may either learn what the other has decided until he has irrevocably made his decision. Each is informed that the other prisoner is being offered the very same deal. Each prisoner is concerned only with his own welfare—with minimizing his own prison sentence.

This leads to four different possible outcomes for prisoners A and B:

1. If A and B both remain silent, they will each serve one year in prison.
2. If A testifies against B but B remains silent, A will be set free while B serves three years in prison.
3. If A remains silent but B testifies against A, A will serve three years in prison and B will be set free.
4. If A and B testify against each other, they will each serve two years.
